专项突击练手

#### [剑指 Offer II 001. 整数除法](https://leetcode-cn.com/problems/xoh6Oh/)

#### [剑指 Offer II 002. 二进制加法](https://leetcode-cn.com/problems/JFETK5/)

#### [剑指 Offer II 003. 前 n 个数字二进制中 1 的个数](https://leetcode-cn.com/problems/w3tCBm/)

**动态规划**

```java
class Solution {
    public int[] countBits(int n) {
        int[] dp = new int[n+1];
        for (int i =1; i<=n ; i++){
            dp[i] = dp[i>>1] + (i&1);
        }
        return dp;
    }
}
```

#### [剑指 Offer II 004. 只出现一次的数字 ](https://leetcode-cn.com/problems/WGki4K/)

#### [剑指 Offer II 005. 单词长度的最大乘积](https://leetcode-cn.com/problems/aseY1I/)

**二进制优化判断是否存在**

```java
class Solution {
    public int maxProduct(String[] words) {
        int ans = 0;
        int[] nums = new int[words.length];
        for (int i = 0; i < words.length; i++) {
            int num = 0;
            for (char c : words[i].toCharArray()) {
                num |= (1 << (c - 'a'));
            }
            nums[i] = num;
        }
        for (int i = 0; i < words.length; i++) {
            for (int j = i + 1; j < words.length; j++) {
                if ((nums[i] & nums[j]) == 0)
                    ans = Math.max(ans, words[i].length() * words[j].length());
            }
        }
        return ans;
    }
}
```

#### [剑指 Offer II 006. 排序数组中两个数字之和](https://leetcode-cn.com/problems/kLl5u1/)

**双指针**

```java
class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int l =0, r = numbers.length-1;
        for (;l <r;) {
            if (numbers[l] + numbers[r] < target) {
                l++;
            }else if (numbers[l]+numbers[r]>target)r--;
            else{
                int []ans = {l, r};
                return ans;
            }
        }
        return new int[2];
    }
}
```

#### [剑指 Offer II 007. 数组中和为 0 的三个数](https://leetcode-cn.com/problems/1fGaJU/)

```java
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> ans = new ArrayList<>();
        Arrays.sort(nums);

        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            for (int l = i + 1, r = nums.length - 1; l < r; l++) {
                if (l > i + 1 && nums[l] == nums[l - 1]) continue;
                while (l < r-1 && nums[i] + nums[l] + nums[r] > 0) r--;
                if (nums[i] + nums[l] + nums[r] == 0) ans.add(Arrays.asList(nums[i], nums[l], nums[r]));
            }
        }
        return ans;
    }
}
```

#### [剑指 Offer II 008. 和大于等于 target 的最短子数组](https://leetcode-cn.com/problems/2VG8Kg/)

**滑动窗口**

```java
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int l = 0, r = 0;
        int ans = nums.length + 1;
        while(r<nums.length) {
            target -= nums[r++];
            while ( l< r && target<=0) {
                ans = Math.min(ans, r-l);
                target+=nums[l++];
            }
        }
        return ans == nums.length + 1? 0: ans;
    }
}
```

#### [剑指 Offer II 009. 乘积小于 K 的子数组](https://leetcode-cn.com/problems/ZVAVXX/)

**滑动窗口**

枚举 以`r - 1`结尾的 满足乘积小于 K 的子数组

```java
class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
        int win = 1;
        int l = 0, r = 0;
        int cnt=0;
        while (r<nums.length){
            win*=nums[r++];
            while (l<r && win>=k){
                win /= nums[l++];
            }
            cnt+= r-l;
        }
        return cnt;
    }
}
```

#### [560. 和为 K 的子数组](https://leetcode-cn.com/problems/subarray-sum-equals-k/)

整数数组，有整有负有 0，不满足单调性，不能用滑动窗口

**前缀和+哈希表**

哈希表记录前缀和 s[i]出现的次数

```java
class Solution {
    public int subarraySum(int[] nums, int k) {
        int[]s = new int[nums.length+1];
        for (int i =1; i<=nums.length;i++) s[i] = s[i-1] + nums[i-1];
        Map<Integer, Integer> hash = new HashMap<>();
        hash.put(0, 1);
        int cnt = 0;
        for (int i = 1; i <= nums.length; i++){
            cnt+= hash.getOrDefault(s[i] - k, 0);
            hash.put(s[i], hash.getOrDefault(s[i], 0)+ 1);
        }
        return cnt;
    }
}
```

#### [剑指 Offer II 011. 0 和 1 个数相同的子数组](https://leetcode-cn.com/problems/A1NYOS/)

