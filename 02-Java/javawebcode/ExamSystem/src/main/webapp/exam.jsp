<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="com.exam.entity.Question,java.util.*" %>
<html>
<head>
    <title>JavaWeb 在线考试</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Microsoft YaHei", sans-serif;
        }

        body {
            background-color: #f5f7fa;
            padding-bottom: 100px;
        }

        .header {
            background: linear-gradient(135deg, #429fff, #5677fc);
            color: white;
            padding: 22px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .container {
            width: 820px;
            margin: 30px auto;
        }

        .question-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: 0.2s;
        }

        .question-card:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        }

        .title {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 16px;
            line-height: 1.6;
        }

        .options {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .option {
            padding: 10px 14px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
            font-size: 15px;
        }

        .option:hover {
            background-color: #eef5ff;
        }

        input[type="radio"] {
            margin-right: 8px;
            transform: scale(1.1);
        }

        .submit-box {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: white;
            padding: 18px;
            text-align: center;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }

        .submit-btn {
            padding: 12px 45px;
            background: #429fff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: 0.2s;
        }

        .submit-btn:hover {
            background: #358bee;
        }
    </style>
</head>
<body>

<div class="header">
    <h2>JavaWeb 在线考试系统（20题）</h2>
</div>

<div class="container">
    <form action="submit" method="post">
        <%
            List<Question> questions = (List<Question>) request.getAttribute("questions");
            int num = 1;
            for (Question q : questions) {
        %>
        <div class="question-card">
            <div class="title"><%=num++%>. <%=q.getTitle()%></div>
            <div class="options">
                <label class="option">
                    <input type="radio" name="q<%=q.getId()%>" value="A" required>
                    A. <%=q.getOptionA()%>
                </label>
                <label class="option">
                    <input type="radio" name="q<%=q.getId()%>" value="B">
                    B. <%=q.getOptionB()%>
                </label>
                <label class="option">
                    <input type="radio" name="q<%=q.getId()%>" value="C">
                    C. <%=q.getOptionC()%>
                </label>
                <label class="option">
                    <input type="radio" name="q<%=q.getId()%>" value="D">
                    D. <%=q.getOptionD()%>
                </label>
            </div>
        </div>
        <% } %>

        <div class="submit-box">
            <button class="submit-btn" type="submit">提交试卷</button>
        </div>
    </form>
</div>

</body>
</html>