# 前置概念理解

## 主控端 和 被控端

## 代理程序 和 无代理

通过代理软件管理是有代理的，ssh 是无代理的

代理软件性能更好

ansible 是无代理的，通过 ssh 管理，适用于中小型环境，几百台机器最多了

# 企业实战场景

![image-20220515015923560](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515015923560.png)

# 特性

![image-20220515020324645](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515020324645.png)

ansible 的幂等性 是如何实现的？比如拷贝文件，第二次执行会提示；创建用户，第二次执行会报错

# 架构

![image-20220515021314591](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515021314591.png)

# 工作原理

![image-20220515021342201](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515021342201.png)

# 安装使用

## 安装

```shell
 brew install ansible@2.9 --verbose
 echo 'export PATH="/usr/local/opt/ansible@2.9/bin:$PATH"' >> ~/.zshrc
 source ~/.zshrc
 ansible --version    # 检查是否安装成功
```

## 配置文件修改

### 主配置文件

```
 sudo vim /etc/ansible/ansible.cfg
```

### hosts 文件

```
sudo vim /etc/ansible/host
```

### 配置用户名密码登录

#### 安装 sshpass

```
 # 手动下载 sshpass.rb  的brew源文件，然后执行安装命令
 brew install sshpass.rb
```

#### 根据 IP 批量生成信息追加到~/.ssh/knows_hosts 文件

```shell
#!/bin/bash
set
#定义knows_hosts所在目录
SSH_DIR=~/.ssh

SCRIPT_PREFIX=./tmp
TMP_SCRIPT=$SCRIPT_PREFIX.sh
for ip in $(cat ip_list)
do
#不相等，则IP不为空
    if [ "x$ip" != "x" ]; then
        echo -------------------------
        echo "x$ip","x"
        TMP_SCRIPT=${SCRIPT_PREFIX}.$ip.sh
        echo $TMP_SCRIPT
        # check known_hosts
        #判断IP是否已存在known_hosts
        val=`ssh-keygen -F $ip`
        #相等则IP不存在于known_hosts
        if [ "x$val" == "x" ]; then
            echo "$ip not in $SSH_DIR/known_hosts, need to add"
            val=`ssh-keyscan $ip 2>/dev/null`
            if [ "x$val" == "x" ]; then
                echo "ssh-keyscan $ip failed!"
            else
                echo $val>>$SSH_DIR/known_hosts
            fi
        fi
     fi
done
```

ip_list 文件格式如下：

```
172.16.245.15
172.16.245.11
172.16.245.14
172.16.244.251
172.16.244.192
172.16.244.220
172.16.244.199
```

# 常用工具

## ansible

### 执行远程命令

```shell
# 列出所有主机
ansible all --list-hosts

# 所有主机执行命令
ansible all -m command -a 'ls ~'
# 执行分组执行
ansible workServer -m command -a 'ls ~'
# 通配符
ansible *WebServer -m command -a 'ls ~'
ansible 172.168.* -m command -a 'ls ~'

# 或 关系 :
ansible WebServer:DBServer -m command -a 'ls ~'
```

### 命令执行过程

![image-20220515234529451](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515234529451.png)

通过 -v, -vv, -vvv 查看整个执行过程

```
 ansible 172.16.244.192 -m ping -vvv
```

## ansible-doc

查看帮助文档

```
ansible-doc -s ping
```