**前缀和+哈希表**

前缀和记录以 i 位置结尾的前缀数组中 0 比 1 多的个数

哈希表记录，0 比 1 多 key 次出现的第一个下标 i

```java
class Solution {
    public int findMaxLength(int[] nums) {
        int[] s = new int [nums.length+1];
        for (int i = 1; i<= nums.length; i++) {
            if (nums[i -1]== 0) s[i] = s[i-1]+1;
            else s[i] = s[i-1]-1;
        }
        Map<Integer, Integer> hash = new HashMap<>();
        hash.put(0, 0);
        int ans = 0;
        for (int i = 1; i<=nums.length; i++){
            if (hash.containsKey(s[i])) ans = Math.max(ans, i-hash.get(s[i]));
            else hash.put(s[i], i);
        }
        return ans;
    }
}
```

#### [剑指 Offer II 012. 左右两边子数组的和相等](https://leetcode-cn.com/problems/tvdfij/)

**前缀和+后缀和**

```java
class Solution {
    public int pivotIndex(int[] nums) {
        int n = nums.length;
        int[] p = new int[n + 1];
        int[] q = new int[n + 1];
        for (int i = 1; i <= n; i++) p[i] = p[i - 1] + nums[i - 1];
        for (int i = n - 1; i >= 0; i--) q[i] = q[i + 1] + nums[i];
        for (int i = 0; i<n; i++){
            if (p[i] == q[i+1])return i;
        }
        return -1;
    }
}
```

**常量空间优化**

记录总和+计算前缀和

```java
class Solution {
    public int pivotIndex(int[] nums) {
        int sum = 0;
        for (int x: nums) sum+=x;
        for (int p =0, i =0; i<nums.length; i++){
            if (p == sum -nums[i] -p)return i;
            p+=nums[i];
        }
        return -1;
    }
}
```

#### [剑指 Offer II 013. 二维子矩阵的和](https://leetcode-cn.com/problems/O4NDxx/)

**二维前缀和**

```java
class NumMatrix {
    int [][]s;
    public NumMatrix(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        s = new int[m+1][n+1];
        for (int i = 1; i<=m; i++){
            for (int j = 1; j<=n; j++){
                s[i][j] = matrix[i-1][j-1] + s[i-1][j] + s[i][j-1] - s[i-1][j-1];
            }
        }
    }
    public int sumRegion(int row1, int col1, int row2, int col2) {
        return s[row2+1][col2+1] - s[row1][col2+1] - s[row2+1][col1] + s[row1][col1];
    }
}
```

#### [剑指 Offer II 014. 字符串中的变位词](https://leetcode-cn.com/problems/MPnaiL/)

**滑动窗口**

```java
class Solution {
    public boolean checkInclusion(String s1, String s2) {
        int[] w = new int[26];
        for (char ch : s1.toCharArray()) {
            w[ch - 'a']++;
        }
        int l = 0, r = 0;
        while (r < s2.length()) {
            char c = s2.charAt(r++);
            w[c - 'a']--;
            while (l < r && w[c-'a'] < 0) {
                w[s2.charAt(l++) - 'a']++;
            }
            if(r-l == s1.length()) return true;
        }
        return false;
    }
}
```

#### [剑指 Offer II 015. 字符串中的所有变位词](https://leetcode-cn.com/problems/VabMRr/)

**滑动窗口**

```java
class Solution {
    public List<Integer> findAnagrams(String p, String s) {
        int []w = new int[26];
        for (char c: s.toCharArray()) w[c-'a']++;
        int l = 0, r = 0;
        List<Integer> as = new ArrayList<>();
        while (r < p.length()){
            char c = p.charAt(r++);
            w[c-'a']--;
            while(l<r && w[c-'a'] < 0){
               w[p.charAt(l++) - 'a']++;
            }
            if (r-l == s.length()) as.add(l);
        }
        return as;
    }
}
```

#### [剑指 Offer II 016. 不含重复字符的最长子字符串](https://leetcode-cn.com/problems/wtcaE1/)

**滑动窗口**

```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> w = new HashSet<>();
        int ans = 0;
        int l = 0, r = 0;
        while (r < s.length()) {
            char ch = s.charAt(r++);
            while (l<r && w.contains(ch)) {
                w.remove(s.charAt(l++));
            }
            w.add(ch);
            ans = Math.max(ans, r-l);
        }
        return ans;
    }
}
```

#### [剑指 Offer II 017. 含有所有字符的最短字符串](https://leetcode-cn.com/problems/M1oyTv/)

### HARD

#### [剑指 Offer II 018. 有效的回文](https://leetcode-cn.com/problems/XltzEq/)

