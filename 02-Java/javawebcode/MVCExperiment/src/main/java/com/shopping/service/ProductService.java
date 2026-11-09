package com.shopping.service;

import com.shopping.dao.ProductDao;
import com.shopping.entity.Product;

import java.sql.SQLException;
import java.util.List;

public class ProductService {
    private ProductDao productDao = new ProductDao();

    public List<Product> findAll() {
        try {
            return productDao.findAll();
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public Product findById(Integer id) {
        try {
            return productDao.findById(id);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }
}
