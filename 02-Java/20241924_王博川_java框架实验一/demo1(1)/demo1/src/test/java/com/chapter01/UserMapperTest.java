package com.chapter01;

import com.entity.User;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class UserMapperTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws IOException {
        InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
    }

    @Test
    public void testfindByMap() {
        System.out.println("========== 测试Map多条件（XML方式） ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            UserMapper userMapper = sqlSession.getMapper(UserMapper.class);

            Map<String, Object> map = new HashMap<>();
            map.put("abc", "123456");
            map.put("username", "lisi");

            List<User> users = userMapper.findByMap(map);
            System.out.println(users);
        }
    }

    @Test
    public void testFindAll() {
        System.out.println("========== 注解方式查询所有 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
            List<User> users = userMapper.findAll();
            for (User user : users) {
                System.out.println(user);
            }
        }
    }

    @Test
    public void testFindById() {
        System.out.println("========== 注解方式根据ID查询 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
            User user = userMapper.findById(1);
            System.out.println(user);
        }
    }

    @Test
    public void testFindByUsernameLike() {
        System.out.println("========== 注解方式模糊查询 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
            List<User> users = userMapper.findByUsernameLike("user");
            for (User user : users) {
                System.out.println(user);
            }
        }
    }
}