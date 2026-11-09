package com.house.listener;

import com.alibaba.druid.pool.DruidDataSource;
import com.house.util.DruidUtil;
import jakarta.servlet.ServletContextEvent;
import jakarta.servlet.ServletContextListener;
import jakarta.servlet.annotation.WebListener;

import java.sql.Connection;
import java.sql.SQLException;

@WebListener
public class AppListener implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        System.out.println("===========================================");
        System.out.println("房屋销售系统正在启动...");
        System.out.println("===========================================");
        
        try {
            Connection conn = DruidUtil.getConnection();
            if (conn != null && !conn.isClosed()) {
                System.out.println("✓ 数据库连接池初始化成功");
                System.out.println("✓ 数据库连接测试成功");
                conn.close();
            } else {
                System.err.println("✗ 数据库连接失败！");
            }
        } catch (SQLException e) {
            System.err.println("✗ 数据库连接测试失败: " + e.getMessage());
            e.printStackTrace();
        }
        
        sce.getServletContext().setAttribute("systemName", "房屋销售管理系统");
        sce.getServletContext().setAttribute("version", "1.0.0");
        
        System.out.println("✓ 系统上下文属性设置完成");
        System.out.println("===========================================");
        System.out.println("房屋销售系统启动完成！");
        System.out.println("===========================================");
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        System.out.println("===========================================");
        System.out.println("房屋销售系统正在关闭...");
        System.out.println("===========================================");
        
        try {
            DruidDataSource dataSource = (DruidDataSource) DruidUtil.getConnection().getMetaData().getConnection().getClass().cast(DruidDataSource.class);
            if (dataSource != null) {
                dataSource.close();
                System.out.println("✓ 数据库连接池已关闭");
            }
        } catch (Exception e) {
            System.err.println("✗ 关闭数据库连接池时出错: " + e.getMessage());
            e.printStackTrace();
        }
        
        System.out.println("===========================================");
        System.out.println("房屋销售系统已关闭");
        System.out.println("===========================================");
    }
}
