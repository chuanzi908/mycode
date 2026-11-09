package com.lab.emp.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.lab.emp.dto.EmpQueryDTO;
import com.lab.emp.entity.Emp;

/**
 * 员工业务接口。
 */
public interface EmpService extends IService<Emp> {

    /** 分页 + 多条件（姓名模糊、性别与部门精确匹配） */
    Page<Emp> pageQuery(int page, int size, EmpQueryDTO query);

    /** 演示事务：插入后抛出异常，用于验证回滚 */
    void saveWithTx(Emp emp);
}
