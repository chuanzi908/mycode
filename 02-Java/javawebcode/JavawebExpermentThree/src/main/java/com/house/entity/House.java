package com.house.entity;

import java.math.BigDecimal;

public class House {
    private Integer id;
    private String title;
    private String area;
    private String houseType;
    private BigDecimal price;
    private String address;
    private Integer status;

    // getter & setter
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getArea() { return area; }
    public void setArea(String area) { this.area = area; }
    public String getHouseType() { return houseType; }
    public void setHouseType(String houseType) { this.houseType = houseType; }
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
}