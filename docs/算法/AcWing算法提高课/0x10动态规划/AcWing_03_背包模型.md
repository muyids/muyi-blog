# 背包 dp

对于背包问题的学习，推荐看下[dd 大牛的《背包九讲》](https://www.cnblogs.com/jbelial/articles/2116074.html)

# 背包模型

01 背包：每个物品只有一个：选、不选

完全背包：每个物品有无限个：选 0、选 1、选 2、...

多重背包：每个物品有 $S_i$ 个：选 0、选 1、选 2、...、选 $s_i$ 个

- [分组背包问题](#分组背包问题) 一组里面只能选一种
- [混合背包问题](#混合背包问题)
- [二维费用的背包问题](#二维费用的背包问题)
- [背包问题求方案数](#背包问题求方案数)
- [求背包问题的方案](#求背包问题的方案)
- [有依赖的背包问题](#有依赖的背包问题)
  我们重点掌握常用的背包四讲，即：**01 背包、完全背包、多重背包、分组背包**

# 01 背包

给定 $N$ 个物品，每个物品可以选择取或不取；背包总体积 $V$；物品价值数组 $w_i$ ，体积数组 $v_i$ ；求背包可以容纳的最大价值

## 求最大价值

[AcWing 423. 采药](https://www.acwing.com/activity/content/problem/content/1267/)

[AcWing 426. 开心的金明](https://www.acwing.com/problem/content/428/)

## 求最小剩余空间

[AcWing 1024. 装箱问题](https://www.acwing.com/activity/content/problem/content/1268/)

背包总体积 $V$，物品体积数组 $v_i$ ，求背包可以剩余的空间最小值

思路：

$f[i] $ 表示 是否存在 装满体积 $i$ 的方案

## 二维背包费用问题

[AcWing 1022. 宠物小精灵之收服](https://www.acwing.com/activity/content/problem/content/1269/)

$f[n][m]$ 代表 二维背包 精灵球数量，

## 求方案数

[AcWing 278. 数字组合](https://www.acwing.com/activity/content/problem/content/1270/)

# 完全背包

给定 $N$ 种物品，每种物品可以取无限个；背包总体积 $V$，物品价值数组 $w_i$ ，体积数组 $v_i$ ，求背包可以容纳的最大价值

思路：

$f[i][j]$ 表示 前 $i$ 个物品，体积 $j$ 的最大价值

状态转移：

$f[i,j]=max(f[i-1,j],f[i-1,j-v]+w,f[i-1,j-2v]+2w,...,f[i-1,j-sv]+sw)$

$f[i,j-v]=max(f[i-1,j-v],f[i-1,j-2v]+w,...,f[i-1,j-sv])$ =>

=> $f[i,j]=max(f[i-1,j],f[i,j-v]+w)$

## 求方案数

[AcWing 1023. 买书](https://www.acwing.com/activity/content/problem/content/1271/)

[AcWing 1021. 货币系统](https://www.acwing.com/activity/content/problem/content/1272/)

[AcWing 532. 货币系统](https://www.acwing.com/activity/content/problem/content/1273/)

求极大独立集，线性无关组

# 多重背包

有 $N$ 种物品和一个容量是 $V$ 的背包。

第 $i$ 种物品最多有 $s_i$ 件，每件体积是 $v_i$，价值是 $w_i$。

求能放入背包的最大价值。

递推：

$f[i,j]=max(f[i-1,j],f[i-1,j-v]+w,f[i-1,j-2v]+2w,f[i-1,j-3v]+3w,...,f[i-1,j-sv]+sw)$

$f[i,j-v]=max(f[i-1,j-v],f[i-1,j-2v]+w)$

[4. 多重背包问题 I](https://www.acwing.com/problem/content/4/)

**数据范围**

$0<N,V≤100$
$0<vi,wi,si≤100$
思路：

多重背包 可以看成是 每种物品有 $s_i$个，可以看成是 0 个、1 个、2 个，... ，$s_i$个多种情况，用 01 背包模型求解

时间复杂度：

$O(N*V*Si)$

[5. 多重背包问题 $II$](https://www.acwing.com/problem/content/5/)

**数据范围**

$0<N≤1000$
$0<V≤2000$
$0<vi,wi,si≤2000$

提示：考查多重背包的二进制优化

思路：

将物品数 $s_i$ 进行二进制拆解 为 $1+2+4+...+(s_i - 2^k)$ ，然后用 01 背包求解；

可以将 多重背包问题$I$ 看成 拆解方案是 $1+1+1+...$，然后用 01 背包求解；

二进制优化是优化了拆解方案！

```java
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt();
        int V = sc.nextInt();
        int[] v = new int[25000]; // N * logN ： 2000 * log_2_2000
        int[] w = new int[25000];

        int K = 0; // 二进制优化后的物品数
        for (int i = 0; i < N; i++) {
            int vi = sc.nextInt(), wi = sc.nextInt(), si = sc.nextInt();
            for (int j = 1; j < si; j *= 2, K++) {
                v[K] = vi * j;
                w[K] = wi * j;
                si -= j;
            }
            if (si > 0) {
                v[K] = vi * si;
                w[K] = wi * si;
                K++;
            }
        }
        // 01背包
        int f[] = new int[V+1];
        for (int i = 0; i < K; i++) {
            for (int j = V; j >=v[i]; j--) {
                f[j] = Math.max(f[j], f[j-v[i]] + w[i]);
            }
        }
        System.out.println(f[V]);
    }
}
```

[AcWing 6. 多重背包问题 III](https://www.acwing.com/activity/content/problem/content/1274/)

**数据范围**

$0<N≤1000$
$0<V≤20000$
$0<vi,wi,si≤20000$

提示：考查多重背包的单调队列优化

男人八题 之一，比较难

[AcWing 1019. 庆功会](https://www.acwing.com/problem/content/1021/)

多重背包的应用

# 混合背包问题

[AcWing 7. 混合背包问题](https://www.acwing.com/problem/content/7/)

有 $N$ 种物品和一个容量是 $V$ 的背包。

物品一共有三类：

- 第一类物品只能用 1 次（01 背包）；
- 第二类物品可以用无限次（完全背包）；
- 第三类物品最多只能用 $s_i$ 次（多重背包）；

每种体积是 $v_i$，价值是 $w_i$

求最大价值

# 二维费用的背包问题

[AcWing 8. 二维费用的背包问题](https://www.acwing.com/problem/content/8/)

存在 体积、重量 二维限制

求最大价值

[AcWing 1020. 潜水员](https://www.acwing.com/problem/content/1022/)

# 分组背包问题

有 $N$ 组物品和一个容量是 $V$ 的背包。

每组物品有若干个，**同一组内的物品最多只能选一个**。
每件物品的体积是 $v_{ij}$，价值是 $w_{ij}$，其中 $i$ 是组号，$j$ 是组内编号。
求不超过背包体积的最大价值

[AcWing 9. 分组背包问题](https://www.acwing.com/problem/content/9/)

[AcWing 1013. 机器分配](https://www.acwing.com/problem/content/1015/)

问题转化 成 分组背包问题

输出一种最优方案

# 背包问题求方案数

[AcWing 11. 背包问题求方案数](https://www.acwing.com/problem/content/11/)

思路：

额外开数组记录最优解的方案数

```java
import java.util.*;
public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int N = sc.nextInt(), V = sc.nextInt();
        int MOD = 1000000007;
        int[] f = new int[V+1];
        int[] cnt = new int[V+1]; // 不超过 最大价值的 方案数
        Arrays.fill(cnt, 1);
        for (int i = 0; i < N; i++) {
            int v = sc.nextInt(), w = sc.nextInt();
            for (int j = V; j >= v; j--) {
                int val = f[j-v] +w;
                if (val > f[j]){
                    f[j] = val;
                    cnt[j] = cnt[j-v];
                } else if (val == f[j]){
                    cnt[j] = (cnt[j] + cnt[j-v]) % MOD;
                }
            }
        }
        System.out.println(cnt[V]);
    }
}
```

# 背包问题求具体方案

[AcWing 12. 背包问题求具体方案](https://www.acwing.com/problem/content/12/)

思路：

确定了字典序，从后往前迭代求最优解，从前向后输出方案即可

```java
import java.util.Scanner;
public class Main{
    public static void main(String[]args){
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt(), V = sc.nextInt();
        int v[] = new int[N+1];
        int w[] = new int[N+1];
        for (int i =1; i<=N;i++) {
            v[i] = sc.nextInt();
            w[i] = sc.nextInt();
        }
        int[][]f = new int[N+2][V+1];

        for (int i = N; i > 0; i--){
            for (int j = V; j>= 0; j--){
                f[i][j] = f[i+1][j];
                if (j>=v[i]) f[i][j] = Math.max(f[i][j], f[i+1][j-v[i]] + w[i]);
            }
        }
        int j = V;
        for (int i = 1; i<= N && j > 0; i++){
            if (j >= v[i] && f[i][j] == f[i+1][j-v[i]] + w[i]){
                System.out.printf("%d ", i);
                j -= v[i];
            }
        }

    }
}
```