**双指针**

```java
class Solution {
    public boolean isPalindrome(String s) {
        char[] cs = s.toCharArray();
        for (int i=0; i< cs.length; i++){
            if (cs[i] >='A' && cs[i] <='Z') cs[i] +=32;
        }
        for (int l =0, r=cs.length-1; l <r; ){
            while (l <r && !isNumOrChar(cs[l]))l++;
            while (l<r && !isNumOrChar(cs[r]))r--;
            if (cs[l] == cs[r]){
                l++;r--;
            }else return false;
        }
        return true;
    }
    boolean isNumOrChar(char c){
        if (c>='a' && c<='z') return true;
        if (c>='0'&& c<='9') return true;
        return false;
    }
}
```

#### [剑指 Offer II 019. 最多删除一个字符得到回文](https://leetcode-cn.com/problems/RQku0D/)

**双指针**

```java
class Solution {
    boolean isPali(String s, int l , int r){
        for (;l <r; l++, r--){
            if (s.charAt(l) != s.charAt(r)) return false;
        }
        return true;
    }
    public boolean validPalindrome(String s) {
        for (int l = 0, r = s.length()-1; l < r; l++, r--){
            if(s.charAt(l) != s.charAt(r)) {
                return isPali(s, l+1, r) || isPali(s, l, r-1);
            }
        }
        return true;
    }
}
```

#### [剑指 Offer II 020. 回文子字符串的个数](https://leetcode-cn.com/problems/a7VOhD/)

**枚举**

根据数据范围反推算法复杂度反推算法模型

```java
class Solution {
    public int countSubstrings(String s) {
        int cnt = 0;
        char []sc = s.toCharArray();
        int n = sc.length;
        for (int i = 0; i< n; i++){ // i是奇数长度回文串的中心点
            for (int len = 0, l = i - len, r = i+len; l >=0 && r<n ; l--, r++) { // len 左边 部分的长度
                if (sc[l] == sc[r])cnt++;
                else break;
            }
        }
        for (int i =0;i<n-1; i++){// i是偶数长度回文串的中心点的左边元素
            for (int len= 0, l = i-len, r= i+len+1;l >=0 && r<n ; l--, r++) {
                if (sc[l] == sc[r])cnt++;
                else break;
            }
        }
        return cnt;
    }
}
```

#### [剑指 Offer II 021. 删除链表的倒数第 n 个结点](https://leetcode-cn.com/problems/SLwz0R/)

**快慢指针**

```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummpy = new ListNode();
        ListNode fast = dummpy, slow = dummpy;
        dummpy.next = head;
        while (n-- > 0){
            fast = fast.next;
        }
        while (fast.next!=null){
            fast = fast.next;
            slow = slow.next;
        }
        slow.next = slow.next.next;
        return dummpy.next;
    }
}
```

#### [剑指 Offer II 022. 链表中环的入口节点](https://leetcode-cn.com/problems/c32eOV/)

**快慢指针**

