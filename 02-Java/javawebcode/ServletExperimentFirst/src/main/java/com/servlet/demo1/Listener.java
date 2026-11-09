package com.servlet.demo1;

import jakarta.servlet.ServletContextEvent;
import jakarta.servlet.ServletContextListener;
import jakarta.servlet.annotation.WebListener;

/**
 * 在线考试系统 - 上下文监听器
 * 作用：在Web应用启动时自动初始化数据库
 */
@WebListener
public class Listener implements ServletContextListener {

    /**
     * 应用启动时执行
     * @param sce Servlet上下文事件
     */
    @Override
    public void contextInitialized(ServletContextEvent sce) {
        System.out.println("===========================================");
        System.out.println("🚀 在线考试系统正在启动...");
        System.out.println("===========================================");

        try {
            // 获取应用上下文路径
            String contextPath = sce.getServletContext().getContextPath();
            System.out.println("📁 应用路径：" + (contextPath.isEmpty() ? "/" : contextPath));

            // 设置应用属性
            sce.getServletContext().setAttribute("appName", "在线考试系统");
            sce.getServletContext().setAttribute("version", "v1.0");
            sce.getServletContext().setAttribute("startTime", System.currentTimeMillis());

            // 自动初始化数据库
            System.out.println("📊 开始初始化数据库...");
            DatabaseInitializer.initDatabase();

            System.out.println("✅ 数据库初始化完成");
            System.out.println("🎉 在线考试系统启动成功！");
            System.out.println("===========================================");
            System.out.println("访问地址：http://localhost:8080" + contextPath + "/login");
            System.out.println("===========================================");

        } catch (Exception e) {
            System.err.println("⚠️  应用启动警告：数据库初始化可能存在问题");
            System.err.println("错误信息：" + e.getMessage());
            System.err.println("请检查MySQL服务和数据库配置");
            e.printStackTrace();
        }
    }

    /**
     * 应用关闭时执行
     * @param sce Servlet上下文事件
     */
    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        System.out.println("===========================================");
        System.out.println("🛑 在线考试系统正在关闭...");

        // 获取运行时长
        Long startTime = (Long) sce.getServletContext().getAttribute("startTime");
        if (startTime != null) {
            long runTime = System.currentTimeMillis() - startTime;
            long hours = runTime / (1000 * 60 * 60);
            long minutes = (runTime % (1000 * 60 * 60)) / (1000 * 60);
            System.out.println("⏱️  运行时长：" + hours + "小时" + minutes + "分钟");
        }

        System.out.println("👋 系统已关闭，再见！");
        System.out.println("===========================================");
    }
}
