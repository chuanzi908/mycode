package com.chapter01;

import com.entity.Emp;

import java.util.List;

public interface EmpMapper {

    List<Emp> findAll();

    Emp findById(Integer id);

    int addEmp(Emp emp);

    int updateEmp(Emp emp);

    int deleteEmp(Integer id);

    List<Emp> findByNameLike(String name);
}