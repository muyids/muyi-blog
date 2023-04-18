基于两次 RSA 加密的动态 Token 解决方案

1：在登录页客户端向服务端发出 getSPK 请求，传递 did，由客户端生成，web 使用指纹 id，app 使用设备 id

2：服务端收到后，使用 RSA 算法生成一对密匙，长度是 1024 位，服务端公匙 SPK 和服务端私匙 SSK。
同时生成服务端 10 位时间戳一起发给客户端；
把 SSK 保留在服务端，以 did 为 key,SSK 做为值存储在 redis 的 set 中，过期时间为 10 分钟

## 发送验证码

3：客户端把 SPK 存入本地（如果本地有就更新），客户端使用 RSA 算法生成密钥（客户端公匙 CPK 和客户端私匙 CSK）把 CSK 保存本地变量中

4：构造签名：把(设备 id，手机号，服务端时间戳)进行字符串拼接后按字母排序，再使用 sha1 算法得到签名 sign

5：数据加密：把(手机号，时间戳，sign)进行字符串拼接后按字母排序，再使用 SPK 进行加密，得到加密 data，连同 CPK,did 一起发送给服务端

6：服务端收到 data 后，用 did 查询到私匙 SSK 进行解密；得到客户端 sign，手机号，时间戳。然后用服务器时间和解密出来的时间戳比较，差值大于 10 分钟，返回错

7：把(设备 id，手机号，服务端时间戳)进行字符串拼接后按字母排序，再使用 sha1 算法得到签名 sign-1，和 sign 比较是否相等，然后调用短信服务（传送手机号来发送验证码）

8：把验证码，设备 id，CPK，以及验证码头码更新进以 did 为 key 的缓存中，返回用 CPK 对（生成的验证码头码）加密 head_code

9：客户端把返回的验证码头码保存在本地变量中

## 手机验证码登录

10：构造签名：客户端使用 CSK 解密 head_code，连同输入验证码，设备 id，手机号，服务端时间戳，进行字符串拼接排序后使用 sha1 算法得到 sign

11：数据加密：把手机号，验证码，head_code，时间戳，sign 进行字符串拼接排序后使用 SPK 进行加密得到 data，连同设备 id 一起发送给服务端

12：服务端用 did 查询到私匙 SSK，客户端的公匙 CPK，验证码，head_code，设备 id；然后用 SSK 进行解密 data 得到 sign，手机号，验证码，head_code，时间戳

13：比较签名：重复第 10 步 sha1 加密（验证码，head_code，设备 id，手机号，服务端时间戳），得到 sign-1，然后和 sign 比较

14：比较时间戳：然后用服务器时间和解密出来的时间戳比较，差值大于 10 分钟，返回错

15：比较设备 id：检查设备 id 是否与上次点获取验证码的是否相同

16：比较验证码头码

17：调用短信服务验证 code，不通过就返回错；通过后进行登录操作逻辑（全局映射目前 C 端，B 端用户体系），最终生成用户的 uid

18：把第 12 步中的用户自己的 CPK,SSK 一起保存，key 为用户 uid，并设置 token（120 分钟）与 refresh token（7 天） 的过期时间

19：服务端继续生成 token 和 refresh token，然后用 CPK 对 token 及 refresh token 进行加密，得到 sign-3，一起返回客户端

20：客户端把 token 和 refresh token，uid，CSK 保存在本地，使用的时候，用 CSK 解开，再用 SPK 加密，发送

## 登录状态中

10：客户端用本地私匙 CSK 对 token 解密，后用 SPK 对 token 进行再加密生成服务端可解析的 token，及用户 uid 一起发送到服务端
{uid:xxx,token:SPK(CSK(xxxx))}
11：服务端通过用户 uid 找到对应的 SSK，然后解密 token，验证是否过期，如果过期，返回客户端让其再用本地私匙 CSK 对 refresh token 进行解密后，
再用 SPK 加密生成服务端可以解密的 refresh token，调用/token/refresh 接口发送到服务端{uid:xxx,refresh_token:SPK(CSK(xxxx))}，
再次用 uid 对应的 SSK 解密并验证 refresh token，最后重新生成新的 token，再经过 CPK 加密后返回，客户端更新本地的 token。
反之 refresh token 也过期，提示客户端重新登录；如果在 token 没过期时调用了/token/refresh 时，把当前的 token 取出经过 CPK 加密后返回
