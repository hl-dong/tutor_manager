import sqlite3

def generate_test_data():
    # 1. 初始化建表（顺便调用一下之前的建表逻辑，防止表不存在）
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()

    # 创建 students 表（如果已存在则忽略）
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

    # 创建 lessons 表
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

    # 2. 插入学生数据
    # 注意：因为设置了 AUTOINCREMENT，插入后 ID 会自动生成 1, 2, 3
    students_data = [
        ('张三', '初二', '数学', '13800000001', '周末上课'),
        ('李四', '高一', '物理', '13800000002', '晚辅导'),
        ('王五', '六年级', '英语', '13800000003', '基础薄弱')
    ]
    cursor.executemany(
        "INSERT INTO students (name, grade, subject, contact, note) VALUES (?, ?, ?, ?, ?)",
        students_data
    )

    # 3. 插入课时数据 (student_id 对应上面的 1=张三, 2=李四, 3=王五)
    lessons_data = [
        # 张三的课 (2026-09 和 2026-10)
        (1, '2026-09-15', 2.0, 150.0, 300.0, 1, '讲了函数'),        # 已付
        (1, '2026-10-05', 1.5, 150.0, 225.0, 0, '讲了列表'),        # 未付
        (1, '2026-10-12', 2.0, 150.0, 300.0, 1, '讲了字典'),        # 已付

        # 李四的课 (2026-09 和 2026-10)
        (2, '2026-09-20', 1.5, 200.0, 300.0, 1, '力学基础'),        # 已付
        (2, '2026-10-04', 2.0, 200.0, 400.0, 0, '牛顿定律'),        # 未付

        # 王五的课 (2026-10)
        (3, '2026-10-02', 1.0, 120.0, 120.0, 1, '单词听写'),        # 已付
        (3, '2026-10-10', 1.0, 120.0, 120.0, 0, '语法讲解')         # 未付
    ]
    cursor.executemany(
        "INSERT INTO lessons (student_id, date, duration_hours, hourly_rate, amount, paid, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
        lessons_data
    )

    # 4. 提交并关闭
    conn.commit()
    conn.close()
    print("测试数据生成完毕！")

if __name__ == '__main__':
    generate_test_data()