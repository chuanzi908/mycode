# 用户态 TCP 协议栈与大模型辅助模糊测试

这是一个教学演示项目：Linux 内核 TCP 客户端经 TUN 接口发送 IPv4 包，Python 用户态程序解析 IP/TCP 并作为 TCP 回显服务器。模糊测试在进程内直接调用协议栈，包含单包和状态序列测试；可选大模型参与多轮测试策略调整。Python 标准库即可运行，无第三方依赖。详细原理、实验和答辩边界见 [DESIGN.md](DESIGN.md)。

## 架构

```text
Linux socket 客户端 -> 内核路由 -> TUN 虚拟三层接口 -> 用户态 IP/TCP 解析器
                  <- TUN <- 生成 TCP 包 <- TCP 状态机/回显
固定种子或大模型策略 -> 变异器 -> 解析器和状态机 -> JSON 测试记录
```

TUN 承载 IP 包，不承载以太网帧；不需要 TAP 或 ARP。程序按网络字节序处理 IPv4 和 TCP 首部，验证 IPv4 校验和及包括伪首部的 TCP 校验和。连接使用 SYN_RECEIVED、ESTABLISHED、LAST_ACK 状态；使用累计 ACK 和单个待确认报文的定时重传。服务器原样回显收到的数据。

## 环境与启动（WSL2 / Linux）

需要 Linux、Python 3.8+、`ip` 命令、`/dev/net/tun` 和 sudo 权限。Windows 必须先安装 WSL2 与 Linux 发行版，并在 **Linux 终端**运行下列命令。若文件在 Windows `Documents/Codex/.../outputs/tcp-lab` 下，可通过 `/mnt/c/Users/Lenovo/Documents/Codex/2026-10-29/new-chat/outputs/tcp-lab` 进入；实际路径请以本机为准。

打开两个 Linux 终端，均进入项目目录。终端 A：

```bash
sudo python3 stack.py
```

保持终端 A 运行。终端 B：

```bash
sudo ip addr add 10.0.0.1/24 dev tunlab0
sudo ip link set tunlab0 up
python3 client.py --message 'Hello TCP from WSL2'
```

预期看到 `Sent` 与 `Received` 内容一致及 `Result: PASS`。终端 A 按 Ctrl+C 输出统计并退出；进程退出后 TUN 接口随之删除。地址段须未与本机现有网络冲突；若冲突，需同时修改 `stack.py` 的服务地址、客户端地址及接口地址。

可用 `sudo tcpdump -ni tunlab0 tcp port 8080` 在另一终端观察握手、数据和关闭过程（需另行安装 tcpdump）。命令需 sudo 是因为创建和配置网络接口需要相应权限。

若希望留存报文，将终端 A 命令改为 `sudo python3 stack.py --pcap traffic.pcap`，退出后可在 Wireshark 中打开 `traffic.pcap`，或用 `python3 inspect_pcap.py traffic.pcap` 查看序号、确认号和标志位。抓包可能包含明文业务数据，请只使用演示数据。

### 可选：隔离的 Linux 集成测试

在 Linux 中运行 `sudo python3 integration_linux.py --output-dir integration-output`。它创建唯一名称的临时网络命名空间，在其中配置 TUN 和运行三次真实 TCP 回显，然后删除自己创建的命名空间。它保存 `integration.json`、`server.log` 和 `traffic.pcap`。要求 `iproute2`、`/dev/net/tun`、root 和创建网络命名空间的系统权限；受限容器或某些 WSL 配置可能不允许，失败信息会保存在 JSON 中。一次 Ubuntu WSL 实测的三个连接均通过，结果保存在 `integration-output`；不同环境仍需重新验证。

## 离线验证

Windows 或 Linux 都可执行：

```bash
python3 -m unittest discover -s tests -v
python3 fuzz.py --seed 42 --cases 10000 --output fuzz-results.json
python3 agent_fuzz.py --seed 2026 --rounds 5 --episodes 200 --output agent-results.json
python3 experiment.py --output comparison.json --csv comparison.csv
```

固定种子可复现输入；JSON 中包含算子权重、每类数量、未处理异常及触发包的十六进制。这个测试主要验证畸形输入不使解析器抛出未处理异常；**零异常不代表协议正确、没有安全漏洞或覆盖了所有状态**。

状态序列测试先完成握手，然后按当前连接状态构造合法报文、异常序号/确认号、重复报文、RST 和错误校验和报文，检查输出报文及少量不变量。每轮记录自定义状态事件，并依据反馈更新下一轮权重。若记录失败，可用 `python3 replay.py agent-results.json --index 0` 重放记录的包；应进一步核实性质是否仍然失败。事件不是代码覆盖率。

`experiment.py` 对固定和反馈策略使用相同轮数、每轮 episode 数及多个互不重叠的种子范围，输出逐轮明细 JSON 和汇总 CSV。策略分歧后即使相同种子也不会生成完全相同的输入；事件是人工观测点，不构成覆盖率。当前附带结果只比较离线固定和反馈策略，不包含真实大模型实验。

## 大模型辅助策略（可选，需自行准备兼容接口）

大模型只返回六个变异算子的 1–10 权重；程序严格校验 JSON 后进行本地测试，不执行模型生成的代码。未配置时使用均匀权重，不能称为实际调用过大模型。密钥通过环境变量提供，不写入项目或结果文件。以下 URL、模型名为占位示例，请换成自己有权限使用的、支持 Chat Completions 的服务，并遵循其使用规则：

```bash
export LLM_API_KEY='你的密钥'
python3 fuzz.py --llm-url 'https://你的服务地址/v1/chat/completions' --model '你的模型名' --seed 42 --cases 10000 --output llm-results.json
python3 agent_fuzz.py --llm-url 'https://你的服务地址/v1/chat/completions' --model '你的模型名' --seed 2026 --rounds 5 --episodes 200 --output llm-agent-results.json
unset LLM_API_KEY
```

状态测试第一轮采用固定权重，之后把每轮事件和失败数量发送给模型，校验其建议后用于下一轮；记录模型名称、权重及指标。单包测试发送固定描述。不会发送项目文件或测试包。应对比相同测试预算的基线，但权重变化会改变输入序列，不能单凭崩溃次数得出模型更优的结论。由于服务的输出格式或网络条件不同，大模型模式可能失败；失败时程序报错，不伪造模型结果。

## 范围与已知限制

这是受控环境中的教学子集，不是完整 RFC TCP：无拥塞控制、滑动窗口、SACK、乱序重组、IP 分片处理、持久化或完整 TIME_WAIT；仅有一个未确认的服务器报文，针对短消息回显，不用于生产。状态序列测试基于少量人工定义事件和不变量，而非完整代码覆盖驱动测试；大模型提供多轮策略建议，不执行生成的代码，不具备自动修复能力。

## 答辩建议截图（请在实际运行后截取）

1. 两个 WSL 终端：服务端启动、客户端收发一致、服务端退出统计。
2. `python3 -m unittest discover -s tests -v` 的完整结果。
3. 固定种子模糊测试输出和生成的 JSON。
4. 配好服务且实际执行后，大模型策略输出的 `planner: llm` 和权重；遮盖密钥。
5. 可选：tcpdump 中三次握手和关闭报文。

所有截图应真实来自本组运行，保留环境、命令与结果，避免把预期输出当作实测结果。
