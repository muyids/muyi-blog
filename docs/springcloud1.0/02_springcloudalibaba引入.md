引入 spring cloud alibaba

[毕业版本说明](https://github.com/alibaba/spring-cloud-alibaba/wiki/%E7%89%88%E6%9C%AC%E8%AF%B4%E6%98%8E)

- Spring Cloud Alibaba Version ： 2.2.6.RELEASE

- Spring Boot Version ： 2.3.2.RELEASE

- Spring Cloud Version ： Spring Cloud Hoxton.SR9 如果没有用到 Spring Cloud 的组件，不需要引入

![2021-09-17 pm9.09.38](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-17%20pm9.09.38-4008018.png)

我们选择使用 Spring Cloud Hoxton 版本，在 dependencyManagement 中添加如下内容

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-alibaba-dependencies</artifactId>
    <version>2.2.6.RELEASE</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```
