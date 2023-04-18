# 区间 DP

**区间 DP**也属于 **线性 DP**的一种，以 ”区间长度“ 作为 DP 的 ”阶段“， 使用 两个坐标（区间的左右断点）描述每个维度。

在区间 DP 中，一个状态由若干个比他更小且包含于他的区间所代表的状态转移而来，因此区间 DP 的决策往往就是划分区间的方法。

区间 DP 的初态一般由长度为 1 的”元区间“构成。

这种向下划分，再向上递推的模式与某些树形结构，如线段树，有很大相似之处。

借助区间 DP 这种与树形相关的结构，我们也将提及记忆化搜索 -- 本质是 DP 的递归实现方法。

# 特点

- 区间 DP 在状态计算的时候一定要 认真 划分好 **边界** 和 **转移**; 因为 区间边界 搞错状态 转移方程 是非常常见的错误。

- 合并：即将两个或多个部分进行整合，当然也可以反过来；
- 特征：能将问题分解为能两两合并的形式；
- 求解：对整个问题设最优值，枚举合并点，将问题分解为左右两个部分，最后合并两个部分的最优值得到原问题的最优值。
- 一般用二维数组表示区间
- 区间问题只需要考虑 **区间头和区间尾**

# 代码模板

常用于一维区间 DP

```cpp
for len ∈ [1,N]  		// 长度从小到大
  for i=1,j; (j = i + len -1) && j < N ; i++ // 以 i 为 开头, j 结尾的 区间
    for k ∈ [i, j]  // 以 k 为分割点，进行分治
      // 状态转移方程
```

比如 状态$f(i,j)$表示将下标位置 i 到 j 的所有元素合并能获得的价值的最大值，那么 $f(i,j) = max(f(i,k-1) + f(k+1, j) + cost)$, cost 为将这两组元素合并起来的代价。

其中， $k ，cost，i, j$ 的取值都需要根据具体情况具体分析，上面只是列举了 区间 DP 的大概通用代码模板。

# [282. 石子合并](https://www.acwing.com/problem/content/284/)

题目大意：N 堆石子 排成一排，重量 为 $A_i$，每次选择相邻两堆进行合并，形成新的一堆石子的重量 以及消耗的体力 都是 两堆石子的重量之和。求把全部 N 堆石子合并成一堆消耗的最少 体力。$1<=N<=300$

## 算法思路

我们从最后的结果思考，$[l, r]$堆石子如果已经全部被合并，则最后一定是通过 $[l,k]，[k+1,r]$两堆石子合并而来，其中 $l<=k<r$。

$[l,r]$区间的重量为 $\sum_{i=l}^{r} {Ai}$。

对应到 区间 DP 中，划分点 $k$ 就是 转移的决策。

设 $f[i, j]$ 表示 合并 $[i, j]$ 区间的最小代价，容易写出状态转移方程：

$$
f[i, j] = \min\limits_{l<=k<r}  (f[i, k] + f[k+1, j]) + \sum_{i=l}^r A_i
$$

初值：$\forall i\in[1,N], f[i][i]=0$，其余为 $+\infty$

目标：$f[1,N]$

**注意：**

- 实现状态转移方程时，务必 分清**阶段、状态 与 决策**，三者应按照从外向内的顺序依次循环

- 对于 $\sum_{i=l}^r A_i$ 可以使用前缀和实现

## 代码实现

```cpp
for (int i = 0; i<n; i++){
  cin >> s[i+1];
  s[i+1] += s[i]; // 前缀和
  f[i][i] = 0; // 初值
}
for (int len = 2; len<=n; len++){ // 阶段
  for (int i = 0, j; (j = i+len-1) <n ; i++){ // 状态
    for (int k = i; k<j; k++) { // 决策
      f[i][j] = min(f[i][j], f[i][k] + f[k+1][j]);
    }
    f[i][j] += s[j+1] - s[i]
  }
}
```

# [AcWing 1068. 环形石子合并](https://www.acwing.com/problem/content/1070/)

题意解析：题目与上一题不同之处在于 将链 转变为 环。

## 算法思路

我们对于环形结构一般进行两步操作进行处理：

1. 开两倍长度的数组
2. 结果返回时，枚举每一个长度为 n 的 区间
   核心思想：把环当成 以每一个元素开头的 N 条链

## 代码实现

