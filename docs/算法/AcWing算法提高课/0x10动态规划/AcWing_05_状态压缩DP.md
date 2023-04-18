# 状态压缩 DP

棋盘类型

```
f[i][j] // 到第i行状态为j 的状态表示
for i < n // 枚举每一行
	for j  // 枚举每一个合法状态
		for k  // 枚举上一行可能的合法状态
			f[i][j] = F(f[i-1][k]) // 状态转移
```

集合类型 => 重复覆盖问题

# [291. 蒙德里安的梦想](https://www.acwing.com/problem/content/293/)

## 代码实现

```cpp
#include <iostream>
#include <cstring>

using namespace std;

const int N = 12, M = 1<< N;
int st[M];
long long f[N][M];
int main(){
    int n, m;
    while (cin >> n>> m && (n || m)) {
        for (int i =0; i< 1<< n; i++){
            st[i] = true;
            int cnt = 0;
            for (int j =0; j< n; j++){
                if (i >> j & 1) {
                    if (cnt & 1) {
                        st[i] = false;
                        break;
                    }
                    cnt = 0;
                } else cnt++;
            }
            if (cnt & 1) st[i] = false;
        }
        memset(f, 0, sizeof f);
        f[0][0] = 1;
        for (int i = 1; i <= m; i++){
            for (int j = 0; j< 1 << n; j++){
                for (int k =0; k <1<<n; k++){
                    if ( !(j&k) && st[j|k] ){
                        f[i][j] += f[i-1][k];
                    }
                }
            }
        }
        cout << f[m][0] << endl;
    }
    return 0;
}
```

# [91. 最短 Hamilton 路径](https://www.acwing.com/problem/content/93/)

旅行商问题 NP

$f[i][j]$ 表示状态为 $i$，最后位置为 $j$ 的最短路径

状态 $i$ 表示 经过的所有点 的集合，则 $i$ 一定包含 $j$

```
for i ∈ [0, 2^n -1]
	for j  // 当前位置
		for k // 上一个位置 i排除j
			f[i, j] = min(f[i -j, k] + w[k, j])

f[11...111, n-1]

```

## 代码实现

```cpp
#include <iostream>
#include<cstring>

using namespace std;

int g[21][21];
int f[1 << 21][21];
int main(){
    int n ;
    cin >> n;
    memset(f, 0x3f, sizeof f);
    for (int i =0; i< n; i++){
        for (int j =0; j< n; j++){
            cin >> g[i][j];
        }
    }

    f[1][0] = 0;

    for (int i = 1; i< 1<< n; i++){
        for (int j = 0; j < n; j++){
            if (!(i & 1<< j)) continue;
            int a = i - (1 << j);
            for (int k = 0; k <n; k++){
                if (!(a &(1<< k))) continue;
                f[i][j] = min(f[i][j], f[i - (1<<j)][k] +g[k][j]);
            }
        }
    }
    cout << f[(1<<n) -1][n-1]<< endl;
    return 0;
}
```

# [AcWing 1064. 小国王](https://www.acwing.com/problem/content/1066/)

在 $n×n$ 的棋盘上放 $k$ 个国王，国王可攻击相邻的 $8$ 个格子，求使它们无法互相攻击的方案总数。

思路：

$f[i][k][j]$ 表示前 $i$行放了 $k$ 个国王， 状态为 $j$

```cpp
#include <iostream>
#include <vector>
using namespace std;
const int N = 12, C = N*N, M = 1<< N;
int cnt[M];
vector<int> legal;
vector<int> pre[M];
int n, K;
long long f[N][C][M];
bool check(int s){
    return !(s & s>> 1);
}
int count(int s){
    int res = 0;
    for (int i =0; i< n; i++){
        if (s >> i & 1) res++;
    }
    return res;
}
int main(){

    cin >> n>> K;

    for (int i =0; i< 1<< n; i++){
        if (check(i)){
            cnt[i] = count(i);
            legal.push_back(i);
        }
    }
    for (int i : legal){
        for (int j : legal){
            if (!(i&j) && check(i|j)){
                pre[i].push_back(j);
            }
        }
    }
    f[0][0][0]= 1;
    for (int i = 1; i<= n+1; i++){
        for (int j : legal){
            for (int k= cnt[j]; k<=K; k++){
                for (int p: pre[j]){
                    f[i][k][j] += f[i-1][k-cnt[j]][p];
                }
            }
        }
    }
    cout << f[n+1][K][0] <<endl;
    return 0;
}
```

# [AcWing 327. 玉米田](https://www.acwing.com/problem/content/329/)

## 思路

$f[i][j]$ 表示 第 $i$ 行，状态 为 $j$ 的方案数

## 代码实现

```cpp
#include <iostream>
#include<vector>
using namespace std;
const int M = 13, N = 13, K = 1<<N, MOD = 1e8;
int m, n;
int f[M][K];
int g[M];
vector<int> legal;

bool check(int s){
    return !(s & s>> 1);
}
int main(){
    cin>> m >> n;
    for (int i = 1; i<= m ; i++){
        for (int j= 0; j< n; j++){
            int c ;
            cin >> c;
            if (c == 0) {
                g[i] += 1 << j;
            }
        }
    }
    for (int i =0; i< 1<< n; i++){
        if (check(i)) legal.push_back(i);
    }

    f[0][0] = 1;
    for (int i = 1; i<= m+1; i++){
        for (int j : legal){
            if (j & g[i]) continue;
            for (int p: legal){
                if(j & p || p & g[i-1]) continue;
                f[i][j] = (f[i][j] + f[i-1][p]) %MOD;
            }
        }
    }
    cout << f[m+1][0] << endl;
    return 0;
}
```

