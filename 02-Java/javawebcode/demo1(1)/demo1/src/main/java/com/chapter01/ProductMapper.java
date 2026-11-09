package com.chapter01;

import com.entity.Product;

import java.util.List;

public interface ProductMapper {

    List<Product> findAll();

    Product findById(Integer id);

    int addProduct(Product product);

    int updateProduct(Product product);

    int deleteProduct(Integer id);

    List<Product> findByNameLike(String name);
}