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

public class EmpXmlUpdateTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    @Test
    public void testUpdateEmp() {
        System.out.println("========== XML方式-修改 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            EmpMapper mapper = sqlSession.getMapper(EmpMapper.class);

            Emp emp = mapper.findById(1);
            System.out.println("修改前: " + emp);

            emp.setName("张三_修改");
            emp.setAge(29);
            emp.setDept("产品部");
            emp.setSalary(new BigDecimal("16000.00"));

            int rows = mapper.updateEmp(emp);
            sqlSession.commit();

            Emp updated = mapper.findById(1);
            System.out.println("影响行数: " + rows);
            System.out.println("修改后: " + updated);
        }
    }
}