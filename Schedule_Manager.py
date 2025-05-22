import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableView, QPushButton, QLabel, QLineEdit, QDateEdit, 
                             QComboBox, QMessageBox, QHeaderView, QFormLayout, QDialog,
                             QTimeEdit, QDialogButtonBox, QMenu, QTableWidget, QTableWidgetItem,
                             QCheckBox)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import Qt, QDate, QTime
import sqlite3
from sqlite3 import Error
from datetime import datetime

class ProjectInfo:
    """项目信息元数据（集中管理所有项目相关信息）"""
    VERSION = "1.17.0"
    BUILD_DATE = "2025-05-15"
    AUTHOR = "杜玛"
    LICENSE = "MIT"
    COPYRIGHT = "© 永久 杜玛"
    URL = "https://github.com/duma520"
    MAINTAINER_EMAIL = "不提供"
    NAME = "排班表管理系统"
    DESCRIPTION = "一个简单易用的排班表管理系统，支持多种功能"
    HELP_TEXT = """
排班表管理系统使用说明:

"""


    @classmethod
    def get_metadata(cls) -> dict:
        """获取主要元数据字典"""
        return {
            'version': cls.VERSION,
            'author': cls.AUTHOR,
            'license': cls.LICENSE,
            'url': cls.URL
        }


    @classmethod
    def get_header(cls) -> str:
        """生成标准化的项目头信息"""
        return f"{cls.NAME} {cls.VERSION} | {cls.LICENSE} License | {cls.URL}"


# 马卡龙色系定义
class MacaronColors:
    # 粉色系
    SAKURA_PINK = QColor(255, 183, 206)  # 樱花粉
    ROSE_PINK = QColor(255, 154, 162)    # 玫瑰粉
    
    # 蓝色系
    SKY_BLUE = QColor(162, 225, 246)    # 天空蓝
    LILAC_MIST = QColor(230, 230, 250)   # 淡丁香
    
    # 绿色系
    MINT_GREEN = QColor(181, 234, 215)   # 薄荷绿
    APPLE_GREEN = QColor(212, 241, 199)  # 苹果绿
    
    # 黄色/橙色系
    LEMON_YELLOW = QColor(255, 234, 165) # 柠檬黄
    BUTTER_CREAM = QColor(255, 248, 184) # 奶油黄
    PEACH_ORANGE = QColor(255, 218, 193) # 蜜桃橙
    
    # 紫色系
    LAVENDER = QColor(199, 206, 234)     # 薰衣草紫
    TARO_PURPLE = QColor(216, 191, 216)  # 香芋紫
    
    # 中性色
    CARAMEL_CREAM = QColor(240, 230, 221) # 焦糖奶霜


