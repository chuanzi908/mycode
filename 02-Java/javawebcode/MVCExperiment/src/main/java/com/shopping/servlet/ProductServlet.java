package com.shopping.servlet;

import com.google.gson.Gson;
import com.shopping.entity.Product;
import com.shopping.service.ProductService;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@WebServlet("/product/list")
public class ProductServlet extends HttpServlet {
    private ProductService productService = new ProductService();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json;charset=UTF-8");
        List<Product> products = productService.findAll();
        resp.getWriter().write(new Gson().toJson(products));
    }
}
