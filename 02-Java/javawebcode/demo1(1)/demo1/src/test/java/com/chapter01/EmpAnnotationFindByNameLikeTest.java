package com.chapter01;

import com.entity.Emp;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.InputStream;
import java.util.List;

public class EmpAnnotationFindByNameLikeTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config-annotation.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    @Test
    public void testFindByNameLike() {
        System.out.println("========== 注解方式-模糊查询 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            EmpMapperAnnotation mapper = sqlSession.getMapper(EmpMapperAnnotation.class);
            List<Emp> list = mapper.findByNameLike("张");
            for (Emp emp : list) {
                System.out.println(emp);
            }
        }
    }
}