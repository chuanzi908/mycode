package com.chapter02;

import com.entity.Product;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.InputStream;
import java.math.BigDecimal;
import java.util.List;

/**
 * 可直接运行的演示类：一次性跑完 XML 与注解两套的六个方法。
 * 运行方式（任选其一）：
 *   1) 在 IDEA 里右键本文件 -> Run 'ProductDemo.main()'
 *   2) 命令行：mvn -q exec:java -Dexec.mainClass=com.chapter02.ProductDemo
 * 前置条件：MySQL 已启动，且所连库中存在 product 表（见 sql/product_employee_db.sql）。
 */
public class ProductDemo {

    public static void main(String[] args) throws Exception {
        // 1. 读取 mybatis-config.xml，构建 SqlSessionFactory
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(is);

        // openSession(true) = 自动提交，增删改无需手动 commit
        SqlSession session = factory.openSession(true);
        try {
            System.out.println("################ XML 方式（ProductMapper.xml） ################");
            demoSixMethods_Xml(session.getMapper(ProductMapper.class));
        } finally {
            session.close();
        }

        System.out.println();
        System.out.println("################ 注解方式（ProductMapperAnnotation） ################");
        session = factory.openSession(true);
        try {
            demoSixMethods_Annotation(session.getMapper(ProductMapperAnnotation.class));
        } finally {
            session.close();
        }

        System.out.println();
        System.out.println("全部演示结束。");
    }

    /** XML 版的六个方法 */
    private static void demoSixMethods_Xml(ProductMapper mapper) {
        // 1. 查全部
        List<Product> all = mapper.findAll();
        System.out.println("【1】查全部：共 " + all.size() + " 条");

        // 2. 按 ID 查
        System.out.println("【2】按 ID 查 id=1 -> " + mapper.findById(1));

        // 3. 新增 + 自增主键回填
        Product np = new Product();
        np.setName("Demo商品_" + System.currentTimeMillis());
        np.setPrice(new BigDecimal("88.88"));
        np.setStock(10);
        np.setCategory("演示");
        System.out.println("【3】新增前 id = " + np.getId());
        System.out.println("    影响行数 = " + mapper.insert(np) + "，回填后 id = " + np.getId());

        // 4. 修改
        np.setPrice(new BigDecimal("66.66"));
        np.setStock(5);
        System.out.println("【4】修改影响行数 = " + mapper.update(np));

        // 5. 删除（删掉上面新增的演示数据，保持库干净）
        System.out.println("【5】删除影响行数 = " + mapper.deleteById(np.getId()));

        // 6. 模糊查询
        System.out.println("【6】模糊查询 keyword=手机 -> ");
        mapper.findByKeyword("手机").forEach(p -> System.out.println("    " + p));
    }

    /** 注解版的六个方法（与上面一一对应） */
    private static void demoSixMethods_Annotation(ProductMapperAnnotation mapper) {
        // 1. 查全部
        List<Product> all = mapper.findAll();
        System.out.println("【1】查全部：共 " + all.size() + " 条");

        // 2. 按 ID 查
        System.out.println("【2】按 ID 查 id=2 -> " + mapper.findById(2));

        // 3. 新增 + 自增主键回填
        Product np = new Product();
        np.setName("Anno商品_" + System.currentTimeMillis());
        np.setPrice(new BigDecimal("99.99"));
        np.setStock(20);
        np.setCategory("演示");
        System.out.println("【3】新增前 id = " + np.getId());
        System.out.println("    影响行数 = " + mapper.insert(np) + "，回填后 id = " + np.getId());

        // 4. 修改
        np.setPrice(new BigDecimal("77.77"));
        np.setStock(8);
        System.out.println("【4】修改影响行数 = " + mapper.update(np));

        // 5. 删除
        System.out.println("【5】删除影响行数 = " + mapper.deleteById(np.getId()));

        // 6. 模糊查询
        System.out.println("【6】模糊查询 keyword=电脑 -> ");
        mapper.findByKeyword("电脑").forEach(p -> System.out.println("    " + p));
    }
}
