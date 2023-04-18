使用 Maven Helper 插件的 Dependency Analyzer 来分析工程的多级依赖关系，解决依赖冲突问题

摘自：[https://blog.csdn.net/qq_25809317/article/details/109506462](https://blog.csdn.net/qq_25809317/article/details/109506462)

**使用场景**

在升级项目时常常遇到类似这样的情况：我们要将一个较老旧的项目做一个 Spring、Mybatis 或者 fastjson 等等依赖包的升级，将该项目 pom 文件中版本号提升后，项目运行时仍然使用的是旧版本的包。

出现这种情况的原因可能是在该项目中引用了其他的包，这些包中也在 pom 文件中引用了旧版本的依赖包。

![2021-10-18 am10.33.45](https://muyids.oss-cn-beijing.aliyuncs.com/2021-10-18%20am10.33.45.png)

为了对项目做一个全面彻底的升级，我们要从上至下分析包间的依赖引用关系，从最底层开始由下至上地进行升级。此时使用 Maven Helper 插件可以很好地帮助我们分析依赖关系。

**使用方法**

<1>插件下载
