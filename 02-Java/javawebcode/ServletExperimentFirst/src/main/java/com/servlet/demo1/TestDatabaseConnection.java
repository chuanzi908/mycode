package com.servlet.demo1;

import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.SQLException;

/**
 * 测试数据库连接
 */
public class TestDatabaseConnection {

    public static void main(String[] args) {
        System.out.println("===========================================");
        System.out.println("开始测试数据库连接...");
        System.out.println("===========================================");

        Connection conn = null;
        try {
            // 测试连接
            System.out.println("1. 尝试连接数据库...");
            conn = DBUtil.getConnection();
            System.out.println("   ✓ 连接成功！");

            // 获取数据库信息
            System.out.println("\n2. 获取数据库信息:");
            DatabaseMetaData metaData = conn.getMetaData();
            System.out.println("   数据库产品：" + metaData.getDatabaseProductName());
            System.out.println("   数据库版本：" + metaData.getDatabaseProductVersion());
            System.out.println("   JDBC 版本：" + metaData.getJDBCMajorVersion() + "." + metaData.getJDBCMinorVersion());

            // 检查数据库是否存在
            System.out.println("\n3. 检查数据库 exam_system 是否存在...");
            String catalog = conn.getCatalog();
            System.out.println("   当前数据库：" + catalog);

            if ("exam_system".equals(catalog)) {
                System.out.println("   ✓ exam_system 数据库存在");
            } else {
                System.out.println("   ⚠ 当前不是 exam_system 数据库");
            }

            System.out.println("\n===========================================");
            System.out.println("测试完成！数据库连接正常");
            System.out.println("===========================================");

        } catch (SQLException e) {
            System.err.println("\n===========================================");
            System.err.println("✗ 测试失败！");
            System.err.println("===========================================");
            System.err.println("错误信息：" + e.getMessage());
            System.err.println("");
            System.err.println("请检查：");
            System.err.println("1. MySQL 服务是否已启动？");
            System.err.println("2. 数据库 exam_system 是否已创建？");
            System.err.println("3. 用户名密码是否正确？(当前配置：root/123456)");
            System.err.println("4. MySQL 端口是否为 3306？");
            System.err.println("===========================================");
            e.printStackTrace();
        } finally {
            DBUtil.close(conn, null, null);
        }
    }
}

