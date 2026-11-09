# 项目长期记忆 — MyBatis JavaWeb demo1

## 技术栈
- Maven war 项目，Java 17，MyBatis 3.5.13，mysql-connector-j 8.0.33，JUnit 5.13.2，内嵌 Tomcat 10.1.34。
- 源码根：`C:\Users\35111\Desktop\java\javawebcode\demo1\demo1`。

## 数据库（关键，容易踩坑）
- MySQL 8.0.44 运行在 **127.0.0.1:3307**（**不是 3306**），账号 `root` / `123456`。
- 连接库名在配置里写作 `USER`（实际库名 `user`，Windows 下大小写不敏感）。
- `mybatis-config.xml` 与 `common/db.properties` 的 url 端口必须用 **3307**。
- 建表脚本：`sql/product_employee_db.sql`；执行时务必加 `--default-character-set=utf8mb4`，否则中文报 1366。
- product / employee 两表已建在 `user` 库（各 10 条数据）。

## 代码结构约定
- chapter01：User（user 表，XML + 注解混合），是旧示例。
- chapter02：Product（XML，`ProductMapper` + `ProductMapper.xml`）与 Patient/Employee（注解）等。
- 六方法标准实现（非 user 表，用 product）：
  - XML：`com.chapter02.ProductMapper` + `resources/com/chapter02/ProductMapper.xml`
  - 注解：`com.chapter02.ProductMapperAnnotation`
  - 六方法 = findAll / findById / insert(自增主键回填) / update / deleteById / findByKeyword(模糊)
  - 可运行入口：`com.chapter02.ProductDemo.main`
- 新增 Mapper 必须注册进 `mybatis-config.xml` 的 `<mappers>`：有 XML 用 `<mapper resource=...>`，纯注解用 `<mapper class=...>`。

## 本机构建/运行环境备忘
- 终端无 java/mvn；用 IntelliJ 自带 JBR：`C:/Program Files/JetBrains/IntelliJ IDEA 2026.2.2/jbr`。
- Maven 用 `~/.m2/wrapper/dists/.../apache-maven-3.9.6`，直接调 plexus-classworlds Launcher 可绕过 shell 脚本路径问题。
- MySQL 客户端：`C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe`。
