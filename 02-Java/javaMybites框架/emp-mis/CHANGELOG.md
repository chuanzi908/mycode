# 更新记录

## v0.6
- 补充 README 的项目结构与常见问题排查表
- 新增 .editorconfig / .gitattributes，统一编码与换行
- 新增接口文档与更新记录
- 补充建库脚本的字段说明

## v0.5
- 新增登录拦截器 LoginInterceptor，未登录访问受保护接口返回 401
- 新增 AOP 操作日志 WebLogAspect
- 新增全局异常处理 GlobalExceptionHandler 与自定义 BusinessException

## v0.4
- 新增 EmpController，提供员工 CRUD 与分页接口
- 新增 AuthController 与统一返回结构 Result

## v0.3
- 新增 Emp 实体、EmpQueryDTO、EmpMapper 与 Service 层
- 实现分页与多条件查询

## v0.2
- 配置 Druid 数据源与 MyBatis-Plus 分页插件
- 新增 jdbc.properties

## v0.1
- 初始化 Maven war 工程，建立包结构
- 新增建库脚本 sql/init.sql
