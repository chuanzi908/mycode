package com.house.dao;

import com.house.entity.User;
import com.house.util.DruidUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class UserDao {
    public User login(String username, String password) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        User user = null;
        String sql = "select * from user where username=? and password=?";

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, username);
            pstmt.setString(2, password);
            rs = pstmt.executeQuery();
            if (rs.next()) {
                user = new User();
                user.setId(rs.getInt("id"));
                user.setUsername(rs.getString("username"));
                user.setRole(rs.getInt("role"));
                user.setRealName(rs.getString("real_name"));
                user.setPhone(rs.getString("phone"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt, rs);
        }
        return user;
    }
}