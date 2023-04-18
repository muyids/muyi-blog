# 编辑器选择

typora： markdown 编辑神器

# shell 直接打开 Typora 编辑文件或目录

您可以用来`open -a typora xxx.md`在 Typora 中打开目标文件或目录。如果 Typora 是您的`.md`文件默认编辑器，那么使用`open xxx.md`可以打开 markdown 文件。 您也可以添加

```
alias typora="open -a typora"
```

在您的 `.bash_profile` 配置文件或其他配置文件中，则可以 `typora xxx.md`直接从 shell 程序/终端打开 markdown 文件。

# 目录如何编辑

markdown 使用 h1, h2, h3,,,,来作为目录，但是编写时 目录是第几级的显示并不明显，有没有方法使其显式地显示出来呢？答案是可以的，因为 markdown 是通过解析成 html 文件来进行显示的，所以我们可以 通过自定义 CSS 的方式 进行 目录层级的显示。

## 参考

Markdown 编辑器 Typora 标题自动编号

https://blog.csdn.net/whitepu/article/details/114370549

# 优雅的插入图片

选择一款顺手的截图软件，推荐 $snipast$， 快捷键截图

设置 图床 软件选择 **PicGo**

![image-20220515010035956](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515010035956.png)

这样就能实现 截图 复制到 $markdown$ 中直接上传到 远程$CDN$

# 编辑数学公式

快速插入数学公式**快捷键**：$⌥ + ⌘ + B$

$$
your\ math\ line
$$

---

## 内联公式

![image-20220515203158948](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515203158948.png)

勾选后，重启 Typora

在插入 行内公式的地方 输入 `$$公式内容$$ `即可，也可以使用快捷键 $⌃ + M$ 直接插入

## 自定义快捷键设置

![image-20220515204956624](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515204956624.png)

Inline Math 为已有快捷键，测试未通过，后续继续探索

# typora 回车中的多余空行处理

typora 编辑后的文件中存在大量的回车键造成的空白行

## sed 命令介绍

删除连续空行但保留一行

```shell
sed -i "" 'N;/^\n/D'
```

这里要注意 mac 系统的 sed 命令 比 linux 多了 一个 `""`，linux 为 `sed -i 'N;/^\n/D'`

## find 命令介绍

打印除 node_modules 路径下的 所有 md 文件

```shell
find . -path ./node_modules -prune -o -name "*.md" -print
```

## 筛选文件并进行连续空行合并

将 -print 命令替换成 `-exec`

```shell
find . -path ./node_modules -prune -o -name "*.md" -exec sed -i "" 'N;/^\n/D' {} \;
```
