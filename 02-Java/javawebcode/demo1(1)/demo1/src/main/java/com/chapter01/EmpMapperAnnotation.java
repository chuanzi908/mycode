package com.chapter01;

import com.entity.Emp;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

public interface EmpMapperAnnotation {

    @Select("SELECT * FROM emp")
    List<Emp> findAll();

    @Select("SELECT * FROM emp WHERE id = #{id}")
    Emp findById(@Param("id") Integer id);

    @Insert("INSERT INTO emp(name, age, dept, salary, hire_date) VALUES(#{name}, #{age}, #{dept}, #{salary}, #{hireDate})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int addEmp(Emp emp);

    @Update("UPDATE emp SET name = #{name}, age = #{age}, dept = #{dept}, salary = #{salary}, hire_date = #{hireDate} WHERE id = #{id}")
    int updateEmp(Emp emp);

    @Delete("DELETE FROM emp WHERE id = #{id}")
    int deleteEmp(@Param("id") Integer id);

    @Select("SELECT * FROM emp WHERE name LIKE CONCAT('%', #{value}, '%')")
    List<Emp> findByNameLike(@Param("value") String name);
}