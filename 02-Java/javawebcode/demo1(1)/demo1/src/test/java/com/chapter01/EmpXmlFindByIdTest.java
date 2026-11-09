package com.chapter01;

import com.entity.Emp;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.InputStream;

public class EmpXmlFindByIdTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    @Test
    public void testFindById() {
        System.out.println("========== XML方式-按ID查询 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            EmpMapper mapper = sqlSession.getMapper(EmpMapper.class);
            Emp emp = mapper.findById(1);
            System.out.println(emp);
        }
    }
}