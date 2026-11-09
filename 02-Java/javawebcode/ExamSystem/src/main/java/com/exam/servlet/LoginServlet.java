package com.exam.servlet;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("utf8");

        // 固定账号密码
        String username = req.getParameter("username");
        String password = req.getParameter("password");

        // 默认账号：admin  密码：123456
        if("20241924".equals(username) && "wbc20050303".equals(password)){
            // 登录成功 → 进入考试
            resp.sendRedirect("exam");
        }else{
            // 登录失败
            resp.getWriter().write("登录失败！账号或密码错误<br><a href='index.jsp'>返回</a>");
        }
    }
}