class UserManager:
    """用户管理类"""
    USERS_DB = 'users.db'
    CONFIG_FILE = 'user_config.ini'
    
    @classmethod
    def init_users_db(cls):
        """初始化用户数据库"""
        try:
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT DEFAULT '',
                    db_file TEXT NOT NULL UNIQUE,
                    last_login TEXT,
                    has_password BOOLEAN DEFAULT FALSE
                )
            ''')
            conn.commit()
            conn.close()
        except Error as e:
            print(f"[DEBUG] 无法初始化用户数据库: {str(e)}")
            raise Exception(f"无法初始化用户数据库: {str(e)}")

    @classmethod
    def create_user(cls, username, password=''):
        """创建新用户"""
        try:
            db_file = f"user_{username}.db"
            conn = sqlite3.connect(db_file)
            conn.close()
            
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            has_password = bool(password)  # 判断是否有密码
            cursor.execute(
                "INSERT INTO users (username, password, db_file, has_password) VALUES (?, ?, ?, ?)",
                (username, password, db_file, has_password)
            )
            conn.commit()
            return True
        except Error as e:
            raise Exception(f"无法创建用户: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def authenticate(cls, username, password=''):
        """验证用户登录"""
        try:
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT db_file, has_password, password FROM users WHERE username=?",
                (username,)
            )
            result = cursor.fetchone()
            
            if not result:
                return None
                
            db_file, has_password, stored_password = result
            
            # 如果有密码但未提供密码，或密码不匹配
            if has_password and (not password or stored_password != password):
                return None
                
            # 更新最后登录时间
            cursor.execute(
                "UPDATE users SET last_login=? WHERE username=?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username)
            )
            conn.commit()
            return db_file  # 返回数据库文件路径
            
        except Error as e:
            raise Exception(f"认证失败: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def delete_user(cls, username):
        """删除用户及其数据库文件"""
        try:
            # 先获取用户的数据库文件路径
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT db_file FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            
            if not result:
                return False
                
            db_file = result[0]
            
            # 从用户表中删除记录
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            
            # 删除用户数据库文件
            if os.path.exists(db_file):
                os.remove(db_file)
                
            return True
        except Error as e:
            raise Exception(f"无法删除用户: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def save_login_config(cls, username, password='', remember=False):
        """保存登录配置"""
        import configparser
        config = configparser.ConfigParser()
        # 总是保存用户名
        config['LOGIN'] = {
            'username': username,
            'password': password if remember else '',
            'remember': 'True' if remember else 'False'
        }
        
        with open(cls.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    
    @classmethod
    def load_login_config(cls):
        """读取登录配置"""
        import configparser
        import os
        config = configparser.ConfigParser()
        if not os.path.exists(cls.CONFIG_FILE):
            return None, None, False
            
        config.read(cls.CONFIG_FILE)
        if 'LOGIN' in config:
            return (
                config['LOGIN'].get('username', ''),
                config['LOGIN'].get('password', ''),
                config['LOGIN'].getboolean('remember', False)
            )
        return None, None, False


class ScheduleManager(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化用户数据库
        try:
            UserManager.init_users_db()
        except Exception as e:
            QMessageBox.critical(None, "初始化错误", str(e))
            sys.exit(1)
            
        # 显示登录对话框
        if not self.show_login_dialog():
            sys.exit(0)
            
        self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} - 当前用户: {self.current_user}")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(1000, 600)
        
        # 初始化数据库
        self.init_db()

        self.name_color_map = {}  # 存储姓名到颜色的映射
        self.color_list = [
            MacaronColors.SAKURA_PINK, MacaronColors.SKY_BLUE, MacaronColors.MINT_GREEN,
            MacaronColors.LEMON_YELLOW, MacaronColors.LAVENDER, MacaronColors.PEACH_ORANGE,
            MacaronColors.ROSE_PINK, MacaronColors.LILAC_MIST, MacaronColors.APPLE_GREEN,
            MacaronColors.BUTTER_CREAM, MacaronColors.TARO_PURPLE, MacaronColors.CARAMEL_CREAM
        ]        
        # 创建UI
        self.init_ui()
        
        # 加载数据
        self.load_data()

    def show_login_dialog(self):
        """显示登录对话框"""
        dialog = QDialog()
        dialog.setWindowTitle("用户登录")
        dialog.setWindowIcon(QIcon('icon.ico'))
        dialog.resize(300, 200)
        
        layout = QFormLayout(dialog)
        
        # 用户名 - 改为QComboBox
        self.username_combo = QComboBox()
        self.username_combo.setEditable(True)  # 允许用户输入新用户名
        self.username_combo.setPlaceholderText("选择或输入用户名")
        layout.addRow("用户名:", self.username_combo)
        
        # 密码
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("输入密码(可选)")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("密码:", self.password_input)
        
        # 记住密码复选框
        self.remember_check = QCheckBox("记住密码")
        layout.addRow(self.remember_check)
        
        # 加载已注册用户
        self.load_registered_users()
        
        # 加载保存的登录配置
        username, password, remember = UserManager.load_login_config()
        if username:
            # 先尝试在下拉框中查找匹配项
            index = self.username_combo.findText(username)
            if index >= 0:
                self.username_combo.setCurrentIndex(index)
            else:
                # 如果没找到，直接设置当前文本
                self.username_combo.setEditText(username)
            
            # 只有当记住密码时才填充密码
            if remember and password:
                self.password_input.setText(password)
                self.remember_check.setChecked(True)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.handle_login(dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        # 创建水平布局用于按钮
        button_row = QHBoxLayout()
        button_row.setSpacing(10)  # 设置按钮间距

        # 注册按钮
        register_btn = QPushButton("注册新用户")
        register_btn.clicked.connect(lambda: self.show_register_dialog(dialog))
        button_row.addWidget(register_btn)

        # 删除用户按钮
        delete_btn = QPushButton("删除用户")
        delete_btn.clicked.connect(lambda: self.show_delete_user_dialog(dialog))
        button_row.addWidget(delete_btn)

        # 将水平布局添加到表单布局中
        layout.addRow(button_row)
            
        return dialog.exec_() == QDialog.Accepted


    def load_registered_users(self):
        """加载已注册用户到下拉列表"""
        try:
            conn = sqlite3.connect(UserManager.USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users ORDER BY username")
            users = cursor.fetchall()
            
            self.username_combo.clear()
            for user in users:
                self.username_combo.addItem(user[0])
                
        except Error as e:
            print(f"加载用户列表失败: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def handle_login(self, dialog):
        """处理登录"""
        username = self.username_combo.currentText().strip()
        password = self.password_input.text().strip()
        remember = self.remember_check.isChecked()
        
        if not username:
            QMessageBox.warning(dialog, "输入错误", "用户名不能为空")
            return
            
        try:
            db_file = UserManager.authenticate(username, password)
            if db_file:
                self.current_user = username
                self.user_db_file = db_file
                # 总是保存用户名，但根据选择决定是否保存密码
                UserManager.save_login_config(username, password, remember)
                dialog.accept()
            else:
                QMessageBox.warning(dialog, "登录失败", "用户名或密码错误")
        except Exception as e:
            QMessageBox.critical(dialog, "登录错误", str(e))



    def show_register_dialog(self, parent_dialog):
        """显示注册对话框"""
        dialog = QDialog(parent_dialog)
        dialog.setWindowTitle("注册新用户")
        dialog.setWindowIcon(QIcon('icon.ico'))
        dialog.resize(300, 250)
        
        layout = QFormLayout(dialog)
        
        # 用户名
        new_username = QLineEdit()
        new_username.setPlaceholderText("输入新用户名")
        layout.addRow("用户名:", new_username)
        
        # 密码
        new_password = QLineEdit()
        new_password.setPlaceholderText("输入密码(可选)")
        new_password.setEchoMode(QLineEdit.Password)
        layout.addRow("密码:", new_password)
        
        # 确认密码
        confirm_password = QLineEdit()
        confirm_password.setPlaceholderText("确认密码(可选)")
        confirm_password.setEchoMode(QLineEdit.Password)
        layout.addRow("确认密码:", confirm_password)
        
        # 提示标签
        info_label = QLabel("提示: 密码是可选的，如果不设置密码，\n任何人都可以使用此用户名登录")
        info_label.setStyleSheet("color: gray;")
        layout.addRow(info_label)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.handle_register(
            dialog, new_username.text(), new_password.text(), confirm_password.text()
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        dialog.exec_()




            
    def handle_register(self, dialog, username, password, confirm_password):
        """处理注册"""
        if not username:
            QMessageBox.warning(dialog, "输入错误", "用户名不能为空")
            return
            
        # 检查密码是否匹配(如果有密码)
        if password or confirm_password:
            if password != confirm_password:
                QMessageBox.warning(dialog, "输入错误", "两次输入的密码不匹配")
                return
                
        try:
            if UserManager.create_user(username, password):
                QMessageBox.information(dialog, "注册成功", "用户注册成功，请登录")
                # 注册成功后刷新用户列表
                self.load_registered_users()
                dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, "注册错误", str(e))

    def show_delete_user_dialog(self, parent_dialog):
        """显示删除用户对话框"""
        dialog = QDialog(parent_dialog)
        dialog.setWindowTitle("删除用户")
        dialog.setWindowIcon(QIcon('icon.ico'))
        dialog.resize(300, 150)
        
        layout = QFormLayout(dialog)
        
        # 用户名选择
        username_combo = QComboBox()
        try:
            conn = sqlite3.connect(UserManager.USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users ORDER BY username")
            users = cursor.fetchall()
            
            for user in users:
                username_combo.addItem(user[0])
        except Error as e:
            QMessageBox.critical(dialog, "错误", f"无法加载用户列表: {str(e)}")
            return
        finally:
            if 'conn' in locals():
                conn.close()
        
        layout.addRow("选择用户:", username_combo)
        
        # 密码验证
        password_input = QLineEdit()
        password_input.setPlaceholderText("输入密码验证")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("密码验证:", password_input)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.handle_delete_user(
            dialog, username_combo.currentText(), password_input.text()
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        dialog.exec_()

    def handle_delete_user(self, dialog, username, password):
        """处理用户删除请求"""
        if not username:
            QMessageBox.warning(dialog, "错误", "请选择要删除的用户")
            return
            
        try:
            # 验证密码
            conn = sqlite3.connect(UserManager.USERS_DB)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE username=?",
                (username,)
            )
            result = cursor.fetchone()
            
            if not result:
                QMessageBox.warning(dialog, "错误", "用户不存在")
                return
                
            stored_password = result[0]
            
            # 如果有密码但未提供密码，或密码不匹配
            if stored_password and (not password or stored_password != password):
                QMessageBox.warning(dialog, "错误", "密码验证失败")
                return
                
            # 确认删除
            reply = QMessageBox.question(
                dialog, "确认删除",
                f"确定要永久删除用户 {username} 吗？此操作不可撤销！",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if UserManager.delete_user(username):
                    QMessageBox.information(dialog, "成功", "用户已删除")
                    dialog.accept()
                    # 刷新登录对话框的用户列表
                    self.load_registered_users()
                else:
                    QMessageBox.warning(dialog, "错误", "删除用户失败")
        except Exception as e:
            print(f"[DEBUG] 删除用户时出错: {str(e)}")
            QMessageBox.critical(dialog, "错误", f"删除用户时出错: {str(e)}")


    def init_db(self):
        """初始化数据库 - 修改为使用用户特定的数据库文件"""
        try:
            # 使用用户特定的数据库文件
            self.conn = sqlite3.connect(self.user_db_file)
            self.cursor = self.conn.cursor()
            
            # 创建部门表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            ''')
            
            # 插入默认部门
            default_depts = ["销售部", "技术部", "人事部", "财务部", "市场部", "客服部"]
            for dept in default_depts:
                try:
                    self.cursor.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (dept,))
                except Error as e:
                    print(f"插入部门 {dept} 时出错: {str(e)}")
            
            # 创建排班表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    position TEXT NOT NULL,
                    work_date TEXT NOT NULL,
                    shift_type TEXT NOT NULL,
                    remarks TEXT,
                    FOREIGN KEY(department) REFERENCES departments(name)
                )
            ''')
            
            # 创建自定义班次表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS custom_shifts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    shift_name TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    UNIQUE(shift_name)
                )
            ''')
            
            # 插入默认班次
            default_shifts = [
                ("早班", "08:00", "16:00"),
                ("中班", "16:00", "24:00"),
                ("晚班", "00:00", "08:00"),
                ("全天班", "08:00", "20:00"),
                ("早班(模糊)", "", ""),
                ("晚班(模糊)", "", "")
            ]
            for shift in default_shifts:
                try:
                    self.cursor.execute("INSERT OR IGNORE INTO custom_shifts (shift_name, start_time, end_time) VALUES (?, ?, ?)", shift)
                except Error as e:
                    print(f"插入班次 {shift[0]} 时出错: {str(e)}")
            
            self.conn.commit()
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法初始化数据库:\n{str(e)}")
            raise
    
    def init_ui(self):
        """初始化用户界面"""
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 添加月份导航和视图切换
        top_bar_layout = QHBoxLayout()
        main_layout.addLayout(top_bar_layout)
        
        # 月份导航
        month_nav_layout = QHBoxLayout()
        top_bar_layout.addLayout(month_nav_layout)
        
        self.prev_month_btn = QPushButton("◀ 上个月")
        self.prev_month_btn.clicked.connect(self.prev_month)
        month_nav_layout.addWidget(self.prev_month_btn)
        
        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        month_nav_layout.addWidget(self.month_label)
        
        self.next_month_btn = QPushButton("下个月 ▶")
        self.next_month_btn.clicked.connect(self.next_month)
        month_nav_layout.addWidget(self.next_month_btn)
        
        # 添加间隔
        top_bar_layout.addStretch()
        
        # 视图切换按钮
        self.view_toggle_btn = QPushButton("切换为列表视图")
        self.view_toggle_btn.clicked.connect(self.toggle_view)
        top_bar_layout.addWidget(self.view_toggle_btn)
        
        self.switch_user_btn = QPushButton(f"切换用户 ({self.current_user})")
        self.switch_user_btn.clicked.connect(self.switch_user)
        top_bar_layout.addWidget(self.switch_user_btn)

        # 当前视图状态
        self.is_calendar_view = True
        
        # 日历视图容器
        self.calendar_container = QWidget()
        self.calendar_layout = QVBoxLayout(self.calendar_container)
        self.calendar_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.calendar_container)
        
        # 列表视图容器
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_container)
        self.list_container.hide()
        
        # 初始化列表视图
        self.init_list_view()
        
        # 设置当前月份
        self.current_date = QDate.currentDate()
        self.update_calendar_view()
        
        # 状态栏
        self.statusBar().showMessage("就绪")


    def prev_month(self):
        """切换到上个月"""
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar_view()

    def next_month(self):
        """切换到下个月"""
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar_view()
        
    def toggle_view(self):
        """切换视图模式"""
        self.is_calendar_view = not self.is_calendar_view
        
        if self.is_calendar_view:
            self.calendar_container.show()
            self.list_container.hide()
            self.view_toggle_btn.setText("切换为列表视图")
            self.update_calendar_view()
        else:
            self.calendar_container.hide()
            self.list_container.show()
            self.view_toggle_btn.setText("切换为月历视图")
            self.load_data()

    def update_calendar_view(self):
        """更新月历视图"""
        # 清除旧视图
        for i in reversed(range(self.calendar_layout.count())): 
            self.calendar_layout.itemAt(i).widget().setParent(None)
        
        # 设置月份标题
        self.month_label.setText(f"{self.current_date.year()}年{self.current_date.month()}月")
        
        # 创建日历表格
        calendar_table = QTableWidget()
        calendar_table.setEditTriggers(QTableWidget.NoEditTriggers)
        calendar_table.setSelectionMode(QTableWidget.NoSelection)
        
        # 设置表格样式
        calendar_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        # 设置表格为7列(一周7天)
        calendar_table.setColumnCount(7)

        # 添加双击事件连接
        calendar_table.doubleClicked.connect(self.handle_calendar_double_click)
        
        calendar_table.setHorizontalHeaderLabels(["周日", "周一", "周二", "周三", "周四", "周五", "周六"])
        
        # 设置表头样式
        calendar_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
        """)
    
        # 启用右键菜单
        calendar_table.setContextMenuPolicy(Qt.CustomContextMenu)
        calendar_table.customContextMenuRequested.connect(self.show_calendar_context_menu)

        # 计算当月天数
        month_days = self.current_date.daysInMonth()
        first_day = QDate(self.current_date.year(), self.current_date.month(), 1)
        start_day = first_day.dayOfWeek() % 7  # Qt的周日是7，我们调整为0
        
        # 计算需要的行数
        rows = ((start_day + month_days - 1) // 7) + 1
        calendar_table.setRowCount(rows)
        
        # 预先加载本月所有排班数据以确定颜色分配
        start_date = QDate(self.current_date.year(), self.current_date.month(), 1)
        end_date = QDate(self.current_date.year(), self.current_date.month(), month_days)
        
        try:
            self.cursor.execute('''
                SELECT DISTINCT employee_name 
                FROM schedules 
                WHERE work_date BETWEEN ? AND ?
                ORDER BY employee_name
            ''', (start_date.toString("yyyy-MM-dd"), end_date.toString("yyyy-MM-dd")))
            employees = self.cursor.fetchall()
            
            # 为每个员工分配颜色
            for emp in employees:
                name = emp[0]
                if name not in self.name_color_map:
                    color_idx = len(self.name_color_map) % len(self.color_list)
                    self.name_color_map[name] = self.color_list[color_idx]
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载员工列表:\n{str(e)}")
            return
        
        # 填充日期
        for day in range(1, month_days + 1):
            date = QDate(self.current_date.year(), self.current_date.month(), day)
            day_of_week = date.dayOfWeek() % 7
            row = (start_day + day - 1) // 7
            
            # 创建日期单元格
            date_item = QTableWidgetItem(str(day))
            date_item.setData(Qt.UserRole, date)  # 存储日期对象
            date_item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)
            
            # 设置周末颜色
            if day_of_week == 0 or day_of_week == 6:  # 周日(0)或周六(6)
                date_item.setForeground(QColor(255, 0, 0))  # 红色
        
            calendar_table.setItem(row, day_of_week, date_item)
            
            # 加载当天的排班数据
            self.load_day_schedules(calendar_table, row, day_of_week, date)
        
        # 调整列宽和行高
        calendar_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        calendar_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置行高
        for row in range(calendar_table.rowCount()):
            calendar_table.setRowHeight(row, 100)  # 固定行高

        self.calendar_layout.addWidget(calendar_table)


    def load_day_schedules(self, table, row, col, date):
        """加载某一天的排班数据"""
        try:
            date_str = date.toString("yyyy-MM-dd")
            self.cursor.execute('''
                SELECT employee_name, department, shift_type 
                FROM schedules 
                WHERE work_date = ?
                ORDER BY department, employee_name
            ''', (date_str,))
            schedules = self.cursor.fetchall()
            
            if not schedules:
                return
                
            # 创建显示内容的文本
            content = QLabel()
            text = f"<div style='font-weight:bold;'>{date.day()}</div>"  # 第一行：日期（加粗显示）
            
            for schedule in schedules:
                name, dept, shift = schedule
                # 为每个姓名分配颜色（如果尚未分配）
                if name not in self.name_color_map:
                    color_idx = len(self.name_color_map) % len(self.color_list)
                    self.name_color_map[name] = self.color_list[color_idx]
                
                # 第二行：人名（带部门）
                text += f"<div>{name}({dept})</div>"
                # 第三行：班次
                text += f"<div>{shift}</div>"
            
            content.setText(text.strip())
            content.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            content.setMargin(5)
            
            # 设置背景色 - 使用第一个员工的颜色
            first_name = schedules[0][0]
            content.setStyleSheet(f"""
                background-color: {self.name_color_map[first_name].name()};
                padding: 5px;
                border-radius: 3px;
            """)

            # 设置单元格属性
            content.setProperty("date", date_str)  # 存储日期信息
            content.setProperty("has_data", True)  # 标记有数据

            # 设置单元格部件
            table.setCellWidget(row, col, content)
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载排班数据:\n{str(e)}")



    def init_list_view(self):
        """初始化列表视图"""
        # 顶部搜索和过滤区域
        filter_layout = QHBoxLayout()
        self.list_layout.addLayout(filter_layout)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入员工姓名或部门搜索...")
        self.search_input.textChanged.connect(self.load_data)
        filter_layout.addWidget(self.search_input)
        
        # 日期过滤
        filter_layout.addWidget(QLabel("开始日期:"))
        self.start_date_edit = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.dateChanged.connect(self.load_data)
        filter_layout.addWidget(self.start_date_edit)
        
        filter_layout.addWidget(QLabel("结束日期:"))
        self.end_date_edit = QDateEdit(QDate.currentDate().addMonths(1))
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.dateChanged.connect(self.load_data)
        filter_layout.addWidget(self.end_date_edit)
        
        # 部门过滤
        self.dept_filter = QComboBox()
        self.dept_filter.addItem("所有部门", "")
        self.load_departments()
        self.dept_filter.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(self.dept_filter)
        
        # 表格视图
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.doubleClicked.connect(self.edit_record)
        
        # 设置表格模型
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "员工姓名", "部门", "职位", "工作日期", "班次类型", "备注"])
        self.table_view.setModel(self.model)
        
        # 调整列宽
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setColumnHidden(0, True)  # 隐藏ID列
        
        self.list_layout.addWidget(self.table_view)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.list_layout.addLayout(button_layout)
        
        # 添加按钮
        self.add_btn = QPushButton("添加排班")
        self.add_btn.clicked.connect(self.add_record)
        button_layout.addWidget(self.add_btn)
        
        # 编辑按钮
        self.edit_btn = QPushButton("编辑排班")
        self.edit_btn.clicked.connect(self.edit_record)
        button_layout.addWidget(self.edit_btn)
        
        # 删除按钮
        self.delete_btn = QPushButton("删除排班")
        self.delete_btn.clicked.connect(self.delete_record)
        button_layout.addWidget(self.delete_btn)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新数据")
        self.refresh_btn.clicked.connect(self.load_data)
        button_layout.addWidget(self.refresh_btn)

    def show_calendar_context_menu(self, pos):
        """显示月历视图的右键菜单"""
        if self.is_calendar_view:
            table = self.sender()
            index = table.indexAt(pos)
            
            if index.isValid():
                # 获取日期数据
                item = table.item(index.row(), index.column())
                if item and item.data(Qt.UserRole):
                    date = item.data(Qt.UserRole)
                    date_str = date.toString("yyyy-MM-dd")
                    
                    # 创建菜单
                    menu = QMenu(self)
                    
                    # 添加排班
                    add_action = menu.addAction("添加排班")
                    add_action.triggered.connect(lambda: self.add_calendar_record(date_str))
                    
                    # 编辑/删除排班
                    try:
                        self.cursor.execute('''
                            SELECT id, employee_name, department, shift_type 
                            FROM schedules 
                            WHERE work_date = ?
                            ORDER BY department, employee_name
                        ''', (date_str,))
                        schedules = self.cursor.fetchall()
                        
                        if schedules:
                            # 添加分隔线
                            menu.addSeparator()
                            
                            # 为每个排班添加编辑和删除选项
                            for schedule in schedules:
                                sched_id, name, dept, shift = schedule
                                sub_menu = menu.addMenu(f"{name}({dept}): {shift}")
                                
                                # 编辑选项
                                edit_action = sub_menu.addAction("编辑")
                                edit_action.triggered.connect(lambda _, id=sched_id: self.edit_calendar_record(id))
                                
                                # 删除选项
                                delete_action = sub_menu.addAction("删除")
                                delete_action.triggered.connect(lambda _, id=sched_id: self.delete_calendar_record(id))
                    
                    except Error as e:
                        QMessageBox.critical(self, "数据库错误", f"无法查询排班数据:\n{str(e)}")
                        return
                    
                    # 添加刷新选项
                    menu.addSeparator()
                    refresh_action = menu.addAction("刷新数据")
                    refresh_action.triggered.connect(self.update_calendar_view)
                    
                    # 显示菜单
                    menu.exec_(table.viewport().mapToGlobal(pos))


    def add_calendar_record(self, date_str):
        """在月历视图中添加排班记录"""
        dialog = ScheduleDialog(self)
        dialog.work_date.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                # 更新最后选择的部门和班次类型
                ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                
                self.cursor.execute('''
                    INSERT INTO schedules 
                    (employee_name, department, position, work_date, shift_type, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', data)
                self.conn.commit()
                self.update_calendar_view()
                self.statusBar().showMessage("排班记录添加成功")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法添加排班记录:\n{str(e)}")

    def edit_calendar_record(self, record_id):
        """在月历视图中编辑排班记录"""
        try:
            self.cursor.execute("SELECT * FROM schedules WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                dialog = ScheduleDialog(self, is_edit_mode=True)  # 设置为编辑模式
                dialog.set_data(record[1:])  # 跳过ID字段
                
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    # 更新最后选择的部门和班次类型
                    ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                    ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                    
                    # 添加ID到数据末尾用于WHERE条件
                    data = data + (record_id,)
                    self.cursor.execute('''
                        UPDATE schedules 
                        SET employee_name=?, department=?, position=?, work_date=?, shift_type=?, remarks=?
                        WHERE id=?
                    ''', data)
                    self.conn.commit()
                    self.update_calendar_view()
                    self.statusBar().showMessage("排班记录更新成功")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法编辑排班记录:\n{str(e)}")


    def delete_calendar_record(self, record_id):
        """在月历视图中删除排班记录"""
        try:
            self.cursor.execute("SELECT employee_name, work_date FROM schedules WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                name, date = record
                reply = QMessageBox.question(
                    self, "确认删除",
                    f"确定要删除 {name} 在 {date} 的排班记录吗?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    self.cursor.execute("DELETE FROM schedules WHERE id = ?", (record_id,))
                    self.conn.commit()
                    self.update_calendar_view()
                    self.statusBar().showMessage("排班记录删除成功")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法删除排班记录:\n{str(e)}")

    def handle_calendar_double_click(self, index):
        """处理月历视图的双击事件"""
        table = self.sender()
        if not index.isValid():
            return
            
        item = table.item(index.row(), index.column())
        if not item or not item.data(Qt.UserRole):
            return
            
        date = item.data(Qt.UserRole)
        date_str = date.toString("yyyy-MM-dd")
        
        # 检查该日期是否有排班记录
        try:
            self.cursor.execute('''
                SELECT id, employee_name, department, shift_type 
                FROM schedules 
                WHERE work_date = ?
                ORDER BY department, employee_name
            ''', (date_str,))
            schedules = self.cursor.fetchall()
            
            if schedules:
                # 如果有记录，弹出编辑窗口（编辑第一条记录）
                self.edit_calendar_record(schedules[0][0])
            else:
                # 如果没有记录，弹出添加窗口
                self.add_calendar_record(date_str)
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法查询排班数据:\n{str(e)}")




    def load_departments(self):
        """加载部门列表"""
        try:
            self.cursor.execute("SELECT DISTINCT department FROM schedules ORDER BY department")
            departments = self.cursor.fetchall()
            for dept in departments:
                self.dept_filter.addItem(dept[0], dept[0])
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载部门列表:\n{str(e)}")
    
    def load_data(self):
        """加载排班数据(列表视图)"""
        if self.is_calendar_view:
            return
            
        try:
            # 获取过滤条件
            search_text = self.search_input.text().strip()
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
            dept_filter = self.dept_filter.currentData()
            
            # 构建查询
            query = '''
                SELECT id, employee_name, department, position, work_date, shift_type, remarks 
                FROM schedules 
                WHERE work_date BETWEEN ? AND ?
            '''
            params = [start_date, end_date]
            
            # 添加搜索条件
            if search_text:
                query += " AND (employee_name LIKE ? OR department LIKE ?)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # 添加部门过滤
            if dept_filter:
                query += " AND department = ?"
                params.append(dept_filter)
            
            query += " ORDER BY work_date, department, employee_name"
            
            self.cursor.execute(query, params)
            records = self.cursor.fetchall()
            
            # 更新模型
            self.model.setRowCount(0)
        
            # 重置颜色映射（可选，如果希望每次加载都重新分配颜色）
            # self.name_color_map = {}
            
            for row_num, row_data in enumerate(records):
                self.model.insertRow(row_num)
                employee_name = str(row_data[1])  # 员工姓名在索引1的位置
                
                # 为每个姓名分配颜色（如果尚未分配）
                if employee_name not in self.name_color_map:
                    color_idx = len(self.name_color_map) % len(self.color_list)
                    self.name_color_map[employee_name] = self.color_list[color_idx]
            
                for col_num, col_data in enumerate(row_data):
                    item = QStandardItem(str(col_data))
                    item.setEditable(False)

                    # 设置背景色
                    if col_num in [1, 2, 3]:  # 姓名、部门、职位列
                        item.setBackground(self.name_color_map[employee_name])
                    
                    self.model.setItem(row_num, col_num, item)
            
            self.statusBar().showMessage(f"共加载 {len(records)} 条排班记录")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载排班数据:\n{str(e)}")
    
    def add_record(self):
        """添加新排班记录"""
        dialog = ScheduleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                # 更新最后选择的部门和班次类型
                ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                
                self.cursor.execute('''
                    INSERT INTO schedules 
                    (employee_name, department, position, work_date, shift_type, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', data)
                self.conn.commit()
                if self.is_calendar_view:
                    self.update_calendar_view()
                else:
                    self.load_data()
                self.statusBar().showMessage("排班记录添加成功")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法添加排班记录:\n{str(e)}")

    def edit_record(self):
        """编辑排班记录"""
        if self.is_calendar_view:
            # 在月历视图中不支持编辑
            QMessageBox.information(self, "提示", "请在列表视图中编辑排班记录")
            return
            
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择要编辑的排班记录")
            return
        
        row = selected[0].row()
        record_id = self.model.item(row, 0).text()
        
        try:
            self.cursor.execute("SELECT * FROM schedules WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                dialog = ScheduleDialog(self, is_edit_mode=True)  # 设置为编辑模式
                dialog.set_data(record[1:])  # 跳过ID字段
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    # 更新最后选择的部门和班次类型
                    ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                    ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                    
                    # 添加ID到数据末尾用于WHERE条件
                    data = data + (record_id,)
                    self.cursor.execute('''
                        UPDATE schedules 
                        SET employee_name=?, department=?, position=?, work_date=?, shift_type=?, remarks=?
                        WHERE id=?
                    ''', data)
                    self.conn.commit()
                    self.load_data()
                    self.statusBar().showMessage("排班记录更新成功")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法编辑排班记录:\n{str(e)}")

    def delete_record(self):
        """删除排班记录"""
        if self.is_calendar_view:
            # 在月历视图中不支持删除
            QMessageBox.information(self, "提示", "请在列表视图中删除排班记录")
            return
            
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择要删除的排班记录")
            return
        
        row = selected[0].row()
        record_id = self.model.item(row, 0).text()
        employee_name = self.model.item(row, 1).text()
        work_date = self.model.item(row, 4).text()
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除 {employee_name} 在 {work_date} 的排班记录吗?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM schedules WHERE id = ?", (record_id,))
                self.conn.commit()
                self.load_data()
                self.statusBar().showMessage("排班记录删除成功")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法删除排班记录:\n{str(e)}")



    def closeEvent(self, event):
        """关闭窗口时关闭数据库连接"""
        self.conn.close()
        event.accept()

    def switch_user(self):
        """切换用户"""
        reply = QMessageBox.question(
            self, "切换用户", 
            "确定要切换用户吗？当前未保存的更改将会丢失。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 关闭当前数据库连接
            self.conn.close()
            
            # 显示登录对话框
            if self.show_login_dialog():
                # 重新初始化数据库
                self.init_db()
                
                # 重新加载数据
                if self.is_calendar_view:
                    self.update_calendar_view()
                else:
                    self.load_data()
                
                # 更新窗口标题和按钮文本
                self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} - 当前用户: {self.current_user}")
                self.switch_user_btn.setText(f"切换用户 ({self.current_user})")
                self.statusBar().showMessage(f"已切换到用户: {self.current_user}")

class ScheduleDialog(QDialog):
    """排班记录编辑对话框"""
    last_department = ""  # 类变量存储最后选择的部门
    last_shift_type = ""  # 类变量存储最后选择的班次类型
    
    def __init__(self, parent=None, is_edit_mode=False):
        super().__init__(parent)
        self.is_edit_mode = is_edit_mode
        self.setWindowTitle("排班记录")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(400, 350)
        
        # 表单布局
        layout = QFormLayout()
        self.setLayout(layout)
        
        # 员工姓名
        self.employee_name = QLineEdit()
        layout.addRow("员工姓名:", self.employee_name)
        
        # 部门
        self.department = QComboBox()
        self.department.setEditable(True)
        
        try:
            parent.cursor.execute("SELECT name FROM departments ORDER BY name")
            depts = parent.cursor.fetchall()
            self.department.addItems([dept[0] for dept in depts])
            
            # 如果不是编辑模式，使用最后选择的部门
            if not self.is_edit_mode and ScheduleDialog.last_department:
                dept_index = self.department.findText(ScheduleDialog.last_department)
                if dept_index >= 0:
                    self.department.setCurrentIndex(dept_index)
                else:
                    self.department.setCurrentText(ScheduleDialog.last_department)
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载部门列表:\n{str(e)}")
        
        layout.addRow("部门:", self.department)
        
        # 自定义部门按钮
        self.custom_dept_btn = QPushButton("自定义部门")
        self.custom_dept_btn.clicked.connect(self.show_custom_dept_dialog)
        layout.addRow("", self.custom_dept_btn)
        
        # 职位
        self.position = QLineEdit()
        layout.addRow("职位:", self.position)
        
        # 工作日期
        self.work_date = QDateEdit(QDate.currentDate())
        self.work_date.setCalendarPopup(True)
        layout.addRow("工作日期:", self.work_date)
        
        # 班次类型
        self.shift_type = QComboBox()
        self.shift_type.setEditable(True)
        
        try:
            parent.cursor.execute("SELECT shift_name || ' (' || start_time || '-' || end_time || ')' FROM custom_shifts ORDER BY shift_name")
            shifts = parent.cursor.fetchall()
            self.shift_type.addItems([shift[0] for shift in shifts])
        
            # 设置最后选择的班次类型
            if ScheduleDialog.last_shift_type:
                shift_index = self.shift_type.findText(ScheduleDialog.last_shift_type)
                if shift_index >= 0:
                    self.shift_type.setCurrentIndex(shift_index)
                else:
                    self.shift_type.setCurrentText(ScheduleDialog.last_shift_type)
            else:
                # 如果没有最后选择的班次，设置默认选中"全天班"
                full_day_index = -1
                for i in range(self.shift_type.count()):
                    if "全天班" in self.shift_type.itemText(i):
                        full_day_index = i
                        break
                
                if full_day_index != -1:
                    self.shift_type.setCurrentIndex(full_day_index)
            
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载班次列表:\n{str(e)}")
        
        layout.addRow("班次类型:", self.shift_type)
        
        # 自定义班次按钮
        self.custom_shift_btn = QPushButton("自定义时间段")
        self.custom_shift_btn.clicked.connect(self.show_custom_shift_dialog)
        layout.addRow("", self.custom_shift_btn)
        
        # 备注
        self.remarks = QLineEdit()
        layout.addRow("备注:", self.remarks)
        
        # 按钮
        button_layout = QHBoxLayout()
        layout.addRow(button_layout)
        
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)





    def show_custom_dept_dialog(self):
        """显示自定义部门对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("自定义部门")
        dialog.resize(300, 150)
        
        layout = QFormLayout(dialog)
        
        self.new_dept = QLineEdit()
        self.new_dept.setPlaceholderText("输入新部门名称")
        layout.addRow("部门名称:", self.new_dept)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted and self.new_dept.text().strip():
            new_dept = self.new_dept.text().strip()
            try:
                self.parent().cursor.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (new_dept,))
                self.parent().conn.commit()
                self.department.addItem(new_dept)
                self.department.setCurrentText(new_dept)
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法添加部门:\n{str(e)}")

    def show_custom_shift_dialog(self):
        """显示自定义时间段对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("自定义班次时间段")
        dialog.resize(300, 200)
        
        layout = QFormLayout(dialog)
        
        # 班次名称
        self.shift_name = QLineEdit()
        self.shift_name.setPlaceholderText("例如: 弹性班")
        layout.addRow("班次名称:", self.shift_name)
        
        # 开始时间
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setTime(QTime(8, 0))  # 默认8:00
        self.start_time.setSpecialValueText("无")  # 添加特殊值显示
        layout.addRow("开始时间:", self.start_time)
        
        # 结束时间
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setTime(QTime(17, 0))  # 默认17:00
        self.end_time.setSpecialValueText("无")  # 添加特殊值显示
        layout.addRow("结束时间:", self.end_time)
    
        # 添加说明标签
        info_label = QLabel("提示: 可以留空时间创建模糊班次")
        info_label.setStyleSheet("color: gray;")
        layout.addRow(info_label)
    
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            shift_name = self.shift_name.text().strip()
            if not shift_name:
                QMessageBox.warning(self, "警告", "请输入班次名称")
                return
                
            # 处理时间输入
            start_time = self.start_time.time().toString("HH:mm") if self.start_time.time().isValid() else ""
            end_time = self.end_time.time().toString("HH:mm") if self.end_time.time().isValid() else ""
            
            try:
                # 保存到数据库
                self.parent().cursor.execute(
                    "INSERT OR REPLACE INTO custom_shifts (shift_name, start_time, end_time) VALUES (?, ?, ?)",
                    (shift_name, start_time, end_time)
                )
                self.parent().conn.commit()
                
                # 更新下拉框
                shift_text = f"{shift_name} ({start_time}-{end_time})" if start_time and end_time else shift_name
                if self.shift_type.findText(shift_text) == -1:
                    self.shift_type.addItem(shift_text)
                self.shift_type.setCurrentText(shift_text)
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法保存自定义班次:\n{str(e)}")

    def get_data(self):
        """获取表单数据"""
        return (
            self.employee_name.text().strip(),
            self.department.currentText().strip(),
            self.position.text().strip(),
            self.work_date.date().toString("yyyy-MM-dd"),
            self.shift_type.currentText(),
            self.remarks.text().strip()
        )
    
    def set_data(self, data):
        """设置表单数据"""
        self.employee_name.setText(data[0])
        
        dept_index = self.department.findText(data[1])
        if dept_index >= 0:
            self.department.setCurrentIndex(dept_index)
        else:
            self.department.setCurrentText(data[1])
        
        self.position.setText(data[2])
        self.work_date.setDate(QDate.fromString(data[3], "yyyy-MM-dd"))
        
        shift_index = self.shift_type.findText(data[4])
        if shift_index >= 0:
            self.shift_type.setCurrentIndex(shift_index)
        else:
            self.shift_type.setCurrentText(data[4])
        
        self.remarks.setText(data[5] if data[5] else "")

        # 只有在添加模式下才更新最后选择的值
        if not self.is_edit_mode:
            ScheduleDialog.last_department = data[1]
            ScheduleDialog.last_shift_type = data[4]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置中文字体
    font = app.font()
    font.setFamily("Microsoft YaHei")
    app.setFont(font)
    
    try:
        window = ScheduleManager()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "错误", f"应用程序启动失败: {str(e)}")
        sys.exit(1)
