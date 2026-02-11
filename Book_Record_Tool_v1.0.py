import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QListWidget, QListWidgetItem,
                            QLineEdit, QTextEdit, QLabel, QComboBox, QMessageBox,
                            QGroupBox, QFormLayout, QTabWidget, QDialog, 
                            QComboBox, QSplitter, QFrame, QMenuBar, QMenu, QAction, QActionGroup)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap, QPainter, QBrush, QPen

# 设置护眼配色方案
EYE_PROTECTION_COLORS = {
    'background': '#F5F5DC',
    'widget_bg': '#FAFAF0',
    'text': '#2F4F4F',
    'button_bg': '#8FBC8F',
    'button_hover': '#7CCD7C',
    'button_delete': '#FF7F50',
    'button_delete_hover': '#FF6347',
    'list_bg': '#FFFFF0',
    'list_selected': '#EEE8AA',
    'group_bg': '#F0F8FF',
    'tab_bg': '#F5F5F5',
    'tab_selected': '#E0EEE0',
    'year_filter_bg': '#E6E6FA',
}

# 字体大小设置 - 增加更多选项
FONT_SIZES = {
    '8 pt': 8,
    '9 pt': 9,
    '10 pt': 10,
    '11 pt': 11,
    '12 pt': 12,  # 默认
    '13 pt': 13,
    '14 pt': 14,
    '15 pt': 15,
    '16 pt': 16,
    '17 pt': 17,
    '18 pt': 18,
    '20 pt': 20,
    '22 pt': 22,
    '24 pt': 24,
}

# 默认字体大小
DEFAULT_FONT_SIZE = '12 pt'

# 全局字体管理器
class FontManager:
    """字体管理器"""
    def __init__(self):
        self.current_size = DEFAULT_FONT_SIZE
        self.base_font = QFont("Microsoft YaHei", FONT_SIZES[self.current_size])
        self.font_actions = {}  # 存储字体菜单项
        self.font_action_group = None  # 字体菜单动作组
    
    def get_font_size(self):
        """获取当前字体大小"""
        return FONT_SIZES[self.current_size]
    
    def get_font_size_name(self):
        """获取当前字体大小名称"""
        return self.current_size
    
    def set_font_size(self, size_name):
        """设置字体大小"""
        if size_name in FONT_SIZES:
            self.current_size = size_name
            self.base_font.setPointSize(FONT_SIZES[size_name])
            
            # 更新菜单项的勾选状态
            if self.font_action_group:
                for action_name, action in self.font_actions.items():
                    action.setChecked(action_name == size_name)
            
            return True
        return False
    
    def get_font(self, bold=False, size_multiplier=1.0):
        """获取字体"""
        font = QFont(self.base_font)
        font.setBold(bold)
        font.setPointSize(int(font.pointSize() * size_multiplier))
        return font

FONT_MANAGER = FontManager()

def get_resource_path(relative_path):
    """获取资源文件的绝对路径，支持打包和开发模式"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def create_book_icon():
    """创建一个书籍图标的QIcon"""
    # 创建不同大小的图标
    sizes = [16, 24, 32, 48, 64, 128, 256]
    icon = QIcon()
    
    for size in sizes:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 计算缩放比例
        scale = size / 64.0
        
        # 使用护眼主题颜色
        book_color = QColor(143, 188, 143)  # 暗海绿色
        book_outline = QColor(111, 156, 111)
        page_color = QColor(245, 245, 220)  # 米色
        
        # 根据大小调整线宽
        line_width = max(1, int(2 * scale))
        
        # 绘制书脊
        painter.setBrush(QBrush(book_color))
        painter.setPen(QPen(book_outline, line_width))
        x1, y1 = int(20 * scale), int(12 * scale)
        w1, h1 = int(12 * scale), int(40 * scale)
        painter.drawRect(x1, y1, w1, h1)
        
        # 绘制封面
        painter.setBrush(QBrush(page_color))
        painter.setPen(QPen(book_outline, line_width))
        points = [
            (int(32 * scale), int(12 * scale)),    # 左上
            (int(52 * scale), int(24 * scale)),    # 右上
            (int(52 * scale), int(52 * scale)),    # 右下
            (int(32 * scale), int(40 * scale))     # 左下
        ]
        painter.drawPolygon(*points)
        
        # 绘制书页线
        if size >= 32:  # 只在较大图标上绘制细节
            painter.setPen(QPen(QColor(180, 180, 180), max(1, int(1 * scale))))
            for i in range(3):
                y = int((20 + i * 10) * scale)
                painter.drawLine(int(32 * scale), y, int(52 * scale), int((y + 12 * scale)))
        
        painter.end()
        icon.addPixmap(pixmap)
    
    return icon

def get_application_icon():
    """获取应用程序图标，优先从文件加载，失败则使用程序生成"""
    # 1. 首先尝试从ICO文件加载
    try:
        icon_path = get_resource_path("book_icon.ico")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            if not icon.isNull():
                return icon
    except:
        pass
    
    # 2. 尝试从PNG文件加载
    try:
        icon_path = get_resource_path("book_icon.png")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            if not icon.isNull():
                return icon
    except:
        pass
    
    # 3. 如果文件加载失败，使用程序生成的图标
    return create_book_icon()

# 全局图标变量
APP_ICON = None

def get_app_icon():
    """获取应用程序图标（单例模式）"""
    global APP_ICON
    if APP_ICON is None:
        APP_ICON = get_application_icon()
    return APP_ICON

class Book:
    """书籍数据类"""
    def __init__(self, title="", author="", status="想读", notes="", finish_date=None):
        self.title = title
        self.author = author
        self.status = status
        self.notes = notes
        self.add_date = datetime.now().strftime("%Y-%m-%d")
        self.finish_date = finish_date
        self.start_date = None
        if status == "在读":
            self.start_date = datetime.now().strftime("%Y-%m-%d")
        elif status == "已读" and not finish_date:
            self.finish_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        """转换为字典，方便JSON序列化"""
        return {
            'title': self.title,
            'author': self.author,
            'status': self.status,
            'notes': self.notes,
            'add_date': self.add_date,
            'finish_date': self.finish_date,
            'start_date': self.start_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建Book对象"""
        book = cls()
        book.title = data.get('title', '')
        book.author = data.get('author', '')
        book.status = data.get('status', '想读')
        book.notes = data.get('notes', '')
        book.add_date = data.get('add_date', '')
        book.finish_date = data.get('finish_date')
        book.start_date = data.get('start_date')
        return book

