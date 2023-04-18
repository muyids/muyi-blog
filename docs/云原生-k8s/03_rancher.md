#### Projects/Namespaces 介绍

创建 project，创建 namespace

#### Resources/WorkLoad 介绍

Deploy Workload

- Name :

- Workload Type:

  1.  Scalable deployment of 1 pod
  2.  Run one pod on each node
  3.  Stateful set of 1 pod
  4.  Run on a cron schedule
  5.  Job

- Docker image

- Namespace

- Port Mapping

  > PortName
  >
  > Publish the container port :
  >
  > Protocol:
  >
  > As a :
  >
  > 1. NodePort (On every node)
  > 2. HostPort
  > 3. Cluster IP
  > 4. Layer-4 Load Balancer
  >
  > On listening port : 主机端口
  > 部署一个 nginx workloads

#####

#### Load Balancing 介绍

##### Ingress 是什么？

k8s 上的概念，7 层负载均衡

##### Add Ingress 操作

- Name

- namespace

- Rules
  1. Automatically generate a `.xip.io` hostname
  2. Specify a hostname to use :
  3. Use as the default backend
- Target Backend
  - service
  - Workload

#### Services Discovery 介绍

对应的是 k8s 中的 service

5 种 service 类型：

- One or more external IP addresses ： 外部目标 IP 地址
- An external hostname ： 外部目标 hostname
- Alias of another DNS record's value
- One or more workloads :
