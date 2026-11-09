package com.lab.emp.interceptor;

import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.PrintWriter;

/**
 * 登录拦截器：未登录访问业务接口时返回 401 的 JSON。
 */
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        Object user = request.getSession().getAttribute("loginUser");
        if (user == null) {
            response.setContentType("application/json;charset=UTF-8");
            try (PrintWriter writer = response.getWriter()) {
                writer.write("{\"code\":401,\"message\":\"未登录\",\"data\":null}");
            }
            return false;
        }
        return true;
    }
}
