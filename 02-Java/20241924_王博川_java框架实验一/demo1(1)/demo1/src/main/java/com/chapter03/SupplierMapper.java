package com.chapter03;

import com.entity.SupplierProductCustomer;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.math.BigDecimal;
import java.util.List;

public interface SupplierMapper {

    // ==================== 方法1: 供应商名 ====================

    @Select("SELECT s.id AS supplier_id, s.name AS supplier_name, " +
            "p.id AS product_id, p.name AS product_name, p.price AS product_price, " +
            "c.id AS customer_id, c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "u.id AS user_id, u.username, u.email AS user_email, " +
            "cp.quantity, cp.created_at " +
            "FROM supplier s " +
            "INNER JOIN product p ON p.supplier_id = s.id " +
            "INNER JOIN customer_product cp ON cp.product_id = p.id " +
            "INNER JOIN customer c ON c.id = cp.customer_id " +
            "LEFT JOIN user_customer uc ON uc.customer_id = c.id " +
            "LEFT JOIN user u ON u.id = uc.user_id " +
            "WHERE s.name LIKE CONCAT('%', #{supplierName}, '%')")
    List<SupplierProductCustomer> findBySupplierName(@Param("supplierName") String supplierName);

    List<SupplierProductCustomer> findBySupplierNameXml(@Param("supplierName") String supplierName);

    // ==================== 方法2: 供应商名 + 商品名 ====================

    @Select("SELECT s.id AS supplier_id, s.name AS supplier_name, " +
            "p.id AS product_id, p.name AS product_name, p.price AS product_price, " +
            "c.id AS customer_id, c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "u.id AS user_id, u.username, u.email AS user_email, " +
            "cp.quantity, cp.created_at " +
            "FROM supplier s " +
            "INNER JOIN product p ON p.supplier_id = s.id " +
            "INNER JOIN customer_product cp ON cp.product_id = p.id " +
            "INNER JOIN customer c ON c.id = cp.customer_id " +
            "LEFT JOIN user_customer uc ON uc.customer_id = c.id " +
            "LEFT JOIN user u ON u.id = uc.user_id " +
            "WHERE s.name LIKE CONCAT('%', #{supplierName}, '%') " +
            "AND p.name LIKE CONCAT('%', #{productName}, '%')")
    List<SupplierProductCustomer> findBySupplierAndProduct(@Param("supplierName") String supplierName,
                                                            @Param("productName") String productName);

    List<SupplierProductCustomer> findBySupplierAndProductXml(@Param("supplierName") String supplierName,
                                                               @Param("productName") String productName);

    // ==================== 方法3: 供应商ID + 客户名 ====================

    @Select("SELECT s.id AS supplier_id, s.name AS supplier_name, " +
            "p.id AS product_id, p.name AS product_name, p.price AS product_price, " +
            "c.id AS customer_id, c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "u.id AS user_id, u.username, u.email AS user_email, " +
            "cp.quantity, cp.created_at " +
            "FROM supplier s " +
            "INNER JOIN product p ON p.supplier_id = s.id " +
            "INNER JOIN customer_product cp ON cp.product_id = p.id " +
            "INNER JOIN customer c ON c.id = cp.customer_id " +
            "LEFT JOIN user_customer uc ON uc.customer_id = c.id " +
            "LEFT JOIN user u ON u.id = uc.user_id " +
            "WHERE s.id = #{supplierId} " +
            "AND c.name LIKE CONCAT('%', #{customerName}, '%')")
    List<SupplierProductCustomer> findBySupplierIdAndCustomer(@Param("supplierId") Integer supplierId,
                                                               @Param("customerName") String customerName);

    List<SupplierProductCustomer> findBySupplierIdAndCustomerXml(@Param("supplierId") Integer supplierId,
                                                                  @Param("customerName") String customerName);

    // ==================== 方法4: 供应商名 + 价格范围 ====================

    @Select("SELECT s.id AS supplier_id, s.name AS supplier_name, " +
            "p.id AS product_id, p.name AS product_name, p.price AS product_price, " +
            "c.id AS customer_id, c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "u.id AS user_id, u.username, u.email AS user_email, " +
            "cp.quantity, cp.created_at " +
            "FROM supplier s " +
            "INNER JOIN product p ON p.supplier_id = s.id " +
            "INNER JOIN customer_product cp ON cp.product_id = p.id " +
            "INNER JOIN customer c ON c.id = cp.customer_id " +
            "LEFT JOIN user_customer uc ON uc.customer_id = c.id " +
            "LEFT JOIN user u ON u.id = uc.user_id " +
            "WHERE s.name LIKE CONCAT('%', #{supplierName}, '%') " +
            "AND p.price BETWEEN #{minPrice} AND #{maxPrice}")
    List<SupplierProductCustomer> findBySupplierAndPriceRange(@Param("supplierName") String supplierName,
                                                               @Param("minPrice") BigDecimal minPrice,
                                                               @Param("maxPrice") BigDecimal maxPrice);

    List<SupplierProductCustomer> findBySupplierAndPriceRangeXml(@Param("supplierName") String supplierName,
                                                                  @Param("minPrice") BigDecimal minPrice,
                                                                  @Param("maxPrice") BigDecimal maxPrice);

    // ==================== 方法5: 供应商ID + 商品名 + 日期范围 ====================

    @Select("SELECT s.id AS supplier_id, s.name AS supplier_name, " +
            "p.id AS product_id, p.name AS product_name, p.price AS product_price, " +
            "c.id AS customer_id, c.name AS customer_name, c.phone AS customer_phone, c.level AS customer_level, " +
            "u.id AS user_id, u.username, u.email AS user_email, " +
            "cp.quantity, cp.created_at " +
            "FROM supplier s " +
            "INNER JOIN product p ON p.supplier_id = s.id " +
            "INNER JOIN customer_product cp ON cp.product_id = p.id " +
            "INNER JOIN customer c ON c.id = cp.customer_id " +
            "LEFT JOIN user_customer uc ON uc.customer_id = c.id " +
            "LEFT JOIN user u ON u.id = uc.user_id " +
            "WHERE s.id = #{supplierId} " +
            "AND p.name LIKE CONCAT('%', #{productName}, '%') " +
            "AND cp.created_at >= #{startDate} " +
            "AND cp.created_at <= #{endDate}")
    List<SupplierProductCustomer> findBySupplierProductAndDate(@Param("supplierId") Integer supplierId,
                                                                @Param("productName") String productName,
                                                                @Param("startDate") String startDate,
                                                                @Param("endDate") String endDate);

    List<SupplierProductCustomer> findBySupplierProductAndDateXml(@Param("supplierId") Integer supplierId,
                                                                   @Param("productName") String productName,
                                                                   @Param("startDate") String startDate,
                                                                   @Param("endDate") String endDate);
}