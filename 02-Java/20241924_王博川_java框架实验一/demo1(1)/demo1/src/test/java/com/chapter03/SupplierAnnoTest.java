package com.chapter03;

import com.entity.SupplierProductCustomer;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.InputStream;
import java.math.BigDecimal;
import java.util.List;

public class SupplierAnnoTest {

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
    public void test1_findBySupplierName() {
        System.out.println("\n---- 查询：供应商名（注解方式）----");
        System.out.println("  条件：供应商名含\"华为\"");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SupplierMapper mapper = sqlSession.getMapper(SupplierMapper.class);
            List<SupplierProductCustomer> list = mapper.findBySupplierName("华为");
            printResult(list);
        }
    }

    @Test
    public void test2_findBySupplierAndProduct() {
        System.out.println("\n---- 查询：供应商名 + 商品名（注解方式）----");
        System.out.println("  条件：供应商名含\"苹果\"，商品名含\"Mac\"");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SupplierMapper mapper = sqlSession.getMapper(SupplierMapper.class);
            List<SupplierProductCustomer> list = mapper.findBySupplierAndProduct("苹果", "Mac");
            printResult(list);
        }
    }

    @Test
    public void test3_findBySupplierIdAndCustomer() {
        System.out.println("\n---- 查询：供应商ID + 客户名（注解方式）----");
        System.out.println("  条件：供应商ID=3（苹果），客户名含\"刘\"");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SupplierMapper mapper = sqlSession.getMapper(SupplierMapper.class);
            List<SupplierProductCustomer> list = mapper.findBySupplierIdAndCustomer(3, "刘");
            printResult(list);
        }
    }

    @Test
    public void test4_findBySupplierAndPriceRange() {
        System.out.println("\n---- 查询：供应商名 + 价格范围（注解方式）----");
        System.out.println("  条件：供应商名含\"华为\"，价格1000元至8000元");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SupplierMapper mapper = sqlSession.getMapper(SupplierMapper.class);
            List<SupplierProductCustomer> list = mapper.findBySupplierAndPriceRange(
                    "华为", new BigDecimal("1000"), new BigDecimal("8000"));
            printResult(list);
        }
    }

    @Test
    public void test5_findBySupplierProductAndDate() {
        System.out.println("\n---- 查询：供应商ID + 商品名 + 日期范围（注解方式）----");
        System.out.println("  条件：供应商ID=3（苹果），商品名含\"Mac\"，日期2024-01-01至2026-12-31");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            SupplierMapper mapper = sqlSession.getMapper(SupplierMapper.class);
            List<SupplierProductCustomer> list = mapper.findBySupplierProductAndDate(
                    3, "Mac", "2024-01-01", "2026-12-31");
            printResult(list);
        }
    }
}