package com.house.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class DBUtil {
    // 适配你的数据库信息：端口3307，密码123456
    private static final String URL = "jdbc:mysql://localhost:3307/house_sale?useSSL=false&serverTimezone=Asia/Shanghai";
    private static final String USER = "root";
    private static final String PASSWORD = "123456";

    // 获取连接
    public static Connection getConnection() {
        Connection conn = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            conn = DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return conn;
    }

    // 释放资源
    public static void close(Connection conn, PreparedStatement pstmt, ResultSet rs) {
        try { if (rs != null) rs.close(); } catch (Exception e) { e.printStackTrace(); }
        try { if (pstmt != null) pstmt.close(); } catch (Exception e) { e.printStackTrace(); }
        try { if (conn != null) conn.close(); } catch (Exception e) { e.printStackTrace(); }
    }

    public static void close(Connection conn, PreparedStatement pstmt) {
        close(conn, pstmt, null);
    }
}