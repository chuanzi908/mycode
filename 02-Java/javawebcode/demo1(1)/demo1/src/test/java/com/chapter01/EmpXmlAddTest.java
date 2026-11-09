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

public class EmpXmlAddTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    @Test
    public void testAddEmp() {
        System.out.println("========== XML方式-新增+自增主键回填 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            EmpMapper mapper = sqlSession.getMapper(EmpMapper.class);

            Emp emp = new Emp();
            emp.setName("XM新增_" + System.currentTimeMillis());
            emp.setAge(28);
            emp.setDept("运维部");
            emp.setSalary(new BigDecimal("9500.00"));
            emp.setHireDate(new java.util.Date());

            int rows = mapper.addEmp(emp);
            sqlSession.commit();

            System.out.println("影响行数: " + rows);
            System.out.println("自增主键ID: " + emp.getId());
            System.out.println("新增对象: " + emp);
        }
    }
}