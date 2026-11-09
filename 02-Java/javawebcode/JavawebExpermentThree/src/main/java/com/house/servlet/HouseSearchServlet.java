package com.house.servlet;

import com.house.dao.HouseDao;
import com.house.entity.House;
import com.house.util.JsonUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet("/house/search")
public class HouseSearchServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        // 获取前端筛选参数
        String area = request.getParameter("area");
        String houseType = request.getParameter("houseType");
        String minPriceStr = request.getParameter("minPrice");
        String maxPriceStr = request.getParameter("maxPrice");

        BigDecimal minPrice = null;
        BigDecimal maxPrice = null;
        if (minPriceStr != null && !"".equals(minPriceStr)) {
            minPrice = new BigDecimal(minPriceStr);
        }
        if (maxPriceStr != null && !"".equals(maxPriceStr)) {
            maxPrice = new BigDecimal(maxPriceStr);
        }

        HouseDao houseDao = new HouseDao();
        List<House> list = houseDao.findHouseByCondition(area, houseType, minPrice, maxPrice);

        Map<String, Object> result = new HashMap<>();
        result.put("code", 200);
        result.put("data", list);
        JsonUtil.writeJson(response, result);
    }
}