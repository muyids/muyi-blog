---
title: Restful Api
date: 2016-05-18T00:00:00+08:00
categories: [系统设计]
tags: [系统设计]
---

`RESTful`是目前最流行的`API设计规范`，用于`Web数据接口的设计`。

<!--more-->

## 原则

1. 每一个 URI 代表一种资源；所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的”集合”（collection），所以 API 中的名词也应该使用复数。
1. 客户端和服务器之间，传递这种资源的某种表现层；
1. 客户端通过四个 HTTP 动词，对服务器端资源进行操作，实现”表现层状态转化”。

## Restful 规范的 API 设计

### 一、协议

API 与用户的通信协议，总是使用 HTTPS 协议。

### 二、域名

应该尽量将 API 部署在专用域名之下。

    https://api.example.com

如果确定 API 很简单，不会有进一步扩展，可以考虑放在主域名下。

    https://example.org/api/

### 三、版本

应该将 API 的版本号放入 URL。

https://api.example.com/v1/

另一种做法是，将版本号放在 HTTP 头信息中，但不如放入 URL 方便和直观。

### 四、路径

路径又称”终点”（endpoint），表示 API 的具体网址。

在 RESTful 架构中，每个网址代表一种资源（resource），所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的”集合”（collection），所以 API 中的名词也应该使用复数。

举例来说，有一个 API 提供学校（school）的信息，还包括各种学校和学生的信息，则它的路径应该设计成下面这样。

- https://api.example.com/v1/schools
- https://api.example.com/v1/students

### 五、HTTP 动词

对于资源的具体操作类型，由 HTTP 动词表示。

常用的 HTTP 动词有下面五个（括号里是对应的 SQL 命令）。

- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。 (使用较少)
- DELETE（DELETE）：从服务器删除资源。

还有两个不常用的 HTTP 动词。

- HEAD：获取资源的元数据。
- OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。
  下面是一些例子。

- GET /schools：列出所有学校
- POST /schools：新建一个学校
- GET /schools/ID：获取某个指定学校的信息
- PUT /schools/ID：更新某个指定学校的信息（提供该学校的全部信息）
- PATCH /schools/ID：更新某个指定学校的信息（提供该学校的部分信息）
- DELETE /schools/ID：删除某个学校
- GET /schools/ID/students：列出某个指定学校的所有学生
- DELETE /zoos/ID/students/ID：删除某个学校的指定学生

### 六、过滤信息（Filtering）

如果记录数量很多，服务器不可能都将它们返回给用户。API 应该提供参数，过滤返回结果。

下面是一些常见的参数。

```
?limit=10：指定返回记录的数量
?offset=10：指定返回记录的开始位置。
?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
?schools_type_id=1：指定筛选条件
参数的设计允许存在冗余，即允许API路径和URL参数偶尔有重复。比如，GET /school/ID/students/ID 与 GET /students?student_id=ID 的含义是相同的。
```

### 七、状态码

服务器向用户返回的状态码和提示信息，常见的有以下一些（方括号中是该状态码对应的 HTTP 动词）。

```
200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的。
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
204 NO CONTENT - [DELETE]：用户删除数据成功。
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。。
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
```

### 八、错误处理

如果状态码是 4xx，就应该向用户返回出错信息。一般来说，返回的信息中将 error 作为键名，出错信息作为键值即可。

    { error: "Invalid API key” }

### 九、返回结果

针对不同操作，服务器向用户返回的结果应该符合以下规范。

- GET /collection：返回资源对象的列表（数组）
- GET /collection/resource：返回单个资源对象
- POST /collection：返回新生成的资源对象
- PUT /collection/resource：返回完整的资源对象
- PATCH /collection/resource：返回完整的资源对象
- DELETE /collection/resource：返回一个空文档

### 十、Hypermedia API

RESTful
API 最好做到 Hypermedia，即返回结果中提供链接，连向其他 API 方法，使得用户不查文档，也知道下一步应该做什么。
比如，当用户向 api.example.com 的根目录发出请求，会得到这样一个文档。

```
  "link”: {
     "rel”: "https: //www.example.com/zoos",
     "href”: "https: //api.example.com/",
     "title”: "Listofzoos”,
     "type”: "application/vnd.yourformat+json”
  }
}
```

上面代码表示，文档中有一个 link 属性，用户读取这个属性就知道下一步该调用什么 API 了。rel 表示这个 API 与当前网址的关系（collection 关系，并给出该 collection 的网址），href 表示 API 的路径，title 表示 API 的标题，type 表示返回类型。

Hypermedia API 的设计被称为 HATEOAS。Github 的 API 就是这种设计，访问 api.github.com 会得到一个所有可用 API 的网址列表。

    { "current_user_url”: "https://api.github.com/user", "authorizations_url”: "https://api.github.com/authorizations", // … }

从上面可以看到，如果想获取当前用户的信息，应该去访问 api.github.com/user，然后就得到了下面结果。

    { "message”: "Requires authentication”, "documentation_url”: "https://developer.github.com/v3” }

上面代码表示，服务器给出了提示信息，以及文档的网址。

### 十一、其他

- （1）API 的身份认证应该使用 OAuth 2.0 框架。
- （2）服务器返回的数据格式，应该尽量使用 JSON，避免使用 XML。
