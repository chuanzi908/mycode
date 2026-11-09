package com.house.servlet;

import com.house.dao.HouseDao;
import com.house.entity.House;
import com.house.util.JsonUtil;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/house/add")
public class HouseAddServlet extends HttpServlet {
    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        // 接收前端JSON参数
        House house = mapper.readValue(request.getInputStream(), House.class);
        HouseDao houseDao = new HouseDao();
        int rows = houseDao.addHouse(house);

        Map<String, Object> result = new HashMap<>();
        if (rows > 0) {
            result.put("code", 200);
            result.put("msg", "房源添加成功");
        } else {
            result.put("code", 500);
            result.put("msg", "房源添加失败");
        }
        JsonUtil.writeJson(response, result);
    }
}