```cpp
#include<cstring>
#include <iostream>

using  namespace std;

const int N = 420, INF = 0x3f3f3f3f;
int s[N], A[N];
int fmin[N][N];
int fmax[N][N];
int n;

int main(){
    memset(fmin, 0x3f, sizeof fmin);
    memset(fmax, -0x3f, sizeof fmax);

    cin >> n;

    for (int i = 0; i < n; i++){
        cin >> A[i];
        A[i+n] = A[i];
    }
    for (int i = 0; i< 2*n; i++){
        s[i+1] = s[i] + A[i];
    }

    for (int len = 1; len<=n; len++){
        for (int i = 0; i + len - 1 < 2*n; i++){
            if (len == 1) {
                fmin[i][i] = fmax[i][i] = 0;
                continue;
            }
            int j = i+len -1;
            for (int k = i; k < j ; k++){
                fmin[i][j] = min(fmin[i][j], fmin[i][k] + fmin[k+1][j] + s[j+1] - s[i]);
                fmax[i][j] = max(fmax[i][j], fmax[i][k] + fmax[k+1][j] + s[j+1] - s[i]);
            }
        }
    }

    int minv = INF, maxv = -INF;
    for (int i =0; i< n; i++){
        minv= min(fmin[i][i+n-1], minv);
        maxv = max(fmax[i][i+n-1], maxv);
    }
    cout << minv<< endl;
    cout<< maxv << endl;
    return 0;
}
```

# [320. 能量项链](https://www.acwing.com/problem/content/322/)

题意解析：

N 个珠子两两相连，形成一条项链；前一颗珠子的 头标记为 $m$，尾标记为 $r$ ，后面一颗的 头标记 为 $r$, 尾标记 为 $n$; 合并 前后两个珠子 释放 能量为 $m * r * n $；新产生的珠子 头标记为 $m$，尾标记 为 $n$ 。

求 最终只剩下一颗珠子 输出能量的最大值。

## 算法思路

环形 结构 处理 同上一题；

珠子合并，我们可以把 $(m,r)$ 和 $(r,n)$ 合并成 $(m,n)$ 当成矩阵乘法 更容易理解；

我们用头标记的值 作为珠子的值，则尾标记一定是下一个珠子的值；比如

设 $N=4$，4 颗珠子的头标记与尾标记依次为 $(2，3)(3，5)(5，10)(10，2)$。

我们记录 此 项链数列 为 ${2,3,5,10}$

使用二倍长度数组存储处理环形结构 ${2,3,5,10,2,3,5,10}$，数组下标从 0 开始

**阶段**：我们用 区间的 $len$ 作为 阶段；

则可以记**状态** $f[l,r]$ 表示 合并 $[l,r]$ 区间释放的最大能量，其中 $0<=l<r<=n$，需要注意的一点是我们要合并的区间范围是 $[0,n]$；

**注意：**这里的 $l, r$ 指的是珠子的头尾标记下标，$0<=l<r<=n$

**决策**的 $k$ 的取值范围是 $l<k<r$，则 区间 $[l, k], [k, r]$分别表示合并左右两边区间，最后一步合并释放的能量 为 $l*k*r$;

状态转移方程：

$$
\max\limits_{0<=l<k<r<=n} f[l][k] + f[k][r] + A[l]*A[k]*A[r]
$$

初值：

$\forall i \in [0, 2*n-1]$，有 $f[i][i] = f[i][i+1] = 0$，其中 $f[i][i]$ 表示一个珠子的 头标记或 尾标记，$f[i][i+1]$ 表示 一个珠子的头尾标记；

目标：$\max\limits_{0<=i<n} {f[i][i+n]}$

## 代码实现

```cpp
for (int i = 0; i < n; i++){
  cin >>w[i];
  w[i+n] = w[i];
}
for (int len = 3; len <= n+1; len++ ){
  for (int i = 0, j; (j = i+len-1) < n << 1; i++ ){
    for (int k = i+1; k < j; k++){
      f[i][j] = max(f[i][j], f[i][k] + f[k][j] + w[i] * w[k] * w[j]);
    }
  }
}
int res = 0;
for (int i = 0; i< n; i++) res = max(res, f[i][i+n]);
```

# 加分二叉树

题意解析：

一颗$N$个节点的二叉树，中序遍历为 $1,2,3,4，..., n$。

每一棵子树的加分定义为 左子树的加分 \* 右子树的加分 + 根的分数；

求：二叉树的最高加分，输出前序遍历方案（若存在多个，输出字典序最小的）

## 算法思路

中序遍历的性质：遍历顺序为 左 根 右；也就是说 对于 每一个 节点 $i$ , 小于 $i$ 的节点都在其左子树， 大于 $i$ 的节点都在其 右子树；

因此，我们可以 以 每一棵 子树的根节点进行区间划分；

我们定义 $[l, r]$ 表示节点区间为 $[l, r]$ 的子树

阶段：根据区间长度划分；我们从区间长度较小的区间向长度较大的区间递推；

状态：$f[l,r]$ 表示 区间为 $[l, r]$ 的子树 的最大分数

策略：我们以 $k$ 作为区间子树的根节点，则 $[l,k-1]$ 表示 $k$ 的 左子树区间，$[k+1, r]$ 表示右子树。

状态转移

$$
\max\limits_{1<=l<=k<=r<=n} f[l][k-1] * f[k+1][r] + A[k]
$$

