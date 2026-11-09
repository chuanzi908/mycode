package com.house.servlet;

import com.house.dao.UserDao;
import com.house.entity.User;
import com.house.util.JsonUtil;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    // 让GET请求也走POST的逻辑
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");

        String username = request.getParameter("username");
        String password = request.getParameter("password");

        User user = new UserDao().login(username, password);
        Map<String, Object> result = new HashMap<>();

        if (user != null) {
            request.getSession().setAttribute("user", user);
            result.put("code", 200);
            result.put("msg", "登录成功");
            result.put("data", user);
        } else {
            result.put("code", 500);
            result.put("msg", "账号或密码错误");
        }
        JsonUtil.writeJson(response, result);
    }
}