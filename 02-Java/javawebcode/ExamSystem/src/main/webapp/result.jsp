<%@ page contentType="text/html;charset=UTF-8" %>
<html>
<head>
    <title>考试成绩 - JavaWeb在线考试系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Microsoft YaHei", sans-serif;
        }

        body {
            background-color: #f5f7fa;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .result-card {
            background: white;
            width: 500px;
            padding: 50px 40px;
            border-radius: 16px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            text-align: center;
        }

        .result-card h2 {
            font-size: 24px;
            color: #333;
            margin-bottom: 25px;
        }

        .score-box {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: bold;
            color: white;
            background: linear-gradient(135deg, #429fff, #5677fc);
            box-shadow: 0 4px 15px rgba(66, 159, 255, 0.3);
        }

        .msg {
            font-size: 18px;
            margin-bottom: 35px;
            font-weight: 500;
        }

        .pass {
            color: #00b42a;
        }

        .fail {
            color: #ff4d4f;
        }

        .back-btn {
            display: inline-block;
            padding: 14px 40px;
            background: #429fff;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-size: 16px;
            transition: 0.2s;
        }

        .back-btn:hover {
            background: #358bee;
        }
    </style>
</head>

<body>
    <div class="result-card">
        <h2>考试完成！</h2>

        <div class="score-box">${score}</div>

        <%
        int score = (Integer) request.getAttribute("score");
        if (score >= 60) {
        %>
            <div class="msg pass">✅ 恭喜你，考试通过！</div>
        <% } else { %>
            <div class="msg fail">❌ 很遗憾，未通过考试！</div>
        <% } %>

        <a href="index.jsp" class="back-btn">返回重新考试</a>
    </div>
</body>
</html>