# #include\<vector>

## 声明

```cpp
vector<int> a; // 相当于长度动态变化的 int数组
vector<int> b[233]; // 一维长度 233，二维长度动态变化的 int数组

vector<int> a = {1,2,3}; // 初始化并赋值
vector<int>{1, 2, 3}; // 初始化并赋值
// 使用迭代器声明
vector<int>(res.begin() + i, res.begin() + j); // 截取 [i, j) 区间
vector<int>(ans.rbegin(), ans.rend()); // 翻转 vector
vector<int>(res.rbegin(), res.rbegin() + 2); // 截取 末尾 两个元素，且倒序输出
```

## begin/end

begin/end 都是 vector 的迭代器函数；

begin() 指向第一个元素，end() 指向 vector 的尾部（最后一个元素的下一个位置）；

举例：对于 `vector<int> a;`，$*a.begin()$ 等价于 $a[0]$，$*a.end()$ 和 $a[n]$ 都是越界访问。$a.begin() ++$ 指向 $a[1]$， $a.begin() + i$ 指向 $a[i]$

$rbegin / rend$ 是倒序的迭代器，$rbegin()$ 指向 vector 的尾部最后一个元素，rend() 指向 vector 的头部（第一个元素的前一个位置）；

**rbegin/rend** 可以用来翻转 vector

## front/back

## push_back/pop_back

$a.push\_back(x)$ 插入 x 到 a 的尾部

$a.pop\_back()$ 删除 a 尾部最后一个元素

结合使用可以实现模拟 栈 的操作

# #include\<queue>

## queue

循环队列

### 声明

```cpp
queue<int> q;
```

### 方法

```
push() 插入堆
pop() 注意 q.pop() 方法 没有返回值
front() // 获取队头
back() // 获取队尾
```

## priority_queue

默认为 大根堆

### 方法：

- push() 插入堆
- pop() 注意 q.pop() 方法 没有返回值
- top() 查询堆顶

### 小根堆实现

重载 运算符 "<" ，return 改成 ">" 即可

```cpp
struct rec{int id; double val; };
bool operator < (const rec &a , const rec &b) {
  return a.val > b.val;
}
```

对于 $priority\_queue<int, vector<int>>$ ，可以直接使用 比较器 $greater<int>$ 实现

### 惰性删除

开辟额外空间记录元素是否已经从堆中删除

## deque

# #include\<set>

与 优先队列一样， set 和 multiset 也必须定义 **“小于号”** 操作符

## 声明

```cpp
set<int> s;
struct rec{...}; set<rec> s;
multiset<double> s;
```

## 方法

### insert()

### find()

### lower_bound() / upper_bound()

### erase()

### count()
