package com.chapter01;

import com.entity.EmpCustomer;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EmpCustomerMapper {

    List<EmpCustomer> findAll();

    List<EmpCustomer> findByEmpId(@Param("empId") Integer empId);

    List<EmpCustomer> findByCustomerId(@Param("customerId") Integer customerId);

    int addEmpCustomer(EmpCustomer empCustomer);

    int deleteById(Integer id);

    int deleteByEmpId(@Param("empId") Integer empId);

    int deleteByCustomerId(@Param("customerId") Integer customerId);
}