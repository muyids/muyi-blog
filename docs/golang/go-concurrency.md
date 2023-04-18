---
title: Go的并发编程
date: 2019-09-07T04:53:00+08:00
draft: false
categories: [Golang]
tags: [Golang]
---

Go 语言实现了`CSP（通信顺序进程）模型`来作为`goroutine`间的推荐通信方式

<!--more-->

## 并发和并行

- 并发：同一时间内执行多个任务
- 并行：同一**时刻**执行多个任务
  Go 语言的并发通过 goroutine 实现。goroutine 类似于线程，属于用户态的线程。操作系统的线程属于内核级的线程。

我们可以根据需要创建成千上万个 goroutine 并发工作。

## golang 的 CSP 并发模型

CSP（Communicating Sequential Process）并发模型，中文可以叫做**通信顺序进程**

CSP 模型由并发执行的实体（线程或者进程）所组成，实体之间通过发送消息进行通信，
这里发送消息时使用的就是通道，或者叫 channel
请记住下面这句话：
Do not communicate by sharing memory; instead, share memory by communicating.
**不要以共享内存的方式来通信，相反，要通过通信来共享内存。**

普通的线程并发模型，就是像 Java、C++、或者 Python，他们线程间通信都是通过共享内存的方式来进行的。

非常典型的方式就是，在访问共享数据（例如数组、Map、或者某个结构体或对象）的时候，通过锁来访问，
因此，在很多时候，衍生出一种方便操作的数据结构，叫做**线程安全的数据结构**
例如 Java 提供的包”java.util.concurrent”中的数据结构。Go 中也实现了传统的线程并发模型。

Go 的 CSP 并发模型，是通过**goroutine 和 channel**来实现的。

goroutine 是 Go 语言中并发的执行单位。
channel 是 Go 语言中各个并发结构体(goroutine)之前的通信机制。
通俗的讲，就是各个 goroutine 之间通信的”管道“，有点类似于 Linux 中的管道。

## goroutine

go 语言中使用 goroutine 非常简单，只需要在函数前面加上 go 关键字

```
var wg sync.WaitGroup
func say(s string, i int) {
	fmt.Println(s, i)
	wg.Done()
}
func main() {
	for i := 0; i < 1000; i++ {
		wg.Add(1)
		//go say("hello", i)
		go func(i int) {
			fmt.Println(i)
			wg.Done()
		}(i)
	}

	wg.Wait()
}
```

**可增长的栈**

OS 线程（操作系统线程）一般都有固定的栈空间（通常为 2MB）

goroutine 初始状态为 2kb, 可以增长到 1G

`runtime.GOMAXPROCS(4)` // 设置用几个 cpu 运行代码

## channel

go 的并发模型是 CSP（Communicating Sequential Processes），提倡**通过通信共享内存，而不是通过共享内存而实现通信**

goroutine 是 go 程序并发的执行体，channel 是他们之间的连接

channel 是可以让一个 goroutine 发送特定值到另一个 goroutine 的通信机制

```
var ch1 chan int // 声明一个传递整型的通道
ch1 = make(chan int, 1)
ch1 <- 10 // 发送
x := <-ch1 // 接收
close(ch1) // 关闭通道
```

```
ch1 = make(chan int, 1) // 带缓冲区通道
ch2 = make(chan int) // 无缓冲区通道，又称为同步通道
```

## goroutine + channel 协同工作

```
func producer(ch chan int) {
	for i := 0; i < 100; i++ {
		ch <- i
	}
	close(ch)
}

func consumer(ch1 chan int, ch2 chan int) {
	// 从通道中取值的方式1
	for {
		value, ok := <-ch1
		if !ok {
			break
		}
		ch2 <- value * value
	}
	close(ch2)
}

func main() {
	ch1 := make(chan int, 100)
	ch2 := make(chan int, 100)
	go producer(ch1)
	go consumer(ch1, ch2)

	// 从通道中取值的方式2
	for ret := range ch2 {
		fmt.Println(ret)
	}
}
```

**select 多路复用**

```
select {
	case <-ch1:
		break
	case <-ch2:
		break
	default:
        // 默认操作
}
```
