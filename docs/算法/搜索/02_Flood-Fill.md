# Flood Fill

# AcWing 1097. **池塘计数**

## 方向表示

**8 个方向 VS 4 个方向**

4 方向表示

```cpp
int dx[] = {-1, 0, 1, 0, -1};
for (int d = 0; d< 4; d++) {
  int x = i + dx[d], y = j + dx[d];
}
```

8 方向表示

```cpp
for (int dx =-1; dx <= 1; dx++){
  for (int dy = -1; dy<=1; dy++){
    int x = i+dx, y = j+dy;
  }
}
```

此题为 8 方向表示法

## DFS VS BFS

DFS 代码实现

```cpp
#include<iostream>
using namespace std;

const int N = 1010, M = N;
char g[N][M];
int n, m;

void dfs(int i, int j){
    g[i][j] = '.'; // 注意：dfs 和 bfs 都需要开始就 进行 flood fill 操作
    for (int dx =-1; dx<=1; dx++){
        for (int dy = -1; dy<= 1; dy++){
            if(dx == 0 && dy == 0) continue;
            if (g[i+dx][j+dy] == 'W') {
                dfs(i+dx, j+dy);
            }
        }
    }
}

int main(){
    cin >> n >> m;
    for (int i =1; i<=n; i++)
        for (int j = 1; j<=m; j++) {
            cin>>g[i][j];
        }
    int ans =0;
    for (int i=1; i<=n; i++){
        for (int j =1; j<=m; j++){
            if (g[i][j] == 'W'){
                ans++;
                dfs(i, j);
            }
        }
    }
    cout << ans << endl;
    return 0;
}
```

BFS 代码实现

```cpp
#include<iostream>
#define    x first
#define    y second
using namespace std;

typedef pair<int, int> PII;
const int N = 1010, M = N;
char g[N][M];
PII q[M*N];
int n, m, ans;

void bfs(int i, int j){
    int hh=0, tt= -1;
    q[++tt] = {i,j};
    g[i][j] = '.';
    while (hh <= tt){
        PII t = q[hh++];
        for (int dx = -1; dx <=1; dx++){
            for (int dy= -1; dy<=1; dy++){
                if (dx ==0 && dy == 0) continue;
                int x = dx + t.x, y = dy+t.y;
                if (g[x][y] == 'W') {
                    g[x][y] = '.';
                    q[++tt] = {x,y};
                }
            }
        }
    }
}
int main(){
    cin >> n>> m;
    for (int i =1; i<=n; i++)
        for (int j = 1; j<=m; j++){
            cin >> g[i][j];
        }
    for (int i =1; i<=n; i++)
        for (int j = 1; j<=m; j++){
            if (g[i][j]== 'W') {
                bfs(i, j);
                ans++;
            }
        }

    cout << ans << endl;
    return 0;
}
```

DFS 代码较短

## 并查集思路
