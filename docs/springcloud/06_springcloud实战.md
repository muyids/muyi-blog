### 大纲

- 写作意图
- 构建父工程项目 - cloud2021
- Helloworld 子模块 - passport
- 抽象 framework 模块
- 引入 MySQL 数据库；Framework-db
- 用户服务 Passport
- nacos 服务发现
- 分布式 ID 系统
- 分布式注册服务中心 ：[Nacos](https://github.com/alibaba/Nacos)
- 网关
- Web 业务系统开发：
- 服务调用 ：
- 分布式事务 ： [Seata](https://github.com/seata/seata)
- 服务配置
- 服务限流
- 服务总线
- 。。。

---

#### 写作意图

知识总结，实战演练

参考文档：

- [Spring Cloud Alibaba 中文文档](https://github.com/alibaba/spring-cloud-alibaba/blob/master/README-zh.md)
- [spring-cloud-alibaba/wiki](https://github.com/alibaba/spring-cloud-alibaba/wiki)
- [Spring Cloud 中文网](https://www.springcloud.cc/)

#### 构建父子项目

##### **选择版本**：

参考：https://start.spring.io/actuator/info

- spring cloud : 2020.0.3
- Spring Boot: 2.5.4
- cloud alibaba : 2021.1
- java: java8

##### **搭建项目**

**父项目搭建**

父项目作用：

- 统一依赖管理
- 控制插件版本
- 聚合项目

**项目创建**

1. File-new-maven 项目

2. pom 文件编辑

   - g、a、v、packaging 配置
   - 统一管理 jar 包版本
   - 父模块的依赖引入

3. idea 配置

   - java 编译版本选 8
   - Maven 版本选择
   - 字符编码：Preference > Editor > File Encoding 设置为 utf8
   - 注解生效激活: Preference > Build, Execution, Deployment > Compiler > Annotation Processors，在`Enable annotation processing`前打勾
   - 自动删除没用的包：editor>general>auto import>optimize imports on fly

4. idea 开发高级配置（初学者暂时略过）

   - 微服务开发多个 application 同时启动
   - 自动生成 serialversionuid: Editor>Inspections>Serialization issues 全勾
   - idea 代码截长图 screen shot 插件
   - .yml 文件自动补全
   - 。。。

**pom 文件编辑：**

```xml
<groupId>org.ydw</groupId>
<artifactId>cloud1</artifactId>
<version>1.0-SNAPSHOT</version>
<packaging>pom</packaging>
```

**统一管理 jar 包版本**

```xml
<!-- 统一管理jar包版本 -->
<properties>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  <maven.compiler.source>1.8</maven.compiler.source>
  <maven.compiler.target>1.8</maven.compiler.target>
  <junit.version>4.12</junit.version>
  <log4j.version>1.2.17</log4j.version>
  <lombok.version>1.16.18</lombok.version>
  <mysql.version>5.1.47</mysql.version>
  <druid.version>1.1.21</druid.version>
  <mybatis.spring.boot.version>1.3.0</mybatis.spring.boot.version>
</properties>
```

**父工程依赖引入：**

三个核心 jar 包：

- spring boot - 2.5.4
- spring cloud - 2020.0.3
- spring cloud alibaba - 2021.1

```xml
<!-- https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-dependencies -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-dependencies</artifactId>
  <version>2.5.4</version>
  <type>pom</type>
  <scope>import</scope>
</dependency>

<!-- https://mvnrepository.com/artifact/org.springframework.cloud/spring-cloud-dependencies -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-dependencies</artifactId>
    <version>2020.0.3</version>
    <type>pom</type>
    <scope>runtime</scope>
</dependency>
<!-- https://github.com/alibaba/spring-cloud-alibaba/releases-->
<dependency>
  <groupId>com.alibaba.cloud</groupId>
  <artifactId>spring-cloud-alibaba-dependencies</artifactId>
  <version>${spring.cloud.alibaba.version}</version>
  <type>pom</type>
  <scope>import</scope>
</dependency>
```

**java 编译版本选择：**

`Preference > Build, Execution, Deployment > Compiler > Java Compiler` 下选择 `bytecode version` 为 8

**maven 版本选择:**

Build,execution,deployment>build tools>maven

设置 maven home directory，user settings file

#### 构建子工程项目

1. 创建项目
2. pom 编写
   - gav - groupId，artifactId，version
   - 依赖导入 - 继承父项目的依赖 - 导入 spring boot start web
     **继承父项目依赖**

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.muyids</groupId>
      <artifactId>cloud2021</artifactId>
      <version>${framwork.version}</version>
      <scope>import</scope>
      <type>pom</type>
    </dependency>
  </dependencies>
</dependencyManagement>
```

**spring boot start web 依赖包**

```xml
<!-- https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-web -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
  <version>${spring-boot.version}</version>
</dependency>
```

`${spring-boot.version}` : 使用父工程中的`springframework.boot`版本

**helloword web 程序**

- application.yml
- Main
- RestController

#### 抽象 framework 模块

**引入 MySQL 数据库**

1. Framework-db
   - 创建项目
   - 导入依赖
2. passport 接入 mysql
   - 配置数据源

**Framework-db 导入依赖**

```xml
<dependencies>
  <!-- https://mvnrepository.com/artifact/com.github.pagehelper/pagehelper-spring-boot-starter -->
  <dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.3.1</version>
  </dependency>
  <!-- mysql -->
  <dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <scope>runtime</scope>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
  </dependency>
  <dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>1.3.2</version>
  </dependency>
  <dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>1.2.4</version>
  </dependency>
</dependencies>
```

**passport 接入 mysql 数据源配置**

- application.yml 文件配置
- Mapper 接口定义
- resources/mapper/\*Mapper.xml 编写

**application.yml 文件配置**

```yaml
spring:
  datasource:
    url: jdbc:mysql://127.0.0.1:3306/cloud_passport?serverTimezone=Asia/Shanghai&allowMultiQueries=true&characterEncoding=UTF-8
    username: root
    password:
    driver-class-name: com.mysql.cj.jdbc.Driver
    druid:
      filter:
        stat:
          #是否开启慢sql查询监控
          log-slow-sql: true
          #慢SQL执行时间
          slow-sql-millis: 1
      #初始化时建立物理连接的个数
      initial-size: 30
      #最大连接池数量
      max-active: 100
      #获取连接时最大等待时间
      max-wait: 60000
      #最小连接池数量
      min-idle: 3
      stat-view-servlet:
        #配置监控页面访问登录名称
        login-password: admin
        #配置监控页面访问密码
        login-username: admin
  jackson:
    #值为null的对象将不会包含在序列化的结果里
    default-property-inclusion: non_empty
mybatis:
  mapper-locations: classpath:mapper/*Mapper.xml
```

**Mapper 接口定义**

```java
@Mapper
public interface UserMapper {
    Integer insert(UserDO user);
}
```

**resources/mapper/\*Mapper.xml 编写**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.muyids.cloud.passport.mapper.UserMapper">
    <sql id="tblUser">ob_user</sql>
    <insert id="insert" parameterType="com.muyids.cloud.passport.entity.UserDO">
        INSERT INTO
        <include refid="tblUser"/>
        (id,update_time,create_time,is_del,user_id,salt,password,nickname,male,head_image_url)
        VALUES (#{id}, #{updateTime}, #{createTime}, #{isDel}, #{userId},#{salt}, #{password}, #{nickname},
        #{male},#{headImageUrl})
    </insert>
</mapper>
```

#### 用户服务 Passport

- 用户鉴权设计

  引入 redis 组件做 session 存储

- 用户相关 API

  新建，注销，登录，退出

- nacos 服务发现配置

**用户鉴权设计**

- 最简单的方案 token
- shiro
- toke, jwt

**用户登录鉴权**

- Md5(passpord + salt) 与数据库中的 password 对比
- token 存储
  **redis 的引入**

TODO

**分页支持**

#### nacos 服务发现

**nacos 安装启动**

Nacos 源码下载 1.4.2 版本

修改 console 模块下的配置

```
spring.datasource.platform=mysql
db.num=1

db.url.0=jdbc:mysql://127.0.0.1:3306/nacos?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=true&useSSL=false&serverTimezone=UTC
db.user=root
db.password=123456
```

启动 Nacos 类

console/src/main/java/com/alibaba/nacos/Nacos.java

**配置中心**

```xml
<dependency>
  <groupId>com.alibaba.cloud</groupId>
  <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-configuration-processor</artifactId>
  <optional>true</optional>
</dependency>
```

```java

@Data
@ConfigurationProperties(value = "my-conf")
public class MyConf {
    private String[] names;
    private List<Float> scores;
}
@RestController
@RefreshScope
@RequestMapping("/passport/v1/config")
@EnableConfigurationProperties(MyConf.class)
public class ConfigController {

    @Value("${useLocalCache}")
    private Boolean useLocalCache;
    @Value("${black}")
    private List<Long> blackIds;
    private final MyConf myConf;

    public ConfigController(MyConf myConf) {
        this.myConf = myConf;
    }

    @GetMapping("/cache")
    public ApiResponse<Boolean> getCached() {
        return ApiResponseUtil.success(useLocalCache);
    }
    @GetMapping("/black/ids")
    public ApiResponse<List<Long>> getBlackIds() {
        return ApiResponseUtil.success(blackIds);
    }
    @GetMapping("/myConf")
    public ApiResponse<MyConf> getMyConf() {
        return ApiResponseUtil.success(myConf);
    }
}
```

Bootstrap.yml

```yml
cloud:
  nacos:
    config:
      server-addr: 127.0.0.1:8848
      file-extension: yaml # 配置文件格式
      namespace: 3697aac5-d9df-4eb2-839d-495e27865ca5 # dev namespace id（自动生成）
      group: DEV_GROUP
```

cloud-passport-local.yaml - DEV_GROUP

```yaml
useLocalCache: true
black: 1223,2342,8764
my-conf:
  names:
    - dongwei
    - siming
    - duqian
  scores:
    - 90.8
    - 98.3
    - 67.2
```

**服务发现**

```xml
<dependency>
  <groupId>com.alibaba.cloud</groupId>
  <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```
