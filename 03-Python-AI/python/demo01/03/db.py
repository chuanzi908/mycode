import pymysql

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='wenjingelibrary',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )