package com.entity;

import java.math.BigDecimal;
import java.util.Date;

public class SupplierProductCustomer {
    private Integer supplierId;
    private String supplierName;
    private Integer productId;
    private String productName;
    private BigDecimal productPrice;
    private Integer customerId;
    private String customerName;
    private String customerPhone;
    private String customerLevel;
    private Integer userId;
    private String username;
    private String userEmail;
    private Integer quantity;
    private Date createdAt;

    public Integer getSupplierId() { return supplierId; }
    public void setSupplierId(Integer supplierId) { this.supplierId = supplierId; }

    public String getSupplierName() { return supplierName; }
    public void setSupplierName(String supplierName) { this.supplierName = supplierName; }

    public Integer getProductId() { return productId; }
    public void setProductId(Integer productId) { this.productId = productId; }

    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }

    public BigDecimal getProductPrice() { return productPrice; }
    public void setProductPrice(BigDecimal productPrice) { this.productPrice = productPrice; }

    public Integer getCustomerId() { return customerId; }
    public void setCustomerId(Integer customerId) { this.customerId = customerId; }

    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getCustomerPhone() { return customerPhone; }
    public void setCustomerPhone(String customerPhone) { this.customerPhone = customerPhone; }

    public String getCustomerLevel() { return customerLevel; }
    public void setCustomerLevel(String customerLevel) { this.customerLevel = customerLevel; }

    public Integer getUserId() { return userId; }
    public void setUserId(Integer userId) { this.userId = userId; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getUserEmail() { return userEmail; }
    public void setUserEmail(String userEmail) { this.userEmail = userEmail; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    @Override
    public String toString() {
        String dateStr = createdAt != null ? new java.text.SimpleDateFormat("yyyy-MM-dd").format(createdAt) : "";
        String priceStr = productPrice != null ? productPrice.toPlainString() : "0";
        String sName = supplierName != null ? supplierName : "未知供应商";
        String pName = productName != null ? productName : "未知商品";
        String cName = customerName != null ? customerName : "未知客户";
        int qty = quantity != null ? quantity : 0;
        return String.format("  供应商【%s】→ 商品【%s】（%s元）→ 客户【%s】购买了%d件，日期%s",
                sName, pName, priceStr, cName, qty, dateStr);
    }
}