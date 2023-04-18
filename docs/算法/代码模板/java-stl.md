# 常用 STL

排序：

- Arrays.sort
- Collections.sort
  集合和数组互转：

- 数组转集合：Arrays.asList
- 集合转数组：`collectionObj.toArray();`

## Deque

队列

常用方法：

- void addFirst(E e); //插入头部，异常会报错
- void addLast(E e); //插入尾部，异常会报错
- removeFirst(); // 移除头部，异常不报错
- removeLast(); // 移除尾部，异常不报错
- getFirst(); // 获取头部，异常会报错
- getLast(); // 获取尾部，异常会报错
  左进右出 是队列；右进右出 是栈

## PriorityQueue

优先队列、堆

支持动态排序，用于实现 大顶堆，小顶堆

常用方法：

- add(Object o) : 添加对象到集合
- remove(Object o) : 删除指定的对象
- size() : 返回当前集合中元素的数量
- contains(Object o) : 查找集合中是否有指定的对象
- isEmpty() : 判断是否为空

## TreeMap

红黑树的实现，只需要用到 key 时可以使用 $TreeSet$

用于求 下一个 大于等于、严格大于、小于等于、严格小于等情况，相当于 C++中的 lower_bound

常用方法：

- `containsKey(Object key)`：是否包含 Key 为 key 的元素
- get(Object key): 获取元素的 Value
- `put(K key, V value)`：添加元素

- isEmpty(): 检出 map 集合中是否有元素

- size(): 返回 map 集合中元素个数

- remove(Object key): 删除 Key 为 key 值的元素

- clear()：把 map 集合中所有的键值删除

- `Set<Map.Entry<K,V>> entrySet()` : 遍历 Map 使用，将 map 集合以 Key=Value 的形式返回到 set 中

  ```java
  for (Map.Entry<Integer,Integer> entry: map.entrySet()) {
  	map.getKey(); map.getValue();
  }
  ```

## Comparator 接口

自定义比较器

使用方法：覆写 $compare$ 方法

```java
int m = 10, n = 2;
int f[][] = new int[m][n];

Random r = new Random();
for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
        f[i][j] = r.nextInt(10);
    }
}
Arrays.sort(f, new Comparator<int[]>() {
    @Override
    public int compare(int[] o1, int[] o2) {
        if (o1[0] == o2[0]) {
            return o2[1] - o1[1]; // 第1项从大到小排序
        }
        return o1[0] - o2[0]; // 第0项从小到大排序
    }
});
```

# 其他注意操作

## 数据类型互转

- Integer.valueOf(E) : string 等转成 `int` 类型

- String.valueOf(E) : `int , char[]` 等转成 $string$

- String.toCharArray() ：string 转成 `char[]`

## 数组常用操作

- 一维数组初始化

  ```java
  int f[] = new int[3] // 声明数组(`int data[]` 和 `int []data` 两种写法均可)
  int[] f = {1,2,3}  // 静态初始化

  Arrays.fill(f, -1) //赋值
  Arrays.fill(f, 0, n-1, -1) //赋值
  ```

- 二维数组初始化

  ```java
  // 声明并赋值
  int f[][] = new int[m][n];
  for (int i = 0; i < m; i++) {
    Arrays.fill(f[i], -1);
  }
  // 静态初始化
  int f[][] = new int[][]{{1, 2, 3}, {4, 5}, {6, 7, 8, 9}}
  ```

- $Arrays.copyOf$(数组名，扩容后长度) : 数组扩容

- $Arrays.copy()$：数组的复制

- $Arrays.sort()$：数组排序

- $Arrays.fill(数组名, 开始位置 , 结束位置, 填入的值)$：向数组中填充元素

- 获取数组长度注意：$arr.length$ 不带括号，对象用$length()$函数，基本数据类型不带括号

# 集合 Collection（TL;DR）

- List 队列接口 extends Collection<E>
  - LinkedList 双端链表列表类 implements List<E>, Deque<E>
  - ArrayList 数组列表类 implements List<E>
  - Vector 容器类 implements List<E> 不推荐使用
    - Stack 栈类 extends Vector<E> 不推荐使用，请使用 Queue 队列接口的
- Set 集合接口 extends Collection<E>
  - HashSet 哈希集合类 implements Set<E>
  - TreeSet
- Queue 队列接口 extends Collection<E>
  - PriorityQueue 优先队列类 implements Queue<E>
  - Deque 双端队列接口 extends Queue<E>
    主要方法:
- Map 接口？

## 通用方法

