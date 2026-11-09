# fix_admin.py
import pymysql
import bcrypt

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': '123456',
    'database': 'newlibrary',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


def fix_admin_password():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 生成admin123的bcrypt加密密码
        password = 'admin123'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        print(f"生成的加密密码: {hashed_password}")

        # 检查admin用户是否存在
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        user = cursor.fetchone()

        if user:
            # 更新密码
            cursor.execute("UPDATE users SET password = %s WHERE username = 'admin'", (hashed_password,))
            print("✅ 管理员密码已更新")
        else:
            # 创建admin用户
            cursor.execute("""
                INSERT INTO users (username, password, email, user_type)
                VALUES ('admin', %s, 'admin@library.com', 'admin')
            """, (hashed_password,))
            print("✅ 管理员账号已创建")

        conn.commit()
        conn.close()

        print("✅ 修复完成！")
        print("👉 请使用以下账号登录：")
        print("   用户名: admin")
        print("   密码: admin123")

    except Exception as e:
        print(f"❌ 修复失败: {e}")


if __name__ == '__main__':
    fix_admin_password()