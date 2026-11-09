package com.servlet.demo1;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * 数据库工具类 - 获取数据库连接
 */
public class DBUtil {

    // 数据库配置信息
    private static final String URL = "jdbc:mysql://localhost:3307/exam_system?useSSL=false&serverTimezone=UTC&characterEncoding=utf-8";
    private static final String USERNAME = "root";
    private static final String PASSWORD = "123456";

    static {
        try {
            // 加载 MySQL 驱动
            Class.forName("com.mysql.cj.jdbc.Driver");
            System.out.println("[DEBUG] MySQL 驱动加载成功");
        } catch (ClassNotFoundException e) {
            System.err.println("[ERROR] MySQL 驱动加载失败！");
            System.err.println("[ERROR] 请检查 pom.xml 中 mysql-connector-java 依赖是否正确");
            e.printStackTrace();
        }
    }

    /**
     * 获取数据库连接
     */
    public static Connection getConnection() throws SQLException {
        try {
            System.out.println("[DEBUG] 开始连接数据库...");
            System.out.println("[DEBUG] URL: " + URL);
            System.out.println("[DEBUG] 用户名：" + USERNAME);
            
            Connection conn = DriverManager.getConnection(URL, USERNAME, PASSWORD);
            
            System.out.println("[DEBUG] ✓ 数据库连接成功！");
            return conn;
        } catch (SQLException e) {
            System.err.println("[ERROR] 数据库连接失败！");
            System.err.println("[ERROR] URL: " + URL);
            System.err.println("[ERROR] 用户名：" + USERNAME);
            System.err.println("[ERROR] 错误信息：" + e.getMessage());
            System.err.println("[ERROR] 可能原因：");
            System.err.println("[ERROR] 1. MySQL 服务未启动");
            System.err.println("[ERROR] 2. 数据库 exam_system 不存在");
            System.err.println("[ERROR] 3. 端口号错误（当前使用 3307）");
            System.err.println("[ERROR] 4. 密码错误");
            throw e;
        }
    }

    /**
     * 关闭数据库资源
     */
    public static void close(Connection connection, java.sql.Statement statement, java.sql.ResultSet resultSet) {
        try {
            if (resultSet != null) resultSet.close();
            if (statement != null) statement.close();
            if (connection != null) connection.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

