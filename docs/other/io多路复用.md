## BIO

B 就是 blocking 的意思，“阻塞”，

作为服务端开发的话，我们使用 ServerSocket 绑定完端口号之后，我们会监听该端口，等待 accpet 时间，accept 会阻塞当前线程；当收到 accept 事件时，程序拿到一个客户端与服务端连接的 socket；针对这个 socket 我们可以进行读写，但是呢，这个 socket 的读写方法是会阻塞当前线程的。

一般会使用多线程的方式来进行 c/s 交互，但是这样很难做到 C10K。因为 1W 客户端需要服务端 1W 个线程去支持，这样的话且不说 cpu 肯定就会爆炸了，然后线程上下文切换，也会把机器负载给拉飞的。

## NIO

NIO 是怎么解决 C10K 的问题的呀

答：站在 java 的角度看，NIO 包给我们提供了一套非阻塞的接口，这样就不需要我们为每一个 c/s 长连接保留一个单独的处理线程了。NIO API 具备非阻塞特性，可以用 1 个线程去检查 n 个 socket。在 java 代码层面，nio 包给我们提供了一个选择器 selector，然后，我们需要把检查的 socket 注册到这个 selector 中，然后主线程阻塞在 selector#select 方法里头。

然后，当选择器发现某个 socket 就绪了，就会唤醒主线程，然后咱们可以通过 selector 获取到就绪状态的 socket 进行相应的处理

---

站在 java 层面去聊 NIO 没有多大意义， selector 底层是 java 包装的这个 native api，再底层的实现，是 jvm 虚拟机去使用的系统调用 systemCall kernel 去实现的，下面聊一下底层 io 多路复用的实现吧

## 1.操作系统 kernel 提供的 select(..)函数

实现原理：

我们每次调用 kernel#select 函数，都会涉及到 用户态/内核态 的切换；还需要传递 需要检查的 socket 集合，其实就是需要检查的 fd(ps:文件描述符)；

操作系统这个 select 函数被调用以后，首先会按照 fd 集合去检查内存中的 socket 套接字状态，这个复杂度是 O(N)的，然后检查完一遍后，如果有就绪状态的 socket，那么直接返回，不会阻塞当前调用线程；否则，说明当前 fd 集合对应的 socket 没有就绪状态的，那么就需要阻塞当前调用线程了，直到某个 socket 有数据之后，才唤醒线程。

Q：select(..)函数去监听 socket 的时候，socket 数量有没有限制呢？

A: 默认最大可以监听 1024 个 socket

Q: 为啥是 1024 呢

A: 因为 fd_set 是一个 bitmap 位图结构

fd_set 使用数组实现
1.fd_size 有限制 1024 bitmap
fd[i] = accept()
2.fdset 不可重用，新的 fd 进来，重新创建 3.用户态和内核态拷贝产生开销
4.O(n)时间复杂度的轮询
成功调用返回结果大于 0，出错返回结果为 -1，超时返回结果为 0
具有超时时间

## poll 函数

使用数组结构

## epoll 函数

为了解决 select 和 poll 的缺陷

1. 缺陷 1：这两个系统函数每次调用都需要我们提供给他所有的需要监听的 socket 文件描述符集合

   程序的主线程是死循环调用 select/poll 函数的，这里面涉及到用户空间数据到内核空间拷贝的过程

   需要监听的 socket 集合，数据变化非常小，可能每次也就 1~2 个 socket_fd 需要更改，但是没办法，因为 select 和 poll 只是很单纯的函数，在 kernel 层面不会保留任何数据信息，所以说只能每次调用都进行数据拷贝了，这是第一个缺陷

2. 缺陷 2：select 和 poll 函数的返回值是 int 整型值，只能代表有几个 socket 就绪或是有错误了

   没办法表示出具体是哪些 socket 就绪了，导致了程序被唤醒以后，需要新一轮系统调用去检查哪些个 socket 是就绪的

eventpoll 对象

socket_fd 列表

就绪的 socket 信息

两个函数：

epoll_ctl(..)

epoll_wait

---

## select

fd_set 使用数组实现
1.fd_size 有限制 1024 bitmap
fd[i] = accept()
2.fdset 不可重用，新的 fd 进来，重新创建 3.用户态和内核态拷贝产生开销
4.O(n)时间复杂度的轮询
成功调用返回结果大于 0，出错返回结果为 -1，超时返回结果为 0
具有超时时间

## poll

基于结构体存储 fd
struct pollfd{
int fd;
short events;
short revents; //可重用
}
解决了 select 的 1,2 两点缺点

## epoll

解决 select 的 1，2，3，4
不需要轮询，时间复杂度为 O(1)
epoll_create 创建一个白板 存放 fd_events
epoll_ctl 用于向内核注册新的描述符或者是改变某个文件描述符的状态。已注册的描述符在内核中会被维护在一棵红黑树上
epoll_wait 通过回调函数内核会将 I/O 准备好的描述符加入到一个链表中管理，进程调用 epoll_wait() 便可以得到事件完成的描述符

## 两种触发模式：

LT:水平触发
当 epoll_wait() 检测到描述符事件到达时，将此事件通知进程，进程可以不立即处理该事件，下次调用 epoll_wait() 会再次通知进程。是默认的一种模式，并且同时支持 Blocking 和 No-Blocking。
ET:边缘触发
和 LT 模式不同的是，通知之后进程必须立即处理事件。
下次再调用 epoll_wait() 时不会再得到事件到达的通知。很大程度上减少了 epoll 事件被重复触发的次数，
因此效率要比 LT 模式高。只支持 No-Blocking，以避免由于一个文件句柄的阻塞读/阻塞写操作把处理多个文件描述符的任务饿死。
