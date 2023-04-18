java 的注解学习

aop 实现 redis 分布式锁，可以通过注解+spel 表达式拼出你的 key，加在方法纬度上就可以了。部门现在确实有这么一个组件，不过我还是比较喜欢自己拿锁手动释放，异常处理逻辑比较清晰。

![179981629461259_.pic](https://muyids.oss-cn-beijing.aliyuncs.com/179981629461259_.pic.jpg)

![180071629462006_.pic](https://muyids.oss-cn-beijing.aliyuncs.com/180071629462006_.pic.jpg)

![180081629462023_.pic](https://muyids.oss-cn-beijing.aliyuncs.com/180081629462023_.pic.jpg)

注解

- 反射机制

Java 的注解 实战一下

---

中间件架构

nodejs express 框架中间件架构

```
// 路由层
// 签到功能API
router.post('/daily/sign/accept',
    signMiddleware.checkTime,
    middleware.lock('signAccept', 'userId'),
    middleware.checkAppSign,
    middleware.checkToken,
    middleware.checkMacAddress,
    middleware.midCheckUser(),
    signMiddleware.getSignInfo, middleware.verifyValidateCode, middleware.todaySignIn,
    middleware.getUserInfo, middleware.getUserBirthDay,
    signService.accept)

// 中间件层
exports.lock = function (prefix, param) {
    return function (req, res, next) {
        var key = 'lock-' + prefix + '-' + req.param(param)
        redisClient.incr(key, function (err, value) {
            redisClient.EXPIRE(key, 30)
            console.log('[%j], lockID: %j, value: %j, err: %j', new Date().toLocaleString(), key, value, err)
            if (err) {
                return res.send(500, '系统繁忙')
            }
            if (value > 1) {
                return res.send(403, '操作太频繁')
            }
            req.lockID = key
            return next()
        })
    }
}
```
