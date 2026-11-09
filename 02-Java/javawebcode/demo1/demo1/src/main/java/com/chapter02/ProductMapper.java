package com.chapter02;

import com.entity.Product;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * XML 方式：六个方法，全部 SQL 写在 resources/com/chapter02/ProductMapper.xml 中。
 * 操作表：product（非 user 表）。
 *
 * 1. findAll                        查全部
 * 2. findById                       按 ID 查
 * 3. insert                         新增 + 自增主键回填
 * 4. update                         修改
 * 5. deleteById                     删除
 * 6. findByKeyword                  模糊查询（name 或 category）
 */
public interface ProductMapper {

    /** 1. 查全部 */
    List<Product> findAll();

    /** 2. 按 ID 查 */
    Product findById(@Param("id") Integer id);

    /** 3. 新增（useGeneratedKeys 回填自增主键到 product.id） */
    int insert(Product product);

    /** 4. 修改 */
    int update(Product product);

    /** 5. 删除 */
    int deleteById(@Param("id") Integer id);

    /** 6. 模糊查询：name 或 category 中包含关键字 */
    List<Product> findByKeyword(@Param("keyword") String keyword);
}
