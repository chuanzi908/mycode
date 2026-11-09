package com.servlet.demo1;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * 在线考试系统 - 答题界面 Servlet
 * 访问路径：http://localhost:8080/ServletExperimentFirst/exam
 */
@WebServlet("/exam")
public class ExamServlet extends HttpServlet {
    
    // 试题数据类
    private static class Question {
        int number;
        String text;
        String optionA;
        String optionB;
        String optionC;
        String optionD;
        String correctAnswer;
        
        public Question(int number, String text, String optionA, String optionB, 
                       String optionC, String optionD, String correctAnswer) {
            this.number = number;
            this.text = text;
            this.optionA = optionA;
            this.optionB = optionB;
            this.optionC = optionC;
            this.optionD = optionD;
            this.correctAnswer = correctAnswer;
        }
    }
    
    // 存储所有试题
    private List<Question> questions = new ArrayList<>();

    // 初始化：从数据库加载试题
    @Override
    public void init() throws ServletException {
        loadQuestionsFromDatabase();
    }

    // 从数据库加载试题
    private void loadQuestionsFromDatabase() {
        String sql = "SELECT question_number, question_text, option_a, option_b, option_c, option_d, correct_answer " +
                     "FROM exam_questions ORDER BY question_number";
        
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                Question q = new Question(
                    rs.getInt("question_number"),
                    rs.getString("question_text"),
                    rs.getString("option_a"),
                    rs.getString("option_b"),
                    rs.getString("option_c"),
                    rs.getString("option_d"),
                    rs.getString("correct_answer")
                );
                questions.add(q);
            }
            
            System.out.println("✓ 从数据库加载了 " + questions.size() + " 道题目");
            
        } catch (SQLException e) {
            System.err.println("✗ 加载题目失败：" + e.getMessage());
            e.printStackTrace();
        }
    }

    // 处理 GET 请求：展示答题界面
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();

        // 生成答题界面 HTML
        out.println("<!DOCTYPE html>");
        out.println("<html lang='zh-CN'>");
        out.println("<head>");
        out.println("<meta charset='UTF-8'>");
        out.println("<title>JavaWeb 在线考试 - 答题界面</title>");
        out.println("<style>");
        out.println("body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }");
        out.println(".exam-container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }");
        out.println(".question { margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #eee; }");
        out.println(".question h4 { margin: 0 0 10px 0; color: #333; }");
        out.println(".option { margin: 8px 0; padding-left: 5px; }");
        out.println(".submit-btn { padding: 12px 24px; background-color: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }");
        out.println(".submit-btn:hover { background-color: #218838; }");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");
        out.println("<div class='exam-container'>");
        out.println("<h2 style='text-align:center; margin-bottom: 30px;'>JavaWeb 核心知识单选题（共 20 题，每题 5 分）</h2>");
        // 表单提交到当前 Servlet 的 POST 方法，处理判分
        out.println("<form action='/ServletExperimentFirst/exam' method='post'>");

        // 循环展示所有试题
        for (Question q : questions) {
            out.println("<div class='question'>");
            out.println("<h4>" + q.number + ". " + q.text + "</h4>");
            // 选项 A/B/C/D
            out.println("<div class='option'><input type='radio' name='q" + q.number + "' value='A' required> A. " + q.optionA + "</div>");
            out.println("<div class='option'><input type='radio' name='q" + q.number + "' value='B'> B. " + q.optionB + "</div>");
            out.println("<div class='option'><input type='radio' name='q" + q.number + "' value='C'> C. " + q.optionC + "</div>");
            out.println("<div class='option'><input type='radio' name='q" + q.number + "' value='D'> D. " + q.optionD + "</div>");
            out.println("</div>");
        }

        out.println("<div style='text-align:center; margin-top: 30px;'>");
        out.println("<button type='submit' class='submit-btn'>提交试卷</button>");
        out.println("</div>");
        out.println("</form>");
        out.println("</div>");
        out.println("</body>");
        out.println("</html>");

        out.close();
    }

    // 处理 POST 请求：提交答案后判分
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();

        int score = 0; // 总分
        StringBuilder result = new StringBuilder(); // 判分结果

        // 遍历所有题目，对比答案
        for (Question q : questions) {
            // 获取用户提交的答案
            String userAnswer = request.getParameter("q" + q.number);
            // 获取正确答案
            String correctAnswer = q.correctAnswer;

            // 判分（每题 5 分）
            if (correctAnswer.equals(userAnswer)) {
                score += 5;
                result.append("<p style='color:green;'>第").append(q.number).append("题：回答正确 ✔</p>");
            } else {
                result.append("<p style='color:red;'>第").append(q.number).append("题：回答错误 ❌ 正确答案：").append(correctAnswer).append("</p>");
            }
        }

        // 生成判分结果页面
        out.println("<!DOCTYPE html>");
        out.println("<html lang='zh-CN'>");
        out.println("<head>");
        out.println("<meta charset='UTF-8'>");
        out.println("<title>考试结果 - JavaWeb 在线考试</title>");
        out.println("<style>");
        out.println("body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }");
        out.println(".result-container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }");
        out.println(".score { text-align:center; font-size: 24px; margin-bottom: 20px; color: #dc3545; }");
        out.println(".back-btn { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 20px; }");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");
        out.println("<div class='result-container'>");
        out.println("<h2 style='text-align:center;'>考试结果</h2>");
        out.println("<div class='score'>你的得分：" + score + " / " + (questions.size() * 5) + "分</div>");
        out.println("<hr>");
        out.println("<h3>答题详情：</h3>");
        out.println(result.toString());
        out.println("<div style='text-align:center; margin-top: 30px;'>");
        out.println("<a href='/ServletExperimentFirst/exam' class='back-btn'>重新答题</a>");
        out.println("&nbsp;&nbsp;");
        out.println("<a href='/ServletExperimentFirst/login' class='back-btn'>返回登录页</a>");
        out.println("</div>");
        out.println("</div>");
        out.println("</body>");
        out.println("</html>");

        out.close();
    }
}