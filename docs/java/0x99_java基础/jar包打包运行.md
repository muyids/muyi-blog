# 手动打包 jar 包

## 普通 java 文件

### 要打包的 java 文件

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("hello world!");
    }

}
```

### javac 编译\*.class

```java
javac *.java
```

### 编辑 MANIFEST 文件

```
Main-Class: Hello
```

注意，最后一行必须为空行

### 打包 jar 包

```java
jar cfm hello.jar Manifest.txt *.class
```

### 运行 jar 包

```java
java -jar hello.jar
```