class BookManager:
    """书籍数据管理器"""
    def __init__(self, data_file='books_data.json'):
        # 获取可执行文件所在的目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            base_path = os.path.dirname(sys.executable)
        else:
            # 如果是Python脚本
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.data_file = os.path.join(base_path, data_file)
        self.books = []
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        self.load_data()
        print(f"数据文件路径: {self.data_file}")
        print(f"文件存在: {os.path.exists(self.data_file)}")
        print(f"加载了 {len(self.books)} 本书籍")
    
    def add_book(self, book):
        """添加书籍"""
        self.books.append(book)
        self.save_data()
        print(f"添加书籍: {book.title}")
    
    def update_book(self, index, book):
        """更新书籍信息"""
        if 0 <= index < len(self.books):
            self.books[index] = book
            self.save_data()
    
    def delete_book(self, index):
        """删除书籍"""
        if 0 <= index < len(self.books):
            del self.books[index]
            self.save_data()
    
    def get_books_by_status(self, status):
        """按状态获取书籍"""
        return [book for book in self.books if book.status == status]
    
    def get_books_by_year(self, year):
        """按年份获取已读书籍"""
        finished_books = self.get_books_by_status("已读")
        if year == "全部":
            return finished_books
        try:
            year_int = int(year)
            return [book for book in finished_books 
                    if book.finish_date and book.finish_date.startswith(str(year_int))]
        except:
            return []
    
    def get_years(self):
        """获取所有已读书籍的年份"""
        years = set()
        for book in self.books:
            if book.status == "已读" and book.finish_date:
                try:
                    year = int(book.finish_date[:4])  # 提取年份
                    years.add(year)
                except:
                    continue
        return sorted(list(years), reverse=True)  # 从新到旧排序
    
    def save_data(self):
        """保存数据到文件"""
        try:
            data = [book.to_dict() for book in self.books]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到: {self.data_file}")
        except Exception as e:
            print(f"保存数据时出错: {e}")
            QMessageBox.critical(None, "错误", f"保存数据时出错: {e}")
    
    def load_data(self):
        """从文件加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(item) for item in data]
                print(f"从 {self.data_file} 加载了 {len(self.books)} 本书籍")
            else:
                print(f"数据文件不存在，将创建新文件: {self.data_file}")
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                self.books = []
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            QMessageBox.warning(None, "数据文件错误", f"数据文件格式错误，将创建新文件。\n错误: {e}")
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            self.books = []
        except Exception as e:
            print(f"加载数据时出错: {e}")
            QMessageBox.warning(None, "加载错误", f"加载数据时出错: {e}")
            self.books = []

class BookDialog(QDialog):
    """书籍编辑对话框"""
    def __init__(self, book_manager, book=None, index=-1, parent=None):
        super().__init__(parent)
        self.book_manager = book_manager
        self.current_book = book
        self.current_index = index
        self.is_edit_mode = book is not None
        self.parent_window = parent
        
        self.init_ui()
        self.set_eye_protection_theme()
        
        # 设置对话框图标
        self.setWindowIcon(get_app_icon())
        
        if self.is_edit_mode:
            self.load_book_data()
    
    def init_ui(self):
        self.setWindowTitle("编辑书籍" if self.is_edit_mode else "添加新书")
        self.setMinimumSize(500, 500)
        self.resize(550, 500)
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # 设置字体
        label_font = FONT_MANAGER.get_font(bold=True)
        input_font = FONT_MANAGER.get_font()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("请输入书名（必填）")
        self.title_input.setMinimumHeight(35)
        self.title_input.setFont(input_font)
        form_layout.addRow(QLabel("书名:"), self.title_input)
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("请输入作者")
        self.author_input.setMinimumHeight(35)
        self.author_input.setFont(input_font)
        form_layout.addRow(QLabel("作者:"), self.author_input)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["想读", "在读", "已读"])
        self.status_combo.setMinimumHeight(35)
        self.status_combo.setFont(input_font)
        self.status_combo.currentTextChanged.connect(self.on_status_changed)
        form_layout.addRow(QLabel("状态:"), self.status_combo)
        
        notes_label = QLabel("笔记:")
        notes_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        notes_label.setFont(label_font)
        
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("请输入读书笔记或感想...")
        self.notes_text.setMinimumHeight(150)
        self.notes_text.setFont(input_font)
        form_layout.addRow(notes_label, self.notes_text)
        
        layout.addLayout(form_layout)
        layout.addStretch(1)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        button_font = FONT_MANAGER.get_font(bold=True)
        
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_book)
        self.save_button.setMinimumHeight(40)
        self.save_button.setMinimumWidth(100)
        self.save_button.setFont(button_font)
        self.save_button.setObjectName("saveButton")
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setMinimumWidth(100)
        self.cancel_button.setFont(button_font)
        self.cancel_button.setObjectName("cancelButton")
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_book_data(self):
        """加载现有书籍数据"""
        if self.current_book:
            self.title_input.setText(self.current_book.title)
            self.author_input.setText(self.current_book.author)
            self.status_combo.setCurrentText(self.current_book.status)
            self.notes_text.setPlainText(self.current_book.notes)
    
    def on_status_changed(self, status):
        """状态改变事件"""
        if self.is_edit_mode and self.current_book:
            if status == "已读" and self.current_book.finish_date is None:
                self.current_book.finish_date = datetime.now().strftime("%Y-%m-%d")
            elif status == "在读" and self.current_book.start_date is None:
                self.current_book.start_date = datetime.now().strftime("%Y-%m-%d")
    
    def save_book(self):
        """保存书籍"""
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "警告", "请输入书名！")
            return
        
        author = self.author_input.text().strip()
        status = self.status_combo.currentText()
        notes = self.notes_text.toPlainText()
        
        if not self.is_edit_mode:
            finish_date = datetime.now().strftime("%Y-%m-%d") if status == "已读" else None
            start_date = datetime.now().strftime("%Y-%m-%d") if status == "在读" else None
            
            new_book = Book(
                title=title,
                author=author,
                status=status,
                notes=notes,
                finish_date=finish_date
            )
            
            if start_date:
                new_book.start_date = start_date
            
            self.book_manager.add_book(new_book)
        else:
            new_status = status
            old_status = self.current_book.status
            
            if new_status == "已读" and old_status != "已读":
                self.current_book.finish_date = datetime.now().strftime("%Y-%m-%d")
            
            if new_status == "在读" and old_status == "想读":
                self.current_book.start_date = datetime.now().strftime("%Y-%m-%d")
            
            self.current_book.title = title
            self.current_book.author = author
            self.current_book.status = new_status
            self.current_book.notes = notes
            
            self.book_manager.update_book(self.current_index, self.current_book)
        
        if self.parent_window:
            self.parent_window.refresh_book_lists()
            self.parent_window.update_stats()
        
        self.accept()
    
    def set_eye_protection_theme(self):
        """设置护眼主题"""
        font_size = FONT_MANAGER.get_font_size()
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {EYE_PROTECTION_COLORS['background']};
                font-size: {font_size}px;
            }}
            QLineEdit, QTextEdit {{
                background-color: white;
                border: 1px solid #C0C0C0;
                border-radius: 4px;
                padding: 8px;
                color: {EYE_PROTECTION_COLORS['text']};
                font-size: {font_size}px;
            }}
            QComboBox {{
                background-color: white;
                border: 1px solid #C0C0C0;
                border-radius: 4px;
                padding: 8px;
                color: {EYE_PROTECTION_COLORS['text']};
                font-size: {font_size}px;
            }}
            QLabel {{
                color: {EYE_PROTECTION_COLORS['text']};
                font-weight: bold;
                font-size: {font_size}px;
            }}
            QPushButton#saveButton {{
                background-color: {EYE_PROTECTION_COLORS['button_bg']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: {font_size}px;
            }}
            QPushButton#saveButton:hover {{
                background-color: {EYE_PROTECTION_COLORS['button_hover']};
            }}
            QPushButton#cancelButton {{
                background-color: #B0B0B0;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: {font_size}px;
            }}
            QPushButton#cancelButton:hover {{
                background-color: #A0A0A0;
            }}
        """)

