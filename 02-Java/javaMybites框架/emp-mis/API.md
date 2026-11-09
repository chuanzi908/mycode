# emp-mis 接口文档

所有接口返回统一结构：

```json
{ "code": 200, "message": "success", "data": null }
```

code 约定：200 成功；400 参数或业务校验失败；401 未登录；500 服务器异常。

## 认证
### POST /auth/login
请求：```json {"username":"admin","password":"123456"} ```
响应：```json {"code":200,"message":"success","data":{"username":"admin"}} ```

### POST /auth/logout
清空 session，返回 200。

## 员工管理（除登录外均需先登录）

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | /emps | 新增员工 |
| PUT | /emps | 修改员工 |
| DELETE | /emps/{id} | 删除单条 |
| DELETE | /emps | 批量删除，body 为 id 数组 |
| GET | /emps/{id} | 单条查询 |
| GET | /emps | 分页 + 多条件 |

### POST /emps 新增
```json
{"empName":"张三","gender":"男","dept":"研发部","post":"后端工程师",
 "salary":12000,"hireDate":"2026-03-01","status":1}
```

### GET /emps 分页
参数：page（默认 1）、size（默认 10）、name、gender、dept，均可为空。

返回 `data` 为 MyBatis-Plus 的 Page 对象，包含 records、total、size、current、pages。

## 其它
- GET /hello、GET /hello.json：整合验证接口，不受登录拦截器约束
- POST /emps/tx-demo：事务回滚演示
