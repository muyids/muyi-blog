---
title: 画图工具graphviz
date: 2019-12-04T04:53:00+08:00
categories: [工具]
tags: [工具]
---

DOT 语言学习笔记

<!--more-->

设置点和线的形状与颜色

digraph 是有向图，graph 是无向图。要注意，->和--都表示图中的一条边，但是前者用于有向图中，而后者用于无向图中，不能混用。

代码示例

```
digraph G{
    main -> parse -> execute
    main -> init
    main -> cleanup
    execute -> make_string
    execute -> printf
    init -> make_string
    main -> printf
    execute -> compare
}
```

然后在命令行(cmd)中运行此文件，

dot -T 输出格式 程序文件名.dot -o 输出文件名.输出格式

我们可以手动设置图的属性，即设置图中边的属性与图中点的属性。

我们可以在每条边后面添加中括号，在其中设置边的相关属性，也可以使用 edge 设置边的默认值。点的属性设置方法相同，node 表示点的默认值。

```
digraph G{
    size = "4, 4"  /*设置图片尺寸为4 * 4（英寸）*/
    main[shape = box] /*设置点main形状为矩形，默认为椭圆形*/
    main -> parse[weight = 8]  /*设置main到parse的边的重要程度，默认为1*/
    parse -> execute
    main -> init[style = dotted] /*设置main到init的边的样式为点，默认为实线*/
    main -> cleanup
    execute -> {make_string printf} /*一次连接两条边，以隔开目标点*/
    init -> make_string
    edge[color = red]  /*将此语句后的边的颜色设置为红色*/
    main -> printf[style = bold, label = "100 times"]
    node[shape = box, style = filled, color = ".7 .3 1.0"] /*设置此语句后的点的默认属性， 其中color的值采用RGB标准*/
    make_string[label = "make a\nstring"]
    execute -> compare
    compare -> return
}
```

此外，还可以使用 dir 设置每条边的箭头方向，有 forward(default),back,both,nonc，分别表示前向，反向，双向和无。如下所示：

```digraph
digraph G{
    A -> B[dir = both]
    B -> C[dir = nonc]
    C -> D[dir = back]
    D -> A[dir = forward]
}
```

点的属性除了 record 和 Mrecord 这两种之外，其他的形状都是多边形，而我们可以对多边形进行设置。sides 用于设置边数，peripheries 用于设置多边形外框的层数，`regular = true`可以使你的多边形是一个规则的多边形，`orientation = *`可以让你的多边形旋转\*角度，skew 后面跟一个（-1.0~1.0）的小数，能使你的图形斜切一个角度，distortion 则可以令你的图形产生透视效果。

```digraph
digraph G{
    a -> b -> c
    b -> d
    a[shape = polygon, sides = 5, peripheries = 3, color = lightblue, style = filled]
    c[shape = polygon, sides = 4, skew = 0.4, label = "hello world"]
    d[shape = invtriangle]
    e[shape = polygon, sizes = 4, distortion = .7]
}

digraph G{
    A -> B
    A[orientation = 15, regular = true, shape = polygon, sides = 8,
     peripheries = 4, color = red, style = filled]
    B[shape = polygon, sides = 4, skew = 0.5, color = blue]
}
```

record 与 Mrecord 的区别就是 Mrecord 的角是圆的，而 record 是由横竖的矩形组成的图形。

```
digraph G{
   node[shape = record]
   struct1[label = "<f0> left | <f1> middle | <f2> right"]
   struct2[label = "<f0> one | <f1> two"]
   struct3[label = "hello \nworld | {b | {c | <here> d | e} | f} | g | h"]
   struct1 -> struct2
   struct1 -> struct3
}
```

当你的线与线的 label 较多时，可以设置线的属性 decorate=true 使得每条线与其属性之间产生连线。你还可以为每条线设置属性 headlabel，taillabel，给每条线的起始点和终点设置属性，它们的颜色由 labelfontcolor 决定，而 label 的颜色由 fontcolor 来决定。

```
graph G{
   label = "我爱你" /*为图设置标签*/
   labelloc = b    /*图标签的位置在底部，也可以设置为r到顶部*/
   labeljust = l   /*图标签的位置在左边，也可以设置为r到右边*/

   edge[decorate = true]
   C -- D[label = "s1"]
   C -- E[label = "s2"]
   C -- F[label = "s3"]
   D -- E[label = "s4"]
   D -- F[label = "s5"]
   edge[decorate = false, labelfontcolor = blue, fontcolor = red]
   C1 -- D1[headlabel = "d1", taillabel = "c1", label = "c1 - d1"]
}
```

在 dot 语言中，我们可以使用 html 语言制作表格。在 label 后添加<>，而不是""就能添加 html 语言。

