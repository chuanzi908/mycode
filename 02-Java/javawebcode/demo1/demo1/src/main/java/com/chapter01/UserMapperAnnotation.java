package com.chapter01;

import com.entity.User;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

public interface UserMapperAnnotation {

    @Select("SELECT * FROM user")
    List<User> findAll();

    @Select("SELECT * FROM user WHERE id = #{id}")
    User findById(@Param("id") Integer id);

    @Insert("INSERT INTO user(username, password, email) VALUES(#{username}, #{password}, #{email})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int addUser(User user);

    @Update("UPDATE user SET username = #{username}, password = #{password}, email = #{email} WHERE id = #{id}")
    int updateUser(User user);

    @Delete("DELETE FROM user WHERE id = #{id}")
    int deleteUser(@Param("id") Integer id);

    @Select("SELECT * FROM user WHERE username LIKE CONCAT('%', #{value}, '%')")
    List<User> findByUsernameLike(@Param("value") String username);
}