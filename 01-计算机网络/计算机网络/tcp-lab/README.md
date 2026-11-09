# 用户态 TCP 协议栈与智能体驱动的模糊测试（TUN）

这是两天内交付的教学项目版本，仅依赖 Python 3.8+ 标准库。请先读 [DELIVERY.md](DELIVERY.md)，其中包含运行步骤、模型接口解释、限制和待补的联网验证。

## Windows / Linux 离线验收

在项目目录运行：

```text
python verify.py
```

应显示四项 PASS。结果、日志、环境和源码 SHA-256 位于 validation-output/。此命令不会安装依赖、配置网络接口或调用真实模型。

## Linux TUN 验证

需 Linux、Python、iproute2、/dev/net/tun、sudo 和网络命名空间权限：

```bash
sudo python3 integration_linux.py --output-dir integration-output-current
python3 inspect_pcap.py integration-output-current/traffic.pcap
```

新版应通过四次连接（含 2700 字节数据流）且清理成功。不能用 historical-evidence 中旧版三次连接的结果代替。命名空间受限时可按 DELIVERY 的说明及历史 README 的双终端方式操作；相关 IP 和接口需同步配置。

## 模糊测试

```text
python fuzz.py --seed 42 --cases 10000 --output fuzz-results.json
python agent_fuzz.py --policy feedback --rounds 5 --episodes 200 --output agent-results.json
python experiment.py --output comparison.json --csv comparison.csv
```

单包测试有六种变异。状态测试有七个算子：valid、bad_seq、bad_ack、duplicate、rst、bad_checksum、wait。固定握手后基于内部状态生成报文，边界预期另由回归测试验证。事件不是代码覆盖率，零失败不证明没有错误。

只有发现并保存了失败样本时才运行：

```text
python replay.py agent-results.json --index 0
```

重放报文和虚拟时间并重新检查性质，输出 reproduced。旧格式缺少动作/性质信息时会要求重新生成。

真实模型模式和三组对照的配置见 DELIVERY。没有模型接口时可运行规则反馈，但不能声称真实调用过大模型。接口测试使用模拟响应，实际服务兼容性需补跑。

## 功能范围

服务端自行解析/构造 IPv4/TCP，通过 TUN 与 Linux socket 客户端交互。具备校验和、握手、按序连续回显、有界发送队列、重复/部分 ACK、序号回绕、被动关闭、RST、固定间隔重传、空闲清理和连接上限。仍只保持一个未确认服务端段；发送段最多 1000 字节，待发送队列最多 4096 字节。

状态路径：无连接 → SYN_RECEIVED → ESTABLISHED → CLOSE_WAIT（等待已接受数据排空）→ LAST_ACK → 无连接。

未实现 TAP/ARP、对端窗口约束、完整滑动窗口、乱序重组、拥塞控制、IP 分片重组、主动连接/关闭与完整 TIME_WAIT。仅用于受控教学演示，不是完整 RFC TCP。

validation-output 是本版离线实测；historical-evidence 是原项目历史资料；新版 TUN 和真实模型实验需要你们补跑。
