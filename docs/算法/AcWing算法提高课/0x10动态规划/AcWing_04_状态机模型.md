# 状态机模型

# [AcWing 1049. 大盗阿福](https://www.acwing.com/problem/content/description/1051/)

```cpp
#include <iostream>
using namespace std;

int f[100010][2];
int main(){
    int T;
    cin >> T;
    while (T--){
        int n ;
        cin >> n;
        cin >> f[0][1];
        for (int i = 1; i< n; i++){
            cin >> f[i][1];
            f[i][1] = f[i-1][0] + f[i][1];
            f[i][0] = max(f[i-1][1], f[i-1][0]);
        }
        cout << max(f[n-1][0], f[n-1][1])<< endl;
    }
    return 0;
}
```

# [1057. 股票买卖 IV](https://www.acwing.com/problem/content/description/1059/)

```cpp
#include<iostream>
#include <cstring>
using namespace std;
int A[100010];
int f[100010][110][2];
int main(){
    int N, K;
    cin >> N >> K;

    for (int i = 1; i<= N; i++) cin>> A[i];

    memset(f, 0xcf, sizeof f);

    f[0][0][0] = 0;
    for (int i = 1; i<= N; i++){
        for (int k = K; k>= 0 ; k--){
            f[i][k][0] = f[i-1][k][0];
            if (k) f[i][k][0] = max(f[i-1][k-1][1] + A[i], f[i][k][0]);
            f[i][k][1] = max(f[i-1][k][0] - A[i], f[i-1][k][1]);
        }
    }
    int res =0;
    for (int i = 1; i<=K; i++) {
        res = max(res, f[N][i][0]);
    }
    cout << res << endl;
    return 0;
}
```
