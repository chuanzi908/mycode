package com.chapter01;

import com.entity.CustomerProduct;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface CustomerProductMapper {

    List<CustomerProduct> findAll();

    List<CustomerProduct> findByCustomerId(@Param("customerId") Integer customerId);

    List<CustomerProduct> findByProductId(@Param("productId") Integer productId);

    int addCustomerProduct(CustomerProduct customerProduct);

    int updateQuantity(CustomerProduct customerProduct);

    int deleteById(Integer id);

    int deleteByCustomerId(@Param("customerId") Integer customerId);
}