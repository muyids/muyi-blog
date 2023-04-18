# 强连通分量

## 概念

连通分量：对于一个有向图，连通分量中的两点 $u、v$，如果存在 $u$ 到 $v$的路径，则一定存在 $v$ 到 $u$ 的路径

强连通分量：最大的连通分量

## 常见应用

任一有向图 通过 **缩点操作** 转化为 **有向无环图**。缩点操作：将所有连通分量 缩成一个点。

拓扑图的好处：求最短路/最长路 可以通过递推求得。时间复杂度 $O(M+N)$

# Tarjan 算法求强连通分量（SCC）

**SCC** **:** $Strong\ Connected\ Component$

## 算法思路

1. 对每个点定义两个时间戳：
   1. $dfn[u]$ 表示遍历到 $u$ 的时间戳
   2. $low[u]$ 表示从 $u$ 开始走，所能遍历到的最小时间戳
2. $u$ 是其所在强连通分量的最高点，等价于 $dfn[u] == low[u]$
   $Tarjan$ 算法基于有向图的 $DFS$ ，能够在线性时间内求一张有向图的 各个 强连通分量。

## 代码模板

### TODO

```java
import java.util.Arrays;
public class Main {
    static int N = 110, M = N << 1;
    static int h[] = new int[N], e[] = new int[M], ne[] = new int[M], idx;
    static int dfn[] = new int[N], low[] = new int[N], timestamp;
    static int stk[] = new int[N], top;
    static boolean in_stk[] = new boolean[N];
    static int id[] = new int[N], scc_cnt, Size[] = new int[N]; // 每个强连通分的节点个数

    static void add(int a, int b) {
        e[idx] = b;
        ne[idx] = h[a];
        h[a] = idx++;
    }

    static void dfs(int x) {
        for (int i = h[x]; i != -1; i = ne[i]) {
            int u = e[i];
            System.out.printf("dfs %d -> %d\n", i, u);
            dfs(u);
        }
    }

    static void tarjan(int u) {
        System.out.printf("tarjan %d\n", u);
        dfn[u] = low[u] = ++timestamp;
        stk[++top] = u;
        in_stk[u] = true;
        for (int i = h[u]; i != -1; i = ne[i]) {
            int j = e[i];
            if (dfn[j] == 0) {
                tarjan(j);
                low[u] = Math.min(low[u], low[j]);
            } else if (in_stk[j]) {
                low[u] = Math.min(low[u], dfn[j]);
            }
        }
//        if (dfn[u] == low[u]) {
//            int y;
//            ++scc_cnt;
//            do {
//                y = stk[top--];
//                in_stk[y] = false;
//                id[y] = scc_cnt;
//                Size[scc_cnt]++;
//            } while (y != u);
//        }
    }

    public static void main(String[] args) {

        int[][] ed = {
                {1, 6}, {1, 2}, {2, 3}, {3, 4}, {4, 5}, {6, 8}, {6, 7}, {8, 9}
        };
        Arrays.fill(h, -1);
        for (int[] e : ed) {
            System.out.printf("add e: %d -> %d\n", e[0], e[1]);
            add(e[0], e[1]);
        }
        dfs(1);
//        for (int i = 1; i <= 9; i++) {
//            if (dfn[i] == 0) {
//                tarjan(i);
//            }
//        }
//        for (int i = 1; i < 10; i++) {
//            System.out.printf("low[%d]=%d\n", i, low[i]);
//        }

    }

}
```
