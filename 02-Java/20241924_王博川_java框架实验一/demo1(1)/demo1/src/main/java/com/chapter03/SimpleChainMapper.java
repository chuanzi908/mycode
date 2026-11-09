package com.chapter03;

import com.entity.CustomerProductDetail;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.math.BigDecimal;
import java.util.List;

public interface SimpleChainMapper {

    // ==================== 方法1: 客户名 + 商品名 ====================

    // 注解版
    @Select("SELECT cp.id, cp.customer_id, cp.product_id, cp.quantity, cp.created_at, " +
            "c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "p.name AS product_name, p.price AS product_price, p.stock AS product_stock " +
            "FROM customer_product cp " +
            "LEFT JOIN customer c ON cp.customer_id = c.id " +
            "LEFT JOIN product p ON cp.product_id = p.id " +
            "WHERE c.name LIKE CONCAT('%', #{customerName}, '%') " +
            "AND p.name LIKE CONCAT('%', #{productName}, '%')")
    List<CustomerProductDetail> findByCustomerAndProduct(@Param("customerName") String customerName,
                                                          @Param("productName") String productName);

    // XML版（无 @Select，走 SimpleChainMapper.xml 的同名 <select>）
    List<CustomerProductDetail> findByCustomerAndProductXml(@Param("customerName") String customerName,
                                                             @Param("productName") String productName);

    // ==================== 方法2: 客户ID + 客户名 + 日期范围 ====================

    // 注解版
    @Select("SELECT cp.id, cp.customer_id, cp.product_id, cp.quantity, cp.created_at, " +
            "c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "p.name AS product_name, p.price AS product_price, p.stock AS product_stock " +
            "FROM customer_product cp " +
            "LEFT JOIN customer c ON cp.customer_id = c.id " +
            "LEFT JOIN product p ON cp.product_id = p.id " +
            "WHERE c.id = #{customerId} " +
            "AND c.name LIKE CONCAT('%', #{customerName}, '%') " +
            "AND cp.created_at >= #{startDate} " +
            "AND cp.created_at <= #{endDate}")
    List<CustomerProductDetail> findByCustomerUserDate(@Param("customerId") Integer customerId,
                                                       @Param("customerName") String customerName,
                                                       @Param("startDate") String startDate,
                                                       @Param("endDate") String endDate);

    // XML版
    List<CustomerProductDetail> findByCustomerUserDateXml(@Param("customerId") Integer customerId,
                                                          @Param("customerName") String customerName,
                                                          @Param("startDate") String startDate,
                                                          @Param("endDate") String endDate);

    // ==================== 方法3: 客户ID + 商品ID ====================

    // XML版（已有，无 @Select）
    List<CustomerProductDetail> findByCustomerIdAndProductId(@Param("customerId") Integer customerId,
                                                              @Param("productId") Integer productId);

    // 注解版（新增）
    @Select("SELECT cp.id, cp.customer_id, cp.product_id, cp.quantity, cp.created_at, " +
            "c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "p.name AS product_name, p.price AS product_price, p.stock AS product_stock " +
            "FROM customer_product cp " +
            "LEFT JOIN customer c ON cp.customer_id = c.id " +
            "LEFT JOIN product p ON cp.product_id = p.id " +
            "WHERE cp.customer_id = #{customerId} " +
            "AND cp.product_id = #{productId}")
    List<CustomerProductDetail> findByCustomerIdAndProductIdAnno(@Param("customerId") Integer customerId,
                                                                  @Param("productId") Integer productId);

    // ==================== 方法4: 客户名 + 商品价格范围 ====================

    // XML版（已有，无 @Select）
    List<CustomerProductDetail> findByCustomerAndPriceRange(@Param("customerName") String customerName,
                                                             @Param("minPrice") BigDecimal minPrice,
                                                             @Param("maxPrice") BigDecimal maxPrice);

    // 注解版（新增）
    @Select("SELECT cp.id, cp.customer_id, cp.product_id, cp.quantity, cp.created_at, " +
            "c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "p.name AS product_name, p.price AS product_price, p.stock AS product_stock " +
            "FROM customer_product cp " +
            "LEFT JOIN customer c ON cp.customer_id = c.id " +
            "LEFT JOIN product p ON cp.product_id = p.id " +
            "WHERE c.name LIKE CONCAT('%', #{customerName}, '%') " +
            "AND p.price BETWEEN #{minPrice} AND #{maxPrice}")
    List<CustomerProductDetail> findByCustomerAndPriceRangeAnno(@Param("customerName") String customerName,
                                                                 @Param("minPrice") BigDecimal minPrice,
                                                                 @Param("maxPrice") BigDecimal maxPrice);

    // ==================== 方法5: 客户ID + 商品名 + 日期范围 ====================

    // XML版（已有，无 @Select）
    List<CustomerProductDetail> findByCustomerProductAndDate(@Param("customerId") Integer customerId,
                                                              @Param("productName") String productName,
                                                              @Param("startDate") String startDate,
                                                              @Param("endDate") String endDate);

    // 注解版（新增）
    @Select("SELECT cp.id, cp.customer_id, cp.product_id, cp.quantity, cp.created_at, " +
            "c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "p.name AS product_name, p.price AS product_price, p.stock AS product_stock " +
            "FROM customer_product cp " +
            "LEFT JOIN customer c ON cp.customer_id = c.id " +
            "LEFT JOIN product p ON cp.product_id = p.id " +
            "WHERE cp.customer_id = #{customerId} " +
            "AND p.name LIKE CONCAT('%', #{productName}, '%') " +
            "AND cp.created_at >= #{startDate} " +
            "AND cp.created_at <= #{endDate}")
    List<CustomerProductDetail> findByCustomerProductAndDateAnno(@Param("customerId") Integer customerId,
                                                                  @Param("productName") String productName,
                                                                  @Param("startDate") String startDate,
                                                                  @Param("endDate") String endDate);
}