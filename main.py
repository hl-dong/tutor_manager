import json
import csv

#将学生信息保存到文件
def save_students(students):
    with open('students.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=4)


#添加新的学生信息
def add_student(students):
    #输入学生信息
    name = input("请输入学生姓名: ")
    grade = input("请输入学生年级: ")
    subject = input("请输入学科: ")
    contact = input("请输入学生联系方式: ")
    note = input("请输入备注: ")

    #存入一个字典student_info
    student_info = {
        "name": name,
        "grade": grade,
        "subject": subject,
        "contact": contact,
        "note": note
    }

    #把字典存入列表students
    students.append(student_info)

    #将学生信息保存到文件
    save_students(students)


#从文件读取学生信息
def load_students():
    try:
        with open('students.json', 'r', encoding='utf-8') as f:
            students = json.load(f)
            return students
    except FileNotFoundError:#预防文件不存在的情况
        return []#返回空列表, 避免主程序拿到None从而崩溃


#展示所有学生
def show_students(students):
    #如果没有学生
    if len(students) == 0:
        print('暂无学生.')
        return

    #遍历列表, 提取学生字典
    for index, student in enumerate(students, start=1):
        print(f'{index}. {student["name"]} | '
              f'{student["grade"]} | '
              f'{student["subject"]} | '
              f'{student["contact"]} | '
              f'{student["note"]} ')


#将课程信息保存到文件
def save_lessons(lessons):
    with open('lessons.json', 'w', encoding='utf-8') as f:
        json.dump(lessons, f, ensure_ascii=False, indent=4)


#选择学生(返回学生姓名
def choose_student(students):
    #展示学生列表供选择
    show_students(students)

    choice = input('请输入被选择学生的序号: ').strip()

    try:
        # 把字符串转为整数, 并且用户索引为1, 计算机索引为0, 故减1
        index = int(choice) - 1
    except ValueError:
        print('输入无效, 请输入数字! ')
        return

    if index < 0 or index >= len(students):
        print('序号不存在, 请重新选择!')
        return

    student_name = students[index]['name']

    return student_name


#添加课时记录
def add_lesson(lessons, students):
    #如果没有学生
    if len(students) == 0:
        print('请先添加学生!')
        return

    #选择学生
    student_name = choose_student(students)

    #防止student_name获取失败(None)
    if student_name is None: return

    #获取日期,时长,单价,备注
    date = input('请输入上课日期: ')
    duration = get_float_input('请输入上课时长(小时): ')
    rate = get_float_input('请输入课程单价(元): ')
    note = input('请输入备注: ')

    #获取是否已付(输入y转小写,等于则True, 反之则False
    paid = (input('请输入是否已付(是为y,否为n): ')).strip().lower() =='y'

    #计算金额
    amount = duration * rate

    #上述信息打包为字典
    lesson_info = {
        "student_name": student_name,
        "date": date,
        "duration": duration,
        "rate": rate,
        "amount": amount,
        "paid": paid,
        "note": note
    }

    #添加到列表lessons
    lessons.append(lesson_info)

    #添加到json文件保存
    save_lessons(lessons)

    print('成功添加课时记录! ')


#文件读取课时信息
def load_lessons():
    try:
        with open('lessons.json', 'r', encoding='utf-8') as f:
            lessons = json.load(f)
            return lessons
    except FileNotFoundError:
        return []


#展示课时信息
def show_lessons(lessons):
    if len(lessons) == 0:
        print('暂无课时记录.')
        return
    for index, lesson in enumerate(lessons, start=1):
        print(f'{index}. {lesson["student_name"]} | '
              f'{lesson["date"]} | '
              f'{lesson["duration"]}小时 | '
              f'{lesson["rate"]}元/时 | '
              f'{lesson["amount"]}元 '
              f'{"已付" if lesson["paid"] else "未付"} | '
              f'{lesson["note"]}'
        )


#按学生筛选课时
def filter_lessons_by_student(lessons, students):
    if len(lessons) == 0:
        print('暂无课时记录.')
        return
    if len(students) == 0:
        print('请先添加学生.')
        return

    #选择学生
    target_name = choose_student(students)
    #如果失败直接结束
    if target_name is None: return

    #筛选过程(遍历
    filtered_lessons = []
    for lesson in lessons:
        if lesson['student_name'] == target_name:
            filtered_lessons.append(lesson)

    #展示结果
    show_lessons(filtered_lessons)


#按月份筛选课时
def filter_lessons_by_month(lessons):
    if len(lessons) == 0:
        print('暂无课时记录.')
        return

    #输入目标年月
    target_month = input('请输入月份(格式如2026-10): ')

    #遍历寻找
    filtered_lessons = []

    for lesson in lessons:
        if lesson['date'].startswith(target_month):
            filtered_lessons.append(lesson)

    #展示结果
    show_lessons(filtered_lessons)


#标记已付/未付
def mark_lesson_paid(lessons):
    if len(lessons) == 0:
        print('暂无课时记录.')
        return

    show_lessons(lessons)
    choice = input('请输入课时记录序号: ').strip()
    try:
        index = int(choice) - 1
    except ValueError:
        print('输入无效, 请输入数字序号! ')
        return
    if index < 0 or index >= len(lessons):
        print('序号不存在, 请重新选择! ')
        return

    #取出记录
    lesson = lessons[index]

    #.lower()确保输入为小写
    paid_input = input("请输入状态(已付输入y, 未付输入n): ").strip().lower()
    #如果y则True, 如果不等y则False
    lesson["paid"] = (paid_input == 'y')

    #保存文件
    save_lessons(lessons)

    print('已成功修改标记')


#统计月收入
def calculate_monthly_income(lessons):
    if len(lessons) == 0:
        print('暂无课时记录.')
        return

    target_month = input('请输入月份(格式如2026-10): ')
    filtered_lessons = []
    for lesson in lessons:
        if lesson['date'].startswith(target_month):
            filtered_lessons.append(lesson)

    #初始化累加器
    total_duration = 0 #总课时
    total_income = 0   #应收总额
    paid_income = 0    #已收总额
    unpaid_income = 0  #未收总额

    #遍历累加
    for lesson in filtered_lessons:
        total_duration += lesson["duration"]
        total_income += lesson["amount"]
        if lesson["paid"]:
            paid_income += lesson["amount"]
        else:
            unpaid_income += lesson["amount"]

    #打印结果
    print(f'''
===== {target_month} 月度统计 =====
总课时: {total_duration}小时
应收总额: {total_income} 元
已收金额: {paid_income} 元
未收金额: {unpaid_income} 元
    ''')


#导出csv
def export_lessons_to_csv(lessons):
    if len(lessons) == 0:
        print('暂无课时记录，无法导出。')
        return

    with open('lessons.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f) #把文件变成csv写入器
        writer.writerow(['student_name','date', 'duration', 'rate', 'amount', 'paid', 'note'])

        for lesson in lessons:
            #把paid从True/False转为'已付/未付'(数据清洗
            paid_text = '已付' if lesson['paid'] else '未付'

            writer.writerow(
                [
                    lesson['student_name'],
                    lesson['date'],
                    lesson["duration"],
                    lesson["rate"],
                    lesson["amount"],
                    paid_text,
                    lesson['note']
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



#主函数
if __name__ == '__main__':
    students = load_students()
    lessons = load_lessons()

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
0. 退出
        ''')

        #获取用户选择(strip去除首尾空白字符)
        choice = input('请输入数字: ').strip()

        if choice == '1':
            add_student(students)
        elif choice == '2':
            show_students(students)
        elif choice == '3':
            add_lesson(lessons,students)
        elif choice == '4':
            show_lessons(lessons)
        elif choice == '5':
            filter_lessons_by_student(lessons, students)
        elif choice == '6':
            filter_lessons_by_month(lessons)
        elif choice == '7':
            mark_lesson_paid(lessons)
        elif choice == '8':
            calculate_monthly_income(lessons)
        elif choice == '9':
            export_lessons_to_csv(lessons)
        elif choice == '0':
            print('已退出程序.')
            break
        else:
            print('输入有误, 请重新输入.')
