# 使用 lua 脚本的好处

1. 减少网络开销：本来 5 次网络请求的操作，可以用一个请求完成
2. 原子操作：Redis 会将整个脚本作为一个整体执行，中间不会被其他命令插入
3. 复用：客户端发送的脚本会永久存储在 Redis 中，意味着其他客户端可以复用这一脚本而不需要使用代码完成同样的逻辑。

# 准备条件

- redis 在服务器端内置 lua 解释器（版本 2.6 以上）
- redis-cli 提供了`EVAL`与`EVALSHA`命令执行 Lua 脚本

# redis 内置 lua 执行命令

## EVAL 命令语法

> EVAL script numkeys key [key …] arg [arg …]

- EVAL —- lua 程序的运行环境上下文
- script —- lua 脚本
- numkeys —- 参数的个数(key 的个数)
- key —- redis 键,访问下标从 1 开始,例如:KEYS[1]
- arg —- redis 键的附加参数

## EVALSHA 命令语法

> EVALSHA SHA1 numkeys key [key …] arg [arg …]

EVALSHA 命令允许通过脚本的 SHA1 来执行(节省带宽)

Redis 在执行 EVAL/SCRIPT LOAD 后会计算脚本 SHA1 缓存, EVALSHA 根据 SHA1 取出缓存脚本执行

## Redis 中管理 Lua 脚本

- script load script 将 Lua 脚本加载到 Redis 内存中(如果 redis 重启则会丢失)
- script exists sh1 [sha1 …] 判断 sha1 脚本是否在内存中
- script flush 清空 Redis 内存中所有的 Lua 脚本
- script kill 杀死正在执行的 Lua 脚本。（如果此时 Lua 脚本正在执行写操作，那么 script kill 将不会生效）
  Redis 提供了一个 lua-time-limit 参数，默认 5 秒，它是 Lua 脚本的超时时间,如果 Lua 脚本超时，其他执行正常命令的客户端会收到“Busy Redis is busy running a script”错误，但是不会停止脚本运行，此时可以使用 script kill 杀死正在执行的 Lua 脚本。

## lua 函数

主要有两个函数来执行 redis 命令

- redis.call() –- 出错时返回具体错误信息,并且终止脚本执行
- redis.pcall() –- 出错时返回 lua table 的包装错误,但不引发错误
  使用流程如下：

1. 编写脚本
2. 脚本提交到 REDIS 并获取 SHA
3. 使用 SHA 调用 redis 脚本

# redis 运行 lua 脚本

## EVAL 直接运行脚本

> EVAL "return {KEYS[1],KEYS[2],ARGV[1],ARGV[2]}" 2 key1 key2 first second

## EVALSHA 使用

需要`SCRIPT LOAD`和`EVALSHA`配合使用

1. SCRIPT LOAD 加载到内存，返回 SHA 签名
2. EVALSHA 使用已经存在的签名
   这样只用加载一次，便可重复使用已经加载的签名脚本，可以多次使用，避免长脚本输入

```
> SCRIPT LOAD "return {KEYS[1],KEYS[2],ARGV[1],ARGV[2]}"
"a42059b356c875f0717db19a51f6aaca9ae659ea"
EVALSHA "a42059b356c875f0717db19a51f6aaca9ae659ea" 2 key1 key2 first second
1) "key1"
2) "key2"
3) "first"
4) "second"
```

## 在 redis 下使用脚本文件执行

在路径下创建脚本文件，这里直接在`redis/bin`下创建，方便使用，其他目录可以使用全路径

`set.lua`

```lua
--[[ set.lua, redis的set命令使用
redis: set key val
--]]
local key = KEYS[1]
local val = ARGV[1]
return redis.call('set', key, val)
```

设置 k-v 值，运行命令

> redis-cli --eval ./set.lua foo , bar

**注意**：`redis-cli --eval set.lua foo , bar`，foo 和 bar 之间的逗号左右都有空格分隔,否则会当做一个字符串

通过 redis-cli 查看值

```
127.0.0.1:6379> get foo
"bar"
```

`get.lua`

```lua
--[[ get.lua, redis的get命令使用
redis: get key
--]]
local key = KEYS[1]
local val = redis.call("GET", key);
return val;
```

获取 k 值，运行命令

> redis-cli --eval ./get.lua foo

通常做法是

