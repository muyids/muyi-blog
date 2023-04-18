---
title: javascript实现继承的几种方式
date: 2016-09-18T04:53:00+08:00
draft: false
categories: [javascript]
tags: [javascript]
---

介绍几种 js 实现继承的方式

## 原型链继承

核心：将父类的实例作为子类的原型

缺点：父类新增原型方法/原型属性，子类都能访问到，父类一变其它的都变了

```javascript
// 原型链继承
function Person(name) {
  this.name = name;
}
Person.prototype.getName = function () {
  return this.name;
};
function Women(age) {
  this.age = age;
}
Women.prototype = new Person("娜扎");
Women.prototype.getAge = function () {
  return this.age;
};

let p = new Women(18);
console.log("人名：", p.getName());
console.log("年龄：", p.getAge());

Person.prototype.afterAdd = function () {
  console.log("afterAdd....");
};
p.afterAdd();
```

## 构造继承

基本思想

借用构造函数的基本思想就是利用 call 或者 apply 把父类中通过 this 指定的属性和方法复制（借用）到子类创建的实例中。
因为 this 对象是在运行时基于函数的执行环境绑定的。
也就是说，在全局中，this 等于 window，而当函数被作为某个对象的方法调用时，this 等于那个对象。
call、apply 方法可将一个函数的对象上下文从初始的上下文改变为由 thisObj 指定的新对象。
所以，这个借用构造函数就是，new 对象的时候(new 创建的时候，this 指向创建的这个实例)，创建了一个新的实例对象，
并且执行 Parent 里面的代码，而 Parent 里面用 call 调用了 Person，也就是说把 this 指向改成了指向新的实例，
所以就会把 Person 里面的 this 相关属性和方法赋值到新的实例上，而不是赋值到 Person 上面,
所以所有实例中就拥有了父类定义的这些 this 的属性和方法。
因为属性是绑定到 this 上面的，所以调用的时候才赋到相应的实例中，各个实例的值就不会互相影响了。

核心：使用父类的构造函数来增强子类实例，等于是复制父类的实例属性给子类（没用到原型）
缺点：方法都在构造函数中定义，只能继承父类的实例属性和方法，不能继承原型属性/方法，无法实现函数复用，
每个子类都有父类实例函数的副本，影响性能

```javascript
function Person(name) {
  this.name = name;
  this.getName = function () {
    return this.name;
  };
}

function Parent(age) {
  Person.call(this, "娜扎");
  this.age = age;
}
let p = new Parent(18);
console.log("姓名：", p.getName());
console.log("年龄：", p.age);
```

## 组合继承

组合继承（所有的实例都能拥有自己的属性，并且可以使用相同的方法，组合继承避免了原型链和借用构造函数的缺陷，
结合了两个的优点，是最常用的继承方式）
核心：通过调用父类构造，继承父类的属性并保留传参的优点，然后再通过将父类实例作为子类原型，实现函数复用

缺点：调用了两次父类构造函数，生成了两份实例（子类实例将子类原型上的那份屏蔽了）

```javascript
function Person(name) {
  this.name = name;
  this.getName = function () {
    return this.name;
  };
}

function Parent(age) {
  Person.call(this, "娜扎"); //这一步很关键
  this.age = age;
}
Parent.prototype = new Person("娜扎"); //这一步也很关键
Parent.prototype.getAge = function () {
  return this.age;
};
var result = new Parent(18);
console.log("姓名：", result.getName());
console.log("年龄：", result.getAge());
```
