package com.chapter03;

import com.entity.CustomerProductDetail;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.InputStream;
import java.math.BigDecimal;
import java.util.List;

public class SimpleChainAnnoTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    private void printResult(List<?> list) {
        if (list.isEmpty()) {
            System.out.println("  （无结果）");
        } else {
            for (int i = 0; i < list.size(); i++) {
                System.out.println(list.get(i));
            }
        }
        System.out.println("  ---- 共" + list.size() + "条 ----\n");
    }

    @Test
    public void test1_findByCustomerAndProduct() {
        System.out.println("\n---- 查询：客户名 + 商品名（注解方式）----");
        System.out.println("  条件：客户名含\"Liu\"，商品名含\"Mac\"");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SimpleChainMapper mapper = sqlSession.getMapper(SimpleChainMapper.class);
            List<CustomerProductDetail> list = mapper.findByCustomerAndProduct("Liu", "Mac");
            printResult(list);
        }
    }

    @Test
    public void test2_findByCustomerUserDate() {
        System.out.println("\n---- 查询：客户ID + 客户名 + 日期范围（注解方式）----");
        System.out.println("  条件：ID=1，客户名含\"Liu\"，日期2024-01-01至2026-12-31");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SimpleChainMapper mapper = sqlSession.getMapper(SimpleChainMapper.class);
            List<CustomerProductDetail> list = mapper.findByCustomerUserDate(
                    1, "Liu", "2024-01-01", "2026-12-31");
            printResult(list);
        }
    }

    @Test
    public void test3_findByCustomerIdAndProductId() {
        System.out.println("\n---- 查询：客户ID + 商品ID（注解方式）----");
        System.out.println("  条件：客户ID=1，商品ID=1");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SimpleChainMapper mapper = sqlSession.getMapper(SimpleChainMapper.class);
            List<CustomerProductDetail> list = mapper.findByCustomerIdAndProductIdAnno(1, 1);
            printResult(list);
        }
    }

    @Test
    public void test4_findByCustomerAndPriceRange() {
        System.out.println("\n---- 查询：客户名 + 价格范围（注解方式）----");
        System.out.println("  条件：客户名含\"Liu\"，价格1000元至8000元");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SimpleChainMapper mapper = sqlSession.getMapper(SimpleChainMapper.class);
            List<CustomerProductDetail> list = mapper.findByCustomerAndPriceRangeAnno(
                    "Liu", new BigDecimal("1000"), new BigDecimal("8000"));
            printResult(list);
        }
    }

    @Test
    public void test5_findByCustomerProductAndDate() {
        System.out.println("\n---- 查询：客户ID + 商品名 + 日期范围（注解方式）----");
        System.out.println("  条件：客户ID=1，商品名含\"Mac\"，日期2024-01-01至2026-12-31");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SimpleChainMapper mapper = sqlSession.getMapper(SimpleChainMapper.class);
            List<CustomerProductDetail> list = mapper.findByCustomerProductAndDateAnno(
                    1, "Mac", "2024-01-01", "2026-12-31");
            printResult(list);
        }
    }
}