1. 脚本文件保存到一个路径下或者数据库中，比如：`/mnt/redis/lua/set.lua`
2. `SCRIPT LOAD` 加载脚本文件内容，返回 SHA 签名保存到应对的值 K-V 值，(set,SHA)
3. 获取对应脚本名称的 SHA 签名，如果存在则执行，否则进行第二步操作

# 实际开发应用实战

## 访问次数限制

需求场景：限制用户在一段时间内只能访问某一资源限定次数

ratelimiting.lua

```lua
local times = redis.call('incr',KEYS[1])
if times == 1 then
    redis.call('expire',KEYS[1], ARGV[1])
end

if times > tonumber(ARGV[2]) then
    return 0
end
return 1
```

运行脚本（限定 10 秒内最多访问 3 次）：

```
redis-cli --eval ratelimiting.lua rate.limitingl:127.0.0.1 , 10 3
(integer) 1
redis-cli --eval ratelimiting.lua rate.limitingl:127.0.0.1 , 10 3
(integer) 1
redis-cli --eval ratelimiting.lua rate.limitingl:127.0.0.1 , 10 3
(integer) 1
redis-cli --eval ratelimiting.lua rate.limitingl:127.0.0.1 , 10 3
(integer) 0
```

- rate.limitingl:127.0.0.1 是前缀+ip 组成的 KEY，用 KEYS[1]获取，
- ","后面的 10 和 3 是参数，在脚本中能够使用 ARGV[1]和 ARGV[2]获得
  命令的作用是将访问频率限制为每 10 秒最多 3 次，所以在终端中不断的运行此命令会发现当访问频率在 10 秒内小于或等于 3 次时返回 1，否则返回 0。

## lua 实现 redis 分布式锁

分布式锁需要考虑的问题

1. 失效时间；如果没有失效时间，当解锁失败时，就会导致锁记录一直在 tair 中，其他线程无法再获得到锁。
2. 非阻塞：分布式锁应该是非阻塞的，无论成功还是失败都直接返回
3. 非重入：一个线程获得锁之后，在释放锁之前，无法再次获得该锁

### 实现思路

**setnx**：如果 key 不存在则添加值并返回 1，如果已经存在 key 则返回 0

**加锁**

使用业务 setnx(key,业务流水号)当加锁成功返回 1 时设置过期时间，避免业务异常没有解锁时防止死锁

**重入锁**

当同一业务再次申请锁时，如果随机值相同 则认为是重试,则直接设置过期时长；如果随机值不同则直接返回 0，获取锁失败

**解锁**

业务完成直接 del(key)完成

以上方案是很多客户端实现的方式，建立和释放锁，并保证绝对的安全，是这个锁的设计比较棘手的地方。有两个潜在的陷阱：

1. 应用程序通过网络和 redis 交互，这意味着从应用程序发出命令到 redis 结果返回之间会有延迟。这段时间内，redis 可能正在运行其他的命令，而 redis 内数据的状态可能不是你的程序所期待的。如果保证程序中获取锁的线程和其他线程不发生冲突？
2. 如果程序在获取锁后突然 crash，而无法释放它？这个锁会一直存在而导致程序进入“死锁”
   对于第一个问题，除了 pile 批量一次执行，目前只有 lua 脚本是在同一个线程中一次执行完的。
   第二个问题，如果在获取锁之后，设置 expire 之前发生了异常，那么这个 key-v 永远都不会过期，即便是 lua 脚本也是一样会发生这样的情况（通常是设置过期时间这个参数设置的不是数字类型，虽然这种情况不太可能发生），但仍然比客户端多条命令执行来的更加简短
   lock.lua

```lua
-- Set a lock
--  如果获取锁成功，则返回 1
local key     = KEYS[1]
local content = ARGV[1]
local ttl     = tonumber(ARGV[2])
local lockSet = redis.call('setnx', key, content)
if lockSet == 1 then
  redis.call('PEXPIRE', key, ttl)
else
  -- 如果value相同，则认为是同一个线程的请求，则认为重入锁
  local value = redis.call('get', key)
  if(value == content) then
    lockSet = 1;
    redis.call('PEXPIRE', key, ttl)
  end
end
return lockSet
```

unlock.lua

```lua
-- unlock key
local key     = KEYS[1]
local content = ARGV[1]
local value = redis.call('get', key)
if value == content then
  return redis.call('del', key)
else
    return 0
end
```

测试加锁和解锁

```
redis-cli  --eval lock.lua lo3 , 2 60000
redis-cli  --eval unlock.lua lo3 , 2
```
