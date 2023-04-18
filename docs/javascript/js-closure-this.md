---
title: javascript的闭包和this关键字
date: 2016-09-06T04:53:00+08:00
draft: false
categories: [javascript]
tags: [javascript]
---

javascript 中的`this`是一个在每个函数作用域中自动定义的`特殊标识符关键字`

## 闭包

闭包这个概念，在函数式编程里很常见，简单的说，就是`使内部函数可以访问定义在外部函数中的变量`。

假如我们要实现一系列的函数：add10，add20，它们的定义是 int add10(int n)。

为此我们构造了一个名为 adder 的构造器，如下：

```javascript
var adder = function (x) {
  var base = x;
  return function (n) {
    return n + base;
  };
};

var add10 = adder(10);
console.log(add10(5));
var add20 = adder(20);
console.log(add20(5));
```

每次调用 adder 时，adder 都会返回一个函数给我们。我们传给 adder 的值，会保存在一个名为 base 的变量中。
由于返回的函数在其中引用了 base 的值，于是 base 的引用计数被 +1。当返回函数不被垃圾回收时，则 base 也会一直存在。

### 闭包的一个坑

```javascript
for (var i = 0; i < 5; i++) {
  setTimeout(function () {
    console.log(i);
  }, 5);
}
```

上面这个代码块会打印 5 5 5 5 5 出来，不会打印 0 1 2 3 4。

之所以会这样，是因为 setTimeout 中的 i 是对外层 i 的引用。当 setTimeout 的代码被解释的时候，运行时只是记录了 i 的引用，而不是值。
而当 setTimeout 被触发时，五个 setTimeout 中的 i 同时被取值，由于它们都指向了外层的同一个 i，而那个 i 的值在迭代完成时为 5，所以打印了五次 5。
为了得到我们预想的结果，我们可以把 i 赋值成一个局部的变量，从而摆脱外层迭代的影响。

```javascript
for (var i = 0; i < 5; i++) {
  (function (idx) {
    setTimeout(function () {
      console.log(idx);
    }, 5);
  })(i);
}
```

另一种方案是使用 ES6 的块作用域关键字 let

## this 的作用域

在函数执行时，this 总是指向调用该函数的对象。要判断 this 的指向，其实就是判断 this 所在的函数属于谁。

在《javaScript 语言精粹》这本书中，把 this 出现的场景分为四类，简单的说就是：

- 有对象就指向调用对象
- 没调用对象就指向全局对象
- 用 new 构造就指向新对象
- 通过 apply 或 call 或 bind 来改变 this 的所指。

### 函数有所属对象时：指向所属对象

函数有所属对象时，通常通过`.表达式`调用，这时 this 自然指向所属对象。比如下面的例子：

```javascript
var myObject = { value: 100 };
myObject.getValue = function () {
  console.log(this.value); // 输出 100
  console.log(this);
  // 输出 { value: 100, getValue: [Function] }，
  // 其实就是 myObject 对象本身
  return this.value;
};

console.log(myObject.getValue()); // => 100
```

getValue() 属于对象 myObject，并由 myOjbect 进行`.表达式`调用，因此 this 指向对象 myObject。

### 函数没有所属对象：指向全局对象

```javascript
var myObject = { value: 100 };
myObject.getValue = function () {
  var foo = function () {
    console.log(this.value); // => undefined
    console.log(this); // 输出全局对象 global
  };

  foo();

  return this.value; // return 100
};
console.log(myObject.getValue()); // => 100
```

在上述代码块中，foo 函数虽然定义在 getValue 的函数体内，但实际上它既不属于 getValue 也不属于 myObject。
foo 并没有被绑定在任何对象上，所以当调用时，它的 this 指针指向了全局对象 global。
据说这是个设计错误。

### 构造器中的 this：指向新对象

js 中，我们通过 new 关键词来调用构造函数，此时 this 会绑定在该新对象上。

```javascript
var SomeClass = function () {
  this.value = 100;
};
var myCreate = new SomeClass();

console.log(myCreate.value); // 输出100
```

### apply 和 call 调用以及 bind 绑定：指向绑定的对象

apply() 方法接受两个参数第一个是函数运行的作用域，另外一个是一个参数数组(arguments)。

call() 方法第一个参数的意义与 apply() 方法相同，只是其他的参数需要一个个列举出来。

简单来说，call 的方式更接近我们平时调用函数，而 apply 需要我们传递 Array 形式的数组给它。它们是可以互相转换的。

```javascript
var myObject = { value: 100 };
var foo = function () {
  console.log(this);
};

foo(); // 全局变量 global
foo.apply(myObject); // { value: 100 }
foo.call(myObject); // { value: 100 }

var newFoo = foo.bind(myObject);
newFoo(); // { value: 100 }
```
