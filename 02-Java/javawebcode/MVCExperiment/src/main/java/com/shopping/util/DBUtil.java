package com.shopping.util;

import com.alibaba.druid.pool.DruidDataSource;
import javax.sql.DataSource;
import java.io.InputStream;
import java.sql.*;
import java.util.Properties;

public class DBUtil {
    private static DruidDataSource dataSource;

    static {
        try {
            Properties properties = new Properties();
            InputStream is = DBUtil.class.getClassLoader().getResourceAsStream("druid.properties");
            properties.load(is);

            dataSource = new DruidDataSource();
            dataSource.setDriverClassName(properties.getProperty("driverClassName"));
            dataSource.setUrl(properties.getProperty("url"));
            dataSource.setUsername(properties.getProperty("username"));
            dataSource.setPassword(properties.getProperty("password"));
            dataSource.setInitialSize(Integer.parseInt(properties.getProperty("initialSize")));
            dataSource.setMaxActive(Integer.parseInt(properties.getProperty("maxActive")));
            dataSource.setMaxWait(Long.parseLong(properties.getProperty("maxWait")));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static DataSource getDataSource() {
        return dataSource;
    }

    public static Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }

    public static void close(Statement stmt, Connection conn) {
        close(null, stmt, conn);
    }

    public static void close(ResultSet rs, Statement stmt, Connection conn) {
        try {
            if (rs != null) rs.close();
            if (stmt != null) stmt.close();
            if (conn != null) conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
