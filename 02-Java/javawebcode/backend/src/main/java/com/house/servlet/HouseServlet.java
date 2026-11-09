package com.house.servlet;

import com.house.dao.HouseDao;
import com.house.entity.House;
import com.house.util.JsonUtil;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet("/house/list")
public class HouseServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setCharacterEncoding("UTF-8");
        List<House> list = new HouseDao().list();
        Map<String, Object> result = new HashMap<>();
        result.put("code", 200);
        result.put("data", list);
        JsonUtil.writeJson(response, result);
    }
}