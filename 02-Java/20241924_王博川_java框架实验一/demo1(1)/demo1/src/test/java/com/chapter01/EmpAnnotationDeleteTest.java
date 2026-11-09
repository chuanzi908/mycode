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
import java.util.List;

public class EmpAnnotationDeleteTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config-annotation.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    @Test
    public void testDeleteEmp() {
        System.out.println("========== 注解方式-删除 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            EmpMapperAnnotation mapper = sqlSession.getMapper(EmpMapperAnnotation.class);

            Emp emp = new Emp();
            emp.setName("待删除_" + System.currentTimeMillis());
            emp.setAge(22);
            emp.setDept("临时");
            emp.setSalary(new BigDecimal("5000.00"));
            emp.setHireDate(new java.util.Date());
            mapper.addEmp(emp);
            int newId = emp.getId();
            System.out.println("新增待删除记录，ID = " + newId);

            int rows = mapper.deleteEmp(newId);
            sqlSession.commit();

            System.out.println("删除影响行数: " + rows);

            Emp deleted = mapper.findById(newId);
            System.out.println("删除后查询: " + deleted);
        }
    }
}