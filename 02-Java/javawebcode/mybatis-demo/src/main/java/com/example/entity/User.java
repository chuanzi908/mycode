package com.example.entity;

/**
 * 用户实体类
 * 对应数据库表：user
 */
public class User {
    // 字段（对应数据库表的列）
    private Integer id;       // 用户ID
    private String username;  // 用户名
    private String password;  // 密码
    private String email;     // 邮箱

    // 构造方法
    public User() {
    }

    // getter 和 setter 方法（必须有，否则 Mybatis 无法封装数据）
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    // toString 方法（方便调试）
    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}