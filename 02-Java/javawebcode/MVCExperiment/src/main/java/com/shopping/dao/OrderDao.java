package com.shopping.dao;

import com.shopping.entity.Order;
import com.shopping.entity.OrderItem;
import com.shopping.util.DBUtil;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;

import java.sql.SQLException;
import java.util.List;

public class OrderDao {
    private QueryRunner queryRunner = new QueryRunner(DBUtil.getDataSource());

    public void save(Order order) throws SQLException {
        String sql = "INSERT INTO orders(order_no, user_id, total_amount, status, receiver_name, receiver_phone, receiver_address) VALUES(?, ?, ?, ?, ?, ?, ?)";
        queryRunner.update(sql, order.getOrderNo(), order.getUserId(),
                order.getTotalAmount(), order.getStatus(),
                order.getReceiverName(), order.getReceiverPhone(),
                order.getReceiverAddress());
    }

    public List<Order> findByUserId(Integer userId) throws SQLException {
        String sql = "SELECT * FROM orders WHERE user_id = ? ORDER BY create_time DESC";
        return queryRunner.query(sql, new BeanListHandler<>(Order.class), userId);
    }

    public void saveOrderItem(OrderItem orderItem) throws SQLException {
        String sql = "INSERT INTO order_item(order_id, product_id, product_name, product_price, quantity, subtotal) VALUES(?, ?, ?, ?, ?, ?)";
        queryRunner.update(sql, orderItem.getOrderId(), orderItem.getProductId(),
                orderItem.getProductName(), orderItem.getProductPrice(),
                orderItem.getQuantity(), orderItem.getSubtotal());
    }

    public List<OrderItem> findItemsByOrderId(Integer orderId) throws SQLException {
        String sql = "SELECT * FROM order_item WHERE order_id = ?";
        return queryRunner.query(sql, new BeanListHandler<>(OrderItem.class), orderId);
    }
}
