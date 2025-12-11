from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QRadioButton, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QIntValidator, QDoubleValidator, QPixmap)
from matgen import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Навигация между страницами")
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
        layout = QVBoxLayout()

        title = QLabel("Главное меню")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")

        btn_to_page2 = QPushButton("Перейти на страницу ручного режима")
        btn_to_page2.clicked.connect(lambda: self.go_to_page(1))
        btn_to_page2.setMinimumHeight(50)

        btn_to_page3 = QPushButton("Перейти на страницу эксперементального режима")
        btn_to_page3.clicked.connect(lambda: self.go_to_page(2))
        btn_to_page3.setMinimumHeight(50)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(btn_to_page2)
        layout.addWidget(btn_to_page3)
        layout.addStretch()

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def create_second_page(self):
        """Вторая страница"""
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Страница 2")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")

        btn_back = QPushButton("← Назад в меню")
        btn_back.clicked.connect(lambda: self.go_to_page(0))

        btn_next = QPushButton("Далее →")
        btn_next.clicked.connect(lambda: self.go_to_page(2))

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(QLabel("Это страница ручного режима"))
        layout.addStretch()
        layout.addWidget(btn_back)
        layout.addWidget(btn_next)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def create_third_page(self):
        """Третья страница"""
        page = QWidget()
        main_layout = QHBoxLayout(page)

        left_widget = QWidget()
        optionsLayout = QVBoxLayout(left_widget)

        title = QLabel("Страница 3")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")

        btn_back = QPushButton("← Назад")
        btn_back.clicked.connect(lambda: self.go_to_page(1))

        btn_home = QPushButton("В главное меню")
        btn_home.clicked.connect(lambda: self.go_to_page(0))

        self.number_of_experminets = QLineEdit("5", self)
        self.number_of_experminets.setPlaceholderText("Введите число экспериментов")
        self.number_of_experminets.setValidator(QIntValidator(0, 100, self))

        self.alpha_min = QLineEdit("0.1", self)
        self.alpha_min.setPlaceholderText("alpha min")
        self.alpha_min.setValidator(QDoubleValidator(self))

        self.alpha_max = QLineEdit("0.3", self)
        self.alpha_max.setPlaceholderText("alpha max")
        self.alpha_max.setValidator(QDoubleValidator(self))

        self.beta_min = QLineEdit("0.1", self)
        self.beta_min.setPlaceholderText("beta min")
        self.beta_min.setValidator(QDoubleValidator(0.00001, 0.99999, 5, self))
        
        self.beta_max = QLineEdit("0.3", self)
        self.beta_max.setPlaceholderText("beta max")
        self.beta_max.setValidator(QDoubleValidator(0.00001, 0.99999, 5, self))

        self.matrix_size = QLineEdit("3", self)
        self.matrix_size.setPlaceholderText("matrix_size")
        self.matrix_size.setValidator(QIntValidator(1, 16, self))

        radio_buttons_layout = QHBoxLayout()
        self.concentrated = QRadioButton("concentrated", self)
        self.uniform = QRadioButton("uniform", self)
        radio_buttons_layout.addWidget(self.concentrated)
        radio_buttons_layout.addWidget(self.uniform)
        
        gb = QGroupBox("sugar😎")
        gb.setLayout(radio_buttons_layout)

        self.line_button = QPushButton("Получить результаты эксперимента", self)
        self.line_button.clicked.connect(self.get_integer_from_line_edit)

        self.result_label = QLabel("Result: ", self)
        
        ######################SVEKLA########################
        image_label = QLabel()
        try:
            # Загружаем картинку
            pixmap = QPixmap('svekla.jpg')
            if pixmap.isNull():
                # Если картинка не загрузилась, создаем заглушку
                pixmap = QPixmap(400, 400)
                pixmap.fill(Qt.red)  # Красный фон
                image_label.setText("Картинка не найдена")
                image_label.setAlignment(Qt.AlignCenter)
            else:
                # Масштабируем картинку, если нужно
                image_label.setPixmap(pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            # Если произошла ошибка при загрузке
            pixmap = QPixmap(300, 300)
            pixmap.fill(Qt.gray)
            image_label.setPixmap(pixmap)
            image_label.setText(f"Ошибка: {str(e)}")
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setWordWrap(True)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        ####################################################

        #колво экспериментов, альфа мин макс, бета мин макс, размер матрицы, концетрированое/равномерное распределение сахаристости
        optionsLayout.addWidget(title)
        optionsLayout.addStretch()
        optionsLayout.addWidget(QLabel("Это страница эксперементального режима"))

        optionsLayout.addWidget(QLabel("Количество экспериментов:"))
        optionsLayout.addWidget(self.number_of_experminets)
        optionsLayout.addWidget(QLabel("Alpha min:"))
        optionsLayout.addWidget(self.alpha_min)
        optionsLayout.addWidget(QLabel("Alpha max:"))
        optionsLayout.addWidget(self.alpha_max)
        optionsLayout.addWidget(QLabel("Beta min:"))
        optionsLayout.addWidget(self.beta_min)
        optionsLayout.addWidget(QLabel("Beta max:"))
        optionsLayout.addWidget(self.beta_max)
        optionsLayout.addWidget(QLabel("Размер матрицы:"))
        optionsLayout.addWidget(self.matrix_size)
        optionsLayout.addWidget(gb)

        optionsLayout.addWidget(self.line_button)
        optionsLayout.addWidget(self.result_label)
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