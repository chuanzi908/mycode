package com.chapter01;

import com.entity.Emp;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.InputStream;
import java.math.BigDecimal;
import java.text.SimpleDateFormat;

public class EmpAnnotationUpdateTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config-annotation.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    @Test
    public void testUpdateEmp() {
        System.out.println("========== 注解方式-修改 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            EmpMapperAnnotation mapper = sqlSession.getMapper(EmpMapperAnnotation.class);

            Emp emp = mapper.findById(1);
            System.out.println("修改前: " + emp);

            emp.setName("张三_已修改");
            emp.setAge(30);
            emp.setDept("架构部");
            emp.setSalary(new BigDecimal("15000.00"));

            int rows = mapper.updateEmp(emp);
            sqlSession.commit();

            Emp updated = mapper.findById(1);
            System.out.println("影响行数: " + rows);
            System.out.println("修改后: " + updated);
        }
    }
}