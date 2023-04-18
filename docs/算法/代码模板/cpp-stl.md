# C++ STL

## 头文件和作用域

```cpp
#include <bits/stdc++.h>
using namespace std;
```

## 输入

- 输入数字 `cin >> a`
- 输入字符 `getline(cin, s);`，考虑到中间会有空格，所以用输入流`getline`。
- `cin` 和 `scanf` 读入字符串时遇到空格就停止了。

### 常见的两种输入

第一种：case 组数 不确定

```cpp
while(scanf("%d %d", &a, &b) != EOF){
    cout << getCounts(n) << endl;
}
```

第二种：一共 n 组 case

```cpp
int k;
cin >> k; // k是行数
while (k--){
    int a, b;
    cin >> a >> b;
}
```

- Q: 请问`while(scanf("%d%d",&n,&m))!=EOF` 为什么可以写成 `while(~scanf("%d%d",&n,&m))`，而不是 `while(scanf("%d%d",&n,&m))`？
- A: 论如何正确认识`scanf`的返回值。百科里说什么没读到 n 和 m 返回 0 对吧，下一句，如果碰到错误，比如`End Of File`这个，返回常量`EOF`，`EOF`一般默认定义为`-1`，`-1`按位取反就是`0`，其他的按位取反当然`非0`、最保险的写法其实是，`scanf()!=EOF`

### cin 和 getline 冲突问题解决

```cpp
int n;
cin >> n;
getchar(); // 除去换行符
while (n --) {
    string s;
    getline(cin, s);
}
```

## 输出

- 浮点数保留三位小数 `printf("%.3lf", d);`
- 64 位输出请用 `printf("%lld")`

## 内存赋值

### memset

**memset 只能把整型数组的值设置为 0 或-1**

在$memset$使用时要千万小心，在**给 char 以外的数组赋值时**，只能初始化为 $0$ 或者$-1$

**原因**：memset 是按字节一个一个的设置，比如把整型数 a 设置为 1，int 是 32 位的共四个字节，每个字节设置为 1，则为$00000001 00000001 00000001 00000001$转为十进制数是$1+1*2^8+1*2^16+1*2^24=16843009$，而不是 1。

对于 0 和-1，0 为 $00000000 00000000 00000000 00000000$，转化为十进制为 0，

-1 为 $11111111 11111111 11111111 11111111$（负数在内存中是以补码的形式存在），转化后为-1

## 数学

`#define MaxN 0x3f3f3f3f` // 无穷大
`#define MinN 0xc0c0c0c0` // 无穷小

## 运算法优先级

算数 > 移位 > 关系 > 位运算 > 逻辑 > 赋值

```
 算数 *,/,%,+,-
 高于 移位 <<，>>
 高于 关系 >, >=, <，<=, ==, !=
 高于 位运算 &,^,！
 高于 逻辑 &&,||
 高于 赋值 =,+=,-=,*=,/=,%=
```

![image-20220717195436808](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220717195436808.png)

## vector

变长数组，倍增的思想

- size() 返回元素个数
- empty() 返回是否为空
- clear() 清空
- front()/back()
- push_back()/pop_back()
- begin()/end()
- 支持比较运算，按字典序
- slice: `vector<int>(arr.begin()+i, arr.begin()+j)`

## pair<int, int>

- first, 第一个元素
- second, 第二个元素
- 支持比较运算，以 first 为第一关键字，以 second 为第二关键字（字典序）

## string

字符串

- size()/length() 返回字符串长度
- empty()
- clear()
- substr(起始下标，(子串长度)) 返回子串
- c_str() 返回字符串所在字符数组的起始地址
- append(1, c) 末尾追加一个字符
- erase
  - erase(str.begin()) 删除开头
  - erase(str.end() - 1) 删除结尾
  - erase(str.begin() + 3, str.end() - 3) 删除一个区间
  - s.erase(0, s.find_first_not_of(" ")); 删除头部空格
  - s.erase(s.find_last_not_of(" ") + 1); 删除尾部空格
- atoi(s.c_str()) 字符串转数字；更多：atoi、atof、atol
- to_string(123) 数字转字符串
- reverse(s.begin(),s.end()); 反转字符串
- s.insert(s.begin(), c) 插到头部
- s.insert(s.begin() + 3, 'i') 插到中间

string.h 库

- 求字符串长度： int len = strlen(str);
- 字符串复制： strcpy();
- 字符串比较： strcmp();
- 字符串拼接： strcat();
- 查询字串： strchr();
- 查询子串： strstr();

## queue, 队列

- size()
- empty()
- push() 向队尾插入一个元素
- front() 返回队头元素
- back() 返回队尾元素
- pop() 弹出队头元素

## priority_queue

头文件：`#include <queue>`

优先队列，默认是 大根堆

- push() 插入一个元素
- top() 返回堆顶元素
- pop() 弹出堆顶元素
- `priority_queue<int> q;` 默认：大根堆，相当于 `priority_queue<int, vector<int>, less<int>> q;`
- 定义成小根堆的方式：`priority_queue<int, vector<int>, greater<int>> q;`
- 队列元素为 PII; `priority_queue<PII, vector<PII>, greater<PII>> heap;` // 小顶堆
  自定义比较器：

```cpp
struct Node {
    int l, r, h;

    Node(int _l, int _r, int _h) : l(_l), r(_r), h(_h) {};

    bool operator<(const Node &o) const {
        return this->h < o.h;
    }
};
priority_queue<Node> heap; // 大顶堆
```

注意：

- cpp 比较器 默认 `operator <` 为 大顶堆，less
- java 默认是 小顶堆

## stack

栈

- size()
- empty()
- push() 向栈顶插入一个元素
- top() 返回栈顶元素
- pop() 弹出栈顶元素

## deque

双端队列

- size()
- empty()
- clear()
- front()/back()
- push_back()/pop_back()
- push_front()/pop_front()
- begin()/end()

## set, map, multiset, multimap

基于平衡二叉树（红黑树），动态维护有序序列

- size()
- empty()
- clear()
- begin()/end()
- ++, -- 返回前驱和后继，时间复杂度 O(logn)

### set/multiset

- insert() 插入一个数
- find() 查找一个数
- count() 返回某一个数的个数
- erase()
  - 输入是一个数 x，删除所有 x; O(k + logn)
  - 输入一个迭代器，删除这个迭代器
- lower_bound()/upper_bound()
  - lower_bound(x) 返回大于等于 x 的最小的数的迭代器
  - upper_bound(x) 返回大于 x 的最小的数的迭代器

### map/multimap

- insert() 插入的数是一个 pair
- erase() 输入的参数是 pair 或者迭代器
- find()
- [] 注意 multimap 不支持此操作。 时间复杂度是 O(logn)
- lower_bound()/upper_bound()

### unordered_set, unordered_map, unordered_multiset, unordered_multimap

哈希表

- 和上面类似，增删改查的时间复杂度是 O(1)
- 不支持 `lower_bound()/upper_bound()`， 迭代器的++，--

### bitset

圧位

```cpp
bitset<10000> s;
~, &, |, ^
>>, <<
==, !=
[]
```

- count() 返回有多少个 1
- any() 判断是否至少有一个 1
- none() 判断是否全为 0
- set() 把所有位置成 1
- set(k, v) 将第 k 位变成 v
- reset() 把所有位变成 0
- flip() 等价于~
- flip(k) 把第 k 位取反

## 技巧

- unordered_map + priority_queue 应用于有增删操作的求最值操作中
- unordered_map 用作计数器，从堆顶取极值的时候，判断堆顶元素个数是否大于 0