![2021-10-23 pm7.34.16](https://muyids.oss-cn-beijing.aliyuncs.com/2021-10-23%20pm7.34.16.png)

快指针 移动 速度是慢指针的两倍，因为链表存在环，快慢指针必定会相交于一点

相交的时候，快指针比慢指针多移动了 一圈，也就是 b

快指针 移动 2L = a + (n+1) b

慢指针移动 L = a + nb

L = b，也就是说快慢指针相遇 的位置距离链表头长度为 b

这时候如果把一个指针移动到链表头，然后两个指针都移动 a 长度，相遇的位置就是环的入口节点

**算法思路**

- 快慢指针移动，直到相遇
- 慢指针移动到链表头，两个指针同样的速度移动，相遇即为环的入口
  **代码实现**

```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) return null;
        ListNode fast = head.next.next, slow = head.next;
        while (fast != slow) {
            if (fast==null || fast.next == null) return null;
            fast = fast.next.next;
            slow = slow.next;
        }
        slow = head;
        while (fast!=slow){
            fast = fast.next;
            slow = slow.next;
        }
        return slow;
    }
}
```

#### [剑指 Offer II 023. 两个链表的第一个重合节点](https://leetcode-cn.com/problems/3u1WK4/)

```java
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode p = headA, q = headB;
        while (p!=q){
            p=p.next;q=q.next;
            if (p==null && q==null) return null;
            if (p==null) p=headB;
            if (q==null) q=headA;
        }
        return p;
    }
}
```

#### [剑指 Offer II 024. 反转链表](https://leetcode-cn.com/problems/UHnkqh/)

#### **迭代**

```java
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode pre = null, cur = head;
        while (cur!= null){
            ListNode next  = cur.next;
            cur.next = pre;
            pre = cur;
            cur = next;
        }
        return pre;
    }
}
```

#### 递归

#### [剑指 Offer II 025. 链表中的两数相加](https://leetcode-cn.com/problems/lMSNwu/)

#### [剑指 Offer II 026. 重排链表](https://leetcode-cn.com/problems/LGjMqU/)

#### [剑指 Offer II 027. 回文链表](https://leetcode-cn.com/problems/aMhZSa/)

#### [剑指 Offer II 028. 展平多级双向链表](https://leetcode-cn.com/problems/Qv1Da2/)

#### [剑指 Offer II 029. 排序的循环链表](https://leetcode-cn.com/problems/4ueAj6/)

#### [剑指 Offer II 030. 插入、删除和随机访问都是 O(1) 的容器](https://leetcode-cn.com/problems/FortPu/)

#### [剑指 Offer II 031. 最近最少使用缓存](https://leetcode-cn.com/problems/OrIXps/)

LRU

#### [剑指 Offer II 032. 有效的变位词](https://leetcode-cn.com/problems/dKk3P7/)

计数

```java
class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int [] st = new int[26];
        for (char ch: s.toCharArray()){
            st[ch-'a']++;
        }
        for (char ch: t.toCharArray()){
            st[ch-'a']--;
        }
        for (int i = 0; i< 26;i++){
            if(st[i]!=0)return false;
        }
        return !s.equals(t);
    }
}
```

排序

```java
class Solution {
    public boolean isAnagram(String s, String t) {
        char[] sc = s.toCharArray();
        char[] tc = t.toCharArray();
        Arrays.sort(sc);
        Arrays.sort(tc);
        return !s.equals(t) && String.valueOf(sc).equals(String.valueOf(tc));
    }
}
```

#### [剑指 Offer II 033. 变位词组](https://leetcode-cn.com/problems/sfvd7V/)

**排序+哈希**

```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> hash = new HashMap<>();
        for (String s : strs) {
            char[] sc = s.toCharArray();
            Arrays.sort(sc);
            String key = String.valueOf(sc);
            if (hash.containsKey(key)) {
                hash.get(key).add(s);
            } else {
                List<String> list = new ArrayList<>();
                list.add(s);
                hash.put(key, list);
            }
        }
        List<List<String>> res = new ArrayList<>();
        for (Map.Entry<String, List<String>> entry : hash.entrySet()) {
            res.add(entry.getValue());
        }
        return res;
    }
}
```

#### [剑指 Offer II 034. 外星语言是否排序](https://leetcode-cn.com/problems/lwyVBB/)

```java
class Solution {
    public boolean isAlienSorted(String[] words, String order) {
        int []sc = new int[26];
        for (int i =0; i< 26; i++){
            sc[order.charAt(i) - 'a'] = i;
        }
        for (int i = 0; i<words.length -1;i++) {
            if (!compare(words[i], words[i+1], sc)) return false;
        }
        return true;
    }
    // s < t -> true
    boolean compare(String s, String t, int []sc){
        for (int i = 0; i <s.length() && i < t.length(); i++) {
            if (sc[s.charAt(i) - 'a'] > sc[t.charAt(i)-'a']) return false;
            else if (sc[s.charAt(i) - 'a'] < sc[t.charAt(i) - 'a']) return true;
        }
        if (s.length() > t.length()) return false;
        return true;
    }
}
```

#### [剑指 Offer II 035. 最小时间差](https://leetcode-cn.com/problems/569nqc/)

```java

class Solution {
    public int findMinDifference(List<String> timePoints) {
        timePoints.sort(new Comparator<String>() {
            @Override
            public int compare(String o1, String o2) {
                return o1.compareTo(o2);
            }
        });
        int ans = 3700;

        for (int i = 0; i < timePoints.size() - 1; i++) {
            ans = Math.min(ans, minCha(timePoints.get(i), timePoints.get(i + 1)));
        }

        ans = Math.min(ans, minCha("00:00", timePoints.get(0)) + minCha(timePoints.get(timePoints.size() - 1), "24:00"));
        return ans;
    }

    // 05:20  -> 6:40
    int minCha(String s, String t) {
        String[] ss = s.split(":");
        String[] tt = t.split(":");
        return Integer.valueOf(tt[0]) * 60 + Integer.valueOf(tt[1])
                - (Integer.valueOf(ss[0]) * 60 + Integer.valueOf(ss[1]));
    }
}
```

#### [剑指 Offer II 036. 后缀表达式](https://leetcode-cn.com/problems/8Zf90G/)

#### [剑指 Offer II 037. 小行星碰撞](https://leetcode-cn.com/problems/XagZNi/)

#### 栈

题目不难，主要是 java 模拟栈的操作，选择`Deque<Integer> stk = new ArrayDeque<>();`

同样的，队列也一样；使用`addFirst,removeFirst,addLast,removeLast,getFirst,getLast,size,isEmpty`等方法控制和操作实现栈和队列的基本操作；

转数组的时候`int []`，先使用`List<Integer> list = new ArrayList<>(stk);`，然后使用下标进行操作

#### 代码实现

```java

class Solution {
    public int[] asteroidCollision(int[] arr) {
        Deque<Integer> stk = new ArrayDeque<>();

        for (int x : arr) {
            if (x > 0) {
                stk.addLast(x);
                continue;
            }

            while (!stk.isEmpty() && stk.getLast() > 0 && stk.getLast() <-x ) {
                stk.removeLast();
            }
            if (!stk.isEmpty() && stk.getLast() == -x) {
                stk.removeLast();
                continue;
            }
            if (stk.isEmpty() || stk.getLast() < 0) {
                stk.addLast(x);
            }
        }

        List<Integer> list = new ArrayList<>(stk);
        int[] res = new int[stk.size()];
        for (int i = 0; i < list.size(); i++) {
            res[i] = list.get(i);
        }
        return res;
    }
}
```

#### [剑指 Offer II 038. 每日温度](https://leetcode-cn.com/problems/iIQa4I/)

#### 单调栈

```java
class Solution {
    public int[] dailyTemperatures(int[] ts) {
        Deque<Integer> stk = new ArrayDeque<>();
        int[] res = new int[ts.length];
        for (int i = 0; i < ts.length; i++) {
            while (!stk.isEmpty() && ts[stk.getLast()] < ts[i]) {
                res[stk.getLast()] = i - stk.getLast();
                stk.removeLast();
            }
            stk.addLast(i);
        }
        return res;
    }
}
```

#### [剑指 Offer II 039. 直方图最大矩形面积](https://leetcode-cn.com/problems/0ynMMM/)

```java
class Solution {
    public int largestRectangleArea(int[] h) {
        int[] heights = new int[h.length + 1];
        for (int i = 0; i < h.length; i++) heights[i] = h[i];
        Deque<Integer> stk = new ArrayDeque<>();
        int area = 0;
        for (int i = 0; i < heights.length; i++) {
            while (!stk.isEmpty() && heights[stk.getLast()] >= heights[i]) {
                int high = heights[stk.getLast()];
                stk.removeLast();
                int l = stk.isEmpty() ? -1 : stk.getLast();
                area = Math.max(area, high * (i - l -1));
            }
            stk.addLast(i);
        }
        return area;
    }
}
```

#### [剑指 Offer II 040. 矩阵中最大的矩形](https://leetcode-cn.com/problems/PLYXKQ/)

```java
class Solution {
    public int maximalRectangle(String[] matrix) {
        if (matrix.length == 0 || matrix[0].length() == 0) return 0;
        int m = matrix.length, n = matrix[0].length();
        int[][] grid = new int[m ][n + 1];
        for (int j = 0; j < n; j++) {
            grid[0][j] = matrix[0].charAt(j) == '1' ? 1 : 0;
        }
        for (int i = 1; i < m; i++) {
            for (int j = 0; j < n; j++) {
                grid[i][j] = matrix[i].charAt(j) == '1' ? grid[i-1][j] + 1 : 0;
            }
        }
        int area = 0;
        for (int i =0; i< m ; i++) {
            Deque<Integer> stk = new ArrayDeque<>();
            for (int j = 0; j <= n; j++){
                while (!stk.isEmpty() && grid[i][stk.getLast()] >= grid[i][j]) {
                    int high = grid[i][stk.getLast()];
                    stk.removeLast();

                    int l = stk.isEmpty() ? -1: stk.getLast();
                    area = Math.max((j - l -1) * high, area);
                }
                stk.addLast(j);
            }
        }
        return area;
    }
}
```

#### [剑指 Offer II 041. 滑动窗口的平均值](https://leetcode-cn.com/problems/qIsx9U/)

#### [剑指 Offer II 042. 最近请求次数](https://leetcode-cn.com/problems/H8086Q/)

#### [剑指 Offer II 043. 往完全二叉树添加节点](https://leetcode-cn.com/problems/NaqhDT/)

考察 bfs 和完全二叉树的下标性质：父节点的索引位置 = (子节点的索引位置 + 1) / 2 -1

```java

class CBTInserter {

    List<TreeNode> queue;
    TreeNode root;
    Queue<TreeNode> initBfs;

    public CBTInserter(TreeNode root) {
        this.root = root;
        queue = new ArrayList<>();
        initBfs = new LinkedList<>();
        if (root == null) return;
        initBfs.add(root);
        while (!initBfs.isEmpty()) {
            int k = initBfs.size();
            while (k-- > 0) {
                TreeNode cur = initBfs.poll();
                queue.add(cur);
                if (cur.left != null) initBfs.add(cur.left);
                if (cur.right != null) initBfs.add(cur.right);
            }
        }
    }
    public int insert(int v) {
        TreeNode f = queue.get((queue.size() +1) / 2 - 1);
        TreeNode node = new TreeNode(v);
        if (queue.size() % 2 == 1) f.left = node;
        else f.right = node;
        queue.add(node);
        return f.val;
    }
    public TreeNode get_root() {
        return root;
    }
}
```

#### [剑指 Offer II 044. 二叉树每层的最大值](https://leetcode-cn.com/problems/hPov7L/)

#### [剑指 Offer II 045. 二叉树最底层最左边的值](https://leetcode-cn.com/problems/LwUNpT/)

#### [剑指 Offer II 046. 二叉树的右侧视图](https://leetcode-cn.com/problems/WNC0Lk/)

#### [剑指 Offer II 047. 二叉树剪枝](https://leetcode-cn.com/problems/pOCWxh/)

#### [剑指 Offer II 048. 序列化与反序列化二叉树](https://leetcode-cn.com/problems/h54YBf/)

#### [剑指 Offer II 049. 从根节点到叶节点的路径数字之和](https://leetcode-cn.com/problems/3Etpl5/)

Dfs

#### [剑指 Offer II 050. 向下的路径节点之和](https://leetcode-cn.com/problems/6eUYwP/)

dfs

#### [剑指 Offer II 051. 节点之和最大的路径](https://leetcode-cn.com/problems/jC7MId/)

#### [剑指 Offer II 052. 展平二叉搜索树](https://leetcode-cn.com/problems/NYBBNL/)

dfs

#### [剑指 Offer II 053. 二叉搜索树中的中序后继](https://leetcode-cn.com/problems/P5rCT8/)

#### [剑指 Offer II 054. 所有大于等于节点的值之和](https://leetcode-cn.com/problems/w6cpku/)

#### [剑指 Offer II 055. 二叉搜索树迭代器](https://leetcode-cn.com/problems/kTOapQ/)

#### [剑指 Offer II 056. 二叉搜索树中两个节点之和](https://leetcode-cn.com/problems/opLdQZ/)

#### [剑指 Offer II 057. 值和下标之差都在给定的范围内](https://leetcode-cn.com/problems/7WqeDu/)

#### 滑动窗口+MultiSet

java 没有 multiSet

#### [剑指 Offer II 058. 日程表](https://leetcode-cn.com/problems/fi9suh/)

#### **TreeSet**

画图分析

​ [ ) [ ) [ )

插入 [start, end)

以 start 为基准，找到左边和右边相邻的区间，分析

```java
class MyCalendar {
    TreeSet<int[]> ts;

    public MyCalendar() {
        ts = new TreeSet<>(new Comparator<int[]>() {
            @Override
            public int compare(int[] o1, int[] o2) {
                return o1[0] - o2[0];
            }
        });
    }
    public boolean book(int start, int end) {
        int[] cur = {start, end};
        int[] ceiling = ts.ceiling(cur);
        int[] floor = ts.floor(cur);
        if (floor != null && floor[1] > start) return false;
        if (ceiling != null && ceiling[0] < end) return false;
        ts.add(cur);
        return true;
    }
}
```

#### [剑指 Offer II 059. 数据流的第 K 大数值](https://leetcode-cn.com/problems/jBjn9C/)

#### 小顶堆

```java
class KthLargest {
    PriorityQueue<Integer> heap = new PriorityQueue<>();
    int k;
    public KthLargest(int _k, int[] nums) {
        k = _k;
        for (int x: nums){
            heap.add(x);
            if (heap.size() > k) {
                heap.poll();
            }
        }
    }

    public int add(int val) {
        heap.add(val);
        if (heap.size() > k) {
            heap.poll();
        }
        return heap.peek();
    }
}
/**
 * Your KthLargest object will be instantiated and called as such:
 * KthLargest obj = new KthLargest(k, nums);
 * int param_1 = obj.add(val);
 */
```

#### [剑指 Offer II 060. 出现频率最高的 k 个数字](https://leetcode-cn.com/problems/g5c51o/)

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {

        PriorityQueue<int[]> heap = new PriorityQueue<>(new Comparator<int[]>() {
            @Override
            public int compare(int[] o1, int[] o2) {
                return o2[1] - o1[1];
            }
        });
        HashMap<Integer, Integer> cnt = new HashMap<>();

        for (int x : nums) {
            cnt.put(x, cnt.getOrDefault(x, 0) + 1);
        }

        for (Map.Entry<Integer, Integer> entry : cnt.entrySet()) {
            int[] cur = {entry.getKey(), entry.getValue()};
            heap.add(cur);
        }
        int[] ans = new int[k];
        for (int i = 0; i < k; i++) {
            if (heap.isEmpty()) return ans;
            int[] top = heap.peek();
            ans[i] = top[0];
            heap.poll();
        }
        return ans;
    }
}
```

#### [剑指 Offer II 061. 和最小的 k 个数对](https://leetcode-cn.com/problems/qn8gGX/)

```java
class Solution {
    public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        PriorityQueue<int[]> heap = new PriorityQueue<>(new Comparator<int[]>() {
            @Override
            public int compare(int[] o1, int[] o2) {
                return o1[2] - o2[2];
            }
        });
        for (int i = 0; i < k && i < nums1.length; i++) {
            for (int j = 0; j < k && j < nums2.length; j++) {
                int[] cur = {nums1[i], nums2[j], nums1[i] + nums2[j]};
                heap.add(cur);
            }
        }
        List<List<Integer>> ans = new ArrayList<>();
        while (!heap.isEmpty() && k--> 0){
            int[] top =heap.peek();
            ans.add(Arrays.asList(top[0], top[1]));
            heap.poll();
        }
        return ans;
    }
}
```

#### [剑指 Offer II 062. 实现前缀树](https://leetcode-cn.com/problems/QC3q1f/)

#### [剑指 Offer II 063. 替换单词](https://leetcode-cn.com/problems/UhWRSj/)

#### [剑指 Offer II 064. 神奇的字典](https://leetcode-cn.com/problems/US1pGT/)

#### [剑指 Offer II 065. 最短的单词编码](https://leetcode-cn.com/problems/iSwD2y/)

#### [剑指 Offer II 066. 单词之和](https://leetcode-cn.com/problems/z1R5dt/)

#### [剑指 Offer II 067. 最大的异或](https://leetcode-cn.com/problems/ms70jA/)

#### [剑指 Offer II 068. 查找插入位置](https://leetcode-cn.com/problems/N6YdxV/)

二分

#### [剑指 Offer II 069. 山峰数组的顶部](https://leetcode-cn.com/problems/B1IidL/)

二分

#### [剑指 Offer II 070. 排序数组中只出现一次的数字](https://leetcode-cn.com/problems/skFtm2/)

二分

#### [剑指 Offer II 071. 按权重生成随机数](https://leetcode-cn.com/problems/cuyjEf/)

#### [剑指 Offer II 072. 求平方根](https://leetcode-cn.com/problems/jJ0w9p/)

二分

#### [剑指 Offer II 073. 狒狒吃香蕉](https://leetcode-cn.com/problems/nZZqjQ/)

#### [剑指 Offer II 074. 合并区间](https://leetcode-cn.com/problems/SsGoHC/)

#### [剑指 Offer II 075. 数组相对排序](https://leetcode-cn.com/problems/0H97ZC/)

#### [剑指 Offer II 076. 数组中的第 k 大的数字](https://leetcode-cn.com/problems/xx4gT2/)

小顶堆

#### [剑指 Offer II 077. 链表排序](https://leetcode-cn.com/problems/7WHec2/)

#### [剑指 Offer II 078. 合并排序链表](https://leetcode-cn.com/problems/vvXgSW/)

#### [剑指 Offer II 079. 所有子集](https://leetcode-cn.com/problems/TVdhkn/)

#### dfs

```java
class Solution {
    List<List<Integer>> ans;

