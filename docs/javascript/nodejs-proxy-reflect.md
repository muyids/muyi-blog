---
title: nodejs的Proxy与Reflect
date: 2017-03-10T00:00:00+08:00
categories: [Node.js]
tags: [Node.js]
---

`Proxy` 用于修改某些操作的默认行为，等同于在语言层面做出修改，所以属于一种**元编程**（meta programming），即对编程语言进行编程。

<!--more-->

Reflect 对象与 Proxy 对象一样，也是 ES6 为了操作对象而提供的新 API。

Proxy 可以理解成，在目标对象之前架设一层“拦截”，外界对该对象的访问，都必须先通过这层拦截，因此提供了一种机制，可以对外界的访问进行过滤和改写。Proxy 这个词的原意是代理，用在这里表示由它来“代理”某些操作，可以译为“代理器”。

动态代理在很多框架中应用非常广泛，也是大厂面试必考问题，弄懂动态代理模式是小白到高手的必经之路，要彻底弄懂动态代理，需要先从代理模式谈起。

## 应用

- 编程语言中的注解是用代理实现的
- 观察者模式，比如 orm 操作时，实体修改属性，获知通知

```javascript
var obj = new Proxy(
  {},
  {
    get: function (target, key, receiver) {
      console.log(`getting ${key}!`);
      return Reflect.get(target, key, receiver);
    },
    set: function (target, key, value, receiver) {
      console.log(`setting ${key}!`);
      return Reflect.set(target, key, value, receiver);
    },
  }
);
```

## 使用 Proxy 实现观察者模式

观察者模式（Observer mode）指的是函数自动观察数据对象，一旦对象有变化，函数就会自动执行。

```javascript
const queuedObservers = new Set();
const observe = (fn) => queuedObservers.add(fn);
const observable = (obj) => new Proxy(obj, { get, set });
function get(target, key, receiver) {
  return Reflect.get(target, key, receiver);
}

function set(target, key, value, receiver) {
  const result = Reflect.set(target, key, value + " is super hero", receiver);
  queuedObservers.forEach((observer) => observer.call(this, key, value));
  return result;
}

const person = observable({
  name: "张三",
  age: 20,
});
function keyChange(key, value) {
  console.log(`changed key:`, key, value);
}

observe(keyChange);
person.name = "李四";
console.log(person.name);
```

上面代码中，先定义了一个 Set 集合，所有观察者函数都放进这个集合。
然后，observable 函数返回原始对象的代理，拦截赋值操作。
