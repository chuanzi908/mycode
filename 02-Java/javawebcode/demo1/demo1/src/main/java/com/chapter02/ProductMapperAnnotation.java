package com.chapter02;

import com.entity.Product;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

/**
 * 注解方式：六个方法，SQL 直接写在注解里，无需 ProductMapperAnnotation.xml。
 * 操作表：product（非 user 表）。
 *
 * 接口必须注册进 mybatis-config.xml 的 <mappers>，例如：
 *   <mapper class="com.chapter02.ProductMapperAnnotation"/>
 *
 * 1. findAll         查全部
 * 2. findById        按 ID 查
 * 3. insert          新增 + 自增主键回填
 * 4. update          修改
 * 5. deleteById      删除
 * 6. findByKeyword   模糊查询（name 或 category）
 */
public interface ProductMapperAnnotation {

    /** 1. 查全部 */
    @Select("SELECT * FROM product")
    List<Product> findAll();

    /** 2. 按 ID 查 */
    @Select("SELECT * FROM product WHERE id = #{id}")
    Product findById(@Param("id") Integer id);

    /** 3. 新增 + 自增主键回填（@Options 把生成的 id 回填到 product.id） */
    @Insert("INSERT INTO product(name, price, stock, category) " +
            "VALUES(#{name}, #{price}, #{stock}, #{category})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Product product);

    /** 4. 修改 */
    @Update("UPDATE product SET name = #{name}, price = #{price}, " +
            "stock = #{stock}, category = #{category} WHERE id = #{id}")
    int update(Product product);

    /** 5. 删除 */
    @Delete("DELETE FROM product WHERE id = #{id}")
    int deleteById(@Param("id") Integer id);

    /** 6. 模糊查询：name 或 category 中包含关键字 */
    @Select("SELECT * FROM product " +
            "WHERE name LIKE CONCAT('%', #{keyword}, '%') " +
            "   OR category LIKE CONCAT('%', #{keyword}, '%')")
    List<Product> findByKeyword(@Param("keyword") String keyword);
}