class YearReadingWidget(QWidget):
    """年份阅读统计部件"""
    def __init__(self, book_manager, parent=None):
        super().__init__(parent)
        self.book_manager = book_manager
        self.parent_window = parent
        self.init_ui()
        self.refresh_year_filter()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(10)
        
        year_label = QLabel("📅 按年份筛选:")
        year_label.setStyleSheet(f"""
            color: {EYE_PROTECTION_COLORS['text']}; 
            font-weight: bold; 
            font-size: {FONT_MANAGER.get_font_size()}px;
        """)
        
        self.year_combo = QComboBox()
        self.year_combo.setMinimumWidth(120)
        self.year_combo.setMinimumHeight(30)
        self.year_combo.setFont(FONT_MANAGER.get_font())
        self.year_combo.setObjectName("yearCombo")
        self.year_combo.currentTextChanged.connect(self.on_year_changed)
        
        filter_layout.addWidget(year_label)
        filter_layout.addWidget(self.year_combo)
        filter_layout.addStretch()
        
        layout.addWidget(filter_frame)
        
        self.finished_list = QListWidget()
        self.finished_list.itemClicked.connect(self.on_book_selected)
        self.finished_list.setObjectName("bookList")
        
        layout.addWidget(self.finished_list)
        self.setLayout(layout)
    
    def refresh_year_filter(self):
        """刷新年份筛选器"""
        years = self.book_manager.get_years()
        self.year_combo.clear()
        self.year_combo.addItem("全部")
        for year in years:
            self.year_combo.addItem(str(year))
        
        if years:
            self.year_combo.setCurrentText(str(years[0]))
    
    def on_year_changed(self, year_text):
        """年份选择变化"""
        if year_text:
            self.refresh_books_by_year(year_text)
    
    def refresh_books_by_year(self, year):
        """按年份刷新书籍列表"""
        self.finished_list.clear()
        
        books = self.book_manager.get_books_by_year(year)
        for i, book in enumerate(books):
            item_text = f"{book.title}"
            if book.author:
                item_text += f" - {book.author}"
            if book.finish_date:
                item_text += f" ({book.finish_date})"
            
            item = QListWidgetItem(item_text)
            item.setFont(FONT_MANAGER.get_font())
            item.setData(Qt.UserRole, i)
            item.setData(Qt.UserRole + 1, "已读")
            item.setData(Qt.UserRole + 2, year)
            self.finished_list.addItem(item)
    
    def on_book_selected(self, item):
        """书籍被选中"""
        if self.parent_window and hasattr(self.parent_window, 'on_year_book_selected'):
            self.parent_window.on_year_book_selected(item)

