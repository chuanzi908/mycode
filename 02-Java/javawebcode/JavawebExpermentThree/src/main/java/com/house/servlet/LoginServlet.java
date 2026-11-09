package com.house.servlet;

import com.house.dao.UserDao;
import com.house.entity.User;
import com.house.util.JsonUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        String username = request.getParameter("username");
        String password = request.getParameter("password");

        UserDao userDao = new UserDao();
        User user = userDao.login(username, password);

        Map<String,Object> result = new HashMap<>();
        if (user != null) {
            // 登录成功，存入Session
            HttpSession session = request.getSession();
            session.setAttribute("loginUser", user);
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