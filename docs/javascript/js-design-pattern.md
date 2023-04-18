---
title: javascript常用设计模式实现
date: 2016-09-06T04:53:00+08:00
draft: false
categories: [javascript]
tags: [javascript]
---

`设计模式`是对普遍存在问题提出的常规的、可复用的解决方案。

<!--more-->

设计模式的本质是`简约和美`

## 单例

任意对象都是单例，无须特别处理

```
var obj = {name: 'michaelqin', age: 30};
```

## 工厂

同样形式参数返回不同的实例

```
function Person() { this.name = 'Person1'; }
function Animal() { this.name = 'Animal1'; }
function Factory() {}
Factory.prototype.getInstance = function(className) {
    return eval('new ' + className + '()');
}
```

## 单例

单例模式确保一个类只有一个实例。 因为 require 机制，Node.js 中创建单例很方便。

```
//area.js
var PI = Math.PI;

function circle (radius) {
  return radius * radius * PI;
}

module.exports.circle = circle;
```

应用中无论 require 多少次此模块，它都只存在一个实例。

```
var areaCalc = require('./area');
console.log(areaCalc.circle(5));
```

基于 require 的运行机制，单例可能是 NPM 模块中最普遍的 Node.js 设计模式。

## 观察者模式

观察者模式在对象间定义一个一对多的关联，当状态发生改变时，自动通知其他关联对象。
Node.js 中可以使用 EventEmitter 使用观察者模式。

```
// MyFancyObservable.js
var util = require('util');
var EventEmitter = require('events').EventEmitter;
function MyFancyObservable() {
  EventEmitter.call(this);
}

util.inherits(MyFancyObservable, EventEmitter);
```

上面的代码创建了一个可观察的对象，再给它添加一些功能：

```
MyFancyObservable.prototype.hello = function (name) {
  this.emit('hello', name);
};
```

现在这个对象可以发射事件了：

```
var MyFancyObservable = require('MyFancyObservable');
var observable = new MyFancyObservable();

observable.on('hello', function (name) {
  console.log(name);
});

observable.hello('john');
```

## 工厂模式

工厂模式为**创建对象定义一个通用接口**，这种创建模式创建对象时不需要直接掉用构造函数。该模式对于复杂的创建流程非常有用。

```
function MyClass (options) {
  this.options = options;
}
function create(options) {
  // modify the options here if you want
  return new MyClass(options);
}
module.exports.create = create;
```

工厂模式使测试更加简单，因为可以使用此方式注入模块依赖。

## 依赖注入

**依赖注入是一种一个或多个依赖（或者服务）注入或者通过引用传递到一个依赖的对象中的设计模式。**

下面的例子中，我们将创建一个返回一个数据库依赖的 UserModel。

```
function userModel (options) {
  var db;

  if (!options.db) {
    throw new Error('Options.db is required');
  }

  db = options.db;

  return {
    create: function (done) {
      db.query('INSERT ...', done);
    }
  }
}
module.exports = userModel;
```

然后用它创建一个实例：

```
var db = require('./db');
var userModel = require('User')({
  db: db
});
```

这种模式对于测试很有用，编写单元测试的时候可以方便地把假数据传入模型中。

## 中间件/管道

**中间件是一个简单但强大的概念：一个单元/函数输出的结果是下一个的输入。**
Express 和 Koa 都使用了中间件。
我们来了解一下 Koa 的实现：

```
app.use = function(fn){
  this.middleware.push(fn);
  return this;
};
```

添加中间件时只需要将其 push 到中间件数组中，当请求发送到服务器时，中间件会一个接一个地被调用：

```
var i = middleware.length;
while (i--) {
  next = middleware[i].call(this, next);
}
```

### 数据流（Streams）

可以把数据流想象成某种特殊的管道。数据流适合用于处理大量字节数据。

```
process.stdin.on('readable', function () {
    var buf = process.stdin.read(3);
    console.dir(buf);
    process.stdin.read(0);
});
$ (echo abc; sleep 1; echo def; sleep 1; echo ghi) | node consume2.js
<Buffer 61 62 63>
<Buffer 0a 64 65>
<Buffer 66 0a 67>
<Buffer 68 69 0a>
```
