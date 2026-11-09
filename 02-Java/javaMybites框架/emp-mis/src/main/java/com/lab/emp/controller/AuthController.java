package com.lab.emp.controller;

import com.lab.emp.common.Result;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.HashMap;
import java.util.Map;

/**
 * 简易登录：仅用于配合登录拦截器完成 401 场景测试。
 */
@RestController
@RequestMapping("/auth")
public class AuthController {

    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody Map<String, String> body, HttpSession session) {
        String username = body.get("username");
        String password = body.get("password");
        if (username == null || password == null || username.trim().isEmpty()) {
            return Result.fail("用户名和密码不能为空");
        }
        // 教学用：任意非空用户名均可登录，生产环境必须查库并校验密码散列
        session.setAttribute("loginUser", username);
        Map<String, Object> data = new HashMap<>();
        data.put("username", username);
        return Result.ok(data);
    }

    @PostMapping("/logout")
    public Result<Void> logout(HttpSession session) {
        session.invalidate();
        return Result.ok(null);
    }
}
