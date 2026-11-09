package com.servlet.demo1; // 包名保持不变，和你的目录对应

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

/**
 * 在线考试系统 - 登录界面Servlet
 * 访问路径：http://localhost:8080/ServletExperimentFirst/login
 */
@WebServlet("/login") // 登录界面的访问路径
public class LoginServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1. 设置响应格式和编码（解决中文乱码+告诉浏览器是HTML）
        response.setContentType("text/html;charset=UTF-8");
        // 设置请求编码（后续处理表单提交时防止中文乱码）
        request.setCharacterEncoding("UTF-8");

        // 2. 获取输出流，用于输出HTML登录界面
        PrintWriter out = response.getWriter();

        // 3. 编写登录界面的HTML代码（包含CSS样式，界面更美观）
        out.println("<!DOCTYPE html>");
        out.println("<html lang='zh-CN'>");
        out.println("<head>");
        out.println("<meta charset='UTF-8'>");
        out.println("<title>在线考试系统 - 登录</title>");
        out.println("<style>");
        // CSS样式：美化登录表单
        out.println("body { font-family: Arial, sans-serif; background-color: #5f5f5; margin: 0; padding: 0; }");
        out.println(".login-container { width: 400px; margin: 100px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }");
        out.println(".login-title { text-align: center; color: #333; margin-bottom: 20px; }");
        out.println(".form-group { margin-bottom: 20px; }");
        out.println(".form-group label { display: block; margin-bottom: 8px; color: #666; }");
        out.println(".form-group input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }");
        out.println(".login-btn { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }");
        out.println(".login-btn:hover { background-color: #0056b3; }");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");
        out.println("<div class='login-container'>");
        out.println("<h2 class='login-title'>在线考试系统</h2>");
        // 登录表单：提交到当前Servlet的POST方法处理（已替换为你的项目名）
        out.println("<form action='/ServletExperimentFirst/login' method='post'>");
        out.println("<div class='form-group'>");
        out.println("<label for='username'>用户名：</label>");
        out.println("<input type='text' id='username' name='username' placeholder='请输入学号/工号' required>");
        out.println("</div>");
        out.println("<div class='form-group'>");
        out.println("<label for='password'>密码：</label>");
        out.println("<input type='password' id='password' name='password' placeholder='请输入密码' required>");
        out.println("</div>");
        out.println("<button type='submit' class='login-btn'>登录</button>");
        out.println("</form>");
        out.println("</div>");
        out.println("</body>");
        out.println("</html>");

        // 关闭输出流
        out.close();
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 处理登录表单的提交（简单示例，后续可扩展数据库验证）
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();

        // 获取表单提交的用户名和密码
        String username = request.getParameter("username");
        String password = request.getParameter("password");

        // 模拟登录验证（实际项目中需连接数据库查询）
        if ("20241924".equals(username) && "wbc20050303".equals(password)) {
            out.println("<h2>登录成功！欢迎进入在线考试系统</h2>");
            // 跳转至答题界面（修改这里）
            out.println("<a href='/ServletExperimentFirst/exam'>进入答题界面</a>");
        } else {
            out.println("<h2 style='color: red;'>用户名或密码错误！</h2>");
            out.println("<a href='/ServletExperimentFirst/login'>返回登录页</a>");
        }
        out.close();
    }
}