# maven

Maven 是一种 Java 项目管理工具，它可以自动化构建、测试、打包和部署 Java 应用程序。

## 安装

首先，您需要下载并安装 Maven。您可以从 Maven 官网（https://maven.apache.org/）下载Maven，根据您的操作系统选择适当的版本。

1、下载解压

1、配置环境变量

- 添加 MAVEN_HOME

- 添加 PATH

## 学习 Maven 基本概念

学习 Maven 的基本概念是学习 Maven 的第一步。您需要了解 Maven 的核心概念，如 Maven 坐标、POM 文件、依赖关系、生命周期和插件等。

### POM 文件

项目对象模型（Project Object Model，POM）

Maven 使用 POM 文件来描述项目的基本信息和依赖关系，包括项目名称、版本、作者、构建方式、依赖库等。

### Maven 坐标（Coordinates）

Maven 使用坐标来唯一标识一个项目或依赖库，坐标包括 groupId、artifactId 和 version 三个部分。其中，groupId 表示项目或依赖库所属的组织或公司，artifactId 表示项目或依赖库的名称，version 表示项目或依赖库的版本号。

### 依赖管理

依赖管理（Dependency Management）：Maven 通过依赖管理机制来管理项目的依赖库，以确保项目能够正确地编译、运行和测试。依赖管理机制包括依赖库的引入、冲突解决、版本控制等。

### 仓库（Repository）

Maven 使用仓库来管理项目的依赖库和插件库。Maven 仓库分为本地仓库和远程仓库两种，本地仓库存储项目本地使用的依赖库和插件库，远程仓库存储其他开发者或组织共享的依赖库和插件库。

### 生命周期

Maven 的构建过程被分为三个生命周期，分别是 clean、default 和 site。每个生命周期包含一系列的构建阶段，每个阶段对应一个或多个插件的执行。

### 插件

Maven 通过插件来实现各种构建任务，插件通常是由 Maven 社区或第三方开发者提供的。插件的配置包括插件的 groupId、artifactId 和 version 等信息，以及插件的具体执行方式和参数配置。

### profiles

profiles 可以让你基于不同的环境来对你的项目进行不同的配置，可以指定不同的插件，配置不同的依赖等等。

## 编写简单的 Maven 项目

一旦您了解了 Maven 的基本概念，您可以尝试编写一个简单的 Maven 项目。在编写项目之前，您需要创建一个 Maven 项目结构，并编写 POM 文件。POM 文件是 Maven 项目的核心配置文件，它包含了项目的基本信息、依赖关系和构建配置等。

## 理解 Maven 生命周期和插件

Maven 生命周期定义了 Maven 构建过程的不同阶段，每个阶段都与特定的构建目标相关联。Maven 插件是在构建过程中执行特定任务的工具。学习 Maven 生命周期和插件可以帮助您更好地理解 Maven 构建过程。

## 学习 Maven 高级特性

学习了 Maven 的基本概念和构建过程后，您可以深入学习 Maven 的高级特性，如 Maven 聚合、多模块项目、Maven 仓库管理和 Maven 配置文件等。

## 练习 Maven 项目

最后，您可以通过练习 Maven 项目来巩固所学的知识。尝试编写不同类型的 Maven 项目，并使用不同的 Maven 插件和配置。

## 使用 maven 管理 SpringBoot 项目

### 项目启动

```
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

### 依赖 Dependency

#### 查看依赖

```

# 查看依赖树
mvn dependency:tree
# 扁平
mvn dependency:list
```

#### 安装依赖

```
mvn clean compile
```

```
mvn install
```
