## Java ACM 模式获取输入的方法

- 使用 Scanner 获取 System.in 输入
- scan.hasNext() 或者 scan.hasNextLine() 判断是否还有下一组输入
- scan.nextInt() 获取输入的下一个整数

## 列举几种 case 情况的获取

### 1、明确有多少行 case 的时候

（包括只有一组数据，告知有 n 组数据，遇到特殊 case 退出等情况）

使用 scan.hasNext() 配合 scan.nextInt()等 获取 case 数据

**只有一组用例**

**N 组用例结束**

```java
import java.util.*;
class Solution {
    public static void maxValue(int a, int b) {
        System.out.println(a + b);
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        while (scan.hasNext()) {
            int N = scan.nextInt();
            while (N-- > 0) {
                int a = scan.nextInt();
                int b = scan.nextInt();
                Solution.maxValue(a, b);
            }
        }
    }
}
```

**遇到特殊用例结束**

```java
import java.util.*;
class Solution {
    public static void maxValue(int a, int b) {
        System.out.println(a + b);
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        while (scan.hasNext()) {
            int a = scan.nextInt();
            int b = scan.nextInt();
            if (a == 0 && b == 0) {
                return;
            }
            Solution.maxValue(a, b);
        }
    }
}
```

### 2、不知道有多少行，需要按行获取

使用 hasNextLine() 配合 in.nextLine() 获取 case 数据

需要注意的是 in.nextLine() 获取到的 case 数据为字符串 , 如果需要 int 数据则要进行转化

```java
import java.util.*;
public class Main {
    public static void maxValue(int[] nums) {
        int res = 0;
        for (int x : nums) res += x;
        System.out.println(res);
    }
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        while (scan.hasNextLine()) {
            String[] sts = scan.nextLine().split(" ");
            int[] nums = new int[sts.length];
            for (int i = 0; i < sts.length; i++) nums[i] = Integer.valueOf(sts[i]);
            maxValue(nums);
        }
    }
}
```

### 3、字符串的输入

字符串的获取应全部使用 hasNextLine() 和 nextLine()，避免使用 next(), nextInt()等造成操作

```java
import java.util.*;
public class Main {
    public static void work(String[] sts) {
        Arrays.sort(sts);
        for (int i = 0; i < sts.length; i++) {
            System.out.print(sts[i]);
            if (i != sts.length - 1) {
                System.out.print(" ");
            }
        }
    }
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        while (scan.hasNextLine()) {
            scan.nextLine();
            String[] sts = scan.nextLine().split(" ");
            work(sts);
        }
    }
}
```

多行字符串

```java
import java.util.*;
public class Main {
    public static void work(String[] sts) {
        Arrays.sort(sts);
        for (int i = 0; i < sts.length; i++) {
            System.out.print(sts[i]);
            if (i != sts.length - 1) {
                System.out.print(" ");
            }
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        while (scan.hasNextLine()) {
            String[] sts = scan.nextLine().split(" ");
            work(sts);
        }
    }
}
```
