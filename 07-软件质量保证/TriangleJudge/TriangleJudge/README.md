# TriangleJudge（软件质量保证与测试 实验一）

## 运行环境
- Windows 10/11
- Visual Studio 2019/2022（.NET Framework 4.8）
- 或命令行：`dotnet build`（需安装 .NET SDK 与 4.8 目标包）

## 打开方式
用 Visual Studio 打开 `TriangleJudge.csproj`，直接 F5 运行。

## 目录结构
```
TriangleJudge/
├── Program.cs                     程序入口
├── MainForm.cs                    窗体逻辑（输入校验、结果显示）
├── MainForm.Designer.cs           控件定义与布局
├── Models/TriangleType.cs         三角形类型枚举
├── Services/ITriangleClassifier.cs 判定服务接口
└── Services/TriangleClassifier.cs  判定核心实现
```

## 判定规则
1. 三条边必须都是正整数，否则提示具体是哪一条不合法；
2. 任意两边之和必须大于第三边，否则判定为“不能构成三角形”；
3. 三边相等为等边，仅两边相等为等腰，其余为普通。

## 测试用例
| 输入 | 期望结果 |
|---|---|
| 3, 4, 5 | 普通三角形 |
| 5, 5, 6 | 等腰三角形 |
| 6, 6, 6 | 等边三角形 |
| 1, 2, 3 | 不能构成三角形 |
| 0, 4, 5 | 边 A 非法 |
| -1, 4, 5 | 边 A 非法 |
| a, 4, 5 | 边 A 非法 |
| 2147483647, 1, 1 | 不能构成三角形（不溢出） |
