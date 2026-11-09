from flask import Flask, render_template, request, jsonify
from db import get_db
from datetime import date

app = Flask(__name__)

# 首页：图书列表
@app.route('/')
def index():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
    return render_template('index.html', books=books)

# 借书接口
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.json
    book_id = data['book_id']
    member_id = data['member_id']
    due_date = data['due_date']

    db = get_db()
    with db.cursor() as cur:
        # 检查库存
        cur.execute("SELECT available_copies FROM books WHERE id=%s", (book_id,))
        book = cur.fetchone()
        if book['available_copies'] <= 0:
            return jsonify({'success': False, 'msg': '库存不足'})

        # 插入借阅记录
        cur.execute("""
            INSERT INTO borrow_records(book_id, member_id, borrow_date, due_date, status)
            VALUES (%s, %s, %s, %s, '借阅中')
        """, (book_id, member_id, date.today(), due_date))

        # 更新库存
        cur.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id=%s", (book_id,))

    return jsonify({'success': True})

# 还书接口
@app.route('/return', methods=['POST'])
def return_book():
    record_id = request.json['record_id']

    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT book_id FROM borrow_records WHERE record_id=%s", (record_id,))
        record = cur.fetchone()

        cur.execute("""
            UPDATE borrow_records
            SET return_date=%s, status='已归还'
            WHERE record_id=%s
        """, (date.today(), record_id))

        cur.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id=%s", (record['book_id'],))

    return jsonify({'success': True})

# 借阅记录查询
@app.route('/records')
def records():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("""
            SELECT r.*, b.title, m.name
            FROM borrow_records r
            JOIN books b ON r.book_id = b.id
            JOIN members m ON r.member_id = m.member_id
        """)
        records = cur.fetchall()
    return render_template('records.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)