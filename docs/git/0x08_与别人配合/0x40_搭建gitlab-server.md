# Linux 安装包的方式安装

https://docs.gitlab.cn/omnibus/

## 下载安装后修改 `external_url`

修改 gitlab 配置文件 vim /etc/gitlab/gitlab.rb

## 命令

```shell
sudo gitlab-ctl start    # 启动所有 gitlab 组件；
sudo gitlab-ctl stop        # 停止所有 gitlab 组件；
sudo gitlab-ctl restart        # 重启所有 gitlab 组件；
sudo gitlab-ctl status        # 查看服务状态；
sudo gitlab-ctl reconfigure        # 启动服务；
sudo vim /etc/gitlab/gitlab.rb        # 修改默认的配置文件；
gitlab-rake gitlab:check SANITIZE=true --trace    # 检查gitlab；
sudo gitlab-ctl tail        # 查看日志；
```

# Server Hook 配置

## Gitlab 服务器端 custom hook 配置

https://www.jianshu.com/p/5531a21afa68

一、打开 gitlab 相关配置项

vim /etc/gitlab/gitlab.rb

gitlab_shell['custom_hooks_dir'] = "/etc/gitlab/custom_hooks"

二、创建相关文件夹

mkdir -p /etc/gitlab/custom_hooks
