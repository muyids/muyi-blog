# spring 整合 mybatis

# 概述

1. 将第三方资源需要的对象注册在 spring 容器中
2. 将第三方资源的资源文件，交给 spring 管理
3. 所有第三方资源需要的内容全部从 spring 中获取

# 整合 mybatis 需要交给 spring 的对象是什么？

- SqlSessionFactoryBuilder(临时对象)
- SqlSessionFactory（单例）
- SqlSession
- Mapper