```
digraph struct {
   abc[shape=none, margin=0, label=<
   <TABLE BORDER = "0" CELLBORDER = "1" CELLSPACING = "0" CELLPADDING = "4">
   <TR><TD ROWSPAN = "3"><FONT COLOR = "red">hello</FONT><BR/>world</TD>
   <TD COLSPAN = "3">b</TD>
   <TD ROWSPAN = "3" BGCCOLOR = "lightgrey">g</TD>
   <TD ROWSPAN = "3">h</TD>
   </TR>
   <TR><TD>c</TD>
   <TD PORT = "here">d</TD>
   <TD>e</TD>
   </TR>
   <TR><TD COLSPAN = "3">f</TD>
   </TR>
   </TABLE>
   >]
}
```

设置点，线的位置以及子图的概念
图中的线默认是从上往下的，我们可以通过在文件的最上层设置 rankdir=LR 将其改为从左往右。同理，rankdir 可以设置为 TB(默认),BT,RL。
当图中时间表之类的东西时，我们可能需要点排列成一行（列），这时我们就需要 rank，在花括号中设置 rank=same，然后将需要并排的点一次输入。

排列对齐

```
digraph G{
   rankdir = LR
   {
    node[shape = plaintext]
    1995 -> 1996 -> 1997 -> 1998 -> 1999 -> 2000 -> 2001
   }
   {
    node[shape = box, style = filled]
    WAR3 -> Xhero -> Footman -> DOTA
    WAR3 -> Battleship
   }
   {
    {rank = same 1996 WAR3}
    {rank = same 1998 Xhero Battleship}
    {rank = same 1999 Footman}
    {rank = same 2001 DOTA}
   }
}
```

设立一条边时，我们可以制定这条边从起点的哪个位置出发，到终点的哪个位置结束。控制符有"n","ne","e","se","s","sw","w"和"nw"，具体效果见下：

```
digraph G{
   node[shape = box]
   c:n -> d[label = n]
   c1:ne -> d1[label = ne]
   c2:e -> d2[label = e]
   c3:se -> d3[label = se]
   c4:s -> d4[label = s]
   c5:sw -> d5[label = sw]
   c6:w -> d6[label = w]
   c7:nw -> d7[label = nw]
}
```

我们也可以在 record 中给点定义一些 port，以确定 record 中哪个部分用于连线。

```
digraph G{
   label = "Binary Search Tree"
   node[shape = record]
   A[label = "<f0> | <f1> A | <f2>"]
   B[label = "<f0> | <f1> B | <f2>"]
   C[label = "<f0> | <f1> C | <f2>"]
   D[label = "<f0> | <f1> D | <f2>"]
   E[label = "<f0> | <f1> E | <f2>"]
   A: f0: sw -> B: f1
   A: f2: se -> C: f1
   B: f0: sw -> D: f1
   B: f2: se -> E: f1
}
```

我们可以借此构建一个 Hash 表。

```
digraph G{
    nodesep = .05
    rankdir = LR
    node[shape = record, width = .1, height = .1]

    node0[label = "<f0> | <f1> | <f2> | <f3> | <f4> | <f5> | <f6>",height = 2.5]

    node[width = 1.5]

    node1[label = "{<n> n14 | 719 | <p>}"]
    node2[label = "{<n> a1 | 805 | <p>}"]
    node3[label = "{<n> i9 | 718 | <p>}"]
    node4[label = "{<n> e5 | 989 | <p>}"]
    node5[label = "{<n> t20 | 959 | <p>}"]
    node6[label = "{<n> o15 | 794 | <p>}"]
    node7[label = "{<n> s19 | 659 | <p>}"]

    node0: f0 -> node1: n
    node0: f1 -> node2: n
    node0: f2 -> node3: n
    node0: f5 -> node4: n
    node0: f6 -> node5: n
    node2: p -> node6: n
    node4: p -> node7: n
}
```

画一个子图就是 subgraph cluster#，必须有 clutser 前缀。这里"#"代表任意字符，当然为了便于区分，最好将"#"设置为非英文字母。

```digraphviz
digraph G{
    subgraph cluster1{
       node[style = filled, color = white]
       style = filled
       color = lightgrey
       a0 -> a1 -> a2 -> a3
       label = "process1"
    }

    subgraph cluster2{
        node[style = filled]
        color = blue
        b0 -> b1 -> b2 -> b3
        label = "process2"
    }
    start -> a0
    start -> b0
    a1 -> b3
    b2 -> a3
    a3 -> a0
    a3 -> end
    b3 -> end
    start[shape = Mdiamond]
    end[shape = Msquare]
}
```

如果你想将一条边连到一个子图的边界上，先输入 compound=true，然后就能用 lhead 和 ltail 设置连接的子图。

附录

- [点，边和图的属性](http://www.graphviz.org/doc/info/attrs.html)
- [点的形状](http://www.graphviz.org/doc/info/shapes.html)
