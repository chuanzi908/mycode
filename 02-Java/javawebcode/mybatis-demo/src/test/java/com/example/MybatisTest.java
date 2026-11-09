package com.example;

import com.example.entity.User;
import com.example.mapper.UserMapper;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.Test;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

/**
 * Mybatis 测试类
 */
public class MybatisTest {

    @Test
    public void testFindAll() throws IOException {
        // 1. 加载配置文件
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");

        // 2. 创建 SqlSessionFactory
        SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(is);

        // 3. 创建 SqlSession
        SqlSession session = factory.openSession();

        // 4. 获取 Mapper 代理对象
        UserMapper userMapper = session.getMapper(UserMapper.class);

        // 5. 执行查询
        List<User> users = userMapper.findAll();

        // 6. 遍历结果
        for (User user : users) {
            System.out.println(user);
        }

        // 7. 关闭资源
        session.close();
        is.close();
    }
}