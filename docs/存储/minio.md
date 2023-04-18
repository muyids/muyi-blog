https://min.io/

https://min.io/download#/linux

[SpringBoot 整合 Minio 上传文件](https://juejin.cn/post/7101581935486615559)

# minio 安装

## docker 单机启动

### 拉取镜像

```
docker pull minio/minio
```

### 启动

```
docker run -p 9000:9000 -p 9001:9001 -d --name minio -v /usr/local/opt/docker/minio/data:/data -v /usr/local/opt/docker/minio/config:/root/.minio -e "MINIO_ROOT_USER=minio" -e "MINIO_ROOT_PASSWORD=minio@123456" minio/minio server /data --console-address ":9000" --address ":9001"
```

### 登录管理台

地址：http://127.0.0.1:9000/

输入用户名，密码

# 本地配置

配置服务 dxd

$ mc alias set dxd http://172.16.243.28:31037 minioadmin minioadmin

> **mc: Configuration written to `/Users/dw/.mc/config.json`. Please update your access credentials.**
>
> **mc: Successfully created `/Users/dw/.mc/share`.**
>
> **mc: Initialized share uploads `/Users/dw/.mc/share/uploads.json` file.**
