引用：https://juejin.cn/post/6844903863447715848

#### 1、制作镜像

##### 操作步骤

```
mkdir helloworld-nodejs # 项目名称
cd helloworld-nodejs
npm init -y # 一路回车
vim app.js # 创建文件,内容在下面
npm i -S express # 安装依赖
# 在package.json文件中新增 {"start": "node app.js"}
npm start # 测试你的程序没有问题
vim Dockerfile # 创建Dockerfile, 内容在下面
docker build -t dwyang/helloworld-nodejs:v1.0.0 . # 构建镜像, 请更改为自己账号名称
docker run -p 9854:9854 dwyang/helloworld-nodejs:v1.0.0 # 测试你的镜像没有问题

# 推送镜像到 docker hub -- TODO
# 这里需要在你的docker仓库新建镜像,之后执行下面的操作; 我的地址为: https://hub.docker.com/u/pengj
# 如果先登录再创建,则推送会报仓库不存在
docker login # 登录, 输入账号和密码
docker push dwyang/helloworld-nodejs:v1.0.0 # 推送镜像
复制代码
```

##### `app.js`内容

```javascript
var express = require("express");
var PORT = 9854;

var app = express();
app.get("/", function (req, res) {
  res.send("Hello world\n");
});
app.listen(PORT);
console.log("Running on http://localhost:" + PORT);
```

##### `Dockerfile`内容

```yml
#node镜像版本
FROM node:8-alpine

#在image中创建文件夹
RUN mkdir -p /home/Service
#将该文件夹作为工作目录
WORKDIR /home/Service
# 将node工程下所有文件拷贝到Image下的文件夹中
COPY . /home/Service
#使用RUN命令执行npm install安装工程依赖库
RUN npm install
#暴露给主机的端口号
EXPOSE 9845
#执行npm start命令，启动Node工程
CMD [ "npm", "start" ]
```

#### 2、部署到 k8s

##### 前提

已搭建好 k8s 集群

##### 部署

```shell
# 新增名字为`helloworld-node-kube-apps`的namespace,内容在下面,在nodeapp-k8s.yaml会使用
kubectl apply -f helloworld-node-kube-apps.yaml
# 在master机器上创建nodeapp-k8s.yaml,内容在下面,你需要更换`pengj/nodeappk8s:v1.0.0`为你自己的镜像仓库或者直接使用(省事)
vim nodeapp-k8s.yaml
# 部署配置, 如果多次部署会存在重复文件, 可以使用kubectl delete -f nodeapp-k8s.yaml删除
kubectl apply -f nodeapp-k8s.yaml
# 执行成功会输出
# deployment "nodeapp-deploy" created
# service "nodeapp-svc" created
# ingress "nodeapp-ingress" created
```

`nodeapp-k8s.yaml`文件中定义了 3 类资源`Deployment`、`Service`、`Ingress`;

`Deployment`设置了`replicas: 2`，表示会运行两个`POD`

`strategy`的滚动策略为`RollingUpdate`，`resources`区域定义了一个 POD 的资源限制，通过`livenessProbe`和`readinessProbe`设置了健康检查

##### 校验

```shell
# 可能会出现0/2, 1/2的情况, 等一会儿就OK
kubectl get deployments -n kube-apps |grep nodeapp
# nodeapp-deploy   2/2     2            2           109m
kubectl get svc -n kube-apps |grep nodeapp
# nodeapp-svc   NodePort   10.97.144.116   <none>        8080:31000/TCP   109m
kubectl get ingress -n kube-apps |grep nodeapp
# nodeapp-ingress   nodeappk8s.local             80      110m
kubectl get pods -n kube-apps |grep nodeapp
# nodeapp-deploy-5c84c9d676-m7zwc   1/1     Running   0          110m
# nodeapp-deploy-5c84c9d676-v8r6g   1/1     Running   0          110m
```

**两种访问方式:**

1.使用集群之间可见 ip 访问, 只能够在集群部署的机器上可用: `curl http://10.97.144.116:8080/ping`

2.使用通用的 ip 访问, 但是需要使用配置文件中`32000`端口才行

`helloworld-node-kube-apps.yaml`内容

```
apiVersion: v1
kind: Namespace
metadata:
   name: helloworld-node-kube-apps
   labels:
     name: helloworld-node-kube-apps
```

`nodeapp-k8s.yaml`内容

```
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nodeapp-deploy
  namespace: helloworld-node-kube-apps
  labels:
    k8s-app: nodeappk8s
spec:
  replicas: 2
  revisionHistoryLimit: 10
  minReadySeconds: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  template:
    metadata:
      labels:
        k8s-app: nodeappk8s
    spec:
      containers:
      - image: pengj/nodeappk8s:v1.0.0
        imagePullPolicy: Always
        name: nodeappk8s
        ports:
        - containerPort: 8888
          protocol: TCP
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
          requests:
            cpu: 50m
            memory: 50Mi
        livenessProbe:
          tcpSocket:
            port: 8888
          initialDelaySeconds: 10
          timeoutSeconds: 3
        readinessProbe:
          httpGet:
            path: /
            port: 8888
          initialDelaySeconds: 10
          timeoutSeconds: 2
---
apiVersion: v1
kind: Service
metadata:
  name: nodeapp-svc
  namespace: helloworld-node-kube-apps
  labels:
    k8s-app: nodeappk8s
spec:
  type: NodePort
  ports:
    - name: api
      port: 8888
      targetPort: 8888
      nodePort: 32000
  selector:
    k8s-app: nodeappk8s

---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nodeapp-ingress
  namespace: helloworld-node-kube-apps
spec:
  rules:
  - host: nodeappk8s.local
    http:
      paths:
      - path: /
        backend:
          serviceName: nodeapp-svc
          servicePort: api
```
