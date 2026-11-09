# emp-mis（实验二：SSM 整合 + EMP 员工管理 MIS）

## 技术栈
Spring 5.3.31 + SpringMVC + MyBatis-Plus 3.5.3.1 + Druid + MySQL 8 + Tomcat 9 + JDK 8

## 启动步骤
1. 执行 `sql/init.sql` 建库建表
2. 修改 `src/main/resources/jdbc.properties` 里的账号密码
3. IDEA 中配置 Tomcat 9，部署 `emp-mis:war exploded`
4. 先调 `POST /auth/login`（body: {"username":"admin","password":"123456"}）建立会话
5. 再调 `/emps` 下的接口

## 接口
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | /auth/login | 登录，写 session |
| POST | /auth/logout | 注销 |
| POST | /emps | 新增 |
| PUT | /emps | 修改 |
| DELETE | /emps/{id} | 删除单条 |
| DELETE | /emps | 批量删除（body 为 id 数组） |
| GET | /emps/{id} | 单条查询 |
| GET | /emps?page=1&size=5&name=&gender=&dept= | 分页 + 多条件 |
| POST | /emps/tx-demo | 事务回滚演示 |

## 注意事项
- 必须用 Tomcat 9，Tomcat 10 是 jakarta 命名空间，会报 ClassNotFoundException: javax.servlet.Filter
- 分页插件已在 SpringConfig 中注册，控制台能看到 LIMIT 语句

## 项目结构
```
src/main/java/com/lab/emp
├── config/        SpringConfig、SpringMvcConfig、ServletContainersInitConfig
├── controller/    EmpController、AuthController、SystemController
├── service/       EmpService 及其实现
├── mapper/        EmpMapper（继承 BaseMapper）
├── entity/        Emp
├── dto/           EmpQueryDTO
├── common/        Result、BusinessException、GlobalExceptionHandler
├── interceptor/   LoginInterceptor
└── aspect/        WebLogAspect（AOP 操作日志）
```

## 常见问题
| 现象 | 原因与处理 |
|---|---|
| 启动报 Communications link failure | MySQL 未启动，或端口与 jdbc.properties 不一致（本机为 3307） |
| 启动报 Access denied | jdbc.properties 中的密码不正确 |
| 接口返回 401 未登录 | 未先调用 /auth/login，或修改配置后未重启 Tomcat |
| 分页不生效、控制台无 LIMIT | 检查 SpringConfig 中是否注册了 MybatisPlusInterceptor |
