package com.entity;

import java.math.BigDecimal;
import java.util.Date;

public class Employee {
    private Integer id;
    private String name;
    private String department;
    private BigDecimal salary;
    private Date hire_date;
    private Date created_at;
    private Date updated_at;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }

    public BigDecimal getSalary() { return salary; }
    public void setSalary(BigDecimal salary) { this.salary = salary; }

    public Date getHire_date() { return hire_date; }
    public void setHire_date(Date hire_date) { this.hire_date = hire_date; }

    public Date getCreated_at() { return created_at; }
    public void setCreated_at(Date created_at) { this.created_at = created_at; }

    public Date getUpdated_at() { return updated_at; }
    public void setUpdated_at(Date updated_at) { this.updated_at = updated_at; }

    @Override
    public String toString() {
        return "Employee{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", department='" + department + '\'' +
                ", salary=" + salary +
                ", hire_date=" + hire_date +
                ", created_at=" + created_at +
                ", updated_at=" + updated_at +
                '}';
    }
}