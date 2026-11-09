/********************************************************************
* 版权所有 (C)2026, 天津理工大学华信软件学院。
*
* 文件名称：TriangleClassifier.cs
* 文件标识：SQ-LAB1-005
* 内容摘要：三角形判定的核心实现，包含输入解析、三角不等式校验与形状分类。
* 其它说明：判定顺序为 合法性校验 -> 三角不等式 -> 等边 -> 等腰 -> 普通。
* 当前版本：V1.0
* 作    者：王博川
* 完成日期：2026年11月9日
* 修改记录1：
*    修改日期：2026年11月9日
*    版 本 号：V1.0
*    修 改 人：王博川
*    修改内容：首次创建；使用 long 运算避免两边之和溢出。
**********************************************************************/
using System;
using Wbc.SoftwareQuality.Triangle.Models;

namespace Wbc.SoftwareQuality.Triangle.Services
{
    /// <summary>
    /// 三角形判定服务实现。
    /// </summary>
    public sealed class TriangleClassifier : ITriangleClassifier
    {
        /// <summary>
        /// 边长的最小值，边长为正整数。
        /// </summary>
        private const int MinEdgeLength = 1;

        /// <summary>
        /// 判断三条边能否构成三角形。
        /// </summary>
        /// <param name="edgeA">第一条边。</param>
        /// <param name="edgeB">第二条边。</param>
        /// <param name="edgeC">第三条边。</param>
        /// <returns>能构成三角形时返回 true。</returns>
        private static bool IsTriangle(long edgeA, long edgeB, long edgeC)
        {
            // 任意两边之和必须大于第三边；用 long 运算可避免 int 相加溢出。
            return edgeA + edgeB > edgeC
                && edgeA + edgeC > edgeB
                && edgeB + edgeC > edgeA;
        }

        /// <summary>
        /// 判断三条边能够构成的三角形类型。
        /// </summary>
        /// <param name="edgeA">第一条边的长度，必须为正整数。</param>
        /// <param name="edgeB">第二条边的长度，必须为正整数。</param>
        /// <param name="edgeC">第三条边的长度，必须为正整数。</param>
        /// <returns>三角形类型；无法构成三角形时返回 <see cref="TriangleType.NotTriangle"/>。</returns>
        /// <exception cref="ArgumentOutOfRangeException">任一边长小于 1 时抛出。</exception>
        public TriangleType Classify(int edgeA, int edgeB, int edgeC)
        {
            if (edgeA < MinEdgeLength)
            {
                throw new ArgumentOutOfRangeException(nameof(edgeA), edgeA, "边长必须为正整数。");
            }

            if (edgeB < MinEdgeLength)
            {
                throw new ArgumentOutOfRangeException(nameof(edgeB), edgeB, "边长必须为正整数。");
            }

            if (edgeC < MinEdgeLength)
            {
                throw new ArgumentOutOfRangeException(nameof(edgeC), edgeC, "边长必须为正整数。");
            }

            if (!IsTriangle(edgeA, edgeB, edgeC))
            {
                return TriangleType.NotTriangle;
            }

            if (edgeA == edgeB && edgeB == edgeC)
            {
                return TriangleType.Equilateral;
            }

            if (edgeA == edgeB || edgeB == edgeC || edgeA == edgeC)
            {
                return TriangleType.Isosceles;
            }

            return TriangleType.Scalene;
        }

        /// <summary>
        /// 将界面输入的文本解析为正整数边长。
        /// </summary>
        /// <param name="text">界面输入的原始文本。</param>
        /// <param name="edge">解析成功时的边长值；失败时为 0。</param>
        /// <returns>解析成功且大于 0 时返回 true。</returns>
        public bool TryParseEdge(string text, out int edge)
        {
            edge = 0;

            if (string.IsNullOrWhiteSpace(text))
            {
                return false;
            }

            if (!int.TryParse(text.Trim(), out int parsedValue))
            {
                return false;
            }

            if (parsedValue < MinEdgeLength)
            {
                return false;
            }

            edge = parsedValue;
            return true;
        }
    }
}
