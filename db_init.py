import sqlite3

def init_db():
    conn = sqlite3.connect('tutor.db') #连接到数据库
    cursor = conn.cursor() #创建一个游标

    #创建student表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade TEXT,
        subject TEXT,
        contact TEXT,
        note TEXT
        )
    ''')

    #创建lessons表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        duration_hours REAL NOT NULL,
        hourly_rate REAL NOT NULL,
        amount REAL NOT NULL,
        paid INTEGER NOT NULL,
        note TEXT
        )
    ''')

    #提交并关闭
    conn.commit()
    conn.close()
    print('数据库初始化完成. ')


#测试函数
def test():
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO students (name,grade,subject,contact,note) VALUES (?,?,?,?,?)',
        ('测试张三','初二','数学','13800000000','这是测试数据')
    )

    conn.commit()
    print('插入成功')

    cursor.execute('SELECT * FROM students')
    all_students = cursor.fetchall()
    print('当前学生表里的数据:', all_students)

    conn.close()






if __name__ == '__main__':
    init_db()

    test()
