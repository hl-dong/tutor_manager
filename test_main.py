from main import calculate_amount

def test_calculate_amount():
    # 测试1：正常整数 (2小时 * 150元/时 = 300元)
    assert calculate_amount(2, 150) == 300

    # 测试2：带小数的时长 (1.5小时 * 120元/时 = 180元)
    assert calculate_amount(1.5, 120) == 180

    # 测试3：边界情况，0小时 (0 * 150 = 0)
    assert calculate_amount(0, 150) == 0


import sqlite3

def test_sqlite_in_memory():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE students(id INTEGER PRIMARY KEY,name TEXE)')

    cursor.execute('INSERT INTO students(name) VALUES (?)',('测试张三',))
    conn.commit()

    cursor.execute('SELECT name FROM students WHERE id = 1')
    row = cursor.fetchone()

    assert row[0] == '测试张三'

    conn.close()