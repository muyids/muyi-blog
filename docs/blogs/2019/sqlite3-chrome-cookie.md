---
title: golang查询并解析chrome浏览器的cookie
date: 2019-10-01T00:00:00+08:00
categories: [shell, sqlite3, cookie, chrome]
tags: [shell, sqlite3, cookie, chrome]
draft: false
---

怎么在终端里拿到浏览器的 cookie 呢？

<!--more-->

每次查询 cookie，总是要先打开浏览器，然后在设置选项中找，很麻烦

我们能不能写一个工具，直接在 Terminal 中获得相应网站的 cookie 呢？

---

下面，我们以 mac 系统中 chrome 浏览器为例，进行探索。。。

找到 chrome 浏览器的 cookie 文件所在位置`~/Library/Application Support/Google/Chrome/Profile 1/Cookies`

这个位置可能不一致，有些机器在`~/Library/Application Support/Google/Chrome/Default/Cookies`目录下

cookie 文件是 sqlite3 数据库的文件格式，我们使用 sqlite3 加载

```shell script
cd ~/Library/Application\ Support/Google/Chrome/Profile\ 1/ && sqlite3 Cookies
```

查看数据库中有哪些表

```shell script
> .tables
```

查看 cookies 表结构

```shell script
> .schema cookies
```

得到表结构

```shell script
CREATE TABLE cookies(
    creation_utc INTEGER NOT NULL,
    host_key TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    path TEXT NOT NULL,
    expires_utc INTEGER NOT NULL,
    is_secure INTEGER NOT NULL,
    is_httponly INTEGER NOT NULL,
    last_access_utc INTEGER NOT NULL,
    has_expires INTEGER NOT NULL DEFAULT 1,
    is_persistent INTEGER NOT NULL DEFAULT 1,
    priority INTEGER NOT NULL DEFAULT 1,
    encrypted_value BLOB DEFAULT '',
    samesite INTEGER NOT NULL DEFAULT -1,
    UNIQUE (host_key, name, path));
```

哈哈，我们直接用 sql 语句查询相应字段，不就大功告成了，so easy!

等等...encrypted_value 是什么鬼！！！
