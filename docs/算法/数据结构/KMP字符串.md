# KMP 算法 和 基本概念

字符串匹配算法，匹配 字符串 $S$ 中出现的 模板串 $P$ 的所有位置；对暴力方法进行了优化，大大减少了不必要的匹配失败的情况，提高了匹配效率。

核心思想：

# 匹配字符串

# 求 next 数组

$KMP$ 的核心思路是求 $next$ 数组

$next$ 数组表示的 是 模板串 $P$ 前缀 和 后缀的 最大相同长度（部分匹配值）

比如 ：

| P        | a   | b   | c   | a   | b   |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 下标     | 1   | 2   | 3   | 4   | 5   |     |     |     |     |
| $next[]$ | 0   | 0   | 0   | 1   | 2   |     |     |     |     |
