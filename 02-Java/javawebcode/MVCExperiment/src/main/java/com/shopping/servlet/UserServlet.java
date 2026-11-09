package com.shopping.servlet;

import com.google.gson.Gson;
import com.shopping.entity.User;
import com.shopping.service.UserService;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/user/*")
public class UserServlet extends HttpServlet {
    private UserService userService = new UserService();

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        resp.setContentType("application/json;charset=UTF-8");

        String pathInfo = req.getPathInfo();

        if ("/login".equals(pathInfo)) {
            handleLogin(req, resp);
        } else if ("/register".equals(pathInfo)) {
            handleRegister(req, resp);
        } else if ("/logout".equals(pathInfo)) {
            handleLogout(req, resp);
        } else if ("/update".equals(pathInfo)) {
            handleUpdate(req, resp);
        }
    }
    
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json;charset=UTF-8");
        
        String pathInfo = req.getPathInfo();
        
        if ("/info".equals(pathInfo)) {
            handleGetUserInfo(req, resp);
        } else if ("/check".equals(pathInfo)) {
            handleCheckLogin(req, resp);
        }
    }
    
    private void handleLogin(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");

        User user = userService.login(username, password);
        Map<String, Object> result = new HashMap<>();

        if (user != null) {
            HttpSession session = req.getSession();
            session.setAttribute("user", user);
            result.put("success", true);
            result.put("message", "Login success");
            result.put("userId", user.getId());
            result.put("username", user.getUsername());
            result.put("email", user.getEmail());
        } else {
            result.put("success", false);
            result.put("message", "Username or password error");
        }

        resp.getWriter().write(new Gson().toJson(result));
    }
    
    private void handleRegister(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");
        String email = req.getParameter("email");

        Map<String, Object> result = new HashMap<>();
        
        if (username == null || username.trim().isEmpty()) {
            result.put("success", false);
            result.put("message", "Username cannot be empty");
            resp.getWriter().write(new Gson().toJson(result));
            return;
        }
        
        if (password == null || password.length() < 6) {
            result.put("success", false);
            result.put("message", "Password must be at least 6 characters");
            resp.getWriter().write(new Gson().toJson(result));
            return;
        }

        User user = new User(username, password, email);
        boolean success = userService.register(user);

        if (success) {
            result.put("success", true);
            result.put("message", "Register success");
        } else {
            result.put("success", false);
            result.put("message", "Username already exists or invalid input");
        }
        resp.getWriter().write(new Gson().toJson(result));
    }
    
    private void handleLogout(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        req.getSession().invalidate();
        Map<String, Object> result = new HashMap<>();
        result.put("success", true);
        result.put("message", "Logout success");
        resp.getWriter().write(new Gson().toJson(result));
    }
    
    private void handleGetUserInfo(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        HttpSession session = req.getSession(false);
        Map<String, Object> result = new HashMap<>();
        
        if (session != null && session.getAttribute("user") != null) {
            User user = (User) session.getAttribute("user");
            result.put("success", true);
            result.put("userId", user.getId());
            result.put("username", user.getUsername());
            result.put("email", user.getEmail());
        } else {
            result.put("success", false);
            result.put("message", "Not logged in");
        }
        resp.getWriter().write(new Gson().toJson(result));
    }
    
    private void handleCheckLogin(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        HttpSession session = req.getSession(false);
        Map<String, Object> result = new HashMap<>();
        
        if (session != null && session.getAttribute("user") != null) {
            User user = (User) session.getAttribute("user");
            result.put("loggedIn", true);
            result.put("username", user.getUsername());
        } else {
            result.put("loggedIn", false);
        }
        resp.getWriter().write(new Gson().toJson(result));
    }
    
    private void handleUpdate(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        HttpSession session = req.getSession(false);
        Map<String, Object> result = new HashMap<>();
        
        if (session == null || session.getAttribute("user") == null) {
            result.put("success", false);
            result.put("message", "Not logged in");
            resp.getWriter().write(new Gson().toJson(result));
            return;
        }
        
        User currentUser = (User) session.getAttribute("user");
        String email = req.getParameter("email");
        String password = req.getParameter("password");
        
        User updateUser = new User();
        updateUser.setId(currentUser.getId());
        updateUser.setEmail(email);
        if (password != null && !password.isEmpty()) {
            updateUser.setPassword(password);
        }
        
        boolean success = userService.updateUser(updateUser);
        if (success) {
            User updatedUser = userService.getUserById(currentUser.getId());
            session.setAttribute("user", updatedUser);
            result.put("success", true);
            result.put("message", "Update success");
        } else {
            result.put("success", false);
            result.put("message", "Update failed");
        }
        resp.getWriter().write(new Gson().toJson(result));
    }
}
