https://www.bilibili.com/video/BV1rA4y1S7Hk

[Linux 三剑客实例详解「grep、sed 、awk」](https://zhuanlan.zhihu.com/p/139482499)

Linux 操作文本的三大利器分别是 grep、sed 、awk，简称三剑客。

- 大师兄 awk：最擅长取列；
- 二师兄 sed：最擅长取行；
- 三师兄 grep：最擅长过滤。

# 正则表达式

![preview](https://muyids.oss-cn-beijing.aliyuncs.com/img/v2-6795f6c39e02e82d82828fc0fa89cec5_r.jpg)

# grep

配合 通配符、正则表达式 过滤

# sed

最擅长取行

# awk

最擅长取列

[The GNU Awk User’s Guide](http://www.gnu.org/software/gawk/manual/gawk.html)

```shell

docker images | grep ^icyfen | awk '{system("docker push registry.xxx.cn/bi/"$1)}'
```
