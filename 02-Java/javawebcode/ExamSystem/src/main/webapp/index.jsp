<%@ page contentType="text/html;charset=UTF-8" %>
<html>
<head>
    <title>登录 - JavaWeb考试系统</title>
    <style>
        .login{
            width:400px;
            margin:120px auto;
            padding:30px;
            border:1px solid #ccc;
            border-radius:8px;
        }
        input{
            width:100%;
            padding:10px;
            margin:8px 0;
        }
        button{
            width:100%;
            padding:10px;
            background:#429fff;
            color:white;
            border:none;
            font-size:16px;
        }
    </style>
</head>
<body>
<div class="login">
    <h2 style="text-align:center;">JavaWeb 考试系统登录</h2>
    <form action="login" method="post">
        用户名：<input type="text" name="username" placeholder="请输入用户名"><br>
        密&nbsp;&nbsp;&nbsp;码：<input type="password" name="password" placeholder="请输入密码"><br>
        <button type="submit">登录进入考试</button>
    </form>
</div>
</body>
</html>