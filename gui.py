from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QRadioButton, QGroupBox, QScrollArea, QSpinBox, QGridLayout, QSizePolicy, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QIntValidator, QDoubleValidator, QPixmap, QPalette)
from matgen import *
import sys
import numpy as np

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
        
        self.line_button = QPushButton("Получить результаты эксперимента", self)
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
        self.textOutput.setFixedHeight(100)
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
            label_col = QLabel(f"Столбец {j+1}")
            label_col.setAlignment(Qt.AlignCenter)
            label_col.setStyleSheet("font-weight: bold; background-color: #e0e0e0; padding: 2px;")
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
            label_row = QLabel(f"Строка {i+1}")
            label_row.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label_row.setStyleSheet("font-weight: bold; background-color: #e0e0e0; padding: 3px;")
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
                line_edit.setStyleSheet("""
                    QLineEdit {
                        background-color: #ffc2c2;
                    }
                """)
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
                        row.append(float(text))
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
        lineEditStr = ""
        matrix = self.get_matrix_data()
        a = algo(matrix)

        x, y = a.Munkres_Alg()
        lineEditStr += f"total Munkres_Alg {x} {y}\n"
        print(f"total Munkres_Alg {x} {y}")

        x, y = a.Greedy()
        lineEditStr += f"total Greedy {x} {y}\n"
        print(f"total Greedy {x} {y}")

        x, y = a.Thrifty()
        lineEditStr += f"total Thrifty {x} {y}\n"
        print(f"total Thrifty {x} {y}")

        x, y = a.Greedy_Thrifty(matrix.shape[0]//2)
        lineEditStr += f"total Greedy_Thrifty {x} {y}\n"
        print(f"total Greedy_Thrifty {x} {y}")

        x, y = a.Thrifty_Greedy(matrix.shape[0]//2)
        lineEditStr += f"total Thrifty_Greedy {x} {y}\n"
        print(f"total Thrifty_Greedy {x} {y}")

        self.textOutput.setText(lineEditStr)

    def create_third_page(self):
        """Третья страница"""
        page = QWidget()
        main_layout = QHBoxLayout(page)

        left_widget = QWidget()
        optionsLayout = QVBoxLayout(left_widget)
        optionsLayout.setSpacing(15)

        title = QLabel("Экспериментальный режим")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; margin: 10px; color: #2c3e50;")

        btn_back = QPushButton("← Назад")
        btn_back.clicked.connect(lambda: self.go_to_page(1))

        btn_home = QPushButton("В главное меню")
        btn_home.clicked.connect(lambda: self.go_to_page(0))

        # Количество экспериментов
        self.number_of_experminets = QLineEdit("5", self)
        self.number_of_experminets.setPlaceholderText("Введите число экспериментов")
        self.number_of_experminets.setStyleSheet("font-size: 14px; padding: 8px;")
        self.number_of_experminets.setValidator(QIntValidator(0, 100, self))

                # Размер матрицы
        self.matrix_size = QLineEdit("3", self)
        self.matrix_size.setPlaceholderText("matrix_size")
        self.matrix_size.setStyleSheet("font-size: 14px; padding: 8px;")
        self.matrix_size.setValidator(QIntValidator(1, 16, self))

        # Создаем компактный layout для alpha и beta
        alpha_beta_group = QGroupBox("Параметры")
        alpha_beta_layout = QVBoxLayout(alpha_beta_group)
        
        # Создаем таблицу для alpha
        alpha_widget = QWidget()
        alpha_grid = QGridLayout(alpha_widget)
        alpha_grid.setSpacing(10)
        alpha_grid.setContentsMargins(5, 5, 5, 5)
        
        alpha_label = QLabel("Сахаристость:")
        alpha_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        alpha_grid.addWidget(alpha_label, 0, 0, 1, 2)
        
        alpha_min_label = QLabel("min:")
        alpha_min_label.setStyleSheet("font-size: 13px;")
        alpha_grid.addWidget(alpha_min_label, 1, 0)
        
        self.alpha_min = QLineEdit("0.1", self)
        self.alpha_min.setPlaceholderText("min")
        self.alpha_min.setStyleSheet("font-size: 14px; padding: 6px;")
        self.alpha_min.setValidator(QDoubleValidator(self))
        self.alpha_min.setMaximumWidth(100)
        alpha_grid.addWidget(self.alpha_min, 1, 1)
        
        alpha_max_label = QLabel("max:")
        alpha_max_label.setStyleSheet("font-size: 13px;")
        alpha_grid.addWidget(alpha_max_label, 2, 0)
        
        self.alpha_max = QLineEdit("0.3", self)
        self.alpha_max.setPlaceholderText("max")
        self.alpha_max.setStyleSheet("font-size: 14px; padding: 6px;")
        self.alpha_max.setValidator(QDoubleValidator(self))
        self.alpha_max.setMaximumWidth(100)
        alpha_grid.addWidget(self.alpha_max, 2, 1)
        
        # Создаем таблицу для beta
        beta_widget = QWidget()
        beta_grid = QGridLayout(beta_widget)
        beta_grid.setSpacing(10)
        beta_grid.setContentsMargins(5, 5, 5, 5)
        
        beta_label = QLabel("Коэффициент деградации:")
        beta_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        beta_grid.addWidget(beta_label, 0, 0, 1, 2)
        
        beta_min_label = QLabel("         min:")
        beta_min_label.setStyleSheet("font-size: 13px;")
        beta_grid.addWidget(beta_min_label, 1, 0)
        
        self.beta_min = QLineEdit("0.1", self)
        self.beta_min.setPlaceholderText("    min")
        self.beta_min.setStyleSheet("font-size: 14px; padding: 6px;")
        self.beta_min.setValidator(QDoubleValidator(0.00001, 0.99999, 5, self))
        self.beta_min.setMaximumWidth(100)
        beta_grid.addWidget(self.beta_min, 1, 1)
        
        beta_max_label = QLabel("         max:")
        beta_max_label.setStyleSheet("font-size: 13px;")
        beta_grid.addWidget(beta_max_label, 2, 0)
        
        self.beta_max = QLineEdit("0.3", self)
        self.beta_max.setPlaceholderText("    max")
        self.beta_max.setStyleSheet("font-size: 14px; padding: 6px;")
        self.beta_max.setValidator(QDoubleValidator(0.00001, 0.99999, 5, self))
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
        self.concentrated.setStyleSheet("font-size: 14px;")
        self.uniform = QRadioButton("Равномерное", self)
        self.uniform.setStyleSheet("font-size: 14px;")
        radio_buttons_layout.addWidget(self.concentrated)
        radio_buttons_layout.addWidget(self.uniform)
        
        gb = QGroupBox("Распределение😎")
        gb.setLayout(radio_buttons_layout)

        self.line_button = QPushButton("Получить результаты эксперимента", self)
        self.line_button.clicked.connect(self.get_integer_from_line_edit)
        
        ######################SVEKLA########################
        image_label = QLabel()
        try:
            pixmap = QPixmap('svekla.jpg')
            if pixmap.isNull():
                pixmap = QPixmap(400, 400)
                pixmap.fill(Qt.red)
                image_label.setText("Картинка не найдена")
                image_label.setAlignment(Qt.AlignCenter)
            else:
                image_label.setPixmap(pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            pixmap = QPixmap(300, 300)
            pixmap.fill(Qt.gray)
            image_label.setPixmap(pixmap)
            image_label.setText(f"Ошибка: {str(e)}")
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setWordWrap(True)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        ####################################################

        # Собираем элементы в layout
        optionsLayout.addWidget(title)
        optionsLayout.addStretch()
        
        # Количество экспериментов
        exp_label = QLabel("Количество экспериментов:")
        exp_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        optionsLayout.addWidget(exp_label)
        optionsLayout.addWidget(self.number_of_experminets)

                # Размер матрицы
        size_label = QLabel("Размер матрицы:")
        size_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        optionsLayout.addWidget(size_label)
        optionsLayout.addWidget(self.matrix_size)
        
        # Alpha и Beta параметры
        optionsLayout.addWidget(alpha_beta_group)
                
        # Распределение
        optionsLayout.addWidget(gb)
        
        # Кнопка и результат
        optionsLayout.addWidget(self.line_button)
        #optionsLayout.addWidget(self.result_label)
        optionsLayout.addStretch()

        # Кнопки навигации
        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_back)
        button_layout.addWidget(btn_home)
        optionsLayout.addLayout(button_layout)

        main_layout.addWidget(left_widget, stretch=1)
        main_layout.addWidget(image_label, stretch=2)

        page.setLayout(main_layout)
        self.stacked_widget.addWidget(page)

    def go_to_page(self, index):
        """Переход на страницу по индексу"""
        self.stacked_widget.setCurrentIndex(index)

    def get_integer_from_line_edit(self):
            number_of_experminets = int(self.number_of_experminets.text())
            alpha_min = float(self.alpha_min.text())
            alpha_max = float(self.alpha_max.text())
            beta_min = float(self.beta_min.text())
            beta_max = float(self.beta_max.text())
            matrix_size = int(self.matrix_size.text())
            sugar = ""
            if self.concentrated.isChecked():
                sugar = self.concentrated.text()
            elif self.uniform.isChecked():
                sugar = self.uniform.text()

            sumMunkresAlg = 0
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
                print(a.Greedy())
                print(a.Thrifty())
                print(a.Greedy_Thrifty(matrix_size//2))
                print(a.Thrifty_Greedy(matrix_size//2))
                #x += a.Greedy()[0]
                x, y = a.Munkres_Alg()
                sumMunkresAlg += x
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
            print(f"total sumGreedy {sumGreedy}")
            print(f"total sumThrifty {sumThrifty}")
            print(f"total sumGreedyThrifty {sumGreedyThrifty}")
            print(f"total sumThriftyGreedy {sumThriftyGreedy}")
            # print(sugar)
            # print(number_of_experminets, alpha_min, alpha_max, beta_min, beta_max, matrix_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())