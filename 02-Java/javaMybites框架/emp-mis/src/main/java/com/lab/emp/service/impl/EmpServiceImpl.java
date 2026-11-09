package com.lab.emp.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.lab.emp.dto.EmpQueryDTO;
import com.lab.emp.entity.Emp;
import com.lab.emp.mapper.EmpMapper;
import com.lab.emp.service.EmpService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class EmpServiceImpl extends ServiceImpl<EmpMapper, Emp> implements EmpService {

    @Override
    public Page<Emp> pageQuery(int page, int size, EmpQueryDTO query) {
        LambdaQueryWrapper<Emp> wrapper = new LambdaQueryWrapper<>();
        wrapper.like(StringUtils.isNotBlank(query.getName()), Emp::getEmpName, query.getName());
        wrapper.eq(StringUtils.isNotBlank(query.getGender()), Emp::getGender, query.getGender());
        wrapper.eq(StringUtils.isNotBlank(query.getDept()), Emp::getDept, query.getDept());
        wrapper.orderByDesc(Emp::getEmpId);
        return this.page(new Page<>(page, size), wrapper);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void saveWithTx(Emp emp) {
        this.save(emp);
        int i = 1 / 0;   // 制造运行时异常，验证事务回滚
    }
}
