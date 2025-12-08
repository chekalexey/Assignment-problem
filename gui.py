from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QRadioButton, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QIntValidator, QDoubleValidator)
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
        layout = QVBoxLayout()

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

        self.line_button = QPushButton("Получить значение", self)
        self.line_button.clicked.connect(self.get_integer_from_line_edit)

        self.result_label = QLabel("Result: ", self)
        #колво экспериментов, альфа мин макс, бета мин макс, размер матрицы, концетрированое/равномерное распределение сахаристости
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(QLabel("Это страница эксперементального режима"))

        layout.addWidget(self.number_of_experminets)
        layout.addWidget(self.alpha_min)
        layout.addWidget(self.alpha_max)
        layout.addWidget(self.beta_min)
        layout.addWidget(self.beta_max)
        layout.addWidget(self.matrix_size)
        layout.addWidget(gb)

        layout.addWidget(self.line_button)
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addWidget(btn_back)
        layout.addWidget(btn_home)

        page.setLayout(layout)
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
            #z = 0
            sum = 0

            for i in range(number_of_experminets):
                thingie = MatrixGenerator(n=matrix_size, v=matrix_size, distribution_type=sugar, a_min=alpha_min, a_max=alpha_max, beta_min=beta_min, beta_max=beta_max)
                print(f"matrix number {i+1}")
                print(thingie.D_matrix)
                a = algo(thingie.D_matrix)
                print(a.Greedy())
                print(a.Thrifty())
                print(a.Greedy_Thrifty(1))
                print(a.Thrifty_Greedy(1))
                #z += a.Greedy()[0]
                z,v = a.Greedy()
                sum += z
                
                print("------------------------------------------")
            print(f"total sum {sum}")
            # print(sugar)
            # print(number_of_experminets, alpha_min, alpha_max, beta_min, beta_max, matrix_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())