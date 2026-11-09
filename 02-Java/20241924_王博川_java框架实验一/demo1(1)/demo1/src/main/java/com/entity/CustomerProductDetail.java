package com.entity;

import java.math.BigDecimal;
import java.util.Date;

public class CustomerProductDetail {
    private Integer id;
    private Integer customerId;
    private String customerName;
    private String customerPhone;
    private String customerLevel;
    private Integer productId;
    private String productName;
    private BigDecimal productPrice;
    private Integer productStock;
    private Integer quantity;
    private Date createdAt;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public Integer getCustomerId() { return customerId; }
    public void setCustomerId(Integer customerId) { this.customerId = customerId; }

    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getCustomerPhone() { return customerPhone; }
    public void setCustomerPhone(String customerPhone) { this.customerPhone = customerPhone; }

    public String getCustomerLevel() { return customerLevel; }
    public void setCustomerLevel(String customerLevel) { this.customerLevel = customerLevel; }

    public Integer getProductId() { return productId; }
    public void setProductId(Integer productId) { this.productId = productId; }

    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }

    public BigDecimal getProductPrice() { return productPrice; }
    public void setProductPrice(BigDecimal productPrice) { this.productPrice = productPrice; }

    public Integer getProductStock() { return productStock; }
    public void setProductStock(Integer productStock) { this.productStock = productStock; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    @Override
    public String toString() {
        String dateStr = createdAt != null ? new java.text.SimpleDateFormat("yyyy-MM-dd").format(createdAt) : "";
        String priceStr = productPrice != null ? productPrice.toPlainString() : "0";
        String nameStr = customerName != null ? customerName : "未知";
        String pnameStr = productName != null ? productName : "未知商品";
        int qty = quantity != null ? quantity : 0;
        return String.format("  客户【%s】购买了【%s】，单价%s元，共%d件，日期%s",
                nameStr, pnameStr, priceStr, qty, dateStr);
    }
}