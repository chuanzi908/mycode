package com.shopping.dao;

import com.shopping.entity.Product;
import com.shopping.util.DBUtil;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;

import java.sql.SQLException;
import java.util.List;

public class ProductDao {
    private QueryRunner queryRunner = new QueryRunner(DBUtil.getDataSource());

    public List<Product> findAll() throws SQLException {
        String sql = "SELECT * FROM product";
        return queryRunner.query(sql, new BeanListHandler<>(Product.class));
    }

    public Product findById(Integer id) throws SQLException {
        String sql = "SELECT * FROM product WHERE id = ?";
        return queryRunner.query(sql, new BeanHandler<>(Product.class), id);
    }

    public void update(Product product) throws SQLException {
        String sql = "UPDATE product SET name = ?, description = ?, price = ?, stock = ? WHERE id = ?";
        queryRunner.update(sql, product.getName(), product.getDescription(),
                product.getPrice(), product.getStock(), product.getId());
    }
}
