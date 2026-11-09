package com.exam.servlet;

import com.exam.entity.Question;
import com.exam.util.DBUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

@WebServlet("/exam")
public class ExamServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, java.io.IOException {
        List<Question> list = new ArrayList<>();
        Connection conn = DBUtil.getConn();
        try {
            String sql = "SELECT * FROM questions";
            PreparedStatement ps = conn.prepareStatement(sql);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                Question q = new Question();
                q.setId(rs.getInt("id"));
                q.setTitle(rs.getString("title"));
                q.setOptionA(rs.getString("optionA"));
                q.setOptionB(rs.getString("optionB"));
                q.setOptionC(rs.getString("optionC"));
                q.setOptionD(rs.getString("optionD"));
                q.setAnswer(rs.getString("answer"));
                list.add(q);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            DBUtil.close(conn);
        }
        req.setAttribute("questions", list);
        req.getRequestDispatcher("/exam.jsp").forward(req, resp);
    }
}