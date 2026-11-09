/********************************************************************
* 版权所有 (C)2026, 天津理工大学华信软件学院。
*
* 文件名称：ITriangleClassifier.cs
* 文件标识：SQ-LAB1-004
* 内容摘要：三角形判定服务接口，便于单元测试与替换实现。
* 其它说明：接口名以 I 开头，实现类命名为 TriangleClassifier。
* 当前版本：V1.0
* 作    者：王博川
* 完成日期：2026年11月9日
* 修改记录1：
*    修改日期：2026年11月9日
*    版 本 号：V1.0
*    修 改 人：王博川
*    修改内容：首次创建。
**********************************************************************/
using Wbc.SoftwareQuality.Triangle.Models;

namespace Wbc.SoftwareQuality.Triangle.Services
{
    /// <summary>
    /// 三角形判定服务。
    /// </summary>
    public interface ITriangleClassifier
    {
        /// <summary>
        /// 判断三条边能够构成的三角形类型。
        /// </summary>
        /// <param name="edgeA">第一条边的长度，必须为正整数。</param>
        /// <param name="edgeB">第二条边的长度，必须为正整数。</param>
        /// <param name="edgeC">第三条边的长度，必须为正整数。</param>
        /// <returns>三角形类型；三条边无法构成三角形时返回 <see cref="TriangleType.NotTriangle"/>。</returns>
        /// <exception cref="System.ArgumentOutOfRangeException">任一边长小于 1 时抛出。</exception>
        TriangleType Classify(int edgeA, int edgeB, int edgeC);

        /// <summary>
        /// 将界面输入的文本解析为正整数边长。
        /// </summary>
        /// <param name="text">界面输入的原始文本。</param>
        /// <param name="edge">解析成功时的边长值；失败时为 0。</param>
        /// <returns>解析成功且大于 0 时返回 true。</returns>
        bool TryParseEdge(string text, out int edge);
    }
}
