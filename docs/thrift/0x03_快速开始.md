# 快速开始

## 编写 user.thrift

```
namespace java com.muyids
struct User {
    1:i32 id
    2:string name
    3:i32 age=0
}

service UserService {
    User getById(1:i32 id)
    bool isExist(1:string name)
}
```

## 通过编译器编译 user.thrift，生成 java 类接口文件

```
thrift -gen java user.thrift
```

不指定 生成目录，默认会生成在 gen-java 目录下

## Client 端代码编写

```java
public class SimpleClient {
    public static void main(String[] args) {

        try {
            TTransport transport;
            transport = new TSocket("localhost", 9099);
            transport.open();
            TProtocol protocol = new TBinaryProtocol(transport);
            UserService.Client client = new UserService.Client(protocol);
            User user = client.getById(1);
            System.out.println(user.toString());
            transport.close();
        } catch (TException x) {
            x.printStackTrace();
        }
    }
}
```

## Server 端代码编写

### Service 实现

```java
public class UserServiceImpl implements UserService.Iface {
    @Override
    public User getById(int id) throws TException {
        System.out.println("调用 getById ====");
        User user = new User();
        user.setId(id);
        user.setName("dw");
        user.setAge(10);
        return user;
    }

    @Override
    public boolean isExist(String name) throws TException {
        return false;
    }
}
```

## Server 实现

```java
public class SimpleService {
    public static void main(String[] args) {
        try {
            TServerTransport transport = new TServerSocket(9099);

            TServer.Args serverArgs = new TServer.Args(transport)
                    //
                    .processor(new UserService.Processor<>(new UserServiceImpl()))
                    // 二进制协议
                    .protocolFactory(new TBinaryProtocol.Factory());

            TServer server = new TSimpleServer(serverArgs);
            System.out.println("Starting the simple server...");
            server.serve();
        } catch (TTransportException e) {
            e.printStackTrace();
        }
    }
}
```
