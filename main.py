import csv
import sqlite3



#添加新的学生信息
def add_student():
    #获取学生信息
    name = input("请输入学生姓名: ")
    grade = input("请输入学生年级: ")
    subject = input("请输入学科: ")
    contact = input("请输入学生联系方式: ")
    note = input("请输入备注: ")

    #连接数据库
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()

    #插入数据
    cursor.execute(
        "INSERT INTO students (name, grade, subject, contact, note) VALUES (?, ?, ?, ?, ?)",
        (name, grade, subject, contact, note)
    )

    #提交并关闭
    conn.commit()
    conn.close()
    print("添加学生成功！")


#展示所有学生
def show_students():
    #连接数据库
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()

    #查询所有学生
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()#rows接住结果(元组)

    conn.close()

    if len(rows) == 0:
        print('暂无学生.')
        return

    #遍历打印
    for index, row in enumerate(rows, start=1):
        #row0=id,name,grade,subject,contact,note
        print(f'{index}. {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}')


#选择学生(返回学生姓名
def choose_student():
    #连接数据库,查出id和name
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id,name FROM students")
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print('请先添加学生!')
        return None,None #id和name是两个占位符

    #遍历展示学生列表
    for index, row in enumerate(rows, start=1):
        print(f'{index}. {row[1]}')

    #获取用户选择并校验
    choice = input('请输入被选择学生的序号: ').strip()
    try:
        index = int(choice) - 1
    except ValueError:
        print('输入无效，请输入数字！')
        return None, None

    if index < 0 or index >= len(rows):
        print('序号不存在，请重新选择！')
        return None, None

    #获取选中学生的id和name
    student_id = rows[index][0]
    student_name = rows[index][1]

    return student_id, student_name


#添加课时记录
def add_lesson():
    #选择学生
    student_id, student_name = choose_student()
    
    if student_id is None:
        return

    #获取日期,时长,单价,备注
    date = input('请输入上课日期: ')
    duration = get_float_input('请输入上课时长(小时): ')
    rate = get_float_input('请输入课程单价(元): ')
    note = input('请输入备注: ')

    #获取是否已付(输入y转小写,等于则True, 反之则False
    paid = (input('请输入是否已付(是为y,否为n): ')).strip().lower() =='y'

    #计算金额
    amount = calculate_amount(duration, rate)

    #连接数据库并插入
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()

    #paid转为 INTEGER(0或1)
    cursor.execute('''
        INSERT INTO lessons (student_id, date, duration_hours, hourly_rate, amount, paid, note)
        VALUES(?, ?, ?, ?, ?, ?, ?)
    ''',(student_id,date,duration,rate,amount,int(paid),note))

    conn.commit()
    conn.close()
    print(f'成功为{student_name}添加课时记录!')


#展示课时信息
def show_lessons():
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()

    #连表查询
    cursor.execute('''
        SELECT lessons.id, students.name, lessons.date, lessons.duration_hours,
        lessons.hourly_rate, lessons.amount, lessons.paid, lessons.note
        FROM lessons
        JOIN students ON lessons.student_id = students.id
    ''')

    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print('暂无课时记录.')
        return

    #遍历打印
    for index, row in enumerate(rows, start=1):
    #row1=student.name,2=date,3=duration_hours,4=hourly_rate,5=amount,6=paid,7=note
        paid_text = '已付' if row[6] else '未付'
        print(f'{index}. {row[1]} | ' 
              f'{row[2]} | '
              f'{row[3]}小时 | '
              f'{row[4]}元/时 | '
              f'{row[5]}元 | '
              f'{paid_text} | '
              f'{row[7]}'
              )


#按学生筛选课时
def filter_lessons_by_student():
    #选择学生
    student_id, student_name = choose_student()

    #如果失败直接结束
    if student_id is None: return

    #连表查询
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT lessons.id, students.name, lessons.date, lessons.duration_hours, 
               lessons.hourly_rate, lessons.amount, lessons.paid, lessons.note
        FROM lessons
        JOIN students ON lessons.student_id = students.id
        WHERE lessons.student_id = ?
    ''',(student_id,)) #cursor.excute接收两个参数
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print(f'{student_name} 暂无课时记录.')
        return

    #遍历打印
    for index, row in enumerate(rows,start=1):
        paid_text = "已付" if row[6] else "未付"
        print(f'{index}. {row[1]} | '
              f'{row[2]} | '
              f'{row[3]}小时 | '
              f'{row[4]}元/时 | '
              f'{row[5]}元 | '
              f'{paid_text} | '
              f'{row[7]}'
              )


#按月份筛选课时
def filter_lessons_by_month():
    #输入目标年月
    target_month = input('请输入月份(格式如2026-10): ').strip()

    #连表查询
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT lessons.id, students.name, lessons.date, lessons.duration_hours, 
        lessons.hourly_rate, lessons.amount, lessons.paid, lessons.note
        FROM lessons
        JOIN students ON lessons.student_id = students.id
        WHERE lessons.date LIKE ?
    ''',(target_month + '%',))
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print(f'{target_month} 暂无课时记录.')
        return

    for index, row in enumerate(rows, start=1):
        paid_text = "已付" if row[6] else "未付"
        print(f'{index}. {row[1]} | '
              f'{row[2]} | '
              f'{row[3]}小时 | '
              f'{row[4]}元/时 | '
              f'{row[5]}元 | '
              f'{paid_text} | '
              f'{row[7]}'
              )



