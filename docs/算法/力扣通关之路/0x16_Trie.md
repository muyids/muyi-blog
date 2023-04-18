# Road Map

<iframe
  :src="$withBase('/trie.html')"
  width="100%"
  height="800"
  frameborder="0"
  scrolling="No"
  leftmargin="0"
  topmargin="0"
/>

路线推荐：

- Trie 树模板：208 -> 211 -> 677
- 单词拆分：208 -> 139 -> 140 -> 472
- 字典序：208 -> 386 -> 440

# Trie 树

Trie 树，又称前缀树或字典树

## 基本性质

- 根节点不包含字符，除根节点以外每个节点只包含一个字符
- 从根节点到某一个节点，路径上经过的字符连接起来，为该节点对应的字符串
- 每个节点的所有子节点包含的字符串不相同

## 字典树模板

单词构成全部是小写字母 a-z 的情况

**Java 模板**

```java
public class Trie {
    boolean isEnd;
    Trie[] next;
    public Trie() {
        this.isEnd = false;
        this.next = new Trie[26];
    }
    public void insert(String word) {
        Trie node = this;
        for (int i = 0; i < word.length(); i++) {
            int k = word.charAt(i) - 'a';
            if (node.next[k] == null) {
                node.next[k] = new Trie();
            }
            node = node.next[k];
        }
        node.isEnd = true;
    }

    public boolean search(String word) {
        Trie root = this;
        for (int i = 0; i < word.length(); i++) {
            int w = word.charAt(i) - 'a';
            if (root.next[w] == null) return false;
            root = root.next[w];
        }
        return root.isEnd;
    }

    public boolean startsWith(String prefix) {
        Trie root = this;
        for (int i = 0; i < prefix.length(); i++) {
            int w = prefix.charAt(i) - 'a';
            if (root.next[w] == null) return false;
            root = root.next[w];
        }
        return true;
    }
}
```

**cpp 模板**

```cpp
struct treeNode {
    bool isEnd; // 是否存在已当前位置结尾的单词
    treeNode *next[26]; // 仅适用于全部是小写字母a-z的情况；更为鲁棒的情况`map<char, treeNode*> next;`
    treeNode() {
        isEnd = false;
        memset(next, 0, sizeof(next));
    }
};

class Trie {
public:
    treeNode *root; // 共有变量，供外部程序访问字典树
    Trie() {
        root = new treeNode();
    }
    void insert(const string &word) {
        treeNode *node = root;
        for (char c : word) {
            if (node->next[c - 'a'] == NULL) {
                node->next[c - 'a'] = new treeNode(); // 存在分支
            }
            node = node->next[c - 'a']; // 向后插入字符
        }
        node->isEnd = true; // 到达单词某位
    }
    bool search(const string &word) {
        treeNode *node = root;
        for (char c : word) {
            node = node->next[c - 'a']; // 向后迭代
            if (node == NULL) {
                return false; // 当前位置字符不存在
            }
        }
        return node->isEnd; // 搜索存在单词
    }
    bool startsWith(const string &prefix) {
        treeNode *node = root;
        for (char c : prefix) {
            node = node->next[c - 'a']; // 向后迭代
            if (node == NULL) {
                return false; // 当前位置字符不存在
            }
        }
        return node != NULL; // 最后一个字符存在
    }
};
```

## 应用场景

### 字符串检索

事先将已知的一些字符串（字典）的有关信息保存到 trie 树里，查找另外一些未知字符串是否出现过或者出现频率。

举例：

1. 给出 N 个单词组成的熟词表，以及一篇全用小写英文书写的文章，请你按最早出现的顺序写出所有不在熟词表中的生词。
2. 给出一个词典，其中的单词为不良单词。单词均为小写字母。再给出一段文本，文本的每一行也由小写字母构成。判断文本中是否含有任何不良单词。例如，若 rob 是不良单词，那么文本 problem 含有不良单词。
3. 1000 万字符串，其中有些是重复的，需要把重复的全部去掉，保留没有重复的字符串。

### 文本预测、自动完成，see also，拼写检查

### 词频统计