# [AcWing 292. 炮兵阵地](https://www.acwing.com/problem/content/294/)

## 思路

第 $i$ 行的状态依赖上两行，所以定义

$f[i][j][k]$ 表示 到 $i$ 行，且状态为 $j$ ，上一行状态为 $k$ 的 最大炮兵部队 数量

## 代码实现

```cpp
#include <iostream>
#include <vector>
using namespace std;
const int N = 110, M = 13, K = 1 << M;
int f[2][K][K];
int n, m;
char c;
int g[N];
vector<int> legal_status;
int cnt[K];

bool check(int s){
    if (s & (s >> 1 | s>> 2) ) return false;
    return true;
}
int count(int s){
    int res = 0;
    for (int i =0; i<m; i++){
        if (s >> i & 1) res++;
    }
    return res;
}

int main(){

    cin >> n >> m;

    for (int i = 1; i<= n; i++){
        for (int j =0; j <m ; j++){
             cin>> c;
            if (c == 'H') g[i] += 1 << j;
        }
    }
    for (int i =0; i<1<<m; i++) {
        if (check(i)) {
            legal_status.push_back(i);
            cnt[i]= count(i);
        }
    }
    for (int i = 1; i<= n+2; i++){
        for (int a : legal_status){ // 当前行
            for (int b: legal_status){ // 上一行
                if (b & g[i-1]) continue;
                for(int c: legal_status){ // 上上行
                    if (c & g[i-2]) continue;
                    if ((a&b) | (b &c) | (a&c) ) continue;
                    f[i&1][a][b] = max(f[i&1][a][b], f[i-1 & 1][b][c] + cnt[a]);
                }

            }
        }
    }

    cout << f[n + 2& 1][0][0] << endl;

    return 0;
}
```

# 重复覆盖问题

给定 01 矩阵

重复覆盖问题：最少选多少行，可以覆盖所有列

精确覆盖问题： 最少选多少行，使每一列选而且只选一个 1

八皇后，数独：精确覆盖问题

愤怒的小鸟：重复覆盖问题

最优解法：Dancing Link => 优化爆搜

# AcWing 524. 愤怒的小鸟

## 爆搜解决重复覆盖问题

```

res // 全局返回值
path[x,y] 表示经过点x和点y的抛物线 经过所有点的state
void dfs(state，cnt){ // 枚举所有当前覆盖的状态, 抛物线数量
	if state已经覆盖所有点 res = max(cnt)
	for 枚举没有覆盖的点 x
		for 枚举经过没有覆盖的点的所有抛物线（两点确定，也就是枚举所有点y，枚举经过点x和点y的path）
			dfs(state | path[x,y], cnt+1)
}
```

## 爆搜转化成状态压缩 DP

$f[i]$ 表示状态为 i 的最少抛物线数量

$f[i | path[x,y]] = min(f[i] + 1)$

## 代码实现

```cpp
#include <iostream>
#include<algorithm>
#include<cmath>
#include<cstring>

using namespace std;

const int N = 18, M = 1<< 18;
double eps = 1e-8;
typedef pair<double, double> PDD;
#define x first
#define y second

PDD p[N];
int f[M];
int path[N][N];

int cmp(double x, double y){
    if (fabs(x-y) < eps) return 0;
    if (x < y) return -1;
    return 1;
}

int T, n, m;

int main(){

    cin >> T;
    while (T--){
        cin >> n >> m;

        for (int i =0; i< n; i++){
            cin >> p[i].x >> p[i].y;
        }

        memset(path, 0, sizeof path);

        for (int i =0; i <n; i++){
            path[i][i] = 1<< i;
            for (int j =0; j< n; j++){
                double x1 = p[i].x, y1 = p[i].y, x2 = p[j].x, y2 = p[j].y;
                if (!cmp(x1, x2)) continue;
                double a = (y1 / x1 - y2 /x2) / (x1 - x2);
                double b = (y1 - a* x1 *x1) / x1;
                if (cmp(a, 0) >= 0) continue;
                int state =0;
                for (int k = 0; k <n; k++){
                    if (!cmp(a*p[k].x*p[k].x + b*p[k].x, p[k].y)) {
                        state += 1<<k;
                    }
                }
                path[i][j] = state;
            }
        }

        memset(f, 0x3f, sizeof f);
        f[0] =0;
        for (int i = 0; i+1<1<<n; i++){

            int k = 0;
            for (int j =0; j< n; j++){
                if (!(i>> j & 1)) {
                    k = j;
                  	break;
                }
            }

            for (int j =0; j< n; j++){
                f[i|path[k][j]] = min(f[i|path[k][j]], f[i] + 1);
            }
        }
        cout << f[(1<<n )-1] <<endl;
    }
    return 0;
}
```
