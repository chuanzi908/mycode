package com.shopping.service;

import com.shopping.dao.OrderDao;
import com.shopping.dao.ProductDao;
import com.shopping.entity.*;

import java.math.BigDecimal;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Random;

public class OrderService {
    private OrderDao orderDao = new OrderDao();
    private ProductDao productDao = new ProductDao();

    public String createOrder(Integer userId, List<CartItem> cartItems,
                              String receiverName, String receiverPhone, String receiverAddress) {
        try {
            Order order = new Order();
            order.setOrderNo(generateOrderNo());
            order.setUserId(userId);
            order.setStatus(1);
            order.setReceiverName(receiverName);
            order.setReceiverPhone(receiverPhone);
            order.setReceiverAddress(receiverAddress);

            BigDecimal totalAmount = BigDecimal.ZERO;
            for (CartItem item : cartItems) {
                totalAmount = totalAmount.add(item.getSubtotal());
            }
            order.setTotalAmount(totalAmount);

            orderDao.save(order);

            List<Order> orders = orderDao.findByUserId(userId);
            if (orders == null || orders.isEmpty()) {
                throw new RuntimeException("Failed to retrieve created order");
            }
            Order savedOrder = orders.get(0);

            for (CartItem item : cartItems) {
                OrderItem orderItem = new OrderItem();
                orderItem.setOrderId(savedOrder.getId());
                orderItem.setProductId(item.getProduct().getId());
                orderItem.setProductName(item.getProduct().getName());
                orderItem.setProductPrice(item.getProduct().getPrice());
                orderItem.setQuantity(item.getQuantity());
                orderItem.setSubtotal(item.getSubtotal());

                orderDao.saveOrderItem(orderItem);

                Product product = item.getProduct();
                product.setStock(product.getStock() - item.getQuantity());
                productDao.update(product);
            }

            return order.getOrderNo();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    private String generateOrderNo() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
        String dateStr = sdf.format(new Date());
        Random random = new Random();
        int randomNum = random.nextInt(9000) + 1000;
        return dateStr + randomNum;
    }

    public List<Order> findByUserId(Integer userId) {
        try {
            return orderDao.findByUserId(userId);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public List<OrderItem> findItemsByOrderId(Integer orderId) {
        try {
            return orderDao.findItemsByOrderId(orderId);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
