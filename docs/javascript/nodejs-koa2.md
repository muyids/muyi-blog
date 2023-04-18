---
title: nodejs框架之koa
date: 2016-08-10T00:00:00+08:00
categories: [Node.js]
tags: [Node.js]
---

koa 相比 express 主要就是引入了`generator`，来避免回调"地狱"问题。

<!--more-->

nodejs 的 web 框架，我喜欢 express，简洁易用。

但是 express 一个明显的不足，当应用存在大量回调逻辑时，不管是通过 callback 还是通过`promise + generator`的方式，异步流程的代码书写都不是特别直观。

于是，tj 大神领导开发了下一代 web 框架[koa](https://github.com/koajs/koa)。

Koa 应用是一个包含中间件 generator 方法数组的对象

当请求到来时, 这些方法会以 stack-like 的顺序执行, 从这个角度来看，Koa 和其他中间件系统（比如 Ruby Rack 或者 Connect/Express ）非常相似.

Koa 的一大设计理念是: 通过其他底层中间件层提供高级「语法糖」，而不是 Koa.

大大提高了框架的互操作性和健壮性, 并让中间件开发变得简单有趣.

## 中间件架构

代码级联（Cascading）

比如内容协商（content-negotation）、缓存控制（cache freshness）、反向代理（proxy support）重定向等常见功能都由中间件来实现.

将类似常见任务分离给中间件实现, Koa 实现了异常精简的代码.

### 中间件举例

- koa-router
- trie-router
- route
- basic-auth
- etag
- compose
- static
- static-cache
- session
- compress
- csrf
- logger
- mount
- send
  generator functions 以 function\* 声明。以这种关键词声明的函数支持 yield。

## koa 与 express 的区别

- koa 采用 ctx 一个参数来调用中间件，而不是 express 的 req, res。koa 更方便。
- koa 相比 express 主要就是引入了 generator，来避免回调"地狱"问题.
- koa 的编程模型是一种 栈 模型 ，而 express 的设计是串联的
- express 的社区比较早，生态比 koa 要成熟。

### 举例

比如一个服务器处理时间/日志的中间件的开发：

- express

  - request 进来，记录时间到`request._startTime`上。绑定一个函数到 response 的`end`,`finish`以及 response.socket 的`error`,`close`事件上。

  - 那个函数会用当前时间和 startTime 做差，算出运行时间。

- koa2

  ```javascript
  const xTime = async (ctx, next) => {
      let start = new Date();
      await next();
      ctx.set('X-Response-Time', (new Date) - start) + 'ms')
  }
  ```

这是在功能开发上，在错误处理上的友好度就更高了。

没有特意抹黑 express 的中间件开发，那个 express 版的计时器是 express 自带的服务器日志中间件 morgan 的实现。

### 社区

express 的社区还是大。