注意，当 区间长度为 1，即 $l == k$ 和 $r==k$时，表示区间为空(此时$k-1<l或k+1>r$，区间无意义即为空区间)，相应的 $f[l][k-1]$ 和 $f[k+1][r]$ 值为 1

初值（边界）：

- $len==1$时，$f[i][i] = A[i]$

- $len==2时$，$f[i][i+1] = A[i] + A[i+1]$

终值：$f[1,n]$

**最优方案返回**

我们需要记录转移的中间过程，即记录 最优方案 每一步的上一步状态，最后，从最终状态逆推，得到最优方案；这是 DP 问题中 求解最优方案的 通用思路。

具体到这道题，我们每个阶段区间 $[l, r]$的转移 是通过 此区间的根节点实现的 ，所以我们只需要 记录一个中间状态 $root[l][r]$ 定义为 $[l, r]$ 的根节点即可。

## 代码实现

```cpp
#include <iostream>
using namespace std;

const int N = 35;
int A[N];
int f[N][N];
int root[N][N];
void dfs(int l , int r){
    if (l > r) return;
    int k = root[l][r];
    cout << k << " ";
    dfs(l, k-1);
    dfs(k+1, r);
}

int main(){
    int n ;
    cin >> n;

    for (int i = 1; i<= n; i++) cin >> A[i];

    for (int len = 1; len<=n; len++){
        for (int i = 1, j; (j = i+len-1) <=n; i++){
            for (int k= i; k<=j; k++){
                // 处理边界
                if (k==i) f[i][k-1] = 1;
                if (k==j) f[k+1][j] = 1;
                int maxv = f[i][k-1] * f[k+1][j] + A[k];
                if (len == 1) maxv --;
                if (maxv > f[i][j]) {
                    f[i][j] = maxv;
                    root[i][j] = k;
                }
            }
        }
    }

    cout << f[1][n] << endl;

    dfs(1, n);

    cout << endl;

    return 0;
}
```

# 力扣练习 - 区间 DP

## [312. 戳气球](https://leetcode-cn.com/problems/burst-balloons/)

```java
class Solution {
    public int maxCoins(int[] nums) {
        int n = nums.length;
        int[] st = new int[n + 2];
        for (int i = 1; i <= n; i++) st[i] = nums[i - 1];
        st[0] = st[n + 1] = 1;
        int[][] f = new int[n + 2][n + 2];
        for (int len = 3; len <= n + 2; len++) {
            for (int i = 0; i + len - 1 <= n + 1; i++) {
                int j = i + len - 1;
                for (int k = i + 1; k < j; k++) {
                    f[i][j] = Math.max(f[i][j], f[i][k] + f[k][j] + st[i] * st[j] * st[k]);
                }
            }
        }
        return f[0][n+1];
    }
}

```

## [516. 最长回文子序列](https://leetcode-cn.com/problems/longest-palindromic-subsequence/)

```java
class Solution {
    public int longestPalindromeSubseq(String s) {
        int n = s.length();
        int dp[][] = new int[n][n];

        for (int i=0; i< n; i++)dp[i][i] = 1;
        for (int i = 0; i<n-1; i++)dp[i][i+1] = s.charAt(i) == s.charAt(i+1) ? 2: 1;
        for (int len = 3; len<=n; len++){
            for (int i = 0; i+len-1 < n; i++){
                int j = i+len -1 ;
                if (s.charAt(i) == s.charAt(j)) dp[i][j] = dp[i+1][j-1] + 2;
                else dp[i][j] = Math.max(dp[i+1][j], dp[i][j-1]);
            }
        }
        return dp[0][n-1];
    }
}
```

## [877. 石子游戏](https://leetcode-cn.com/problems/stone-game/)

```java
class Solution {
    public boolean stoneGame(int[] a) {
        int n = a.length;
        int[][] f = new int[n][n];
        for (int i = 0; i < n; i++) f[i][i] = a[i];
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                f[i][j] = Math.max(a[i] - f[i + 1][j], a[j] - f[i][j - 1]);
            }
        }
        return f[0][n - 1] > 0;
    }
}
```

## [282. 石子合并](https://www.acwing.com/problem/content/description/284/)

```java
import java.util.Scanner;
public class Main {

    static int minMerge(int n, int[] a) {
        int[][] f = new int[n][n];
        int[] pre = new int[n+1];
        for (int i = 1; i <=n; i++) pre[i]=pre[i-1] + a[i-1];
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                f[i][j] = Integer.MAX_VALUE;
                for (int k = i; k < j; k++) {
                    f[i][j] = Math.min(f[i][j], f[i][k] + f[k+1][j] + pre[j+1] - pre[i]);
                }
            }
        }
        return f[0][n-1];
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        while (scanner.hasNext()) {
            int n = scanner.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                a[i] = scanner.nextInt();
            }
            System.out.println(minMerge(n, a));
        }
    }
}
```