- add(Object o) : 添加对象到集合
- remove(Object o) : 删除指定的对象
- size() : 返回当前集合中元素的数量
- contains(Object o) : 查找集合中是否有指定的对象
- isEmpty() : 判断集合是否为空
- iterator() : 返回一个迭代器
- containsAll(Collection c) : 查找集合中是否有集合 c 中的元素
- addAll(Collection c) : 将集合 c 中所有的元素添加给该集合
- clear() : 删除集合中所有元素
- removeAll(Collection c) : 从集合中删除 c 集合中也有的元素
- retainAll(Collection c) : 从集合中删除集合 c 中不包含的元素

## Map 接口

- HashMap<K,V> 哈希 map 类 implements Map<K,V>
- LinkedHashMap
- TreeMap
- Hashtable 古老的实现类，线程安全，效率低，不可以存储 null 的 key 和 value。底层都使用哈希表结构，查询速度快。

## Queue 队列接口 extends Collection<E>

### Deque 双端队列接口 extends Queue<E>

推荐使用：

- void addFirst(E e); //插入头部，异常会报错
- void addLast(E e); //插入尾部，异常会报错
- E getFirst(); // 获取头部，异常会报错
- E getLast(); // 获取尾部，异常会报错
- E removeFirst(); // 移除头部，异常不报错
- E removeLast(); // 移除尾部，异常不报错
  其他使用

- boolean offerFirst(E e); // 插入头部，异常返回 false
- boolean offerLast(E e); // 插入尾部，异常返回 false
- E peekLast(); // 获取尾部，异常不报错
- E peekFirst(); //获取头部，异常不报错
- E pollLast(); //移除尾部，异常会报错
- E pollFirst(); //移除头部，异常会报错

### PriorityQueue 优先队列类 implements Queue<E>

PriorityQueue 的 peek()和 element 操作是常数时间，add(), offer(), 无参数的 remove()以及 poll()方法的时间复杂度都是 log(N)。

## List

list 主要方法：

- `List<Integer> path = new ArrayList<>()` 初始化
- `new ArrayList<>(path)` 复制
- add(int index,Object element) 在指定位置上添加一个对象
- addAll(int index, Collection c) 将集合 c 的元素添加到指定的位置
- get(int index)返回 List 中指定位置的元素
- indexOf(Object o)返回第一个出现元素 o 的位置.
- remove(int index)删除指定位置的元素
- `set(int index, Object element)`: 用元素 element 取代位置 index 上的元素,返回被取代的元素
- sort()

## Stack

使用双端队列 Deque 来实现

## Set

不包含重复的元素

- HashSet
- SortSet 有序集合
  - TreeSet

**注意：**Java 中没有 multiset 的实现，Guava 中进行了相关实现，需要引包

## Map

一般使用 $HashMap、TreeMap$ 就够了，HashMap 用作最基础的 Map , TreeMap 用作红黑树 Key 有序的情况

常用方法：

- `put(K key, V value)`：添加元素
- `putAll(Map<? extends K,? extends V> m)`：向 map 集合中添加指定集合的所有元素
- clear()：把 map 集合中所有的键值删除
- `containsKey(Object key)`：是否包含 Key 为 key 的元素
- containsValue(Object value)：检出 map 集合中有没有包含 Value 为 value 的元素
- `Set<Map.Entry<K,V>> entrySet()`：返回 map 到一个 Set 集合中，以 map 集合中的 Key=Value 的形式返回到 set 中。
  遍历时使用: `for (Map.Entry<Integer,Integer> entry: map.entrySet()) {map.getKey(); map.getValue();}`
- equals(Object o): 判断两个 Set 集合的元素是否相同
- get(Object key): 根据 map 集合中元素的 Key 来获取相应元素的 Value
- isEmpty(): 检出 map 集合中是否有元素
- `Set<K> keySet()`: 返回 map 集合中所有 Key
- remove(Object key): 删除 Key 为 key 值的元素
- size(): 返回 map 集合中元素个数
- `Collection<V> values()`: 返回 map 集合中所有的 Value 到一个 Collection 集合

# Lower_bound 和 upper_bound

推荐使用 TreeMap 实现

当数组中的元素递增时

- lower_bound 函数返回容器中第一个**大于等于**目标值的位置
- upper_bound 函数返回容器中第一个**大于**目标值的位置。
  若数组中的元素都比目标值小则返回最后一个元素的下一个位置。

当数组中的元素递减时

- lower_bound 函数返回容器中第一个**小于等于**目标值的位置
- upper_bound 函数返回容器中第一个**小于**目标值的位置。
  若数组中的元素都比目标值大则返回最后一个元素的下一个位置。

```java
public static int lower_bound(int[] A, int l, int r, int target) {
    while (l < r) {
        int mid = (l + r) >>> 1;
        if (target <= A[mid]) r = mid;
        else l = mid + 1;
    }
    return l;
}

public static int upper_bound(int[] A, int l, int r, int target) {
    while (l < r) {
        int mid = (l + r) >>> 1;
        if (target < A[mid]) r = mid;
        else l = mid + 1;
    }
    return l;
}
```
