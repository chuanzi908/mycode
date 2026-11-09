package com.chapter01;

import com.entity.User;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.InputStream;
import java.util.List;

public class UserMapperAnnotationTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config-annotation.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    @Test
    public void testFindAll() {
        System.out.println("========== testFindAll ==========");

        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            UserMapperAnnotation userMapper = sqlSession.getMapper(UserMapperAnnotation.class);
            List<User> users = userMapper.findAll();
            for (User user : users) {
                System.out.println(user);
            }
        }
    }

    @Test
    public void testFindById() {
        System.out.println("========== testFindById ==========");

        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            UserMapperAnnotation userMapper = sqlSession.getMapper(UserMapperAnnotation.class);
            User user = userMapper.findById(1);
            System.out.println(user);
        }
    }

    @Test
    public void testAddUser() {
        System.out.println("========== testAddUser ==========");

        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            UserMapperAnnotation userMapper = sqlSession.getMapper(UserMapperAnnotation.class);

            User user = new User();
            user.setUsername("annotation_test_" + System.currentTimeMillis());
            user.setPassword("123456");
            user.setEmail("anno_" + System.currentTimeMillis() + "@qq.com");

            int rows = userMapper.addUser(user);
            System.out.println("rows: " + rows);
            System.out.println("auto-increment id: " + user.getId());

            sqlSession.commit();
        }
    }

    @Test
    public void testRegisterAnnotationMapper() {
        System.out.println("========== how to register annotation Mapper ==========");
        System.out.println("In mybatis-config.xml add:");
        System.out.println("<mappers>");
        System.out.println("    <!-- way 1: single -->");
        System.out.println("    <mapper class=\"com.chapter01.UserMapperAnnotation\"/>");
        System.out.println("");
        System.out.println("    <!-- way 2: package scan -->");
        System.out.println("    <package name=\"com.chapter01\"/>");
        System.out.println("</mappers>");
    }
}