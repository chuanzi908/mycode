package com.shopping.servlet;

import com.google.gson.Gson;
import com.shopping.entity.*;
import com.shopping.service.OrderService;
import com.shopping.service.ProductService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet("/order/*")
public class OrderServlet extends HttpServlet {
    private OrderService orderService = new OrderService();
    private ProductService productService = new ProductService();

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        resp.setContentType("application/json;charset=UTF-8");

        String pathInfo = req.getPathInfo();

        if ("/create".equals(pathInfo)) {
            createOrder(req, resp);
        } else if ("/list".equals(pathInfo)) {
            listOrders(req, resp);
        }
    }

    private void createOrder(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "Please login first");
            resp.getWriter().write(new Gson().toJson(result));
            return;
        }

        User user = (User) session.getAttribute("user");
        String receiverName = req.getParameter("receiverName");
        String receiverPhone = req.getParameter("receiverPhone");
        String receiverAddress = req.getParameter("receiverAddress");
        String productIds = req.getParameter("productIds");
        String quantities = req.getParameter("quantities");

        String[] productIdArray = productIds.split(",");
        String[] quantityArray = quantities.split(",");

        List<CartItem> cartItems = new ArrayList<>();
        for (int i = 0; i < productIdArray.length; i++) {
            Integer productId = Integer.parseInt(productIdArray[i]);
            Integer quantity = Integer.parseInt(quantityArray[i]);

            Product product = productService.findById(productId);
            cartItems.add(new CartItem(product, quantity));
        }

        String orderNo = orderService.createOrder(user.getId(), cartItems,
                receiverName, receiverPhone, receiverAddress);

        Map<String, Object> result = new HashMap<>();
        if (orderNo != null) {
            result.put("success", true);
            result.put("message", "Order created successfully");
            result.put("orderNo", orderNo);
        } else {
            result.put("success", false);
            result.put("message", "Order creation failed");
        }

        resp.getWriter().write(new Gson().toJson(result));
    }

    private void listOrders(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            resp.getWriter().write("[]");
            return;
        }

        User user = (User) session.getAttribute("user");
        List<Order> orders = orderService.findByUserId(user.getId());
        resp.getWriter().write(new Gson().toJson(orders));
    }
}
