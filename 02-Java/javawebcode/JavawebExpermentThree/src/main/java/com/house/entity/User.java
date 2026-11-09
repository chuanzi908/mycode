package com.house.entity;

public class User {
    private Integer id;
    private String username;
    private String password;
    private String realName;
    private String phone;
    private Integer role;

    // 无参、有参构造 + getter/setter
    public User() {}
    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getRealName() { return realName; }
    public void setRealName(String realName) { this.realName = realName; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public Integer getRole() { return role; }
    public void setRole(Integer role) { this.role = role; }
}