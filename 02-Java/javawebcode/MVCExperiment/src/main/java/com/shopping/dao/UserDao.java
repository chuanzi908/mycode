package com.shopping.dao;

import com.shopping.entity.User;
import com.shopping.util.DBUtil;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;

import java.sql.SQLException;

public class UserDao {
    private QueryRunner queryRunner = new QueryRunner(DBUtil.getDataSource());

    public User login(String username, String password) throws SQLException {
        String sql = "SELECT * FROM user WHERE username = ? AND password = ?";
        return queryRunner.query(sql, new BeanHandler<>(User.class), username, password);
    }

    public void register(User user) throws SQLException {
        String sql = "INSERT INTO user(username, password, email) VALUES(?, ?, ?)";
        queryRunner.update(sql, user.getUsername(), user.getPassword(), user.getEmail());
    }
    
    public User findByUsername(String username) throws SQLException {
        String sql = "SELECT * FROM user WHERE username = ?";
        return queryRunner.query(sql, new BeanHandler<>(User.class), username);
    }
    
    public User findById(Integer id) throws SQLException {
        String sql = "SELECT * FROM user WHERE id = ?";
        return queryRunner.query(sql, new BeanHandler<>(User.class), id);
    }
    
    public int update(User user) throws SQLException {
        String sql = "UPDATE user SET email = ?, password = ? WHERE id = ?";
        return queryRunner.update(sql, user.getEmail(), user.getPassword(), user.getId());
    }
}
