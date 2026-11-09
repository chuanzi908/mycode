package com.chapter02;

import com.entity.Product;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.InputStream;
import java.math.BigDecimal;
import java.util.List;

/**
 * 注解方式六个方法的测试（表：product）。
 * 与 ProductMapperTest 一一对应，方便对比 XML 与注解两种写法。
 */
public class ProductMapperAnnotationTest {

    private SqlSessionFactory sqlSessionFactory;

    @BeforeEach
    public void init() throws Exception {
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
    }

    /** 1. 查全部 */
    @Test
    public void testFindAll() {
        System.out.println("========== [注解] 1. 查全部 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            ProductMapperAnnotation mapper = sqlSession.getMapper(ProductMapperAnnotation.class);
            List<Product> list = mapper.findAll();
            list.forEach(System.out::println);
        }
    }

    /** 2. 按 ID 查 */
    @Test
    public void testFindById() {
        System.out.println("========== [注解] 2. 按 ID 查 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            ProductMapperAnnotation mapper = sqlSession.getMapper(ProductMapperAnnotation.class);
            Product product = mapper.findById(2);
            System.out.println(product);
        }
    }

    /** 3. 新增 + 自增主键回填 */
    @Test
    public void testInsert() {
        System.out.println("========== [注解] 3. 新增 + 自增主键回填 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession(true)) {
            ProductMapperAnnotation mapper = sqlSession.getMapper(ProductMapperAnnotation.class);

            Product product = new Product();
            product.setName("注解测试商品_" + System.currentTimeMillis());
            product.setPrice(new BigDecimal("299.00"));
            product.setStock(30);
            product.setCategory("注解分类");

            System.out.println("新增前 id = " + product.getId()); // null
            int rows = mapper.insert(product);
            System.out.println("影响行数 = " + rows);
            System.out.println("回填后的自增主键 id = " + product.getId());
        }
    }

    /** 4. 修改 */
    @Test
    public void testUpdate() {
        System.out.println("========== [注解] 4. 修改 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession(true)) {
            ProductMapperAnnotation mapper = sqlSession.getMapper(ProductMapperAnnotation.class);

            Product product = mapper.findById(3);
            System.out.println("修改前: " + product);

            product.setPrice(new BigDecimal("13999.00"));
            product.setStock(20);
            int rows = mapper.update(product);
            System.out.println("影响行数 = " + rows);
            System.out.println("修改后: " + mapper.findById(3));
        }
    }

    /** 5. 删除 */
    @Test
    public void testDeleteById() {
        System.out.println("========== [注解] 5. 删除 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession(true)) {
            ProductMapperAnnotation mapper = sqlSession.getMapper(ProductMapperAnnotation.class);

            Product product = new Product();
            product.setName("注解待删除商品");
            product.setPrice(new BigDecimal("1.00"));
            product.setStock(1);
            product.setCategory("临时");
            mapper.insert(product);
            System.out.println("已新增 id = " + product.getId());

            int rows = mapper.deleteById(product.getId());
            System.out.println("影响行数 = " + rows);
            System.out.println("删除后查询结果 = " + mapper.findById(product.getId())); // null
        }
    }

    /** 6. 模糊查询 */
    @Test
    public void testFindByKeyword() {
        System.out.println("========== [注解] 6. 模糊查询 ==========");
        try (SqlSession sqlSession = sqlSessionFactory.openSession()) {
            ProductMapperAnnotation mapper = sqlSession.getMapper(ProductMapperAnnotation.class);
            List<Product> list = mapper.findByKeyword("电脑");
            System.out.println("关键字【电脑】命中 " + list.size() + " 条：");
            list.forEach(System.out::println);
        }
    }
}
