---
title: javascript对象拷贝
date: 2015-08-31T04:53:00+08:00
draft: false
categories: [javascript]
tags: [javascript]
---

对象拷贝有深拷贝与浅拷贝两种方式

<!--more-->

- 浅拷贝
  拷贝的是对象的引用，而非对象属性的具体值
- 深拷贝
  拷贝的是对象的引用地址里的值
  **注：**

- 浅拷贝存在的问题是，被拷贝对象和拷贝生成的对象的修改操作会相互影响，不是完全意义的拷贝
- 深拷贝后的新对象，指向的是与原对象不同的地址

---

## 浅拷贝

浅拷贝的实现方法比较简单，只要使用是简单的复制语句即可。

### 属性赋值

```javascript
/* ================ 浅拷贝 ================ */
function simpleClone(o) {
  var obj = {};
  for (var i in o) {
    obj[i] = o[i];
  }
  return obj;
}
```

### Object.assign()方法

.assign()方法的作用：把源对象(sources)的属性分配到目标对象(object)，源对象会从左往右地调用，后面对象的属性会覆盖前面的。

```javascript
Object.assign({}, source);
```

**存在的问题**

- 后面对象的属性会覆盖前面的

```javascript
Object.assign({ b: { c: 2, d: 3 } }, { b: { e: 4 } });
```

- 函数会忽略原型链上的属性。

  ```javascript
  function Foo() {
    this.c = 3;
  }
  Foo.prototype.d = 4;
  Object.assign({ a: 1 }, new Foo());
  // { a: 1, c: 3 }
  ```

  原型链属性跟构造属性有区别

### lodash

lodash 中对象拷贝相关的方法

- \_.assign(object, [sources])
- _.extend(object, [sources]), _.assignIn(object, [sources])
  与\_.assign 不同的是拷贝原型链的属性
- _.merge(object, [sources])
  与_.assign 不同的是递归拷贝属性，实质上为深拷贝

## 深拷贝

### JSON.parse()方法

```javascript
var obj2 = JSON.parse(JSON.stringify(obj1));
```

**存在问题：**

- 会抛弃对象的 constructor

  深拷贝之后，不管这个对象原来的构造函数是什么，在深拷贝之后都会变成 Object。
  这种方法能正确处理的对象只有 Number, String, Boolean, Array, 扁平对象，即那些能够被 json 直接表示的数据结构。
  RegExp 对象是无法通过这种方式深拷贝的。

### 递归拷贝

```javascript
/* ================ 深拷贝 ================ */
function deepClone(initalObj, finalObj) {
  var obj = finalObj || {};
  for (var i in initalObj) {
    if (typeof initalObj[i] === "object") {
      obj[i] = initalObj[i].constructor === Array ? [] : {};
      arguments.callee(initalObj[i], obj[i]); // deepClone(initalObj[i], obj[i]);
    } else {
      obj[i] = initalObj[i];
    }
  }
  return obj;
}
```

上述代码确实可以实现深拷贝。但是当遇到两个互相引用的对象，会出现死循环的情况。

```javascript
var b = {};
var a = { a: b };
deepClone(a, b);
```

运行报错：

```
RangeError: Maximum call stack size exceeded
```

为了避免相互引用的对象导致死循环的情况，则应该在遍历的时候判断是否相互引用对象，如果是则退出循环。

改进版代码如下：

```javascript
function deepClone(initalObj, finalObj) {
  var obj = finalObj || {};
  for (var i in initalObj) {
    var prop = initalObj[i];

    // 避免相互引用对象导致死循环，如initalObj.a = initalObj的情况
    if (prop === obj) {
      continue;
    }
    if (typeof prop === "object") {
      obj[i] = prop.constructor === Array ? [] : {};
      arguments.callee(prop, obj[i]);
    } else {
      obj[i] = prop;
    }
  }
  return obj;
}
```
