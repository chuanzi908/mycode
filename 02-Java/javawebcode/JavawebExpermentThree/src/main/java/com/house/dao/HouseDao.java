package com.house.dao;

import com.house.entity.House;
import com.house.util.DruidUtil;

import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * 房源数据访问层
 * 实现房源的增删改查、条件筛选等数据库操作
 */
public class HouseDao {

    /**
     * 查询所有已发布房源（普通用户可见）
     * @return 房源集合
     */
    public List<House> findAllPublishHouse() {
        List<House> houseList = new ArrayList<>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        // 只查询状态为1（已发布）的房源
        String sql = "select * from house where status = 1";

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            rs = pstmt.executeQuery();
            while (rs.next()) {
                House house = getHouseFromRs(rs);
                houseList.add(house);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt, rs);
        }
        return houseList;
    }

    /**
     * 查询所有房源（管理员后台使用，包含未审核房源）
     * @return 房源集合
     */
    public List<House> findAllHouse() {
        List<House> houseList = new ArrayList<>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        String sql = "select * from house";

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            rs = pstmt.executeQuery();
            while (rs.next()) {
                House house = getHouseFromRs(rs);
                houseList.add(house);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt, rs);
        }
        return houseList;
    }

    /**
     * 根据ID查询单个房源
     * @param id 房源ID
     * @return 房源对象
     */
    public House findHouseById(Integer id) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        House house = null;
        String sql = "select * from house where id = ?";

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            pstmt.setInt(1, id);
            rs = pstmt.executeQuery();
            if (rs.next()) {
                house = getHouseFromRs(rs);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt, rs);
        }
        return house;
    }

    /**
     * 条件筛选房源：区域、户型、价格区间
     * @param area 区域
     * @param houseType 户型
     * @param minPrice 最低价格
     * @param maxPrice 最高价格
     * @return 筛选后的房源集合
     */
    public List<House> findHouseByCondition(String area, String houseType, BigDecimal minPrice, BigDecimal maxPrice) {
        List<House> houseList = new ArrayList<>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        // 动态拼接SQL，实现模糊查询+区间查询
        StringBuilder sql = new StringBuilder("select * from house where status = 1 ");
        List<Object> params = new ArrayList<>();

        if (area != null && !"".equals(area)) {
            sql.append(" and area like ? ");
            params.add("%" + area + "%");
        }
        if (houseType != null && !"".equals(houseType)) {
            sql.append(" and house_type like ? ");
            params.add("%" + houseType + "%");
        }
        if (minPrice != null) {
            sql.append(" and price >= ? ");
            params.add(minPrice);
        }
        if (maxPrice != null) {
            sql.append(" and price <= ? ");
            params.add(maxPrice);
        }

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql.toString());
            // 给占位符赋值
            for (int i = 0; i < params.size(); i++) {
                pstmt.setObject(i + 1, params.get(i));
            }
            rs = pstmt.executeQuery();
            while (rs.next()) {
                House house = getHouseFromRs(rs);
                houseList.add(house);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt, rs);
        }
        return houseList;
    }

    /**
     * 新增房源（管理员添加）
     * @param house 房源对象
     * @return 受影响行数 >0 表示添加成功
     */
    public int addHouse(House house) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        int rows = 0;
        String sql = "insert into house(title,area,house_type,price,address,status) values (?,?,?,?,?,?)";

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, house.getTitle());
            pstmt.setString(2, house.getArea());
            pstmt.setString(3, house.getHouseType());
            pstmt.setBigDecimal(4, house.getPrice());
            pstmt.setString(5, house.getAddress());
            pstmt.setInt(6, house.getStatus());
            rows = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt);
        }
        return rows;
    }

    /**
     * 修改房源信息
     * @param house 房源对象
     * @return 受影响行数 >0 表示修改成功
     */
    public int updateHouse(House house) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        int rows = 0;
        String sql = "update house set title=?,area=?,house_type=?,price=?,address=?,status=? where id=?";

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, house.getTitle());
            pstmt.setString(2, house.getArea());
            pstmt.setString(3, house.getHouseType());
            pstmt.setBigDecimal(4, house.getPrice());
            pstmt.setString(5, house.getAddress());
            pstmt.setInt(6, house.getStatus());
            pstmt.setInt(7, house.getId());
            rows = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt);
        }
        return rows;
    }

    /**
     * 根据ID删除房源
     * @param id 房源ID
     * @return 受影响行数 >0 表示删除成功
     */
    public int deleteHouseById(Integer id) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        int rows = 0;
        String sql = "delete from house where id = ?";

        try {
            conn = DruidUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            pstmt.setInt(1, id);
            rows = pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DruidUtil.close(conn, pstmt);
        }
        return rows;
    }

    /**
     * 封装ResultSet结果集为House对象（抽取公共方法，代码复用）
     * @param rs 结果集
     * @return House对象
     * @throws SQLException 数据库异常
     */
    private House getHouseFromRs(ResultSet rs) throws SQLException {
        House house = new House();
        house.setId(rs.getInt("id"));
        house.setTitle(rs.getString("title"));
        house.setArea(rs.getString("area"));
        house.setHouseType(rs.getString("house_type"));
        house.setPrice(rs.getBigDecimal("price"));
        house.setAddress(rs.getString("address"));
        house.setStatus(rs.getInt("status"));
        return house;
    }
}