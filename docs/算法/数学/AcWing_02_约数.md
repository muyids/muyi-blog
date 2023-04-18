# 最大公约数

最大公约数表示 $(a,b)$

```cpp
/*
求两个正整数 a 和 b 的 最大公约数 d
则有 gcd(a,b) = gcd(b,a%b)
证明：
    设a%b = a - k*b 其中k = a/b(向下取整)
    若d是(a,b)的公约数 则知 d|a 且 d|b 则易知 d|a-k*b 故d也是(b,a%b) 的公约数
    若d是(b,a%b)的公约数 则知 d|b 且 d|a-k*b 则 d|a-k*b+k*b = d|a 故而d|b 故而 d也是(a,b)的公约数
    因此(a,b)的公约数集合和(b,a%b)的公约数集合相同 所以他们的最大公约数也相同 证毕#
*/
int gcd(int a, int b){
    return b ? gcd(b,a%b):a;
}
```

# 最小公倍数

最小公倍数表示 $[a,b]$

```coffeescript

scm = (a,b)->  # 求最小公倍数
  a * b / gcd(a, b)
```
