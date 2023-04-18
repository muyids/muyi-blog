# 背包问题

## 01 背包

### 416.等和子集

01 背包

### 300.最长递增序列

01 背包

### **368.最大整除子集**

01 背包求解决方案

## 完全背包

### 322.零钱兑换

完全背包

### 518.Coin Change 2

完全背包求方案数

## 多重背包

### 474.一和零

多维背包

# 最长序列

- [LeetCode 300. Longest Increasing Subsequence (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/300.longest-increasing-subsequence.md)

- [LeetCode 1143. Longest Common Subsequence (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/1101-1200/1143.longest-common-subsequence.md)

# 图形问题

根据棋盘中图形的性质，通过相邻坐标的状态，进行推导

## 矩形统计

- [LeetCode 221. Maximal Square (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/221.maximal-square.md)

- [LeetCode 1277. Count Square Submatrices with All Ones (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/1201-1300/1277.count-square-submatrices-with-all-ones.md)

# 线性 dp - 序列型

序列型一般分为单序列、双序列

- 一般需要自定义空序列表示$f[0]$
- 有时候会有 K 维序列，表示 K 种状态

## 房子涂色

- [LeetCode 256. Paint House (easy)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/256.paint-house.md)

- [LeetCode 265. Paint House II (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/265.paint-house-ii.md)

## 打家劫舍系列

- [LeetCode 198. House Robber (easy)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/198.house-robber.md)

- [LeetCode 213. House Robber II (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/213.house-robber-ii.md)

打家劫舍 3 是树形 DP

## 股票系列

- [LeetCode 121. Best Time to Buy and Sell Stock (easy)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/121.best-time-to-buy-and-sell-stock.md)

- [LeetCode 122. Best Time to Buy and Sell Stock II (easy)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/122.best-time-to-buy-and-sell-stock-ii.md)

- [LeetCode 123. Best Time to Buy and Sell Stock III (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/123.best-time-to-buy-and-sell-stock-iii.md)

- [LeetCode 188. Best Time to Buy and Sell Stock IV (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/188.best-time-to-buy-and-sell-stock-iv.md)

- [LeetCode 309. Best Time to Buy and Sell Stock with Cooldown (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/301-400/309.best-time-to-buy-and-sell-stock-with-cooldown.md)

- [LeetCode 714. Best Time to Buy and Sell Stock with Transaction Fee (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/701-800/714.best-time-to-buy-and-sell-stock-with-transaction-fee.md)

## 字符串匹配系列

- [LeetCode 10. Regular Expression Matching (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/1-100/10.regular-expression-matching.md)

- [LeetCode 44. Wildcard Matching (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/1-100/44.wildcard-matching.md)

- [LeetCode 72. Edit Distance (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/1-100/72.edit-distance.md)

## 划分型

给定长度为 N 的序列，要求划分为若干段

- 段数不限，或指定 K 段
- 每一段满足一定的性质（最小代价，能不能等）
  做法：

- 类似于序列型动态规划，但是通常要加上段数信息
- 一般用`f[i + 1][k]`来记录前 i 个元素（元素 0~i-1,f[0][k]表示空序列）分成 k 段的性质，如最小代价
- 关注最后一段，枚举最后一段可能情况 + 前面序列, 求最优策略

注意：划分型动态规划每一段序列一定是连续的

### 数字规律一类题目（一维坐标）

把一个完整的数字分成几个，满足一定的性质

- [LeetCode 279. Perfect Squares (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/279.perfect-squares.md)

- [LeetCode 343. Integer Break (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/301-400/343.integer-break.md)

此类问题往往也可以用完全背包模型去解决

### 解码方法

- [LeetCode 91. Decode Ways (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/1-100/91.decode-ways.md)

### 分割回文串

- [LeetCode 132. Palindrome Partitioning II (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/132.palindrome-partitioning-ii.md)

- [LeetCode 1278. Palindrome Partitioning III (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/1201-1300/1278.palindrome-partitioning-iii.md)

### 抄写书籍（领扣 437）

N 本书，每本有 A[i]页；K 个抄写员，每个抄写员可以抄连续的几本书；抄写员抄写速度一样；问最少需要多长时间抄写完毕。

可以用贪心，动态规划更通用，如果稍微变形，贪心就不可以用了

- [LeetCode 410. Split Array Largest Sum (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/401-500/410.split-array-largest-sum.md)
