package com.exam.servlet;

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

@WebServlet("/submit")
public class SubmitServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, java.io.IOException {
        req.setCharacterEncoding("utf8");
        int score = 0;
        List<String> userAnswers = new ArrayList<>();
        List<String> realAnswers = new ArrayList<>();

        Connection conn = DBUtil.getConn();
        try {
            String sql = "SELECT answer FROM questions ORDER BY id";
            PreparedStatement ps = conn.prepareStatement(sql);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) realAnswers.add(rs.getString("answer"));

            for (int i = 1; i <= 20; i++) {
                String ans = req.getParameter("q" + i);
                if (ans == null) ans = "";
                userAnswers.add(ans);
            }

            for (int i = 0; i < 20; i++) {
                if (userAnswers.get(i).equals(realAnswers.get(i))) score += 5;
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            DBUtil.close(conn);
        }

        req.setAttribute("score", score);
        req.getRequestDispatcher("/result.jsp").forward(req, resp);
    }
}
