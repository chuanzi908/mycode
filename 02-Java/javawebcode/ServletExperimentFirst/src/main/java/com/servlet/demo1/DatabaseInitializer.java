package com.servlet.demo1;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * 数据库初始化类 - 创建表并插入初始数据
 */
public class DatabaseInitializer {

    /**
     * 初始化数据库：创建题目表并插入 20 道 JavaWeb 试题
     */
    public static void initDatabase() {
        String createTableSQL =
                "CREATE TABLE IF NOT EXISTS exam_questions (" +
                        "  id INT PRIMARY KEY AUTO_INCREMENT," +
                        "  question_number INT NOT NULL UNIQUE," +
                        "  question_text TEXT NOT NULL," +
                        "  option_a VARCHAR(255) NOT NULL," +
                        "  option_b VARCHAR(255) NOT NULL," +
                        "  option_c VARCHAR(255) NOT NULL," +
                        "  option_d VARCHAR(255) NOT NULL," +
                        "  correct_answer CHAR(1) NOT NULL," +
                        "  created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;";

        String insertQuestionSQL =
                "INSERT INTO exam_questions (question_number, question_text, option_a, option_b, option_c, option_d, correct_answer) " +
                        "VALUES (?, ?, ?, ?, ?, ?, ?)";

        Connection conn = null;
        try {
            System.out.println("正在尝试连接数据库...");
            conn = DBUtil.getConnection();
            System.out.println("✓ 数据库连接成功！");

            try (PreparedStatement createStmt = conn.prepareStatement(createTableSQL)) {
                // 创建表
                createStmt.executeUpdate();
                System.out.println("✓ 题目表创建成功");

                // 准备 20 道题目的数据
                Object[][] questions = {
                        {1, "Servlet 的生命周期中，哪个方法是在 Servlet 被创建时执行，且只执行一次？", "init()", "doGet()", "service()", "destroy()", "A"},
                        {2, "在 TOMCAT 10 中，Servlet API 的包名是？", "javax.servlet", "jakarta.servlet", "org.apache.servlet", "com.tomcat.servlet", "B"},
                        {3, "以下哪个对象用于在 Servlet 中获取客户端的请求参数？", "HttpServletResponse", "ServletContext", "HttpServletRequest", "Session", "C"},
                        {4, "JSP 的内置对象中，用于向客户端输出内容的是？", "out", "request", "response", "pageContext", "A"},
                        {5, "Session 的作用域是？", "单个请求", "单个用户会话", "整个应用", "单个页面", "B"},
                        {6, "以下哪个不是 HTTP 请求方法？", "GET", "POST", "PUT", "CONNECT", "D"},
                        {7, "Servlet 中，设置响应内容类型为 HTML 的代码是？", "response.setContentType(\"text/html;charset=UTF-8\")", "request.setCharacterEncoding(\"UTF-8\")", "response.setCharacterEncoding(\"UTF-8\")", "request.setContentType(\"text/html\")", "A"},
                        {8, "JSP 页面中，声明变量的语法是？", "${变量名}", "<%= 变量名 %>", "<%! 变量声明 %>", "<c:set var=\"变量名\" value=\"값\"/>", "C"},
                        {9, "Filter（过滤器）的核心方法是？", "init()", "doFilter()", "service()", "destroy()", "B"},
                        {10, "Cookie 的默认作用域是？", "当前域名", "所有子域名", "整个服务器", "单个页面", "A"},
                        {11, "以下哪个标签用于在 JSP 中引入其他页面？", "<%= %>", "<%! %>", "<% %>", "<%@ include file=\"路径\" %>", "D"},
                        {12, "ServletContext 的作用域是？", "单个请求", "单个用户会话", "整个 Web 应用", "单个 Servlet", "C"},
                        {13, "处理 POST 请求中文乱码的正确方式是？", "response.setCharacterEncoding(\"UTF-8\")", "request.setCharacterEncoding(\"UTF-8\")", "response.setContentType(\"UTF-8\")", "request.setContentType(\"UTF-8\")", "B"},
                        {14, "JDBC 中，用于执行 SQL 语句的对象是？", "Statement", "Connection", "ResultSet", "DriverManager", "A"},
                        {15, "JSTL 中，遍历集合的标签是？", "<c:if>", "<c:choose>", "<c:forEach>", "<c:set>", "C"},
                        {16, "以下哪个状态码表示请求成功？", "404", "200", "500", "302", "B"},
                        {17, "Servlet 中，重定向的方法是？", "request.getRequestDispatcher().forward()", "response.getWriter()", "request.setAttribute()", "response.sendRedirect()", "D"},
                        {18, "EL 表达式中，获取请求参数的语法是？", "${param.参数名}", "${request.参数名}", "<%= request.getParameter(\"参数名\") %>", "${session.参数名}", "A"},
                        {19, "Listener（监听器）用于监听以下哪种对象的变化？", "只有 Servlet", "只有 JSP", "ServletContext/Session/Request 等", "只有数据库连接", "C"},
                        {20, "MVC 模式中，Servlet 通常扮演哪个角色？", "Model（模型）", "Controller（控制器）", "View（视图）", "以上都不是", "B"}
                };

                // 插入题目数据
                try (PreparedStatement insertStmt = conn.prepareStatement(insertQuestionSQL)) {
                    for (Object[] q : questions) {
                        insertStmt.setInt(1, (Integer) q[0]);
                        insertStmt.setString(2, (String) q[1]);
                        insertStmt.setString(3, (String) q[2]);
                        insertStmt.setString(4, (String) q[3]);
                        insertStmt.setString(5, (String) q[4]);
                        insertStmt.setString(6, (String) q[5]);
                        insertStmt.setString(7, (String) q[6]);
                        insertStmt.addBatch();
                    }

                    int[] results = insertStmt.executeBatch();
                    System.out.println("✓ 成功插入 " + results.length + " 道题目到数据库");
                    System.out.println("===========================================");
                    System.out.println("数据库初始化完成！");
                    System.out.println("===========================================");
                }
            }

        } catch (SQLException e) {
            System.err.println("===========================================");
            System.err.println("✗ 数据库初始化失败！");
            System.err.println("===========================================");
            System.err.println("错误类型：" + e.getClass().getSimpleName());
            System.err.println("错误信息：" + e.getMessage());
            System.err.println("");
            System.err.println("可能的原因：");
            System.err.println("1. MySQL 服务未启动");
            System.err.println("2. 数据库 exam_system 不存在");
            System.err.println("3. 用户名或密码错误");
            System.err.println("4. 数据库端口不是 3306");
            System.err.println("===========================================");
            
            if (e.getMessage().contains("Duplicate entry")) {
                System.out.println("⚠ 题目数据已存在，跳过插入");
            } else if (e.getMessage().contains("Unknown database")) {
                System.err.println("解决方案：请先创建数据库 exam_system");
                System.err.println("执行 SQL: CREATE DATABASE exam_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;");
            } else if (e.getMessage().contains("Access denied")) {
                System.err.println("解决方案：用户名或密码错误，请检查 DBUtil.java 中的配置");
            } else if (e.getMessage().contains("Communications link failure")) {
                System.err.println("解决方案：MySQL 服务未启动，请启动 MySQL 服务");
            }
            
            e.printStackTrace();
        } finally {
            DBUtil.close(conn, null, null);
        }
    }

    /**
     * 主方法 - 可单独运行此方法初始化数据库
     */
    public static void main(String[] args) {
        System.out.println("开始初始化数据库...");
        initDatabase();
        System.out.println("数据库初始化完成！");
    }
}

