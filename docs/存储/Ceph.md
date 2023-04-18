## 公用存储服务信息

OpenEBS HostPath CSI Provider

## Minio 集群

底层存储使用的 HostPath 到 Ceph FS 上的(无其他备选方案)。

其中 filestore bucket 为公用数据共享 bucket，可以放一些 JDK 什么的，share link 的 hostname 手动替换成 http://xxxx 可以 wget 使用。

```shell
brew install minio-mc
mc alias set dxd xxx
mc cp xxxx dxd/filestore
mc policy --recursive links xxx
```
