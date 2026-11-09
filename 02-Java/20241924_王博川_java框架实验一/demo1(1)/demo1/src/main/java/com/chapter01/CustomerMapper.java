package com.chapter01;

import com.entity.Customer;

import java.util.List;

public interface CustomerMapper {

    List<Customer> findAll();

    Customer findById(Integer id);

    int addCustomer(Customer customer);

    int updateCustomer(Customer customer);

    int deleteCustomer(Integer id);

    List<Customer> findByNameLike(String name);
}