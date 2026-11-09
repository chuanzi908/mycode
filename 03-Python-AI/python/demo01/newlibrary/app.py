from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
import pymysql
from datetime import datetime, timedelta
import logging
import bcrypt
from functools import wraps

app = Flask(__name__)
app.secret_key = 'library_system_secret_key_2024'  # 请在生产环境中更改
CORS(app, supports_credentials=True)

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return None


def hash_password(password):
    """加密密码"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(hashed_password, user_password):
    """验证密码"""
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))


def login_required(f):
    """登录装饰器"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """管理员权限装饰器"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        if session.get('user_type') != 'admin':
            return jsonify({'success': False, 'message': '需要管理员权限'}), 403
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    """主页"""
    if 'user_id' in session:
        return render_template('index.html')
    return render_template('login.html')


@app.route('/login')
def login_page():
    """登录页面"""
    return render_template('login.html')


@app.route('/register')
def register_page():
    """注册页面"""
    return render_template('register.html')


@app.route('/admin')
def admin_page():
    """管理员页面"""
    if 'user_id' in session and session.get('user_type') == 'admin':
        return render_template('admin.html')
    return redirect(url_for('login_page'))


@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'})

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user:
                return jsonify({'success': False, 'message': '用户不存在'})

            if not check_password(user['password'], password):
                return jsonify({'success': False, 'message': '密码错误'})

            # 更新最后登录时间
            cursor.execute("UPDATE users SET last_login = NOW() WHERE user_id = %s", (user['user_id'],))

            # 设置session
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['user_type'] = user['user_type']
            session['email'] = user['email']

            conn.commit()

            return jsonify({
                'success': True,
                'message': '登录成功',
                'data': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'user_type': user['user_type'],
                    'email': user['email']
                }
            })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone', '')

    if not username or not password or not email:
        return jsonify({'success': False, 'message': '用户名、密码和邮箱不能为空'})

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            # 检查用户名是否已存在
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': '用户名已存在'})

            # 检查邮箱是否已存在
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': '邮箱已被注册'})

            # 创建用户
            hashed_password = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, password, email, phone, user_type)
                VALUES (%s, %s, %s, %s, 'member')
            """, (username, hashed_password, email, phone))

            user_id = cursor.lastrowid

            # 同时创建会员信息
            cursor.execute("""
                INSERT INTO members (name, email, phone, user_id)
                VALUES (%s, %s, %s, %s)
            """, (username, email, phone, user_id))

            conn.commit()

            return jsonify({'success': True, 'message': '注册成功，请登录'})

    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/logout', methods=['POST'])
def logout():
    """用户退出登录"""
    session.clear()
    return jsonify({'success': True, 'message': '退出成功'})


@app.route('/api/current-user')
def get_current_user():
    """获取当前登录用户信息"""
    if 'user_id' in session:
        return jsonify({
            'success': True,
            'data': {
                'user_id': session['user_id'],
                'username': session['username'],
                'user_type': session['user_type'],
                'email': session['email']
            }
        })
    return jsonify({'success': False, 'message': '未登录'})


@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    """管理员获取所有用户"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.*, m.member_id 
                FROM users u 
                LEFT JOIN members m ON u.user_id = m.user_id
                ORDER BY u.created_at DESC
            """)
            users = cursor.fetchall()

            # 隐藏密码
            for user in users:
                user.pop('password', None)

            return jsonify({'success': True, 'data': users})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/admin/users', methods=['POST'])
@admin_required
def add_user():
    """管理员添加用户"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone', '')
    user_type = data.get('user_type', 'member')

    if not username or not password or not email:
        return jsonify({'success': False, 'message': '用户名、密码和邮箱不能为空'})

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            # 检查用户名是否已存在
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': '用户名已存在'})

            # 检查邮箱是否已存在
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': '邮箱已被注册'})

            # 创建用户
            hashed_password = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, password, email, phone, user_type)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, hashed_password, email, phone, user_type))

            user_id = cursor.lastrowid

            # 如果是会员，同时创建会员信息
            if user_type == 'member':
                cursor.execute("""
                    INSERT INTO members (name, email, phone, user_id)
                    VALUES (%s, %s, %s, %s)
                """, (username, email, phone, user_id))

            conn.commit()

            return jsonify({'success': True, 'message': '用户添加成功'})

    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """管理员删除用户"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            # 检查是否是当前登录用户
            if user_id == session.get('user_id'):
                return jsonify({'success': False, 'message': '不能删除当前登录用户'})

            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()

            return jsonify({'success': True, 'message': '用户删除成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


# 修改原有的API，添加登录验证
@app.route('/api/books', methods=['GET'])
@login_required
def get_books():
    """获取所有图书"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT b.*, 
                       (b.total_copies - b.available_copies) as borrowed_count
                FROM books b
                ORDER BY b.book_id
            """)
            books = cursor.fetchall()
        return jsonify({'success': True, 'data': books})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/members', methods=['GET'])
@login_required
def get_members():
    """获取所有会员"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.*, u.username 
                FROM members m
                JOIN users u ON m.user_id = u.user_id
                ORDER BY m.member_id
            """)
            members = cursor.fetchall()
        return jsonify({'success': True, 'data': members})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/borrow', methods=['POST'])
@login_required
def borrow_book():
    """借阅图书"""
    data = request.json
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({'success': False, 'message': '请选择图书'})

    # 使用当前登录用户的member_id
    user_id = session.get('user_id')

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            # 获取会员ID
            cursor.execute("SELECT member_id FROM members WHERE user_id = %s", (user_id,))
            member = cursor.fetchone()

            if not member:
                return jsonify({'success': False, 'message': '请先完善会员信息'})

            member_id = member['member_id']

            # 检查图书是否可借
            cursor.execute("SELECT available_copies FROM books WHERE book_id = %s", (book_id,))
            book = cursor.fetchone()

            if not book:
                return jsonify({'success': False, 'message': '图书不存在'})

            if book['available_copies'] <= 0:
                return jsonify({'success': False, 'message': '图书已全部借出'})

            # 计算借阅日期和到期日期
            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=30)

            # 创建借阅记录
            cursor.execute("""
                INSERT INTO borrow_records (book_id, member_id, borrow_date, due_date, status)
                VALUES (%s, %s, %s, %s, '借阅中')
            """, (book_id, member_id, borrow_date, due_date))

            # 更新图书可用数量
            cursor.execute("""
                UPDATE books 
                SET available_copies = available_copies - 1 
                WHERE book_id = %s
            """, (book_id,))

            conn.commit()
            record_id = cursor.lastrowid

            return jsonify({
                'success': True,
                'message': '借阅成功',
                'data': {
                    'record_id': record_id,
                    'borrow_date': borrow_date.strftime('%Y-%m-%d'),
                    'due_date': due_date.strftime('%Y-%m-%d')
                }
            })

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        logger.error(f"借阅失败: {e}")
        return jsonify({'success': False, 'message': str(e)})
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/return', methods=['POST'])
@login_required
def return_book():
    """归还图书"""
    data = request.json
    record_id = data.get('record_id')

    if not record_id:
        return jsonify({'success': False, 'message': '请选择借阅记录'})

    user_id = session.get('user_id')

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            # 获取会员ID
            cursor.execute("SELECT member_id FROM members WHERE user_id = %s", (user_id,))
            member = cursor.fetchone()

            if not member:
                return jsonify({'success': False, 'message': '会员信息错误'})

            member_id = member['member_id']

            # 检查借阅记录是否存在且未归还
            cursor.execute("""
                SELECT * FROM borrow_records 
                WHERE record_id = %s AND member_id = %s AND status = '借阅中'
            """, (record_id, member_id))
            record = cursor.fetchone()

            if not record:
                return jsonify({'success': False, 'message': '借阅记录不存在或已归还'})

            return_date = datetime.now().date()

            # 更新借阅记录
            cursor.execute("""
                UPDATE borrow_records 
                SET return_date = %s, status = '已归还'
                WHERE record_id = %s
            """, (return_date, record_id))

            # 更新图书可用数量
            cursor.execute("""
                UPDATE books 
                SET available_copies = available_copies + 1 
                WHERE book_id = %s
            """, (record['book_id'],))

            conn.commit()

            return jsonify({
                'success': True,
                'message': '归还成功',
                'data': {
                    'return_date': return_date.strftime('%Y-%m-%d')
                }
            })

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        logger.error(f"归还失败: {e}")
        return jsonify({'success': False, 'message': str(e)})
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/borrow-records', methods=['GET'])
@login_required
def get_borrow_records():
    """获取当前用户的借阅记录"""
    user_id = session.get('user_id')

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败'})

    try:
        with conn.cursor() as cursor:
            # 获取会员ID
            cursor.execute("SELECT member_id FROM members WHERE user_id = %s", (user_id,))
            member = cursor.fetchone()

            if not member:
                return jsonify({'success': True, 'data': []})

            member_id = member['member_id']

            # 管理员可以查看所有记录，普通用户只能查看自己的
            if session.get('user_type') == 'admin':
                cursor.execute("""
                    SELECT br.*, 
                           b.title as book_title,
                           b.author as book_author,
                           m.name as member_name,
                           u.username
                    FROM borrow_records br
                    JOIN books b ON br.book_id = b.book_id
                    JOIN members m ON br.member_id = m.member_id
                    JOIN users u ON m.user_id = u.user_id
                    ORDER BY br.borrow_date DESC
                """)
            else:
                cursor.execute("""
                    SELECT br.*, 
                           b.title as book_title,
                           b.author as book_author,
                           m.name as member_name,
                           u.username
                    FROM borrow_records br
                    JOIN books b ON br.book_id = b.book_id
                    JOIN members m ON br.member_id = m.member_id
                    JOIN users u ON m.user_id = u.user_id
                    WHERE br.member_id = %s
                    ORDER BY br.borrow_date DESC
                """, (member_id,))

            records = cursor.fetchall()
        return jsonify({'success': True, 'data': records})
    except Exception as e:
        logger.error(f"获取借阅记录失败: {e}")
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


if __name__ == '__main__':
    # 安装bcrypt: pip install bcrypt
    app.run(debug=True, port=5000)