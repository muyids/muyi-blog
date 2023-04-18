# XXL-JOB 文档

## 部署步骤

1、下载 Githup 项目https://github.com/xuxueli/xxl-job

2、执行项目 doc/db/tables_xxl_job.sql 文件在数据库中，此为调度平台的表创建 sql 脚本文件，记录任务的执行，用户信息等信息

3、xxl-job-admin 此为项目的调度平台，本身是一个 springboot 项目，在 resource/applications.properties 中修改 mysql 的 host，user，password 信息，此项目就配置完毕，然后即可启动，登录网址：http://localhost:8080/xxl-job-admin/ 账号：admin， 密码：123456

4、xxl-job-executor-sample-springboot 此为任务执行平台， resource/applications.properties 修改 xxl.job.admin.addresses 的配置，修改为 xxl-job-admin 的登录网址，例如：http://localhost:8080/xxl-job-admin/ 如此，任务执行平台部署完毕

5、如此单实例部署服务完成

## 服务介绍

调度服务主要分为以下几个模块，

Ø 运行报表，显示任务的运行情况，成功失败的比例等任务信息

Ø 任务管理，此为任务调度的配置模块，任务在此模块进行配置

Ø 调度日志，任务日志的运行情况，通过日志进行观察

4、执行器管理，执行任务的服务可以部署多个，多个服务在此进行配置

5、用户管理模块

6、官方使用教程

执行器管理模块详细介绍：

AppName 一般是你的 spingboot 的 server_name

名称：不做限制

注册方式：自动注册，如果服务中配置了 xxl.job.admin.addresses，那么调度服务可以进行自动发现，也可以采用手动注册的方式，同一个机器部署多个或者是部署在不同机器，ip:端口，用逗号进行分割

任务管理模块详细介绍：

![img](https://muyids.oss-cn-beijing.aliyuncs.com/img/202204211633633.png)

Ø 执行器：在执行器管理模块中可以配置多个执行器，在此可以进行选择

Ø 任务描述：执行任务的功能性描述

Ø 负责人：开发责任人

Ø 报警邮件：邮件地址，逗号分隔

Ø 调度类型：cron 表示采用定时的方式进行调度，亦可以不设置调度类型

Ø Cron：即定时时间配置

Ø 运行模式：bean 即 java 开发模式

Ø JobHandle: 需要你代码中开发的注解名字保持一致，例如@XxlJob("demoJobHandler")

Ø 任务参数：可以选择入参，代码中获取参数 String param = XxlJobHelper.getJobParam();

Ø 路由策略：FIRST（第一个）：固定选择第一个机器，

LAST（最后一个）：固定选择最后一个机器；

ROUND（轮询）： 按个机器执行；

RANDOM（随机）：随机选择在线的机器；

CONSISTENT_HASH（一致性 HASH）：每个任务按照 Hash 算法固定选择某一台机器，且所有任务均匀散列在不同机器上。

LEAST_FREQUENTLY_USED（最不经常使用）：使用频率最低的机器优先被选举；

LEAST_RECENTLY_USED（最近最久未使用）：最久未使用的机器优先被选举；

FAILOVER（故障转移）：按照顺序依次进行心跳检测，第一个心跳检测成功的机器选定为目标执行器并发起调度；

BUSYOVER（忙碌转移）：按照顺序依次进行空闲检测，第一个空闲检测成功的机器选定为目标执行器并发起调度；

SHARDING_BROADCAST(分片广播)：广播触发对应集群中所有机器执行一次任务，同时系统自动传递分片参数；可根据分片参数开发分片任务；

Ø 子任务 ID：当前任务执行完成后，执行子任务，如果有多个子任务用逗号分隔

Ø 调度过期策略：立即执行一次或者是忽略

Ø 阻塞处理策略：调度过于密集执行器来不及处理时的处理策略；

单机串行（默认）：调度请求进入单机执行器后，调度请求进入 FIFO 队列并以串行方式运行

丢弃后续调度：调度请求进入单机执行器后，发现执行器存在运行的调度任务，本次请求将会被丢弃并标记为失败；

覆盖之前调度：调度请求进入单机执行器后，发现执行器存在运行的调度任务，将会终止运行中的调度任务并清空队列，然后运行本地调度任务；

Ø 任务超时时间：支持自定义任务超时时间，任务运行超时将会主动中断任务；

Ø 失败重试次数；支持自定义任务失败重试次数，当任务失败时将会按照预设的失败重试次数主动进行重试

## 开发样例：

```java
@Component
public class SampleXxlJob {

    private static Logger logger = LoggerFactory.getLogger(SampleXxlJob.class);

    /**
     * 1、简单任务示例（Bean模式）
     */
    @XxlJob("demoJobHandler")
    public void demoJobHandler() throws Exception {
				//    获取输入的参数
        String param = XxlJobHelper.getJobParam();
				//    此为xxl的log日志，方便后续定是任务的追踪，用此日志类打印的日志可以在调度控制台上查看
        XxlJobHelper.log(param);
        XxlJobHelper.log("XXL-JOB, Hello World.");
				//      定制化业务代码

        for (int i = 0; i < 5; i++) {

            XxlJobHelper.log("beat at:" + i);

            System.out.println("beat at:" + i);

            TimeUnit.SECONDS.sleep(2);

        }

        // default success

    }
}
```
