一天系统化入门 maven(尚硅谷 maven 笔记整理)

https://zhuanlan.zhihu.com/p/145827862

#### 手动安装依赖包

遇到 pom 中的包导入不成功的情况，可以手动下载导入安装

```
mvn install:install-file \
-DgroupId=commons-lang \
-DartifactId=commons-lang \
-Dpackaging=jar \
-Dversion=2.6 \
-Dfile=commons-lang-2.6.jar \
-DgeneratePom=true
```

比如手动装一下：

```
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
    <version>4.5.12</version>
</dependency>
```

```
mvn install:install-file \
-DgroupId=org.apache.httpcomponents \
-DartifactId=httpclient \
-Dpackaging=jar \
-Dversion=4.5.12 \
-Dfile=httpclient-4.5.12.jar
```
