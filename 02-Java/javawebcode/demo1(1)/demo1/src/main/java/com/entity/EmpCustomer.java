package com.entity;

import java.util.Date;

public class EmpCustomer {
    private Integer id;
    private Integer empId;
    private Integer customerId;
    private Date createdAt;

    private Emp emp;
    private Customer customer;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public Integer getEmpId() { return empId; }
    public void setEmpId(Integer empId) { this.empId = empId; }

    public Integer getCustomerId() { return customerId; }
    public void setCustomerId(Integer customerId) { this.customerId = customerId; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Emp getEmp() { return emp; }
    public void setEmp(Emp emp) { this.emp = emp; }

    public Customer getCustomer() { return customer; }
    public void setCustomer(Customer customer) { this.customer = customer; }

    @Override
    public String toString() {
        return "EmpCustomer{" +
                "id=" + id +
                ", empId=" + empId +
                ", customerId=" + customerId +
                ", createdAt=" + createdAt +
                '}';
    }
}