package com.shopping.service;

import com.shopping.dao.UserDao;
import com.shopping.entity.User;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.SQLException;
import java.util.Base64;

public class UserService {
    private UserDao userDao = new UserDao();

    public User login(String username, String password) {
        try {
            String encryptedPassword = encryptPassword(password);
            return userDao.login(username, encryptedPassword);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public boolean register(User user) {
        try {
            if (user.getUsername() == null || user.getUsername().trim().isEmpty()) {
                return false;
            }
            
            if (user.getPassword() == null || user.getPassword().length() < 6) {
                return false;
            }
            
            User existingUser = userDao.findByUsername(user.getUsername());
            if (existingUser != null) {
                return false;
            }
            
            String encryptedPassword = encryptPassword(user.getPassword());
            user.setPassword(encryptedPassword);
            
            userDao.register(user);
            return true;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
    
    public User getUserById(Integer userId) {
        try {
            return userDao.findById(userId);
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }
    
    public boolean updateUser(User user) {
        try {
            if (user.getPassword() != null && !user.getPassword().isEmpty()) {
                String encryptedPassword = encryptPassword(user.getPassword());
                user.setPassword(encryptedPassword);
            }
            return userDao.update(user) > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
    
    private String encryptPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(password.getBytes());
            return Base64.getEncoder().encodeToString(hash);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return password;
        }
    }
}
