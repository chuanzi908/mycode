import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv


class AcademicManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("教务管理系统 v2.0")
        self.root.geometry("1200x700")

        # 初始化数据库
        self.init_database()

        # 创建主框架
        self.create_widgets()

        # 加载初始数据
        self.load_students()
        self.load_courses()

    def init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect('academic_system.db')
        self.cursor = self.conn.cursor()

        # 创建表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                gender TEXT,
                age INTEGER,
                major TEXT,
                class_name TEXT,
                enrollment_date TEXT,
                phone TEXT,
                email TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                credit INTEGER,
                teacher TEXT,
                classroom TEXT,
                schedule TEXT,
                capacity INTEGER,
                enrolled INTEGER DEFAULT 0
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                course_id TEXT,
                score REAL,
                semester TEXT,
                exam_date TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')

        # 创建选课表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                course_id TEXT,
                enroll_date TEXT,
                status TEXT DEFAULT '在修',
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')

        self.conn.commit()

    def create_widgets(self):
        """创建GUI组件"""
        # 创建菜单栏
        self.create_menu()

        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧导航栏
        nav_frame = ttk.LabelFrame(main_frame, text="功能导航", width=200)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # 导航按钮
        buttons = [
            ("👨‍🎓 学生管理", self.show_student_management),
            ("📚 课程管理", self.show_course_management),
            ("📊 成绩管理", self.show_grade_management),
            ("📝 选课管理", self.show_enrollment_management),
            ("📈 数据统计", self.show_statistics),
            ("📤 数据导出", self.export_data)
        ]

        for text, command in buttons:
            btn = ttk.Button(nav_frame, text=text, command=command, width=20)
            btn.pack(pady=5, padx=10, fill=tk.X)

        # 右侧主内容区
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 状态栏
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导入学生数据", command=self.import_student_data)
        file_menu.add_command(label="导入课程数据", command=self.import_course_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 工具菜单
        tool_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tool_menu)
        tool_menu.add_command(label="数据库备份", command=self.backup_database)
        tool_menu.add_command(label="系统设置", command=self.system_settings)

    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_student_management(self):
        """显示学生管理界面"""
        self.clear_content()
        self.status_bar.config(text="学生管理")

        # 创建搜索和操作框架
        search_frame = ttk.LabelFrame(self.content_frame, text="搜索与操作")
        search_frame.pack(fill=tk.X, pady=(0, 10))

        # 搜索条件
        ttk.Label(search_frame, text="学号:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id_search = ttk.Entry(search_frame, width=15)
        self.student_id_search.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="姓名:").grid(row=0, column=2, padx=5, pady=5)
        self.student_name_search = ttk.Entry(search_frame, width=15)
        self.student_name_search.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(search_frame, text="专业:").grid(row=0, column=4, padx=5, pady=5)
        self.major_search = ttk.Entry(search_frame, width=15)
        self.major_search.grid(row=0, column=5, padx=5, pady=5)

        # 按钮
        ttk.Button(search_frame, text="搜索", command=self.search_students).grid(row=0, column=6, padx=5)
        ttk.Button(search_frame, text="添加学生", command=self.add_student_dialog).grid(row=0, column=7, padx=5)
        ttk.Button(search_frame, text="刷新", command=self.load_students).grid(row=0, column=8, padx=5)

        # 创建学生表格
        table_frame = ttk.LabelFrame(self.content_frame, text="学生列表")
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建Treeview
        columns = ("学号", "姓名", "性别", "年龄", "专业", "班级", "入学日期", "电话", "邮箱")
        self.student_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # 设置列
        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=100)

        # 滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 右键菜单
        self.create_student_context_menu()

    def load_students(self):
        """加载学生数据到表格"""
        if hasattr(self, 'student_tree'):
            # 清空现有数据
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)

            # 从数据库加载数据
            self.cursor.execute(
                "SELECT student_id, name, gender, age, major, class_name, enrollment_date, phone, email FROM students")
            students = self.cursor.fetchall()

            for student in students:
                self.student_tree.insert("", tk.END, values=student)

    def search_students(self):
        """搜索学生"""
        if not hasattr(self, 'student_tree'):
            return

        # 获取搜索条件
        student_id = self.student_id_search.get().strip()
        name = self.student_name_search.get().strip()
        major = self.major_search.get().strip()

        # 构建查询
        query = "SELECT student_id, name, gender, age, major, class_name, enrollment_date, phone, email FROM students WHERE 1=1"
        params = []

        if student_id:
            query += " AND student_id LIKE ?"
            params.append(f"%{student_id}%")
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        if major:
            query += " AND major LIKE ?"
            params.append(f"%{major}%")

        # 清空现有数据
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        # 执行查询
        self.cursor.execute(query, params)
        students = self.cursor.fetchall()

        for student in students:
            self.student_tree.insert("", tk.END, values=student)

    def add_student_dialog(self):
        """添加学生对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加学生")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # 表单字段
        fields = [
            ("学号*:", "student_id"),
            ("姓名*:", "name"),
            ("性别:", "gender"),
            ("年龄:", "age"),
            ("专业:", "major"),
            ("班级:", "class_name"),
            ("电话:", "phone"),
            ("邮箱:", "email")
        ]

        entries = {}

        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(dialog, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field_name] = entry

        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="保存", command=lambda: self.save_student(dialog, entries)).pack(side=tk.LEFT,
                                                                                                       padx=10)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def save_student(self, dialog, entries):
        """保存学生信息"""
        try:
            # 获取数据
            student_data = {}
            for field, entry in entries.items():
                student_data[field] = entry.get().strip()

            # 验证必填字段
            if not student_data['student_id'] or not student_data['name']:
                messagebox.showerror("错误", "学号和姓名为必填项")
                return

            # 插入数据库
            self.cursor.execute('''
                INSERT INTO students (student_id, name, gender, age, major, class_name, phone, email, enrollment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_data['student_id'],
                student_data['name'],
                student_data['gender'],
                student_data['age'] if student_data['age'] else None,
                student_data['major'],
                student_data['class_name'],
                student_data['phone'],
                student_data['email'],
                datetime.now().strftime("%Y-%m-%d")
            ))

            self.conn.commit()
            messagebox.showinfo("成功", "学生添加成功！")
            dialog.destroy()
            self.load_students()

        except sqlite3.IntegrityError:
            messagebox.showerror("错误", "学号已存在！")
        except Exception as e:
            messagebox.showerror("错误", f"添加失败: {str(e)}")

    def create_student_context_menu(self):
        """创建学生表格右键菜单"""
        self.student_context_menu = tk.Menu(self.root, tearoff=0)
        self.student_context_menu.add_command(label="查看详情", command=self.view_student_detail)
        self.student_context_menu.add_command(label="编辑", command=self.edit_student)
        self.student_context_menu.add_command(label="删除", command=self.delete_student)
        self.student_context_menu.add_separator()
        self.student_context_menu.add_command(label="查看成绩", command=self.view_student_grades)

        # 绑定右键事件
        self.student_tree.bind("<Button-3>", self.show_student_context_menu)

    def show_student_context_menu(self, event):
        """显示学生右键菜单"""
        item = self.student_tree.identify_row(event.y)
        if item:
            self.student_tree.selection_set(item)
            self.student_context_menu.post(event.x_root, event.y_root)

    def view_student_detail(self):
        """查看学生详情"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择学生")
            return

        item = self.student_tree.item(selection[0])
        student_id = item['values'][0]

        # 查询详细信息
        self.cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        student = self.cursor.fetchone()

        if student:
            # 显示详情对话框
            dialog = tk.Toplevel(self.root)
            dialog.title("学生详情")
            dialog.geometry("400x300")

            info_text = f"""
            学号: {student[1]}
            姓名: {student[2]}
            性别: {student[3] or '未填写'}
            年龄: {student[4] or '未填写'}
            专业: {student[5] or '未填写'}
            班级: {student[6] or '未填写'}
            入学日期: {student[7] or '未填写'}
            电话: {student[8] or '未填写'}
            邮箱: {student[9] or '未填写'}
            """

            text_widget = tk.Text(dialog, wrap=tk.WORD, height=15, width=40)
            text_widget.insert(tk.END, info_text)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def edit_student(self):
        """编辑学生信息"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择学生")
            return

        item = self.student_tree.item(selection[0])
        student_id = item['values'][0]

        # 查询当前信息
        self.cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        student = self.cursor.fetchone()

        if student:
            # 创建编辑对话框
            dialog = tk.Toplevel(self.root)
            dialog.title("编辑学生信息")
            dialog.geometry("400x400")

            fields = [
                ("学号:", "student_id", student[1]),
                ("姓名:", "name", student[2]),
                ("性别:", "gender", student[3] or ""),
                ("年龄:", "age", student[4] or ""),
                ("专业:", "major", student[5] or ""),
                ("班级:", "class_name", student[6] or ""),
                ("电话:", "phone", student[8] or ""),
                ("邮箱:", "email", student[9] or "")
            ]

            entries = {}

            for i, (label_text, field_name, value) in enumerate(fields):
                ttk.Label(dialog, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
                entry = ttk.Entry(dialog, width=30)
                entry.insert(0, str(value))
                if field_name == "student_id":  # 学号不可编辑
                    entry.config(state="readonly")
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries[field_name] = entry

            def save_changes():
                try:
                    update_data = (
                        entries['name'].get().strip(),
                        entries['gender'].get().strip() or None,
                        entries['age'].get().strip() or None,
                        entries['major'].get().strip(),
                        entries['class_name'].get().strip(),
                        entries['phone'].get().strip(),
                        entries['email'].get().strip(),
                        student_id
                    )

                    self.cursor.execute('''
                        UPDATE students SET name=?, gender=?, age=?, major=?, class_name=?, phone=?, email=?
                        WHERE student_id=?
                    ''', update_data)

                    self.conn.commit()
                    messagebox.showinfo("成功", "学生信息已更新！")
                    dialog.destroy()
                    self.load_students()

                except Exception as e:
                    messagebox.showerror("错误", f"更新失败: {str(e)}")

            ttk.Button(dialog, text="保存", command=save_changes).grid(row=len(fields), column=0, pady=20)
            ttk.Button(dialog, text="取消", command=dialog.destroy).grid(row=len(fields), column=1, pady=20)

    def delete_student(self):
        """删除学生"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择学生")
            return

        item = self.student_tree.item(selection[0])
        student_id = item['values'][0]
        student_name = item['values'][1]

        if messagebox.askyesno("确认删除", f"确定要删除学生 {student_name}({student_id}) 吗？"):
            try:
                # 先删除相关的成绩记录
                self.cursor.execute("DELETE FROM grades WHERE student_id=?", (student_id,))
                # 再删除学生
                self.cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
                self.conn.commit()
                messagebox.showinfo("成功", "学生删除成功！")
                self.load_students()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def show_course_management(self):
        """显示课程管理界面"""
        self.clear_content()
        self.status_bar.config(text="课程管理")

        # 实现课程管理界面
        ttk.Label(self.content_frame, text="课程管理功能正在开发中...", font=("Arial", 16)).pack(pady=50)

    def show_grade_management(self):
        """显示成绩管理界面"""
        self.clear_content()
        self.status_bar.config(text="成绩管理")

        # 实现成绩管理界面
        ttk.Label(self.content_frame, text="成绩管理功能正在开发中...", font=("Arial", 16)).pack(pady=50)

    def show_enrollment_management(self):
        """显示选课管理界面"""
        self.clear_content()
        self.status_bar.config(text="选课管理")

        # 实现选课管理界面
        ttk.Label(self.content_frame, text="选课管理功能正在开发中...", font=("Arial", 16)).pack(pady=50)

    def show_statistics(self):
        """显示数据统计界面"""
        self.clear_content()
        self.status_bar.config(text="数据统计")

        # 实现统计界面
        ttk.Label(self.content_frame, text="数据统计功能正在开发中...", font=("Arial", 16)).pack(pady=50)

    def export_data(self):
        """导出数据"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                # 导出学生数据
                self.cursor.execute("SELECT * FROM students")
                students = self.cursor.fetchall()

                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # 写入表头
                    writer.writerow(['ID', '学号', '姓名', '性别', '年龄', '专业', '班级', '入学日期', '电话', '邮箱'])
                    # 写入数据
                    writer.writerows(students)

                messagebox.showinfo("成功", f"数据已导出到: {file_path}")

            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")

    def import_student_data(self):
        """导入学生数据"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # 跳过表头

                    for row in reader:
                        if len(row) >= 3:
                            self.cursor.execute('''
                                INSERT OR IGNORE INTO students (student_id, name, enrollment_date)
                                VALUES (?, ?, ?)
                            ''', (row[1], row[2], datetime.now().strftime("%Y-%m-%d")))

                self.conn.commit()
                messagebox.showinfo("成功", "学生数据导入成功！")
                if hasattr(self, 'student_tree'):
                    self.load_students()

            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}")

    def import_course_data(self):
        """导入课程数据"""
        messagebox.showinfo("提示", "课程数据导入功能正在开发中...")

    def backup_database(self):
        """备份数据库"""
        import shutil
        import os

        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"academic_backup_{timestamp}.db")

        try:
            shutil.copy2('academic_system.db', backup_path)
            messagebox.showinfo("成功", f"数据库已备份到: {backup_path}")
        except Exception as e:
            messagebox.showerror("错误", f"备份失败: {str(e)}")

    def system_settings(self):
        """系统设置"""
        messagebox.showinfo("系统设置", "系统设置功能正在开发中...")

    def view_student_grades(self):
        """查看学生成绩"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择学生")
            return

        item = self.student_tree.item(selection[0])
        student_id = item['values'][0]
        student_name = item['values'][1]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"{student_name}的成绩单")
        dialog.geometry("600x400")

        # 查询学生成绩
        self.cursor.execute('''
            SELECT courses.course_name, grades.score, grades.semester, grades.exam_date
            FROM grades
            JOIN courses ON grades.course_id = courses.course_id
            WHERE grades.student_id = ?
            ORDER BY grades.semester DESC, grades.exam_date DESC
        ''', (student_id,))

        grades = self.cursor.fetchall()

        # 创建表格显示成绩
        columns = ("课程名称", "成绩", "学期", "考试日期")
        tree = ttk.Treeview(dialog, columns=columns, show="headings", height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for grade in grades:
            tree.insert("", tk.END, values=grade)

        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 计算平均分
        if grades:
            total_score = sum(grade[1] for grade in grades if grade[1] is not None)
            avg_score = total_score / len(grades)
            ttk.Label(dialog, text=f"平均分: {avg_score:.2f}", font=("Arial", 12, "bold")).pack(pady=5)

    def load_courses(self):
        """加载课程数据"""
        # 这里可以加载课程数据到课程管理界面
        pass


def main():
    root = tk.Tk()
    app = AcademicManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()