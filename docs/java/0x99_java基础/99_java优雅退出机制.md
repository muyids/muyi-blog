通过信号量

```java
/**
 * 优雅退出
 */
@Slf4j
public class SignalHandlerDemo {
    public static void main(String[] args) {

        // 注册要监听的信号
        RegSignalHandlerImpl signalHandlerImp = new RegSignalHandlerImpl();
        Signal.handle(new Signal("INT"), signalHandlerImp);
        Signal.handle(new Signal("TERM"), signalHandlerImp);
        Signal.handle(new Signal("USR2"), signalHandlerImp);

        try {
            TimeUnit.SECONDS.sleep(Integer.MAX_VALUE);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        log.info("退出程序");
    }
    static class RegSignalHandlerImpl implements SignalHandler {

        @Override
        public void handle(Signal sig) {
            log.info("SignalHandler.handle() => {}:{}", sig.getName(), sig.getNumber());

            // 可以在SignalHandler中动态添加addShutdownHook方法
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                log.info("Runtime.getRuntime().addShutdownHook() => start");
                try {
                    // 模拟应用进程退出前的处理操作
                    TimeUnit.SECONDS.sleep(10);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                log.info("Runtime.getRuntime().addShutdownHook() => ended");
            }));
            Runtime.getRuntime().exit(0);
        }
    }
}
```
