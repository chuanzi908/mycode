package com.chaperMybatisPlus.config;

import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.BlockAttackInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.OptimisticLockerInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;

/**
 * MyBatis-Plus 核心插件配置
 *
 * 本类只管 MybatisPlusInterceptor 链（InnerInterceptor）：
 *   ① PaginationInnerInterceptor      —— 分页（必加，否则 selectPage 不生效）
 *   ② BlockAttackInnerInterceptor     —— 防全表更新删除
 *   ③ OptimisticLockerInnerInterceptor —— 乐观锁（配合 @Version 注解）
 *
 * ⚠️ 注意：MetaObjectHandler（自动填充）不在这里注册！
 *   它不属于 InnerInterceptor，而是通过 GlobalConfigUtils.setGlobalConfig()
 *   挂在全局 GlobalConfig 上。详见 StudentTest.init() 中的写法。
 */
public class MybatisPlusConfig {

    public static MybatisPlusInterceptor buildInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        //分页插件：必加，否则 selectPage 不生效
        PaginationInnerInterceptor pagination = new PaginationInnerInterceptor(DbType.MYSQL);
        pagination.setMaxLimit(500L);
        interceptor.addInnerInterceptor(pagination);
//乐观锁插件
        interceptor.addInnerInterceptor(new BlockAttackInnerInterceptor()); // 防止全表更新删除

        // ============= 锁的概念与使用 =============
        //
        // 【为什么需要锁？】数据库并发更新会丢失修改：
        //   线程A 读取 row(version=1, score=90)
        //   线程B 读取 row(version=1, score=90)  ← A还没提交
        //   线程A UPDATE SET score=100 WHERE id=?   → 成功
        //   线程B UPDATE SET score=80  WHERE id=?   → 也成功！A的修改被覆盖 💀
        //
        // 【锁的两大流派对比】
        //
        //   ┌──────────────┬───────────────────────────┬──────────────────────┐
        //   │              │  悲观锁 Pessimistic Lock   │ 乐观锁 Optimistic Lock│
        //   ├──────────────┼───────────────────────────┼──────────────────────┤
        //   │ 核心思想     │ 先锁住再操作，冲突必发生   │ 先操作再校验，冲突少 │
        //   │ 数据库实现   │ SELECT ... FOR UPDATE     │ version 字段 + WHERE │
        //   │ MP 中对应    │ 手动加 FOR UPDATE        │ @Version + 本插件     │
        //   │ 并发吞吐     │ 低（锁等待）               │ 高（无锁）           │
        //   │ 适用场景     │ 写多、冲突频繁、资金操作   │ 读多写少、偶尔冲突   │
        //   └──────────────┴───────────────────────────┴──────────────────────┘
        //
        // 【乐观锁工作流程（本项目实际使用的方式）】
        //
        //   ① SELECT 读取数据时，拿到 version = 1
        //   ② 业务层修改对象（内存中）
        //   ③ UPDATE 时，OptimisticLockerInnerInterceptor 自动改写 SQL：
        //
        //        你写的：UPDATE student SET score=66 WHERE id=3
        //        插件改：UPDATE student SET score=66, version=version+1
        //                               WHERE id=3 AND version=1
        //
        //   ④ WHERE version=1 匹配到 → 更新成功，version 自动 +1
        //      匹配不到（被别人抢先改过了） → rows=0，业务层自行重试/报错
        //
        // 【本项目中的完整配置链】
        //
        //   DB 表： student 表必须有 version 列（INT，默认值 0）
        //   实体类：@Version  private Integer version;        ← 见 Student.java:70
        //   插件：  下一行 ↓
        //   业务层：updateById(student) 即可，无需手动管理 version
        //
        // 【冲突时怎么办？】rows=0 说明乐观锁冲突，典型处理方式：
        //
        //   // 方案一：简单重试（适合冲突极少的场景）
        //   for (int i = 0; i < 3; i++) {
        //       Student s = studentMapper.selectById(id);
        //       s.setScore(newScore);
        //       if (studentMapper.updateById(s) > 0) break;
        //   }
        //
        //   // 方案二：抛异常让上层决定（推荐）
        //   if (studentMapper.updateById(s) == 0) {
        //       throw new RuntimeException("数据已被他人修改，请刷新后重试");
        //   }
        //
        // 【悲观锁简单对比（本项目未启用，了解即可）】
        //   // 写法：加 FOR UPDATE 锁住行直到事务结束
        //   SELECT * FROM student WHERE id = 3 FOR UPDATE
        //   // 其他线程必须等你 COMMIT/ROLLBACK 后才能读这行
        //   // 代价：长事务 + 锁等待，吞吐量下降
        interceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());

        return interceptor;
    }
}