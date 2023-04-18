# 常用模块

ansible 有非常多的模块，我们只学习常见的

## Command

### 默认模块

```
ansible 172.16.244.192 -m command -a 'ls ~'
可以省略 -m 选项

ansible 172.16.244.192 -a 'ls ~'
```

```
# 新建文件夹
ansible 172.16.244.192 -a 'mkdir  ~/tmp'

# 查看是否创建成功
ansible 172.16.244.192 -a 'ls -dl ~/tmp'
```

### 查看文档

```
ansible-doc command
```

# Shell

# Script

# Copy

查看文档

```
ansible-doc -s copy
```

拷贝文件

```
ansible 172.16.244.192 -m copy -a 'src=~/Downloads/ip_list dest=/root/ backup=yes'
ansible 172.16.244.192 -a 'ls ~'
ansible 172.16.244.192 -a 'rm /root/ip_list'
```
