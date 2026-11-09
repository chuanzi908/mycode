package com.lab.emp.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.emp.common.Result;
import com.lab.emp.dto.EmpQueryDTO;
import com.lab.emp.entity.Emp;
import com.lab.emp.service.EmpService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

/**
 * 员工管理 RESTful 接口。
 */
@RestController
@RequestMapping("/emps")
public class EmpController {

    @Autowired
    private EmpService empService;

    /** 新增 */
    @PostMapping
    public Result<Void> add(@RequestBody @Valid Emp emp) {
        empService.save(emp);
        return Result.ok(null);
    }

    /** 修改 */
    @PutMapping
    public Result<Void> update(@RequestBody @Valid Emp emp) {
        empService.updateById(emp);
        return Result.ok(null);
    }

    /** 删除单条 */
    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Integer id) {
        empService.removeById(id);
        return Result.ok(null);
    }

    /** 批量删除 */
    @DeleteMapping
    public Result<Void> deleteBatch(@RequestBody List<Integer> ids) {
        if (ids == null || ids.isEmpty()) {
            return Result.fail("请选择要删除的记录");
        }
        empService.removeByIds(ids);
        return Result.ok(null);
    }

    /** 单条查询 */
    @GetMapping("/{id}")
    public Result<Emp> getById(@PathVariable Integer id) {
        return Result.ok(empService.getById(id));
    }

    /** 分页 + 多条件 */
    @GetMapping
    public Result<Page<Emp>> page(@RequestParam(defaultValue = "1") int page,
                                  @RequestParam(defaultValue = "5") int size,
                                  EmpQueryDTO query) {
        return Result.ok(empService.pageQuery(page, size, query));
    }

    /** 事务演示：故意抛异常，观察数据是否回滚 */
    @PostMapping("/tx-demo")
    public Result<Void> txDemo(@RequestBody Emp emp) {
        empService.saveWithTx(emp);
        return Result.ok(null);
    }
}