1. 有一个 1G 大小的一个文件，里面每一行是一个词，词的大小不超过 16 字节，内存限制大小是 1M。返回频数最高的 100 个词。
2. 一个文本文件，大约有一万行，每行一个词，要求统计出其中最频繁出现的前 10 个词，请给出思想，给出时间复杂度分析。
3. 寻找热门查询：搜索引擎会通过日志文件把用户每次检索使用的所有检索串都记录下来，每个查询串的长度为 1-255 字节。假设目前有一千万个记录，这些查询串的重复度比较高，虽然总数是 1 千万，但是如果去除重复，不超过 3 百万个。一个查询串的重复度越高，说明查询它的用户越多，也就越热门。请你统计最热门的 10 个查询串，要求使用的内存不能超过 1G。

### 排序

Trie 树是一棵多叉树，只要先序遍历整棵树，输出相应的字符串便是按字典序排序的结果。

比如给你 N 个互不相同的仅由一个单词构成的英文名，让你将它们按字典序从小到大排序输出。

### 字符串最长公共前缀

Trie 树利用多个字符串的公共前缀来节省存储空间，当我们把大量字符串存储到一棵 trie 树上时，我们可以快速得到某些字符串的公共前缀。

举例：

- 给出 N 个小写英文字母串，以及 Q 个询问，即询问某两个串的最长公共前缀的长度是多少？

- 解决方案：首先对所有的串建立其对应的字母树。此时发现，对于两个串的最长公共前缀的长度即它们所在结点的公共祖先个数，于是，问题就转化为了离线（Offline）的最近公共祖先（Least Common Ancestor，简称 LCA）问题。

而**最近公共祖先问题**同样是一个经典问题，可以用下面几种方法：

1. 利用并查集（Disjoint Set），可以采用采用经典的`Tarjan 算法`；
2. 求出字母树的`欧拉序列（Euler Sequence）`后，就可以转为经典的`最小值查询（Range Minimum Query，简称RMQ）`问题了；

### 字符串搜索的前缀匹配

trie 树常用于搜索提示。如当输入一个网址，可以自动搜索出可能的选择。当没有完全匹配的搜索结果，可以返回前缀最相似的可能。

Trie 树检索的时间复杂度可以做到 n，n 是要检索单词的长度，如果使用暴力检索，需要指数级 O(n2)的时间复杂度。

### 作为其他数据结构和算法的辅助结构

如后缀树，AC 自动机等

后缀树可以用于全文搜索

#### 练习题目

- [LeetCode 208. Implement Trie (Prefix Tree) (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/208.implement-trie-prefix-tree.md)

- [211. 添加与搜索单词 - 数据结构设计](https://leetcode-cn.com/problems/design-add-and-search-words-data-structure/)

- [LeetCode 140. Word Break II (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/101-200/140.word-break-ii.md)

- [LeetCode 212. Word Search II (hard)](https://github.com/muyids/leetcode/blob/master/algorithms/201-300/212.word-search-ii.md)

- [LeetCode 820. Short Encoding of Words (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/801-900/820.short-encoding-of-words.md)

- [LeetCode 1268. Search Suggestions System (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/1201-1300/1268.search-suggestions-system.md)

#### [211. 添加与搜索单词 - 数据结构设计](https://leetcode-cn.com/problems/design-add-and-search-words-data-structure/)

```java
class WordDictionary {
    Node root;

    class Node {
        boolean isEnd;
        Node[] child;

        public Node() {
            this.isEnd = false;
            child = new Node[26];
        }
    }

    public WordDictionary() {
        this.root = new Node();
    }

    public void addWord(String word) {
        Node p = this.root;
        for (char ch : word.toCharArray()) {
            if (p.child[ch - 'a'] == null) {
                p.child[ch - 'a'] = new Node();
            }
            p = p.child[ch - 'a'];
        }
        p.isEnd = true;
    }
    public boolean search(String word) {
        return dfs(word, 0, this.root);
    }

    boolean dfs(String word, int i, Node p) {
        if (p == null) return false;
        if (i == word.length()) return p.isEnd;
        if (word.charAt(i) != '.') {
            p = p.child[word.charAt(i) - 'a'];
            return dfs(word, i + 1, p);
        } else {
            for (int d = 0; d < 26; d++) {
                if (dfs(word, i + 1, p.child[d])) return true;
            }
            return false;
        }
    }
}
```
