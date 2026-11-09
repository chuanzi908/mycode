package com.chapter01;

import com.entity.User;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

public interface UserMapper {

    List<User> findByMap(Map<String, Object> map);

    @Select("SELECT * FROM user")
    List<User> findAll();

    @Select("SELECT * FROM user WHERE id = #{id}")
    User findById(@Param("id") Integer id);

    @Select("SELECT * FROM user WHERE username LIKE CONCAT('%', #{value}, '%')")
    List<User> findByUsernameLike(String username);
}