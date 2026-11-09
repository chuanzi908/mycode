package com.house.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

public class JsonUtil {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    // 向前端返回JSON数据
    public static void writeJson(HttpServletResponse resp, Object obj) {
        resp.setContentType("application/json;charset=UTF-8");
        try {
            MAPPER.writeValue(resp.getWriter(), obj);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}