class BookRecordApp(QMainWindow):
    """主应用程序窗口"""
    def __init__(self):
        super().__init__()
        self.book_manager = BookManager()
        self.selected_book = None
        self.selected_index = -1
        
        # 设置窗口图标
        self.setWindowIcon(get_app_icon())
        
        self.init_ui()
        self.set_eye_protection_theme()
        
        # 应用初始字体设置
        self.apply_font_settings()
    
    def init_ui(self):
        self.setWindowTitle('读书记录工具 v1.0 - 护眼版（支持年份查看）')
        self.setGeometry(100, 100, 1200, 700)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 设置基础字体
        self.setFont(FONT_MANAGER.base_font)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        left_widget = QWidget()
        left_widget.setObjectName("leftWidget")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(15)
        
        # 添加新书按钮 - 使用更大字体
        self.add_button = QPushButton("📖 添加新书")
        self.add_button.clicked.connect(self.show_add_dialog)
        self.add_button.setMinimumHeight(45)
        self.add_button.setFont(FONT_MANAGER.get_font(bold=True, size_multiplier=1.1))
        self.add_button.setObjectName("addButton")
        left_layout.addWidget(self.add_button)
        
        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tabWidget")
        self.tab_widget.setFont(FONT_MANAGER.get_font(bold=True))
        
        # 想读标签页
        self.want_read_widget = QWidget()
        want_read_layout = QVBoxLayout(self.want_read_widget)
        self.want_read_list = QListWidget()
        self.want_read_list.itemClicked.connect(self.on_book_selected)
        self.want_read_list.setObjectName("bookList")
        want_read_layout.addWidget(self.want_read_list)
        self.tab_widget.addTab(self.want_read_widget, "📚 想读")
        
        # 在读标签页
        self.reading_widget = QWidget()
        reading_layout = QVBoxLayout(self.reading_widget)
        self.reading_list = QListWidget()
        self.reading_list.itemClicked.connect(self.on_book_selected)
        self.reading_list.setObjectName("bookList")
        reading_layout.addWidget(self.reading_list)
        self.tab_widget.addTab(self.reading_widget, "📖 在读")
        
        # 年份查看标签页
        self.year_reading_widget = YearReadingWidget(self.book_manager, self)
        self.tab_widget.addTab(self.year_reading_widget, "📅 年份查看")
        
        left_layout.addWidget(self.tab_widget)
        
        right_widget = QWidget()
        right_widget.setObjectName("rightWidget")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(15)
        
        # 书籍详情区域
        detail_group = QGroupBox("📋 书籍详情")
        detail_group.setObjectName("detailGroup")
        detail_group.setFont(FONT_MANAGER.get_font(bold=True, size_multiplier=1.1))
        detail_layout = QFormLayout()
        detail_layout.setSpacing(12)
        detail_layout.setLabelAlignment(Qt.AlignRight)
        
        # 设置标签和值标签的字体
        label_font = FONT_MANAGER.get_font(bold=True)
        value_font = FONT_MANAGER.get_font()
        
        self.title_label = QLabel("")
        self.title_label.setWordWrap(True)
        self.title_label.setFont(value_font)
        detail_layout.addRow(QLabel("书名:"), self.title_label)
        
        self.author_label = QLabel("")
        self.author_label.setFont(value_font)
        detail_layout.addRow(QLabel("作者:"), self.author_label)
        
        self.status_label = QLabel("")
        self.status_label.setFont(value_font)
        detail_layout.addRow(QLabel("状态:"), self.status_label)
        
        self.add_date_label = QLabel("")
        self.add_date_label.setFont(value_font)
        detail_layout.addRow(QLabel("添加日期:"), self.add_date_label)
        
        self.start_date_label = QLabel("")
        self.start_date_label.setFont(value_font)
        detail_layout.addRow(QLabel("开始日期:"), self.start_date_label)
        
        self.finish_date_label = QLabel("")
        self.finish_date_label.setFont(value_font)
        detail_layout.addRow(QLabel("完成日期:"), self.finish_date_label)
        
        file_info_label = QLabel(f"数据文件位置: {os.path.basename(self.book_manager.data_file)}")
        file_info_label.setFont(FONT_MANAGER.get_font(size_multiplier=0.9))
        file_info_label.setStyleSheet("color: #666666;")
        file_info_label.setToolTip(f"完整路径: {self.book_manager.data_file}")
        detail_layout.addRow(QLabel("数据文件:"), file_info_label)
        
        detail_group.setLayout(detail_layout)
        right_layout.addWidget(detail_group)
        
        # 笔记区域
        notes_group = QGroupBox("📝 读书笔记")
        notes_group.setObjectName("notesGroup")
        notes_group.setFont(FONT_MANAGER.get_font(bold=True, size_multiplier=1.1))
        notes_layout = QVBoxLayout()
        
        self.notes_display = QTextEdit()
        self.notes_display.setReadOnly(True)
        self.notes_display.setMinimumHeight(200)
        self.notes_display.setFont(value_font)
        self.notes_display.setObjectName("notesDisplay")
        notes_layout.addWidget(self.notes_display)
        
        notes_group.setLayout(notes_layout)
        right_layout.addWidget(notes_group)
        
        # 操作按钮 - 使用更大字体
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        button_font = FONT_MANAGER.get_font(bold=True)
        
        self.edit_button = QPushButton("✏️ 编辑")
        self.edit_button.clicked.connect(self.edit_book)
        self.edit_button.setEnabled(False)
        self.edit_button.setMinimumHeight(40)
        self.edit_button.setMinimumWidth(120)
        self.edit_button.setFont(button_font)
        self.edit_button.setObjectName("editButton")
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("🗑️ 删除")
        self.delete_button.clicked.connect(self.delete_book)
        self.delete_button.setEnabled(False)
        self.delete_button.setMinimumHeight(40)
        self.delete_button.setMinimumWidth(120)
        self.delete_button.setFont(button_font)
        self.delete_button.setObjectName("deleteButton")
        button_layout.addWidget(self.delete_button)
        
        right_layout.addLayout(button_layout)
        
        # 统计信息
        stats_group = QGroupBox("📊 阅读统计")
        stats_group.setObjectName("statsGroup")
        stats_group.setFont(FONT_MANAGER.get_font(bold=True, size_multiplier=1.1))
        stats_layout = QVBoxLayout()
        
        stats_font = FONT_MANAGER.get_font()
        
        self.stats_label = QLabel("总计: 0 | 想读: 0 | 在读: 0 | 已读: 0")
        self.stats_label.setObjectName("statsLabel")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setFont(stats_font)
        stats_layout.addWidget(self.stats_label)
        
        self.year_stats_label = QLabel("年份统计: 无数据")
        self.year_stats_label.setObjectName("yearStatsLabel")
        self.year_stats_label.setAlignment(Qt.AlignCenter)
        self.year_stats_label.setFont(stats_font)
        stats_layout.addWidget(self.year_stats_label)
        
        # 当前字体大小显示
        self.font_size_label = QLabel(f"当前字体大小: {FONT_MANAGER.get_font_size_name()}")
        self.font_size_label.setAlignment(Qt.AlignCenter)
        self.font_size_label.setFont(FONT_MANAGER.get_font(size_multiplier=0.9))
        self.font_size_label.setStyleSheet("color: #666666;")
        stats_layout.addWidget(self.font_size_label)
        
        stats_group.setLayout(stats_layout)
        right_layout.addWidget(stats_group)
        
        main_layout.addWidget(left_widget, 3)
        main_layout.addWidget(right_widget, 2)
        
        # 更新书籍列表
        self.refresh_book_lists()
        self.update_stats()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图')
        
        # 字体大小菜单
        font_size_menu = view_menu.addMenu('字体大小')
        
        # 创建动作组，确保单选
        FONT_MANAGER.font_action_group = QActionGroup(self)
        FONT_MANAGER.font_action_group.setExclusive(True)  # 确保单选
        
        # 创建字体大小菜单项
        for size_name in FONT_SIZES.keys():
            action = QAction(size_name, self)
            action.setCheckable(True)  # 设置为可勾选
            action.setChecked(size_name == FONT_MANAGER.current_size)  # 默认选中当前字体大小
            action.triggered.connect(lambda checked, name=size_name: self.change_font_size(name))
            
            FONT_MANAGER.font_actions[size_name] = action
            FONT_MANAGER.font_action_group.addAction(action)
            font_size_menu.addAction(action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def change_font_size(self, size_name):
        """改变字体大小"""
        if FONT_MANAGER.set_font_size(size_name):
            self.apply_font_settings()
            self.font_size_label.setText(f"当前字体大小: {FONT_MANAGER.get_font_size_name()}")
            # 不再显示提示消息，让用户通过查看统计面板了解当前字体大小
    
    def apply_font_settings(self):
        """应用字体设置到所有控件"""
        font_size = FONT_MANAGER.get_font_size()
        
        # 应用基础字体
        self.setFont(FONT_MANAGER.base_font)
        
        # 更新按钮字体
        button_font = FONT_MANAGER.get_font(bold=True)
        self.add_button.setFont(FONT_MANAGER.get_font(bold=True, size_multiplier=1.1))
        self.edit_button.setFont(button_font)
        self.delete_button.setFont(button_font)
        
        # 更新标签页字体
        self.tab_widget.setFont(FONT_MANAGER.get_font(bold=True))
        
        # 更新列表字体
        list_font = FONT_MANAGER.get_font()
        self.want_read_list.setFont(list_font)
        self.reading_list.setFont(list_font)
        if hasattr(self.year_reading_widget, 'finished_list'):
            self.year_reading_widget.finished_list.setFont(list_font)
        
        # 更新下拉框字体
        if hasattr(self.year_reading_widget, 'year_combo'):
            self.year_reading_widget.year_combo.setFont(list_font)
        
        # 更新分组框字体
        for group in self.findChildren(QGroupBox):
            group.setFont(FONT_MANAGER.get_font(bold=True, size_multiplier=1.1))
        
        # 更新标签字体
        label_font = FONT_MANAGER.get_font(bold=True)
        value_font = FONT_MANAGER.get_font()
        for label in self.findChildren(QLabel):
            if label not in [self.title_label, self.author_label, self.status_label, 
                           self.add_date_label, self.start_date_label, self.finish_date_label,
                           self.stats_label, self.year_stats_label, self.font_size_label]:
                label.setFont(label_font)
        
        # 更新特定标签字体
        self.title_label.setFont(value_font)
        self.author_label.setFont(value_font)
        self.status_label.setFont(value_font)
        self.add_date_label.setFont(value_font)
        self.start_date_label.setFont(value_font)
        self.finish_date_label.setFont(value_font)
        self.stats_label.setFont(value_font)
        self.year_stats_label.setFont(value_font)
        self.font_size_label.setFont(FONT_MANAGER.get_font(size_multiplier=0.9))
        
        # 更新笔记显示字体
        self.notes_display.setFont(value_font)
        
        # 重新设置样式表
        self.set_eye_protection_theme()
        
        # 刷新界面
        self.refresh_book_lists()
    
    def set_eye_protection_theme(self):
        """设置护眼主题"""
        font_size = FONT_MANAGER.get_font_size()
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {EYE_PROTECTION_COLORS['background']};
            }}
            QWidget#leftWidget {{
                background-color: {EYE_PROTECTION_COLORS['widget_bg']};
                border-radius: 8px;
                padding: 10px;
            }}
            QWidget#rightWidget {{
                background-color: {EYE_PROTECTION_COLORS['widget_bg']};
                border-radius: 8px;
                padding: 10px;
            }}
            QPushButton#addButton {{
                background-color: {EYE_PROTECTION_COLORS['button_bg']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: {int(font_size * 1.1)}px;
                font-weight: bold;
            }}
            QPushButton#addButton:hover {{
                background-color: {EYE_PROTECTION_COLORS['button_hover']};
            }}
            QTabWidget::pane {{
                border: 1px solid #C0C0C0;
                background-color: {EYE_PROTECTION_COLORS['tab_bg']};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background-color: {EYE_PROTECTION_COLORS['tab_bg']};
                color: {EYE_PROTECTION_COLORS['text']};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: {int(font_size * 0.9)}px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: {EYE_PROTECTION_COLORS['tab_selected']};
                font-weight: bold;
            }}
            QTabBar::tab:hover {{
                background-color: {EYE_PROTECTION_COLORS['button_hover']};
                color: white;
            }}
            QComboBox#yearCombo {{
                background-color: {EYE_PROTECTION_COLORS['year_filter_bg']};
                border: 1px solid {EYE_PROTECTION_COLORS['button_bg']};
                border-radius: 4px;
                padding: 6px;
                color: {EYE_PROTECTION_COLORS['text']};
                font-weight: bold;
                font-size: {font_size}px;
            }}
            QComboBox#yearCombo:hover {{
                border-color: {EYE_PROTECTION_COLORS['button_hover']};
            }}
            QListWidget#bookList {{
                background-color: {EYE_PROTECTION_COLORS['list_bg']};
                border: 1px solid #C0C0C0;
                border-radius: 4px;
                font-size: {font_size}px;
                color: {EYE_PROTECTION_COLORS['text']};
            }}
            QListWidget#bookList::item {{
                padding: 10px;
                border-bottom: 1px solid #E0E0E0;
            }}
            QListWidget#bookList::item:selected {{
                background-color: {EYE_PROTECTION_COLORS['list_selected']};
                color: {EYE_PROTECTION_COLORS['text']};
                font-weight: bold;
            }}
            QListWidget#bookList::item:hover {{
                background-color: #F0F0F0;
            }}
            QGroupBox {{
                background-color: {EYE_PROTECTION_COLORS['group_bg']};
                border: 2px solid {EYE_PROTECTION_COLORS['button_bg']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: {EYE_PROTECTION_COLORS['text']};
                font-size: {int(font_size * 1.1)}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            QLabel {{
                color: {EYE_PROTECTION_COLORS['text']};
                font-size: {font_size}px;
            }}
            QLabel[objectName^="title_label"], 
            QLabel[objectName^="author_label"] {{
                color: #2E8B57;
                font-weight: bold;
            }}
            QLabel#statsLabel {{
                color: {EYE_PROTECTION_COLORS['button_bg']};
                font-size: {font_size}px;
                font-weight: bold;
            }}
            QLabel#yearStatsLabel {{
                color: #FF8C00;
                font-size: {font_size}px;
                font-weight: bold;
            }}
            QTextEdit#notesDisplay {{
                background-color: white;
                border: 1px solid #C0C0C0;
                border-radius: 4px;
                color: {EYE_PROTECTION_COLORS['text']};
                font-size: {font_size}px;
            }}
            QPushButton#editButton {{
                background-color: {EYE_PROTECTION_COLORS['button_bg']};
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: {font_size}px;
            }}
            QPushButton#editButton:hover {{
                background-color: {EYE_PROTECTION_COLORS['button_hover']};
            }}
            QPushButton#editButton:disabled {{
                background-color: #CCCCCC;
                color: #999999;
            }}
            QPushButton#deleteButton {{
                background-color: {EYE_PROTECTION_COLORS['button_delete']};
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: {font_size}px;
            }}
            QPushButton#deleteButton:hover {{
                background-color: {EYE_PROTECTION_COLORS['button_delete_hover']};
            }}
            QPushButton#deleteButton:disabled {{
                background-color: #CCCCCC;
                color: #999999;
            }}
            QMenuBar {{
                background-color: {EYE_PROTECTION_COLORS['background']};
                color: {EYE_PROTECTION_COLORS['text']};
                font-size: {font_size}px;
            }}
            QMenuBar::item:selected {{
                background-color: {EYE_PROTECTION_COLORS['button_bg']};
                color: white;
            }}
            QMenu {{
                background-color: {EYE_PROTECTION_COLORS['widget_bg']};
                color: {EYE_PROTECTION_COLORS['text']};
                font-size: {font_size}px;
            }}
            QMenu::item:selected {{
                background-color: {EYE_PROTECTION_COLORS['button_bg']};
                color: white;
            }}
        """)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(EYE_PROTECTION_COLORS['background']))
        palette.setColor(QPalette.WindowText, QColor(EYE_PROTECTION_COLORS['text']))
        palette.setColor(QPalette.Base, QColor(EYE_PROTECTION_COLORS['list_bg']))
        palette.setColor(QPalette.Text, QColor(EYE_PROTECTION_COLORS['text']))
        self.setPalette(palette)
    
    def refresh_book_lists(self):
        """刷新所有书籍列表"""
        self.want_read_list.clear()
        self.reading_list.clear()
        
        list_font = FONT_MANAGER.get_font()
        
        for i, book in enumerate(self.book_manager.books):
            item_text = f"{book.title}"
            if book.author:
                item_text += f" - {book.author}"
            
            item = QListWidgetItem(item_text)
            item.setFont(list_font)
            item.setData(Qt.UserRole, i)
            item.setData(Qt.UserRole + 1, book.status)
            
            if book.status == "想读":
                self.want_read_list.addItem(item)
            elif book.status == "在读":
                self.reading_list.addItem(item)
        
        if hasattr(self.year_reading_widget, 'refresh_year_filter'):
            self.year_reading_widget.refresh_year_filter()
            current_year = self.year_reading_widget.year_combo.currentText()
            if current_year:
                self.year_reading_widget.refresh_books_by_year(current_year)
    
    def update_stats(self):
        """更新统计信息"""
        total = len(self.book_manager.books)
        want_read = len(self.book_manager.get_books_by_status("想读"))
        reading = len(self.book_manager.get_books_by_status("在读"))
        finished = len(self.book_manager.get_books_by_status("已读"))
        
        self.stats_label.setText(f"📊 总计: {total} | 📚 想读: {want_read} | 📖 在读: {reading} | ✅ 已读: {finished}")
        self.update_year_stats()
    
    def update_year_stats(self):
        """更新年份统计信息"""
        years = self.book_manager.get_years()
        if years:
            year_stats_text = "📅 年份统计: "
            for i, year in enumerate(years[:3]):
                books_count = len(self.book_manager.get_books_by_year(year))
                year_stats_text += f"{year}年: {books_count}本"
                if i < len(years[:3]) - 1:
                    year_stats_text += " | "
            if len(years) > 3:
                year_stats_text += f" ... (共{len(years)}年)"
            self.year_stats_label.setText(year_stats_text)
        else:
            self.year_stats_label.setText("📅 年份统计: 无已读书籍")
    
    def on_book_selected(self, item):
        """书籍被选中时显示详情"""
        index = item.data(Qt.UserRole)
        status = item.data(Qt.UserRole + 1)
        
        if status == "想读":
            books_list = self.book_manager.get_books_by_status("想读")
        elif status == "在读":
            books_list = self.book_manager.get_books_by_status("在读")
        else:
            return
        
        if 0 <= index < len(books_list):
            self.selected_book = books_list[index]
            self.selected_index = self.book_manager.books.index(self.selected_book)
            self.show_book_details()
    
    def on_year_book_selected(self, item):
        """年份查看标签页中书籍被选中时显示详情"""
        index = item.data(Qt.UserRole)
        year = item.data(Qt.UserRole + 2)
        
        if year:
            books_list = self.book_manager.get_books_by_year(year)
            if 0 <= index < len(books_list):
                self.selected_book = books_list[index]
                self.selected_index = self.book_manager.books.index(self.selected_book)
                self.show_book_details()
    
    def show_book_details(self):
        """显示书籍详情"""
        if self.selected_book is None:
            return
        
        self.title_label.setText(self.selected_book.title or "无")
        self.author_label.setText(self.selected_book.author or "未知")
        self.status_label.setText(self.selected_book.status)
        self.add_date_label.setText(self.selected_book.add_date or "无")
        self.start_date_label.setText(self.selected_book.start_date or "未开始")
        
        if self.selected_book.finish_date:
            self.finish_date_label.setText(self.selected_book.finish_date)
        else:
            self.finish_date_label.setText("未完成" if self.selected_book.status == "已读" else "未完成")
        
        self.notes_display.setPlainText(self.selected_book.notes or "无笔记")
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)
    
    def show_add_dialog(self):
        """显示添加书籍对话框"""
        dialog = BookDialog(self.book_manager, parent=self)
        dialog.exec_()
    
    def edit_book(self):
        """编辑选中的书籍"""
        if self.selected_book is not None and self.selected_index >= 0:
            dialog = BookDialog(self.book_manager, self.selected_book, self.selected_index, self)
            dialog.exec_()
    
    def delete_book(self):
        """删除选中的书籍"""
        if self.selected_book is not None and self.selected_index >= 0:
            reply = QMessageBox.question(
                self, 
                '确认删除', 
                f'确定要删除《{self.selected_book.title}》吗？',
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.book_manager.delete_book(self.selected_index)
                self.refresh_book_lists()
                self.update_stats()
                self.clear_book_details()
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>读书记录工具 v1.0</h2>
        <p>一个简单易用的书籍管理工具，支持记录和管理您的阅读进度。</p>
        <p><b>功能特点：</b></p>
        <ul>
            <li>📖 记录想读、在读、已读的书籍</li>
            <li>📅 按年份查看阅读记录</li>
            <li>📝 添加读书笔记和感想</li>
            <li>📊 统计阅读进度和数量</li>
            <li>🎨 护眼配色方案</li>
            <li>🔤 可调节字体大小 (8-24pt)</li>
        </ul>
        <p><b>数据文件：</b>书籍数据保存在程序目录的 books_data.json 文件中</p>
        <p><b>作者：</b>AI助手</p>
        <p><b>版本：</b>1.0</p>
        """
        QMessageBox.about(self, "关于读书记录工具", about_text)
    
    def clear_book_details(self):
        """清空书籍详情显示"""
        self.title_label.setText("")
        self.author_label.setText("")
        self.status_label.setText("")
        self.add_date_label.setText("")
        self.start_date_label.setText("")
        self.finish_date_label.setText("")
        self.notes_display.clear()
        
        self.selected_book = None
        self.selected_index = -1
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
    
    def closeEvent(self, event):
        """关闭窗口时保存数据"""
        self.book_manager.save_data()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    app.setWindowIcon(get_app_icon())
    
    # 设置应用程序字体
    app.setFont(FONT_MANAGER.base_font)
    
    window = BookRecordApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()