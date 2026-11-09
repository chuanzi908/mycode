package com.example.mapper;

import com.example.entity.User;
import java.util.List;

/**
 * 用户 Mapper 接口
 * 对应 Mapper XML：UserMapper.xml
 */
public interface UserMapper {

    /**
     * 查询所有用户
     * @return 用户列表
     */
    List findAll();

    /**
     * 根据 ID 查询用户
     * @param id 用户ID
     * @return 用户对象
     */
    User findById(Integer id);
}