# 两天内代码交付说明

本版定位：基于 Linux TUN 的教学 TCP 回显服务端，以及可离线运行的状态反馈/大模型策略模糊测试。只使用 Python 标准库，无需 pip 安装依赖。

## 先运行：Windows 无需 WSL 的验证

在本文件所在目录打开终端：

```text
python verify.py
```

四项 PASS 表示单元测试、10000 次单包测试、1000 组状态序列测试及五个种子的两组对照完成。详细输出位于 `validation-output/`，`summary.json` 记录环境、退出码及源码 SHA-256。失败时查看对应 `.log`。零失败不证明完整 TCP 正确或不存在漏洞。

## Linux/WSL 的真实网络验证（交付前需要补跑）

找一台已有 Ubuntu/Linux 的组员电脑最省时间；本代码不要求每个人都安装 WSL。必须有 Python 3.8+、iproute2、`/dev/net/tun`、sudo，以及创建网络命名空间的权限。在 Linux 项目目录运行：

```bash
sudo python3 integration_linux.py --output-dir integration-output-current
```

通过标准：4 次连接全部 PASS，包括 2700 字节数据流，清理成功。保存生成的 JSON、server.log、traffic.pcap；用下面命令看握手、数据、关闭：

```bash
python3 inspect_pcap.py integration-output-current/traffic.pcap
```

受限 WSL/容器若不支持命名空间，可按 README 的双终端方式手动配置 TUN。不要把旧版三次连接的抓包当成本版网络验证。

## “模型接口”是什么

模型接口让 Python 发送测试摘要、接收模型策略，需要服务提供的 Chat Completions 兼容地址、模型名及 API Key。网页登录或聊天订阅不等于已经获得接口权限。API Key 是调用凭证，只在自己的终端环境变量中配置，不提交代码或截图。

未配置接口时，本地反馈策略仍能运行，但必须写成“规则反馈”，不能称为真实大模型调用。无需模型的运行命令：

```text
python agent_fuzz.py --policy feedback --output feedback-results.json
python agent_fuzz.py --policy fixed --output fixed-results.json
```

如果已经有兼容服务，在 Windows PowerShell 中先用本机环境变量设置凭证，再调用（以下值是占位符，不能原样运行）：

```powershell
$env:LLM_API_KEY = '在本机填入凭证'
python agent_fuzz.py --policy llm --llm-url 'https://你的服务/v1/chat/completions' --model '模型名称' --rounds 3 --episodes 100 --output llm-results.json
Remove-Item Env:LLM_API_KEY
```

Linux 使用 `export LLM_API_KEY='在本机填入凭证'`，运行后 `unset LLM_API_KEY`。

第一轮固定策略，后续模型根据上一轮反馈给七个真实状态算子分配 1..10 权重。结果保存请求提示、原始响应、实际采用的权重、耗时和报文计数，不保存认证请求头。接口出错会保存部分结果并退出非零，不会悄悄用本地规则冒充模型。

有接口后可执行三组对照（先用一个种子验证，避免直接发出很多付费请求）：

```text
python experiment.py --seeds 10000 --rounds 3 --episodes 100 --llm-url https://你的服务/v1/chat/completions --model 模型名称 --output model-comparison.json --csv model-comparison.csv
```

该命令包含 fixed、feedback、llm 三组。接口失败的试验会标记 error，并从完成试验的均值中排除。未传模型参数时仅比较前两组。相同 episode/步数上限不代表相同报文数，结果同时保存实际输入/输出数。事件是人工观察点，不是代码覆盖率。

## 本版必要修改

- 连续按序数据可暂存到有界回显队列；区分已确认位置与下一个发送位置，支持重复/部分 ACK 和序号回绕。
- 仍只保持一个服务端未确认段，最多每段 1000 字节、待发送队列 4096 字节；队列满时不确认未保存的数据。关闭会等待已接受的回显数据排出。
- 状态测试加入虚拟时间及重传探索，重复算子重放之前的正常原包；保存报文和时间动作。
- 重放工具重新执行性质检查，输出 `reproduced`。只有有失败样本时才运行：`python replay.py 结果.json --index 0`。旧格式只记录报文，无法可靠检查同一性质，会要求重新生成。
- 模型直接选择 valid、bad_seq、bad_ack、duplicate、rst、bad_checksum、wait，无旧版间接名称映射。
- `client.py --repeat 3` 可在同一连接内发送合并数据流；集成脚本包含 2700 字节用例。

## 明确不做的扩展

TAP/ARP、完整滑动窗口和零窗口探测、乱序重组、拥塞控制、自适应 RTO、主动连接/主动关闭和完整 TIME_WAIT。当前窗口字段仍为固定值，未实现对端窗口约束。仅用于受控实验和短数据流，不是完整 RFC TCP。

## 交付证据的边界

- `validation-output/` 是本版 Windows 离线实测证据。
- `historical-evidence/` 是原压缩包中旧版结果，保留用于对照，不能代表本版验证。
- 本版真实 Linux TUN 和真实模型调用是否通过，必须以你们补跑的结果为准；接口单元测试使用模拟响应。
- `tests/test_delivery.py` 的故障注入仅用于验证重放判定，不是发现了真实漏洞。

今天：确定一台 Linux 演示机器，跑离线验证和四次真实连接；有模型接口则跑小规模真实调用。明天：保留原始结果、统一代码、彩排后冻结版本。核心验收通过后不要继续添加功能。
