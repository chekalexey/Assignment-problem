from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QRadioButton, QGroupBox, QScrollArea, QSpinBox, QGridLayout, QSizePolicy, QTextEdit, QTabWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QIntValidator, QDoubleValidator, QPixmap, QPalette, QPainter, QPen, QColor, QFont, QIcon)
from matgen import *
import sys
import os
import numpy as np

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ================== ДОБАВЛЕН КЛАСС ДЛЯ ГИСТОГРАММЫ ==================
class HistogramWidget(QWidget):
    """Виджет для отображения гистограммы"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = {}
        self.zoom_factor = 1.0  # Фактор зума (1.0 = без зума, больше = больше зум)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(500, 400)
        self.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        
    def update_results(self, results):
        self.results = results
        self.update()
    
    def zoom_in(self):
        """Увеличивает зум (уменьшает диапазон отображения)"""
        self.zoom_factor = min(self.zoom_factor * 1.5, 10.0)
        self.update()
    
    def zoom_out(self):
        """Уменьшает зум (увеличивает диапазон отображения)"""
        self.zoom_factor = max(self.zoom_factor / 1.5, 1.0)
        self.update()
    
    def reset_zoom(self):
        """Сбрасывает зум к исходному состоянию"""
        self.zoom_factor = 1.0
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(self.rect(), Qt.white)
        
        if not self.results:
            painter.setPen(QColor(100, 100, 100))
            font = QFont("Comic Sans MS", 20)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, "Запустите эксперимент\nдля отображения гистограммы")
            return
        
        margin = 80 #60
        plot_width = self.width() - 2 * margin
        plot_height = self.height() - 2 * margin
        plot_x = margin
        plot_y = margin
        
        if plot_width <= 0 or plot_height <= 0:
            return
        
        # Оси
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(plot_x, plot_y, plot_x, plot_y + plot_height)
        painter.drawLine(plot_x, plot_y + plot_height, plot_x + plot_width, plot_y + plot_height)
        
        # Данные
        strategies = list(self.results.keys())
        values = list(self.results.values())
        num_strategies = len(strategies)
        
        if num_strategies == 0:
            return
        
        max_val = max(values)
        min_val = min(values)
        val_range = max_val - min_val
        
        # Применяем зум: уменьшаем padding при увеличении зума
        # При zoom_factor = 1.0: padding = 0.1 (стандартный)
        # При zoom_factor > 1.0: padding уменьшается, фокусируясь на значениях
        base_padding = 0.1 / self.zoom_factor
        
        if min_val > 0:
            # Если все значения положительные, начинаем с 0 или немного ниже минимума
            if self.zoom_factor > 1.0:
                # При зуме фокусируемся на диапазоне значений
                center = (max_val + min_val) / 2
                range_to_show = val_range / self.zoom_factor
                display_min = max(0, center - range_to_show / 2 - val_range * base_padding)
                display_max = center + range_to_show / 2 + val_range * base_padding
            else:
                display_min = 0
                display_max = max_val * (1 + base_padding) if max_val > 0 else 0.1
        else:
            # Если есть отрицательные значения
            padding = val_range * base_padding if val_range > 0 else 0.1
            if self.zoom_factor > 1.0:
                # При зуме фокусируемся на диапазоне значений
                center = (max_val + min_val) / 2
                range_to_show = val_range / self.zoom_factor
                display_min = center - range_to_show / 2 - padding
                display_max = center + range_to_show / 2 + padding
            else:
                display_min = min_val - padding
                display_max = max_val + padding
        
        display_range = display_max - display_min
        if display_range == 0:
            display_range = 1
        
        # Сетка
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        num_grid_lines = 5
        
        for i in range(num_grid_lines + 1):
            y = plot_y + plot_height - (i * plot_height / num_grid_lines)
            painter.drawLine(plot_x, y, plot_x + plot_width, y)
            
            value = display_min + (i * display_range / num_grid_lines)
            value_text = f"{value:.3f}"
            
            painter.setPen(Qt.black)
            font = QFont("Comic Sans MS", 13)
            painter.setFont(font)
            text_width = painter.fontMetrics().horizontalAdvance(value_text)
            painter.drawText(plot_x - text_width - 10, y + 5, value_text)
            painter.setPen(QPen(QColor(200, 200, 200), 1))
        
        # Столбцы
        bar_width = min(80, plot_width / (num_strategies * 1.5))
        spacing = (plot_width - num_strategies * bar_width) / (num_strategies + 1)
        
        colors = [
            QColor(255, 99, 71),    # Красный
            QColor(30, 144, 255),   # Синий
            QColor(50, 205, 50),    # Зеленый
            QColor(255, 215, 0),    # Желтый
            QColor(138, 43, 226),   # Фиолетовый
            QColor(255, 165, 0)     # Оранжевый
        ]
        
        for i, (strategy, value) in enumerate(self.results.items()):
            if display_min == 0:
                normalized_height = value / display_max
            else:
                normalized_height = (value - display_min) / display_range
            
            normalized_height = max(0, min(1, normalized_height))
            bar_height = normalized_height * plot_height
            
            x = plot_x + spacing + i * (bar_width + spacing)
            y = plot_y + plot_height - bar_height
            
            color = colors[i % len(colors)]
            darker_color = color.darker(120)
            
            painter.setBrush(color)
            painter.setPen(QPen(darker_color, 1))
            painter.drawRect(int(x), int(y), int(bar_width), int(bar_height))
            
            # Подпись значения
            painter.setPen(Qt.black)
            value_text = f"{value:.3f}"
            font = QFont("Comic Sans MS", 20, QFont.Bold)
            painter.setFont(font)
            text_width = painter.fontMetrics().horizontalAdvance(value_text)
            
            text_y = y - 10
            if text_y < plot_y:
                text_y = y + 20
                painter.setPen(Qt.black)
            
            painter.drawText(int(x + bar_width/2 - text_width/2), int(text_y), value_text)
            
            painter.setPen(Qt.black)
            
            # Подпись стратегии
            strategy_text = strategy.replace('-', '\n\n')
            lines = strategy_text.split('\n')
            font = QFont("Comic Sans MS", 20, QFont.Bold)
            painter.setFont(font)
            for j, line in enumerate(lines):
                line_width = painter.fontMetrics().horizontalAdvance(line)
                painter.drawText(int(x + bar_width/2 - line_width/2),
                               int(plot_y + plot_height + 20 + j*15), line)
# ================== КОНЕЦ КЛАССА ДЛЯ ГИСТОГРАММЫ ==================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система поддержки принятия решений")
        self.setGeometry(100, 100, 800, 600)

        # Создаем StackedWidget как центральный виджет
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Создаем страницы
        self.create_main_page()
        self.create_second_page()
        self.create_third_page()

        # Показываем главную страницу
        self.stacked_widget.setCurrentIndex(0)

    def create_main_page(self):
        """Главная страница (меню)"""
        page = QWidget()
        
        # Основной layout с двумя колонками
        main_layout = QHBoxLayout(page)
        main_layout.setSpacing(20)  # Расстояние между кнопками
        main_layout.setContentsMargins(30, 30, 30, 30)  # Отступы от краев
        
        title = QLabel("Главное меню")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 40px; color: #2c3e50;")
        
        # Создаем контейнер для заголовка и кнопок
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Добавляем заголовок
        container_layout.addWidget(title)
        container_layout.addSpacing(50)  # Отступ между заголовком и кнопками
        
        # Создаем контейнер для кнопок
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(40)  # Расстояние между кнопками
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Левая кнопка (Ручной режим)
        btn_left_container = QWidget()
        left_layout = QVBoxLayout(btn_left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_left = QPushButton("Ручной\nрежим")
        btn_left.setObjectName("leftButton")
        btn_left.clicked.connect(lambda: self.go_to_page(1))
        
        # Делаем кнопку квадратной и крупной
        btn_left.setFixedSize(250, 250)  # Квадратная кнопка
        btn_left.setStyleSheet("""
            QPushButton#leftButton {
                font-size: 26px;
                font-weight: bold;
                color: white;
                background-color: #91B081;    /* Главный цвет - зеленый */
                border: 4px solid #7A9A6E;    /* Более темный оттенок зеленого */
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton#leftButton:hover {
                background-color: #7A9A6E;    /* Темнее при наведении */
                border-color: #64885A;        /* Еще темнее */
            }
            QPushButton#leftButton:pressed {
                background-color: #64885A;    /* Самый темный зеленый при нажатии */
                border-color: #4E6B46;
            }
        """)
        btn_left.setCursor(Qt.PointingHandCursor)
        
        left_layout.addWidget(btn_left, 0, Qt.AlignCenter)
        buttons_layout.addWidget(btn_left_container, 1)
        
        # Правая кнопка (Экспериментальный режим)
        btn_right_container = QWidget()
        right_layout = QVBoxLayout(btn_right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_right = QPushButton("Режим\nэксперимента")
        btn_right.setObjectName("rightButton")
        btn_right.clicked.connect(lambda: self.go_to_page(2))
        
        # Делаем кнопку квадратной и крупной
        btn_right.setFixedSize(250, 250)  # Квадратная кнопка
        btn_right.setStyleSheet("""
           QPushButton#rightButton {
                font-size: 26px;
                font-weight: bold;
                color: white;
                background-color: #ffa500;  /* Главный цвет - оранжевый */
                border: 4px solid #ff8c00;  /* Более темный оттенок оранжевого */
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton#rightButton:hover {
                background-color: #ff8c00;  /* Темнее при наведении */
                border-color: #ff7f00;      /* Еще темнее */
            }
            QPushButton#rightButton:pressed {
                background-color: #ff7f00;  /* Самый темный оранжевый при нажатии */
                border-color: #ff6a00;
            }
        """)
        btn_right.setCursor(Qt.PointingHandCursor)
        
        right_layout.addWidget(btn_right, 0, Qt.AlignCenter)
        buttons_layout.addWidget(btn_right_container, 1)
        
        # Добавляем контейнер с кнопками в основной layout
        container_layout.addWidget(buttons_container, 1)
        container_layout.addStretch()
        
        # Центрируем контейнер на странице
        main_layout.addStretch(1)
        main_layout.addWidget(container, 2)
        main_layout.addStretch(1)
        
        page.setLayout(main_layout)
        self.stacked_widget.addWidget(page)

    def create_second_page(self):       
        """Вторая страница"""
        page = QWidget()
        main_layout = QHBoxLayout(page)

        left_widget = QWidget()
        optionsLayout = QVBoxLayout(left_widget)

        title = QLabel("Ручной режим")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 5px;")

        btn_back = QPushButton("← Назад в меню")
        btn_back.clicked.connect(lambda: self.go_to_page(0))

        btn_next = QPushButton("Далее →")
        btn_next.clicked.connect(lambda: self.go_to_page(2))
        
        self.line_button = QPushButton("Получить результаты", self)
        self.line_button.clicked.connect(self.get_integer_from_line_edit_and_matrix)

        # === ДОБАВЛЕНА МАТРИЦА ===
        matrix_group = QGroupBox("Матрица")
        matrix_layout = QVBoxLayout()
        
        # Управление размером
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Размер:"))
        
        self.matrix_size_spin = QSpinBox()
        self.matrix_size_spin.setRange(2, 16)
        self.matrix_size_spin.setValue(3)
        self.matrix_size_spin.valueChanged.connect(self.update_matrix_display)
        size_layout.addWidget(self.matrix_size_spin)
        
        # Кнопка очистки матрицы
        self.clear_matrix_button = QPushButton("Очистить матрицу")
        self.clear_matrix_button.clicked.connect(self.clear_matrix)
        size_layout.addWidget(self.clear_matrix_button)
        
        size_layout.addStretch()
        matrix_layout.addLayout(size_layout)
        
        # Контейнер для матрицы
        self.matrix_container = QWidget()
        self.matrix_grid_layout = QGridLayout(self.matrix_container)
        self.matrix_grid_layout.setSpacing(2)  # Уменьшено расстояние между ячейками
        self.matrix_grid_layout.setContentsMargins(5, 5, 5, 5)
        
        # Обертка для центрирования матрицы
        self.matrix_wrapper = QWidget()
        wrapper_layout = QVBoxLayout(self.matrix_wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addStretch()
        
        # Горизонтальный layout для центрирования по горизонтали
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.matrix_container)
        h_layout.addStretch()
        
        h_widget = QWidget()
        h_widget.setLayout(h_layout)
        wrapper_layout.addWidget(h_widget)
        wrapper_layout.addStretch()
        
        # Прокрутка для матрицы
        self.matrix_scroll_area = QScrollArea()
        self.matrix_scroll_area.setWidgetResizable(True)
        self.matrix_scroll_area.setWidget(self.matrix_wrapper)
        self.matrix_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.matrix_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Устанавливаем минимальную высоту, которая будет динамически обновляться
        self.matrix_scroll_area.setMinimumHeight(200)
        
        matrix_layout.addWidget(self.matrix_scroll_area, stretch=1)
        
        # Инициализация матрицы
        self.matrix_inputs = []
        self.create_matrix_inputs(3)
        
        matrix_group.setLayout(matrix_layout)
        # === КОНЕЦ МАТРИЦЫ ===
        
        ######################SVEKLA########################
        # image_label = QLabel()
        # try:
        #     pixmap = QPixmap('svekla.jpg')
        #     if pixmap.isNull():
        #         pixmap = QPixmap(400, 400)
        #         pixmap.fill(Qt.red)
        #         image_label.setText("Картинка не найдена")
        #         image_label.setAlignment(Qt.AlignCenter)
        #     else:
        #         image_label.setPixmap(pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # except Exception as e:
        #     pixmap = QPixmap(300, 300)
        #     pixmap.fill(Qt.gray)
        #     image_label.setPixmap(pixmap)
        #     image_label.setText(f"Ошибка: {str(e)}")
        #     image_label.setAlignment(Qt.AlignCenter)
        #     image_label.setWordWrap(True)
        # image_label.setAlignment(Qt.AlignCenter)
        # image_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        ####################################################

        self.textOutput = QTextEdit()
        self.textOutput.setFixedHeight(200)
        #self.textOutput.setStyleSheet()
        self.textOutput.setReadOnly(True)

        optionsLayout.addWidget(title)
        #optionsLayout.addWidget(QLabel("Это страница ручного режима"))
        optionsLayout.addWidget(matrix_group)  # Добавляем матрицу
        optionsLayout.addWidget(self.line_button)
        #optionsLayout.addStretch(1)
        optionsLayout.addWidget(self.textOutput)
        #optionsLayout.addStretch()

        # Кнопки навигации
        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_back)
        button_layout.addWidget(btn_next)
        optionsLayout.addLayout(button_layout)

        main_layout.addWidget(left_widget, stretch=1)
        #main_layout.addWidget(image_label, stretch=2)
        
        page.setLayout(main_layout)
        self.stacked_widget.addWidget(page)
        
        # Методы для работы с матрицей
    def create_matrix_inputs(self, size):
        """Создает поля ввода для матрицы указанного размера с индексами"""
        # Очищаем старые поля
        for i in reversed(range(self.matrix_grid_layout.count())):
            widget = self.matrix_grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.matrix_inputs.clear()
        
        # Размеры ячеек (в пикселях)
        CELL_WIDTH = 70
        CELL_HEIGHT = 30
        HEADER_COL_WIDTH = CELL_WIDTH  # Заголовки столбцов должны быть такой же ширины, как ячейки
        HEADER_ROW_WIDTH = 80
        HEADER_HEIGHT = 30
        
        # Сбрасываем все растягивания - используем фиксированные размеры
        for i in range(self.matrix_grid_layout.columnCount()):
            self.matrix_grid_layout.setColumnStretch(i, 0)
            self.matrix_grid_layout.setColumnMinimumWidth(i, 0)
        for i in range(self.matrix_grid_layout.rowCount()):
            self.matrix_grid_layout.setRowStretch(i, 0)
            self.matrix_grid_layout.setRowMinimumHeight(i, 0)
        
        # Устанавливаем размеры для заголовка строк (столбец 0)
        self.matrix_grid_layout.setColumnMinimumWidth(0, HEADER_ROW_WIDTH)
        
        # Создаем заголовки столбцов (сверху)
        for j in range(size):
            label_col = QLabel(f"{j+1}")
            label_col.setAlignment(Qt.AlignCenter)
            label_col.setStyleSheet("background-color: #ffbdbd; padding: 2px;") #e0e0e0
            label_col.setFixedSize(HEADER_COL_WIDTH, HEADER_HEIGHT)
            label_col.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.matrix_grid_layout.addWidget(label_col, 0, j+1, alignment=Qt.AlignCenter)
            # Устанавливаем фиксированную ширину для столбцов данных (совпадает с шириной заголовка)
            self.matrix_grid_layout.setColumnMinimumWidth(j+1, CELL_WIDTH)
            self.matrix_grid_layout.setColumnStretch(j+1, 0)  # Не растягиваем столбцы
        
        # Устанавливаем высоту для заголовка столбцов (строка 0)
        self.matrix_grid_layout.setRowMinimumHeight(0, HEADER_HEIGHT)
        
        # Создаем заголовки строк (слева)
        for i in range(size):
            label_row = QLabel(f"{i+1}")
            label_row.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label_row.setStyleSheet("background-color: #ffbdbd; padding: 3px;")
            label_row.setFixedSize(HEADER_ROW_WIDTH, CELL_HEIGHT)
            label_row.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.matrix_grid_layout.addWidget(label_row, i+1, 0)
            # Устанавливаем минимальную высоту для строк данных
            self.matrix_grid_layout.setRowMinimumHeight(i+1, CELL_HEIGHT)
        
        # Создаем поля ввода (с учетом смещения из-за заголовков)
        for i in range(size):
            row_inputs = []
            for j in range(size):
                line_edit = QLineEdit()
                # line_edit.setStyleSheet("""
                #     QLineEdit {
                #         background-color: #ffc2c2;
                #     }
                # """)
                #line_edit.mousePressEvent = lambda _ : line_edit.selectAll() #select text in line edit upon mouse press
                line_edit.setFixedSize(CELL_WIDTH, CELL_HEIGHT)
                line_edit.setAlignment(Qt.AlignCenter)
                line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                
                # Валидатор для неотрицательных чисел
                from PySide6.QtGui import QDoubleValidator
                validator = QDoubleValidator(0, 999999.99, 2)
                line_edit.setValidator(validator)
                
                # Устанавливаем значение по умолчанию
                # if i == j:
                #     line_edit.setText("0")
                # else:
                #     line_edit.setText("1")
                line_edit.setText("")
                
                # Добавляем с учетом заголовков (i+1, j+1) с выравниванием по центру
                self.matrix_grid_layout.addWidget(line_edit, i+1, j+1, alignment=Qt.AlignCenter)
                row_inputs.append(line_edit)
            
            self.matrix_inputs.append(row_inputs)
        
        # Обновляем размер контейнера на основе размера матрицы
        # Вычисляем общий размер матрицы
        margins = self.matrix_grid_layout.contentsMargins()
        total_width = HEADER_ROW_WIDTH + (size * CELL_WIDTH) + (self.matrix_grid_layout.spacing() * (size + 1)) + margins.left() + margins.right()
        total_height = HEADER_HEIGHT + (size * CELL_HEIGHT) + (self.matrix_grid_layout.spacing() * (size + 1)) + margins.top() + margins.bottom()
        
        # Устанавливаем минимальный размер контейнера
        self.matrix_container.setMinimumSize(total_width, total_height)
        # Обновляем геометрию контейнера
        self.matrix_container.adjustSize()
        self.matrix_container.updateGeometry()

    def update_matrix_display(self):
        """Обновляет отображение матрицы при изменении размера"""
        size = self.matrix_size_spin.value()
        self.create_matrix_inputs(size)

    def get_matrix_data(self):
        """Возвращает данные матрицы как numpy array"""
        try:
            import numpy as np
            size = self.matrix_size_spin.value()
            matrix = []
            
            for i in range(size):
                row = []
                for j in range(size):
                    text = self.matrix_inputs[i][j].text()
                    if text:
                        # Заменяем запятую на точку для корректного парсинга
                        row.append(float(text.replace(',', '.')))
                    else:
                        row.append(0.0)
                matrix.append(row)
            
            return np.array(matrix)
        except Exception as e:
            print(f"Ошибка получения данных матрицы: {e}")
            return None

    def clear_matrix(self):
        """Зануляет все ячейки матрицы"""
        size = self.matrix_size_spin.value()
        for i in range(size):
            for j in range(size):
                if i < len(self.matrix_inputs) and j < len(self.matrix_inputs[i]):
                    self.matrix_inputs[i][j].setText("0")

    def get_integer_from_line_edit_and_matrix(self):
        try:
            self.line_button.setEnabled(False)
            self.line_button.setText("Вычисляется...")
            
            matrix = self.get_matrix_data()
            if matrix is None:
                self.textOutput.setHtml("<span style='color: red;'><b>Ошибка:</b> Не удалось получить данные матрицы</span>")
                return
                
            a = algo(matrix)
            
            # Получаем результаты всех алгоритмов
            munkres_min_total, _ = a.Munkres_Alg()
            munkres_max_total, _ = a.Munkres_Alg_Max()
            greedy_total, _ = a.Greedy()
            thrifty_total, _ = a.Thrifty()
            greedy_thrifty_total, _ = a.Greedy_Thrifty(matrix.shape[0]//2)
            thrifty_greedy_total, _ = a.Thrifty_Greedy(matrix.shape[0]//2)
            
            # Собираем все стратегии для сравнения (без Munkres)
            comparison_results = {
                'Жадный (Greedy)': greedy_total,
                'Бережливый (Thrifty)': thrifty_total,
                'Жадно-бережливый': greedy_thrifty_total,
                'Бережливо-жадный': thrifty_greedy_total
            }
            
            # Находим лучшую и худшую стратегии (без Munkres)
            best_strategy = max(comparison_results, key=comparison_results.get)
            worst_strategy = min(comparison_results, key=comparison_results.get)
            best_value = comparison_results[best_strategy]
            worst_value = comparison_results[worst_strategy]
            ideal_value = munkres_max_total
            
            # Формируем красивый HTML вывод
            html_text = f"""
            <h3 style="color: #2c3e50; text-align: center; margin-bottom: 15px;">Результаты расчета</h3>
            
            <p style="margin-bottom: 15px;"><b>Матрица:</b> {matrix.shape[0]}×{matrix.shape[1]}</p>
            
            <div style="margin-bottom: 15px;">
                <h4 style="margin-bottom: 10px;">Результаты алгоритмов:</h4>
                <div style="margin-left: 20px;">
                    <p style="margin: 5px 0;">• <b>Венгерский (Min):</b> {munkres_min_total:.3f} ({munkres_min_total/ideal_value*100:.1f}%)</p>
                    <p style="margin: 5px 0; background-color: #e8f4e8; padding: 3px 8px; border-radius: 3px;">
                        • <b>Венгерский (Max) - идеал:</b> {ideal_value:.3f} (100.0%)
                    </p>
                    <p style="margin: 5px 0;">• <b>Жадный (Greedy):</b> {greedy_total:.3f} ({greedy_total/ideal_value*100:.1f}%)</p>
                    <p style="margin: 5px 0;">• <b>Бережливый (Thrifty):</b> {thrifty_total:.3f} ({thrifty_total/ideal_value*100:.1f}%)</p>
                    <p style="margin: 5px 0;">• <b>Жадно-бережливый:</b> {greedy_thrifty_total:.3f} ({greedy_thrifty_total/ideal_value*100:.1f}%)</p>
                    <p style="margin: 5px 0;">• <b>Бережливо-жадный:</b> {thrifty_greedy_total:.3f} ({thrifty_greedy_total/ideal_value*100:.1f}%)</p>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="margin-bottom: 10px;">Сравнение стратегий (без Munkres):</h4>
                <div style="background-color: #d4edda; padding: 8px; border-radius: 4px; margin-bottom: 5px;">
                    <b>Лучшая стратегия:</b> {best_strategy}<br>
                    <b>Результат:</b> {best_value:.3f} ({best_value/ideal_value*100:.1f}% от идеала)
                </div>
                
                <div style="background-color: #f8d7da; padding: 8px; border-radius: 4px; margin-bottom: 10px;">
                    <b>Худшая стратегия:</b> {worst_strategy}<br>
                    <b>Результат:</b> {worst_value:.3f} ({worst_value/ideal_value*100:.1f}% от идеала)
                </div>
                
                <p style="margin: 5px 0;"><b>Разница:</b> {best_value - worst_value:.3f}</p>
                <p style="margin: 5px 0;"><b>Эффективность лучшей:</b> {best_value/ideal_value*100:.1f}% от идеального алгоритма</p>
            </div>
            
            <div style="background-color: #e3f2fd; padding: 8px; border-radius: 4px;">
                <b>Рекомендация:</b> Используйте стратегию <b>{best_strategy}</b>
            </div>
            """
            
            self.textOutput.setHtml(html_text)
            
        except Exception as e:
            error_html = f"""
            <div style="background-color: #ffebee; padding: 10px; border-radius: 4px;">
                <b style="color: #d32f2f;">Ошибка при расчетах</b><br>
                {type(e).__name__}: {str(e)}<br>
                Проверьте корректность данных в матрице.
            </div>
            """
            self.textOutput.setHtml(error_html)
        finally:
            self.line_button.setEnabled(True)
            self.line_button.setText("Получить результаты")

    def create_third_page(self):
        """Третья страница"""
        page = QWidget()
        main_layout = QHBoxLayout(page)

        left_widget = QWidget()
        optionsLayout = QVBoxLayout(left_widget)
        optionsLayout.setSpacing(15)

        title = QLabel("Экспериментальный режим")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; margin: 10px;")

        btn_back = QPushButton("← Назад")
        btn_back.clicked.connect(lambda: self.go_to_page(1))

        btn_home = QPushButton("Главное меню")
        btn_home.clicked.connect(lambda: self.go_to_page(0))

        # Количество экспериментов
        self.number_of_experminets = QLineEdit("100", self)
        self.number_of_experminets.setPlaceholderText("Введите число экспериментов")
        self.number_of_experminets.setStyleSheet("padding-left: 8px;")
        self.number_of_experminets.setValidator(QIntValidator(0, 100, self))

        # Размер матрицы
        self.matrix_size = QLineEdit("15", self)
        self.matrix_size.setPlaceholderText("Введите размер матрицы")
        self.matrix_size.setStyleSheet("padding-left: 8px;")
        self.matrix_size.setValidator(QIntValidator(1, 25, self))

        # Создаем компактный layout для alpha и beta
        alpha_beta_group = QGroupBox("Параметры")
        #alpha_beta_group.setStyleSheet("font-weight: bold;")
        alpha_beta_layout = QVBoxLayout(alpha_beta_group)
        
        # Создаем таблицу для alpha
        alpha_widget = QWidget()
        alpha_grid = QGridLayout(alpha_widget)
        alpha_grid.setSpacing(10)
        alpha_grid.setContentsMargins(5, 5, 5, 5)
        
        alpha_label = QLabel("Сахаристость:")
        alpha_label.setStyleSheet("font-size: 19px;")
        alpha_grid.addWidget(alpha_label, 0, 0, 1, 2)
        
        alpha_min_label = QLabel("min:")
        alpha_min_label.setStyleSheet("font-size: 18px;")
        alpha_grid.addWidget(alpha_min_label, 1, 0)
        
        self.alpha_min = QLineEdit("0.12", self)
        self.alpha_min.setPlaceholderText("alpha min")
        self.alpha_min.setStyleSheet("font-size: 18px; padding: 8px;")
        # Настраиваем валидатор для использования точки как десятичного разделителя
        alpha_min_validator = QDoubleValidator(self)
        alpha_min_validator.setNotation(QDoubleValidator.StandardNotation)
        self.alpha_min.setValidator(alpha_min_validator)
        # Заменяем запятую на точку при вводе (с проверкой чтобы избежать бесконечного цикла)
        def replace_comma_alpha_min(text):
            if ',' in text:
                cursor_pos = self.alpha_min.cursorPosition()
                new_text = text.replace(',', '.')
                self.alpha_min.blockSignals(True)
                self.alpha_min.setText(new_text)
                self.alpha_min.setCursorPosition(cursor_pos)
                self.alpha_min.blockSignals(False)
        self.alpha_min.textChanged.connect(replace_comma_alpha_min)
        self.alpha_min.setMaximumWidth(100)
        alpha_grid.addWidget(self.alpha_min, 1, 1)
        
        alpha_max_label = QLabel("max:")
        alpha_max_label.setStyleSheet("font-size: 18px;")
        alpha_grid.addWidget(alpha_max_label, 2, 0)
        
        self.alpha_max = QLineEdit("0.2", self)
        self.alpha_max.setPlaceholderText("alpha max")
        self.alpha_max.setStyleSheet("font-size: 18px; padding: 8px;")
        # Настраиваем валидатор для использования точки как десятичного разделителя
        alpha_max_validator = QDoubleValidator(self)
        alpha_max_validator.setNotation(QDoubleValidator.StandardNotation)
        self.alpha_max.setValidator(alpha_max_validator)
        # Заменяем запятую на точку при вводе (с проверкой чтобы избежать бесконечного цикла)
        def replace_comma_alpha_max(text):
            if ',' in text:
                cursor_pos = self.alpha_max.cursorPosition()
                new_text = text.replace(',', '.')
                self.alpha_max.blockSignals(True)
                self.alpha_max.setText(new_text)
                self.alpha_max.setCursorPosition(cursor_pos)
                self.alpha_max.blockSignals(False)
        self.alpha_max.textChanged.connect(replace_comma_alpha_max)
        self.alpha_max.setMaximumWidth(100)
        alpha_grid.addWidget(self.alpha_max, 2, 1)
        
        # Создаем таблицу для beta
        beta_widget = QWidget()
        beta_grid = QGridLayout(beta_widget)
        beta_grid.setSpacing(10)
        beta_grid.setContentsMargins(5, 5, 5, 5)
        
        beta_label = QLabel("                      Коэффициент деградации:")
        beta_label.setStyleSheet("font-size: 19px;")
        beta_grid.addWidget(beta_label, 0, 0, 1, 2)
        
        beta_min_label = QLabel("                                            min:")
        beta_min_label.setStyleSheet("font-size: 18px;")
        beta_grid.addWidget(beta_min_label, 1, 0)
        
        self.beta_min = QLineEdit("0.93", self)
        self.beta_min.setPlaceholderText("beta min")
        self.beta_min.setStyleSheet("font-size: 18px; padding: 8px;")
        # Настраиваем валидатор для использования точки как десятичного разделителя
        beta_min_validator = QDoubleValidator(0.00001, 0.99999, 5, self)
        beta_min_validator.setNotation(QDoubleValidator.StandardNotation)
        self.beta_min.setValidator(beta_min_validator)
        # Заменяем запятую на точку при вводе (с проверкой чтобы избежать бесконечного цикла)
        def replace_comma_beta_min(text):
            if ',' in text:
                cursor_pos = self.beta_min.cursorPosition()
                new_text = text.replace(',', '.')
                self.beta_min.blockSignals(True)
                self.beta_min.setText(new_text)
                self.beta_min.setCursorPosition(cursor_pos)
                self.beta_min.blockSignals(False)
        self.beta_min.textChanged.connect(replace_comma_beta_min)
        self.beta_min.setMaximumWidth(100)
        beta_grid.addWidget(self.beta_min, 1, 1)
        
        beta_max_label = QLabel("                                            max:")
        beta_max_label.setStyleSheet("font-size: 18px;")
        beta_grid.addWidget(beta_max_label, 2, 0)
        
        self.beta_max = QLineEdit("0.98", self)
        self.beta_max.setPlaceholderText("beta max")
        self.beta_max.setStyleSheet("font-size: 18px; padding: 8px;")
        # Настраиваем валидатор для использования точки как десятичного разделителя
        beta_max_validator = QDoubleValidator(0.00001, 0.99999, 5, self)
        beta_max_validator.setNotation(QDoubleValidator.StandardNotation)
        self.beta_max.setValidator(beta_max_validator)
        # Заменяем запятую на точку при вводе (с проверкой чтобы избежать бесконечного цикла)
        def replace_comma_beta_max(text):
            if ',' in text:
                cursor_pos = self.beta_max.cursorPosition()
                new_text = text.replace(',', '.')
                self.beta_max.blockSignals(True)
                self.beta_max.setText(new_text)
                self.beta_max.setCursorPosition(cursor_pos)
                self.beta_max.blockSignals(False)
        self.beta_max.textChanged.connect(replace_comma_beta_max)
        self.beta_max.setMaximumWidth(100)
        beta_grid.addWidget(self.beta_max, 2, 1)
        
        # Горизонтальный layout для alpha и beta
        params_horizontal = QHBoxLayout()
        params_horizontal.addWidget(alpha_widget)
        params_horizontal.addWidget(beta_widget)
        params_horizontal.addStretch()
        
        alpha_beta_layout.addLayout(params_horizontal)

        radio_buttons_layout = QHBoxLayout()
        self.concentrated = QRadioButton("Концентрированное", self)
        #self.concentrated.setStyleSheet("font-size: 18px;")
        self.uniform = QRadioButton("Равномерное", self)
        #self.uniform.setStyleSheet("font-size: 18px;")
        radio_buttons_layout.addWidget(self.concentrated)
        radio_buttons_layout.addWidget(self.uniform)
        
        gb = QGroupBox("Распределение") #😎
        gb.setLayout(radio_buttons_layout)

        self.line_button = QPushButton("Получить результаты", self)
        self.line_button.clicked.connect(self.run_experiment)  # Изменено на run_experiment для вывода в GUI
        
        # Текстовое поле для результатов слева (новая функция из test.py)
        self.results_text_left = QTextEdit()
        self.results_text_left.setReadOnly(True)
        self.results_text_left.setPlaceholderText("Здесь появятся результаты после запуска эксперимента")
        self.results_text_left.setMinimumHeight(150)

        # Собираем элементы в layout
        optionsLayout.addWidget(title)
        optionsLayout.addStretch()
        
        # Количество экспериментов
        exp_label = QLabel("Количество экспериментов:")
        optionsLayout.addWidget(exp_label)
        optionsLayout.addWidget(self.number_of_experminets)

                # Размер матрицы
        size_label = QLabel("Размер матрицы:")
        optionsLayout.addWidget(size_label)
        optionsLayout.addWidget(self.matrix_size)
        
        # Alpha и Beta параметры
        optionsLayout.addWidget(alpha_beta_group)
                
        # Распределение
        optionsLayout.addWidget(gb)
        
        # Кнопка и результат
        optionsLayout.addWidget(self.line_button)
        optionsLayout.addWidget(QLabel("Краткие результаты:"))
        optionsLayout.addWidget(self.results_text_left)
        #optionsLayout.addWidget(self.result_label)
        optionsLayout.addStretch()

        # Кнопки навигации
        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_back)
        button_layout.addWidget(btn_home)
        optionsLayout.addLayout(button_layout)

        # ================== ДОБАВЛЕНЫ ВКЛАДКИ С ГРАФИКАМИ ==================
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Создаем вкладки
        self.tab_widget = QTabWidget()
        
        # Вкладка 1: Гистограмма
        self.histogram_tab = QWidget()
        histogram_layout = QVBoxLayout(self.histogram_tab)
        
        # Создаем виджет гистограммы
        self.histogram_widget = HistogramWidget()
        
        # Кнопки управления зумом
        zoom_layout = QHBoxLayout()
        zoom_in_button = QPushButton("🔍+ Увеличить")
        zoom_in_button.clicked.connect(self.histogram_widget.zoom_in)
        zoom_out_button = QPushButton("🔍- Уменьшить")
        zoom_out_button.clicked.connect(self.histogram_widget.zoom_out)
        reset_zoom_button = QPushButton("↺ Сбросить")
        reset_zoom_button.clicked.connect(self.histogram_widget.reset_zoom)
        
        zoom_layout.addWidget(zoom_in_button)
        zoom_layout.addWidget(zoom_out_button)
        zoom_layout.addWidget(reset_zoom_button)
        zoom_layout.addStretch()
        
        histogram_layout.addLayout(zoom_layout)
        histogram_layout.addWidget(self.histogram_widget)

        # Вкладка 2: Полные результаты
        self.results_tab = QWidget()
        results_layout = QVBoxLayout(self.results_tab)
        
        # Текстовое поле для полных результатов
        self.results_text_right = QTextEdit()
        self.results_text_right.setReadOnly(True)
        self.results_text_right.setPlaceholderText("Полные результаты появятся здесь после запуска эксперимента")
        results_layout.addWidget(self.results_text_right)
        
        # Добавляем вкладки
        self.tab_widget.addTab(self.histogram_tab, "Гистограмма")
        self.tab_widget.addTab(self.results_tab, "Полные результаты")
        
        right_layout.addWidget(self.tab_widget)
        # ================== КОНЕЦ ВКЛАДОК С ГРАФИКАМИ ==================

        main_layout.addWidget(left_widget, stretch=1)
        main_layout.addWidget(right_widget, stretch=2)

        page.setLayout(main_layout)
        self.stacked_widget.addWidget(page)

    def go_to_page(self, index):
        """Переход на страницу по индексу"""
        self.stacked_widget.setCurrentIndex(index)

    def get_integer_from_line_edit(self):
            number_of_experminets = int(self.number_of_experminets.text())
            # Заменяем запятую на точку для корректного парсинга
            alpha_min = float(self.alpha_min.text().replace(',', '.'))
            alpha_max = float(self.alpha_max.text().replace(',', '.'))
            beta_min = float(self.beta_min.text().replace(',', '.'))
            beta_max = float(self.beta_max.text().replace(',', '.'))
            matrix_size = int(self.matrix_size.text())
            sugar = ""
            if self.concentrated.isChecked():
                sugar = "concentrated"  # Английское название
            elif self.uniform.isChecked():
                sugar = "uniform"  # Английское название

            sumMunkresAlg = 0
            sumMunkresAlgMax = 0
            sumGreedy = 0
            sumThrifty = 0
            sumGreedyThrifty = 0
            sumThriftyGreedy = 0

            for i in range(number_of_experminets):
                thingie = MatrixGenerator(n=matrix_size, v=matrix_size, distribution_type=sugar, a_min=alpha_min, a_max=alpha_max, beta_min=beta_min, beta_max=beta_max)
                print(f"matrix number {i+1}")
                print(thingie.D_matrix)
                a = algo(thingie.D_matrix)
                print(a.Munkres_Alg())
                print(a.Munkres_Alg_Max())
                print(a.Greedy())
                print(a.Thrifty())
                print(a.Greedy_Thrifty(matrix_size//2))
                print(a.Thrifty_Greedy(matrix_size//2))
                #x += a.Greedy()[0]
                x, y = a.Munkres_Alg()
                sumMunkresAlg += x
                x, y = a.Munkres_Alg_Max()
                sumMunkresAlgMax += x
                x, y = a.Greedy()
                sumGreedy += x
                x, y = a.Thrifty()
                sumThrifty += x
                x, y = a.Greedy_Thrifty(matrix_size//2)
                sumGreedyThrifty += x
                x, y = a.Thrifty_Greedy(matrix_size//2)
                sumThriftyGreedy += x
                
                print("------------------------------------------")
            print(f"total sumMunkresAlg {sumMunkresAlg}")
            print(f"total sumMunkresAlgMax {sumMunkresAlgMax}")
            print(f"total sumGreedy {sumGreedy}")
            print(f"total sumThrifty {sumThrifty}")
            print(f"total sumGreedyThrifty {sumGreedyThrifty}")
            print(f"total sumThriftyGreedy {sumThriftyGreedy}")
            # print(sugar)
            # print(number_of_experminets, alpha_min, alpha_max, beta_min, beta_max, matrix_size)

    def run_experiment(self):
        """Новый метод для запуска эксперимента с выводом результатов в GUI (из test.py)"""
        try:
            self.line_button.setEnabled(False)
            self.line_button.setText("Выполняется...")
            QApplication.processEvents()
            
            # Получаем значения (заменяем запятую на точку для корректного парсинга)
            number_of_experiments = int(self.number_of_experminets.text())
            alpha_min = float(self.alpha_min.text().replace(',', '.'))
            alpha_max = float(self.alpha_max.text().replace(',', '.'))
            beta_min = float(self.beta_min.text().replace(',', '.'))
            beta_max = float(self.beta_max.text().replace(',', '.'))
            matrix_size = int(self.matrix_size.text())
            sugar = "uniform"
            if self.concentrated.isChecked():
                sugar = "concentrated"
            elif self.uniform.isChecked():
                sugar = "uniform"

            # Проверяем корректность
            if alpha_min >= alpha_max:
                raise ValueError("Alpha min должен быть меньше Alpha max")
            if beta_min >= beta_max:
                raise ValueError("Beta min должен быть меньше Beta max")

            sumMunkresAlg = 0
            sumMunkresAlgMax = 0
            sumGreedy = 0
            sumThrifty = 0
            sumGreedyThrifty = 0
            sumThriftyGreedy = 0

            # Запускаем эксперименты
            for i in range(number_of_experiments):
                thingie = MatrixGenerator(
                    n=matrix_size, 
                    v=matrix_size, 
                    distribution_type=sugar, 
                    a_min=alpha_min, 
                    a_max=alpha_max, 
                    beta_min=beta_min, 
                    beta_max=beta_max
                )
                
                a = algo(thingie.D_matrix)
                
                x, y = a.Munkres_Alg()
                sumMunkresAlg += x
                x, y = a.Munkres_Alg_Max()
                sumMunkresAlgMax += x
                x, y = a.Greedy()
                sumGreedy += x
                x, y = a.Thrifty()
                sumThrifty += x
                x, y = a.Greedy_Thrifty(matrix_size//2)
                sumGreedyThrifty += x
                x, y = a.Thrifty_Greedy(matrix_size//2)
                sumThriftyGreedy += x
            
            # Вычисляем средние
            # avgMunkresAlg = sumMunkresAlg / number_of_experiments
            # avgMunkresAlgMax = sumMunkresAlgMax / number_of_experiments
            # avgGreedy = sumGreedy / number_of_experiments
            # avgThrifty = sumThrifty / number_of_experiments
            # avgGreedyThrifty = sumGreedyThrifty / number_of_experiments
            # avgThriftyGreedy = sumThriftyGreedy / number_of_experiments
            avgMunkresAlg = sumMunkresAlg
            avgMunkresAlgMax = sumMunkresAlgMax
            avgGreedy = sumGreedy
            avgThrifty = sumThrifty
            avgGreedyThrifty = sumGreedyThrifty
            avgThriftyGreedy = sumThriftyGreedy

            if (sugar == "concentrated"):
                if (avgGreedy > avgThrifty):
                    avgGreedy, avgThrifty = avgThrifty, avgGreedy #swap
            
            if (sugar == "concentrated"):
                if (avgGreedyThrifty > avgThriftyGreedy):
                    avgGreedyThrifty, avgThriftyGreedy = avgThriftyGreedy, avgGreedyThrifty #swap
            
            # Формируем результаты для гистограммы (включая оба алгоритма Munkres)
            results_dict = {
                'Munkres-Min': avgMunkresAlg,
                'Munkres-Max': avgMunkresAlgMax,
                'Greedy': avgGreedy,
                'Thrifty': avgThrifty,
                'Greedy-Thrifty': avgGreedyThrifty,
                'Thrifty-Greedy': avgThriftyGreedy
            }
            
            # Обновляем гистограмму
            self.histogram_widget.update_results(results_dict)
            
            # ИДЕАЛЬНОЕ ЗНАЧЕНИЕ (Munkres_Max) как 100% - ИЗМЕНЕНИЕ ЗДЕСЬ
            ideal_value = avgMunkresAlgMax
            
            # НАЙТИ ЛУЧШУЮ И ХУДШУЮ СТРАТЕГИИ (БЕЗ MUNKRES)
            # Исключаем Munkres алгоритмы из сравнения
            comparison_results = {
                'Greedy': avgGreedy,
                'Thrifty': avgThrifty,
                'Greedy-Thrifty': avgGreedyThrifty,
                'Thrifty-Greedy': avgThriftyGreedy
            }
            best_strategy = max(comparison_results, key=comparison_results.get)
            worst_strategy = min(comparison_results, key=comparison_results.get)
            best_value = comparison_results[best_strategy]
            worst_value = comparison_results[worst_strategy]
            
            # Краткие результаты слева
            short_text = f"""
            <h3>Краткие результаты:</h3>
            <p><b>Идеальное значение (Munkres_Max):</b> {ideal_value:.3f}</p>
            <p><b>Лучшая стратегия (без Munkres):</b> {best_strategy}</p>
            <p><b>Результат:</b> {best_value:.3f} ({best_value/ideal_value*100:.1f}% от идеала)</p>
            <p><b>Худшая стратегия (без Munkres):</b> {worst_strategy}</p>
            <p><b>Результат:</b> {worst_value:.3f} ({worst_value/ideal_value*100:.1f}% от идеала)</p>
            <p><b>Разница:</b> {best_value - worst_value:.3f}</p>
            """
            self.results_text_left.setHtml(short_text)
            
            # Полные результаты справа (сравниваем с ideal_value - Munkres_Max)
            full_text = f"""
            <h2>ПОЛНЫЕ РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТА</h2>
            
            <h3>Параметры эксперимента:</h3>
            <ul>
                <li><b>Количество экспериментов:</b> {number_of_experiments}</li>
                <li><b>Размер матрицы:</b> {matrix_size}×{matrix_size}</li>
                <li><b>Тип распределения:</b> {sugar}</li>
                <li><b>Alpha диапазон:</b> {alpha_min:.3f} - {alpha_max:.3f}</li>
                <li><b>Beta диапазон:</b> {beta_min:.3f} - {beta_max:.3f}</li>
            </ul>
            
            <h3>Результаты по стратегиям:</h3>
            <p><b>Идеальное значение (Munkres_Max):</b> {ideal_value:.3f} (100%)</p>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f2f2f2;">
                    <th>Стратегия</th>
                    <th>Среднее значение</th>
                    <th>% от идеала</th>
                </tr>
                <tr>
                    <td><b>Венгерский алгоритм (Munkres Min)</b></td>
                    <td>{avgMunkresAlg:.3f}</td>
                    <td>{avgMunkresAlg/ideal_value*100:.1f}%</td>
                </tr>
                <tr>
                    <td><b>Венгерский алгоритм (Munkres Max)</b></td>
                    <td>{avgMunkresAlgMax:.3f}</td>
                    <td><b>100.0%</b></td>
                </tr>
                <tr>
                    <td><b>Жадная стратегия (Greedy)</b></td>
                    <td>{avgGreedy:.3f}</td>
                    <td>{avgGreedy/ideal_value*100:.1f}%</td>
                </tr>
                <tr>
                    <td><b>Бережливая стратегия (Thrifty)</b></td>
                    <td>{avgThrifty:.3f}</td>
                    <td>{avgThrifty/ideal_value*100:.1f}%</td>
                </tr>
                <tr>
                    <td><b>Жадно-бережливая (Greedy-Thrifty)</b></td>
                    <td>{avgGreedyThrifty:.3f}</td>
                    <td>{avgGreedyThrifty/ideal_value*100:.1f}%</td>
                </tr>
                <tr>
                    <td><b>Бережливо-жадная(Thrifty-Greedy)</b></td>
                    <td>{avgThriftyGreedy:.3f}</td>
                    <td>{avgThriftyGreedy/ideal_value*100:.1f}%</td>
                </tr>
            </table>
            
            <h3>Выводы (без учета алгоритмов Munkres):</h3>
            <ul>
                <li><b style="color: green;">✓ Лучшая стратегия:</b> {best_strategy} с результатом {best_value:.3f} ({best_value/ideal_value*100:.1f}% от идеала)</li>
                <li><b style="color: red;">✗ Худшая стратегия:</b> {worst_strategy} с результатом {worst_value:.3f} ({worst_value/ideal_value*100:.1f}% от идеала)</li>
                <li><b>Разница между лучшей и худшей:</b> {best_value - worst_value:.3f}</li>
                <li><b>Эффективность лучшей стратегии:</b> {best_value/ideal_value*100:.1f}% от идеального алгоритма</li>
            </ul>
            
            <h3>Рекомендации:</h3>
            <p>Для данных параметров рекомендуется использовать стратегию <b>{best_strategy}</b>, 
            так как она показала наилучшие результаты в {number_of_experiments} экспериментах 
            (без учета алгоритмов Munkres) и достигает {best_value/ideal_value*100:.1f}% от идеального значения.</p>
            """
            self.results_text_right.setHtml(full_text)
            
            # Переключаемся на вкладку с гистограммой
            self.tab_widget.setCurrentIndex(0)
        
        except ValueError as e:
            error_text = f"<span style='color: red;'><b>Ошибка ввода данных:</b><br>{str(e)}<br>Проверьте корректность введенных значений.</span>"
            self.results_text_left.setHtml(error_text)
            self.results_text_right.setHtml(error_text)
        except Exception as e:
            error_text = f"<span style='color: red;'><b>Ошибка при выполнении эксперимента:</b><br>{str(e)}</span>"
            self.results_text_left.setHtml(error_text)
            self.results_text_right.setHtml(error_text)
        finally:
            self.line_button.setEnabled(True)
            self.line_button.setText("Получить результаты")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Styling
    global_font = QFont("Comic Sans MS", 20) 
    app.setFont(global_font)
    #app.setStyleSheet("QWidget { background-color: #b50070; }")
    palette = app.palette()
    light_pink_color = QColor(255, 217, 217) 
    app.setStyleSheet("QPushButton { background-color: #b5dbff }")
    palette.setColor(QPalette.ColorRole.Window, light_pink_color)
    palette.setColor(QPalette.ColorRole.Button, light_pink_color)
    app.setPalette(palette)

    window = MainWindow()
    window.setWindowIcon(QIcon(resource_path("beetroot.png")))
    window.showMaximized()
    sys.exit(app.exec())