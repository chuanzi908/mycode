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
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet("/house/list")
public class HouseListServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HouseDao houseDao = new HouseDao();
        List<House> houseList = houseDao.findAllHouse();

        Map<String,Object> res = new HashMap<>();
        res.put("code",200);
        res.put("data",houseList);
        JsonUtil.writeJson(response, res);
    }
}