# 搜索和图论

## 树与图的存储

树是一种特殊的图，与图的存储方式相同。
对于无向图中的边 ab，存储两条有向边 a->b, b->a。
因此我们可以只考虑有向图的存储。

(1) 邻接矩阵：$g[a][b]$ 存储边$a->b$

(2) 邻接表：

```cpp
// 对于每个点k，开一个单链表，存储k所有可以走到的点。h[k]存储这个单链表的头结点
int h[N], e[N], ne[N], idx;

// 添加一条边a->b
void add(int a, int b)
{
    e[idx] = b, ne[idx] = h[a], h[a] = idx ++ ;
}

// 初始化
idx = 0;
memset(h, -1, sizeof h);
```

# [195. 骑士精神](https://www.acwing.com/problem/content/197/)

## DFS 棋盘爆搜

```cpp
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAX_INT = 0x3f3f3f3f;
const int N = 8;
char g[N][N]; // 111111111000000000

int n = 7;
int T;
int dx[8] = {-2, -1, 1, 2, 2, 1, -1, -2};
int dy[8] = {1, 2, 2, 1, -1, -2, -2, -1};
bool check(){
    for (int i = 2; i < n; i ++ ) {
        for (int j = i; j <n; j++){
            if (i <= 3 && g[i][j] != '1') return false;
            if (i == 4 && j == 4 && g[i][j] !='*') return false;
            else if (j > i && g[i][j] != '1'){
                return false;
            }
        }
    }
    return true;
}
int dfs(int i, int j, int step){

    // printf("step=%d, i=%d, j=%d, g[%d][%d]=%c \n", step, i, j ,i,j, g[i][j]);
    if (check()) {
        return step;
    }
    if (step == 8) return MAX_INT;

    int res = MAX_INT;
    for (int d = 0; d < 8; d ++ ) {
        int x = dx[d] + i, y = dy[d] + j;
        if (x > 0 && x <= n && y >0 && y<=n) {
            char next = g[x][y];
            g[i][j] = next;
            g[x][y] = '*';

            res = min(res, dfs(x, y, step + 1));
            g[x][y] = next;
            g[i][j] = '*';
        }
    }
    return res;
}

int main()
{
    cin >> T;

    while (T--){
        for (int i = 2; i < n; i ++ ) {
            for (int j = 2; j < n; j ++ ) {
                cin >> g[i][j];
            }
        }
        int p, q;
        for (int i = 2; i < n; i ++ ) {
            for (int j = 2; j < n; j ++ ) {
                if (g[i][j] == '*') {
                    p = i; q = j;
                }
            }
        }
        int res = dfs(p, q, 0);
        if (res == MAX_INT) res = -1;
        cout << res  <<endl;

    }

    return 0;
}
```

# 状态压缩优化

```cpp
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAX_INT = 0x3f3f3f3f;
const int N = 8;
char g[N][N]; // 111111111000000000
int gg = 1 << 25;
int n = 5;
int T;
int b; // 空白位置 0-24 ； 13

int dx[8] = {-2, -1, 1, 2, 2, 1, -1, -2};
int dy[8] = {1, 2, 2, 1, -1, -2, -2, -1};
int igal = 553951; // 合法棋盘

bool check(){
    if (b!= 12) return false;
    int k12 = (1 << 12) & gg;
    gg = gg | (1 << 12);
    bool flag = (gg == igal);
    gg = gg & k12;
    return flag;
}
int getpos(int x, int y) {
    return x * n + y;
}

int dfs(int i, int j, int step){

    // printf("step=%d, i=%d, j=%d, g[%d][%d]=%c \n", step, i, j ,i,j, g[i][j]);
    if (check()) {
        return step;
    }
    if (step == 8) return MAX_INT;

    int res = MAX_INT;
    for (int d = 0; d < 8; d ++ ) {
        int x = dx[d] + i, y = dy[d] + j;
        if (x >= 0 && x < n && y >=0 && y<n) {
            int u = getpos(x, y);
            int v = getpos(i, j);
            int xy = (gg >> u) & 1;
            int ij = (gg >> v) & 1;
            gg = gg | (1 << v);
            gg = gg & (xy << v);
            b = u;
            res = min(res, dfs(x, y, step + 1));
            b = v;
            // gg = gg | (1 << u);
            // gg = gg & (xy << u);
        }
    }
    return res;
}

int main()
{
    cin >> T;

    while (T--){
        gg = 0;
        int p, q;
        for (int i = 0; i < n; i ++ ) {
            for (int j = 0; j < n; j ++ ) {
                char ch;
                cin >> ch;
                g[i][j] = ch;
                if (ch == '1' || ch == '*') {
                    if (ch == '*'){
                        b = i * n + j;
                        p = i; q = j;
                    }
                    gg = gg | (1 << (i * n + j));
                }
            }
        }

        int res = dfs(p, q, 0);
        if (res == MAX_INT) res = -1;
        cout << res <<endl;
    }
    return 0;
}
```
