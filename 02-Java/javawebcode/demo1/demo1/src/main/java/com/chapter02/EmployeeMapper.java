package com.chapter02;

import com.entity.Employee;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

public interface EmployeeMapper {

    @Select("SELECT * FROM employee WHERE id = #{id}")
    Employee findById(@Param("id") Integer id);

    @Select("SELECT * FROM employee")
    List<Employee> findAll();

    @Select("SELECT * FROM employee WHERE name LIKE CONCAT('%', #{name}, '%')")
    List<Employee> findByNameLike(@Param("name") String name);

    @Select("SELECT * FROM employee WHERE department = #{department}")
    List<Employee> findByDepartment(@Param("department") String department);

    @Insert("INSERT INTO employee(name, department, salary, hire_date) VALUES(#{name}, #{department}, #{salary}, #{hire_date})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Employee employee);

    @Update("UPDATE employee SET name = #{name}, department = #{department}, salary = #{salary}, hire_date = #{hire_date} WHERE id = #{id}")
    int update(Employee employee);

    @Delete("DELETE FROM employee WHERE id = #{id}")
    int deleteById(@Param("id") Integer id);
}