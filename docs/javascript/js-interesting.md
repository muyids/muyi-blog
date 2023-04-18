---
title: javascript奇技淫巧
date: 2016-09-10T04:53:00+08:00
draft: false
categories: [javascript]
tags: [javascript]
---

`javascript`是一门有趣的语言

## 你能想到多少种数组复制方式？

let src = [1, 2, 3]

1. 赋值

```javascript
let dest = new Array(src.length);
for (let i = 0, len = src.length; i < len; i++) {
  dest[i] = src[i];
}
```

2. 通过 slice

```javascript
let dest = src.slice();
```

3. ES6

```javascript
let dest = [...src];
```

## 闭包是啥？写一个看看？闭包能干嘛？

闭包主要涉及到 js 的几个其他的特性:

- 作用域链
- 垃圾(内存)回收机制
- 函数嵌套...等等

```
function A() {
    let z = 10
    function B(i) {
        console.log(i)
    }
    B(z)
}
```

## 继承的实现

es5

```
function Animal(){
  this.name = 'animal';
}
function Cat(name){
  Animal.call(this);
  this.name = name || 'Tom';
}
require('util').inherits(Cat, Animal);
```

es6

```
class Animal {
  constructor() {
    this.name = 'animal'
  }
}
class Cat extends Animal {
  constructor(name) {
    super()
    this.name = name || 'Tom';
  }
}
```

## 内存回收的方式

### 引用计数

循环引用的情况，无法回收内存

```
function f(){
  var o = {};
  var o2 = {};
  o.a = o2; // o 引用 o2
  o2.a = o; // o2 引用 o
  return "azerty";
}
f();
// 两个对象被创建，并互相引用，形成了一个循环
// 他们被调用之后不会离开函数作用域
// 所以他们已经没有用了，可以被回收了
// 然而，引用计数算法考虑到他们互相都有至少一次引用，所以他们不会被回收
```

### 标记清除

这个算法把“对象是否不再需要”简化定义为“对象是否可以获得”。

这个算法假定设置一个叫做根（root）的对象（在 Javascript 里，根是全局对象）。
定期的，垃圾回收器将从根开始，找所有从根开始引用的对象，然后找这些对象引用的对象
从根开始，垃圾回收器将找到所有可以获得的对象和所有不能获得的对象。

这个算法比前一个要好，因为“有零引用的对象”总是不可获得的，但是相反却不一定，参考“循环引用”。

## call 和 apply 作用

- 继承
- 修改运行时的 this

## timer 是如何工作的

- [Philip Roberts: Help, I’m stuck in an event-loop.](https://vimeo.com/96425312)
- [JavaScript 运行机制详解](http://www.ruanyifeng.com/blog/2014/10/event-loop.html)
