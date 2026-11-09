package com.house.dao;

import com.house.entity.House;
import com.house.util.DBUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

public class HouseDao {
    public List<House> list() {
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        List<House> list = new ArrayList<>();
        String sql = "select * from house where status=1";

        try {
            conn = DBUtil.getConnection();
            pstmt = conn.prepareStatement(sql);
            rs = pstmt.executeQuery();
            while (rs.next()) {
                House house = new House();
                house.setId(rs.getInt("id"));
                house.setTitle(rs.getString("title"));
                house.setArea(rs.getString("area"));
                house.setHouseType(rs.getString("house_type"));
                house.setPrice(rs.getBigDecimal("price"));
                list.add(house);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            DBUtil.close(conn, pstmt, rs);
        }
        return list;
    }
}