#标记已付/未付
def mark_lesson_paid():
    show_lessons()

    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM lessons ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print('暂无课时记录.')
        return

    choice = input('请输入课时记录序号: ').strip()
    try:
        index = int(choice) - 1
    except ValueError:
        print('输入无效, 请输入数字序号! ')
        return
    if index < 0 or index >= len(rows):
        print('序号不存在, 请重新选择! ')
        return

    #获取真实id(防止删改导致id缺失, 如1345, 显示为1234
    real_lesson_id = rows[index][0]

    #.lower()确保输入为小写
    paid_input = input("请输入状态(已付输入y, 未付输入n): ").strip().lower()
    new_paid = 1 if paid_input == 'y' else 0

    #UPDATE语句
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE lessons SET paid = ? WHERE id = ?'
                   ,(new_paid, real_lesson_id))
    conn.commit()
    conn.close()

    print('已成功修改标记')


#统计月收入
def calculate_monthly_income():
    target_month = input('请输入月份(格式如2026-10): ').strip()

    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            SUM(duration_hours),
            SUM(amount),
            SUM(CASE WHEN paid=1 THEN amount ELSE 0 END),
            SUM(CASE WHEN paid=0 THEN amount ELSE 0 END)
        FROM lessons
        WHERE date LIKE ?
    ''',(target_month + '%',))

    row = cursor.fetchone() #fetchone只拿一行
    conn.close()

    if row is None or row[0] is None:
        print(f'{target_month} 暂无课时记录，无法统计.')
        return

    total_duration = row[0]
    total_income = row[1]
    paid_income = row[2]
    unpaid_income = row[3]

    #打印结果
    print(f'''
===== {target_month} 月度统计 =====
总课时: {total_duration}小时
应收总额: {total_income} 元
已收金额: {paid_income} 元
未收金额: {unpaid_income} 元
    ''')


#导出csv
def export_lessons_to_csv():
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT students.name, lessons.date, lessons.duration_hours,
            lessons.hourly_rate, lessons.amount, lessons.paid, lessons.note
        FROM lessons
        JOIN students ON students.id = lessons.student_id
        ORDER BY lessons.date ASC
    ''')
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print('暂无课时记录，无法导出。')
        return

    with open('lessons.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f) #把文件变成csv写入器
        #写表头
        writer.writerow(['学生姓名','日期', '时长(小时)', '单价(元)', '金额(元)', '是否已付', '备注'])
        #写数据
        for row in rows:
            #row=0姓名,1日期,2时长,3单价,4金额,5paid,6备注
            paid_text = '已付' if row[5] == 1 else '未付'
            writer.writerow(
                [
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    paid_text,
                    row[6]
                ]
            )

    print('导出成功!')

#异常处理优化: 小数获取
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('输入无效, 请输入数字')


#根据时长和单价计算总金额
def calculate_amount(duration, rate):
    return duration * rate


#删除课程记录
def delete_lessons():
    show_lessons()

    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM lessons ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print('暂无课时记录.')
        return

    choice = input('请输入要删除的课时记录序号: ').strip()
    try:
        index = int(choice) - 1
    except ValueError:
        print('输入无效, 请输入数字序号! ')
        return
    if index < 0 or index >= len(rows):
        print('序号不存在, 请重新选择! ')
        return

    real_lesson_id = rows[index][0]

    confirm = input('确认要删除吗?(y/n):').strip().lower()
    if confirm != 'y':
        print('已取消')
        return

    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lessons WHERE id = ?',(real_lesson_id,))
    conn.commit()
    conn.close()
    print('删除成功')


#修改课程记录
def update_lessons():
    show_lessons()

    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM lessons ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        print('暂无课时记录.')
        return

    choice = input('请输入要修改的课时记录序号: ').strip()
    try:
        index = int(choice) - 1
    except ValueError:
        print('输入无效, 请输入数字序号! ')
        return
    if index < 0 or index >= len(rows):
        print('序号不存在, 请重新选择! ')
        return

    real_lesson_id = rows[index][0]

    date = input('请输入新日期: ')
    duration = get_float_input('请输入新时长(小时): ')
    rate = get_float_input('请输入新单价(元): ')
    note = input('请输入新备注: ')
    paid = (input('请输入是否已付(y/n): ')).strip().lower() == 'y'
    amount = calculate_amount(duration, rate)

    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE lessons SET date=?, duration_hours=?, '
                   'hourly_rate=?, amount=?, paid=?, note=? WHERE id=?'
                   ,(date, duration, rate, amount, int(paid), note, real_lesson_id))
    conn.commit()
    conn.close()
    print('修改成功')



#主函数
if __name__ == '__main__':
    while True:
        #打印菜单
        print('''
=== 家教课时管理工具 ===
1. 添加学生
2. 查看学生
3. 添加课时
4. 查看课时
5. 按学生筛选课时
6. 按月份筛选课时
7. 标记已付/未付
8. 统计月收入
9. 导出课时csv
10. 删除课时记录
11. 修改课时记录
0. 退出
        ''')

        #获取用户选择(strip去除首尾空白字符)
        choice = input('请输入数字: ').strip()

        if choice == '1': add_student()
        elif choice == '2': show_students()
        elif choice == '3': add_lesson()
        elif choice == '4': show_lessons()
        elif choice == '5': filter_lessons_by_student()
        elif choice == '6': filter_lessons_by_month()
        elif choice == '7': mark_lesson_paid()
        elif choice == '8': calculate_monthly_income()
        elif choice == '9': export_lessons_to_csv()
        elif choice == '10': delete_lessons()
        elif choice == '11': update_lessons()
        elif choice == '0':
            print('已退出程序.')
            break
        else:
            print('输入有误, 请重新输入.')
