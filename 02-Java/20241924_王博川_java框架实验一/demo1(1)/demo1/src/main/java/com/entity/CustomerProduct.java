package com.entity;

import java.util.Date;

public class CustomerProduct {
    private Integer id;
    private Integer customerId;
    private Integer productId;
    private Integer quantity;
    private Date createdAt;

    private Customer customer;
    private Product product;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public Integer getCustomerId() { return customerId; }
    public void setCustomerId(Integer customerId) { this.customerId = customerId; }

    public Integer getProductId() { return productId; }
    public void setProductId(Integer productId) { this.productId = productId; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Customer getCustomer() { return customer; }
    public void setCustomer(Customer customer) { this.customer = customer; }

    public Product getProduct() { return product; }
    public void setProduct(Product product) { this.product = product; }

    @Override
    public String toString() {
        return "CustomerProduct{" +
                "id=" + id +
                ", customerId=" + customerId +
                ", productId=" + productId +
                ", quantity=" + quantity +
                ", createdAt=" + createdAt +
                '}';
    }
}