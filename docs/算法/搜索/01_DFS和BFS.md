# 对比 DFS 和 BFS

BFS

- 空间是指数级别的，大
- 不会有爆栈风险
- 可以求最短，最小

DFS

- 空间和深度成正比，小！
- 有爆栈的风险，比如深度最坏可能有 1e5 层，会爆栈（C++一般 4M）；层信息都放在栈空间里
- 不能搜最短、最小

# 注意事项

- 判断当前节点、层是否已得到最终解
- 判断是否可以剪枝
- 防止循环遍历问题（比如存在环路，要退出）
- 遍历顺序如何选择（比如是弧头到弧尾还是弧尾到弧头）

# 习题

DFS

**星期一**
**LeetCode 111. Minimum Depth of Binary Tree**
**星期二**
**LeetCode 279. Perfect Squares**
**星期三**
**LeetCode 733. Flood Fill **
**星期四**
**LeetCode 200. Number of Islands**
**星期五**
**LeetCode 130. Surrounded Regions179 人打卡**
**LeetCode 543. Diameter of Binary Tree178 人打卡**
星期六
LeetCode 127. Word Ladder 149 人打卡
LeetCode 542. 01 Matrix149 人打卡
星期天
LeetCode 207. Course Schedule137 人打卡
LeetCode 210. Course Schedule II132

BFS

走迷宫

八数码

- [LeetCode 111. Minimum Depth of Binary Tree (easy)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/111.minimum-depth-of-binary-tree.md)

- [LeetCode 279. Perfect Squares (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/279.perfect-squares.md)

- [LeetCode 130. Surrounded Regions (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/130.surrounded-regions.md)
