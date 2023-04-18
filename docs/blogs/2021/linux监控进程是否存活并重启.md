#### 启动脚本

```shell
#!/bin/bash
jarname='passport-1.0.0.jar'
pid=`ps aux | grep $jarname | grep -v grep | awk '{print $2}'`
echo $pid
currTime=$(date +"%Y-%m-%d %T")
if [ !$pid ]; then
	echo '$currTime项目重新启动($pid)' >> /root/run.log &
	nohup java -jar -Dspring.profiles.active=prod /root/passport-1.0.0.jar > out.file 2>&1 &
else
	echo "$currTime项目已经启动($pid)" >> /root/run.log &
fi
```

**设置定时任务**

crontab -e

```
*/1 * * * * sh /root/startup.sh&
```

**定时任务状态查看**

```
service crond start     //启动服务
service crond stop      //关闭服务
service crond restart   //重启服务
service crond reload    //重新载入配置
service crond status    //查看crontab服务状态
```