    public List<List<Integer>> subsets(int[] nums) {
        ans = new ArrayList<>();
        dfs(nums, 0, new ArrayList<>());
        return ans;
    }

    void dfs(int[] nums, int i, List<Integer> path) {
        if (i == nums.length){
            ans.add(new ArrayList<>(path));
            return;
        }

        dfs(nums, i+1, path);

        path.add(nums[i]);
        dfs(nums, i+1, path);
        path.remove(path.size()-1);
    }
}
```

#### 位运算枚举

```java
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans = new ArrayList<>();
        int n = 1 << nums.length;
        for (int i = 0; i < n; i++) {
            List<Integer> path = new ArrayList<>();
            for (int k = 0; k < nums.length; k++) {
                if (((1 << k) & i) > 0) path.add(nums[k]);
            }
            ans.add(path);
        }
        return ans;
    }
}
```

#### [剑指 Offer II 080. 含有 k 个元素的组合](https://leetcode-cn.com/problems/uUsW3B/)

```java
class Solution {
    List<List<Integer>> ans = new ArrayList<>();

    public List<List<Integer>> combine(int n, int k) {
        dfs(n, 1, new ArrayList<>(), k);
        return ans;
    }
    void dfs(int n, int i, List<Integer> path, int k) {
        if (i > n) {
            if (k == path.size()) ans.add(new ArrayList<>(path));
            return;
        }

        dfs(n, i + 1, path, k);

        path.add(i);
        dfs(n, i + 1, path, k);
        path.remove(path.size() - 1);
    }
}
```

#### [剑指 Offer II 081. 允许重复选择元素的组合](https://leetcode-cn.com/problems/Ygoe9J/)

DFS

```java
class Solution {
    List<List<Integer>> res;
    int n;
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        res = new ArrayList<>();
        n = candidates.length;
        dfs(candidates, new ArrayList<>(), 0, 0 ,target);
        return res;
    }
    void dfs(int[] candidates, List<Integer> path, int d , int cur, int tar) {
        if (cur >= tar) {
            if (cur == tar)res.add(new ArrayList<>(path));
            return;
        }
        for (int i = d; i < n; i++){
            path.add(candidates[i]);
            dfs(candidates, path, i, cur+candidates[i], tar );
            path.remove(path.size()-1);
        }
    }
}
```

#### [剑指 Offer II 082. 含有重复元素集合的组合](https://leetcode-cn.com/problems/4sjJUc/)

求组合 dfs 时候带位置

排列 dfs 时不带位置

去重复使用辅助数组 st 判断进行剪枝

```java
class Solution {
    List<List<Integer>> res;
    boolean[] st;
    int n ;
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        res = new ArrayList<>();
        n = candidates.length;
        Arrays.sort(candidates);
        st = new boolean[n];
        dfs(candidates, new ArrayList<>(), 0, 0, target);
        return res;
    }

    void dfs(int []cans ,List<Integer> path, int d, int cur, int target ) {
        if (cur >= target) {
            if (cur == target)res.add(new ArrayList<>(path));
            return ;
        }

        for (int i = d; i < n; i++) {
            if (st[i]) continue;
            if (i > 0 && cans[i] == cans[i-1] &&!st[i-1]) continue;
            path.add(cans[i]);
            st[i] = true;
            dfs(cans, path, i+1, cur+cans[i], target);
            st[i] = false;
            path.remove(path.size()-1);
        }
    }
}
```

#### [剑指 Offer II 083. 没有重复元素集合的全排列](https://leetcode-cn.com/problems/VvJkup/)

```java
class Solution {
    List<List<Integer>> res;
    boolean[]st;
    public List<List<Integer>> permute(int[] nums) {
        res = new ArrayList<>();
        st = new boolean[nums.length];
        dfs(nums, new ArrayList<>());
        return res;
    }
    void dfs(int[] nums, List<Integer> path){
        if (path.size() == nums.length) {
            res.add(new ArrayList<>(path));
            return ;
        }

        for (int i = 0; i < nums.length; i++){
            if (st[i]) continue;
            st[i] = true;
            path.add(nums[i]);
            dfs(nums, path);
            path.remove(path.size() -1);
            st[i] = false;
        }
    }
}
```

#### [剑指 Offer II 084. 含有重复元素集合的全排列 ](https://leetcode-cn.com/problems/7p8L0Z/)

全排列不需要 下标，每次都是遍历整个集合

```java
class Solution {
    List<List<Integer>>  res ;
    boolean[]st ;
    int n ;
    public List<List<Integer>> permuteUnique(int[] nums) {
        Arrays.sort(nums);
         n = nums.length;
        st = new boolean[n];
        res = new ArrayList<>();
        dfs(nums, new ArrayList<>());
        return res;
    }

    void dfs(int []nums, List<Integer> path) {
        if (path.size() == n) {
            res.add(new ArrayList<>(path));
            return;
        }

        for (int i = 0; i < n ; i++){
            if (st[i]) continue;
            if (i > 0 && nums[i-1] == nums[i] && !st[i-1]) continue;

            st[i] = true;
            path.add(nums[i]);
            dfs(nums, path);
            path.remove(path.size()-1);
            st[i] = false;
        }
    }
}
```
