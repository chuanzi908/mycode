package com.exam.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

// JDBC连接工具
public class DBUtil {
    private static final String URL = "jdbc:mysql://localhost:3307/exam_system?useSSL=false&characterEncoding=utf8";
    private static final String USER = "root";
    private static final String PWD = "123456";

    // 获取连接
    public static Connection getConn() {
        Connection conn = null;
        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(URL, USER, PWD);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return conn;
    }

    // 关闭连接
    public static void close(Connection conn) {
        if (conn != null) {
            try {
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}