import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor

class LabWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Параметры окна
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("Лабораторная работа: Основы GUI")
        self.resize(400, 350)
        self.original_size = self.size()
        self.layout = QVBoxLayout()

        # Кнопка закрытия
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {background-color: #ff5f55; color: white; border: none; border-radius: 12px; font-weight: bold;}
            QPushButton:hover {background-color: #ff0000;}
        """)
        self.close_btn.clicked.connect(self.close)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.close_btn)
        self.layout.addLayout(top_layout)

        # Надпись (текстом или изображение)
        self.label = QLabel("Надпись - текст")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""QLabel {font-size: 14px; border: 1px solid #ccc; background-color: #f0f0f0;}""")
        self.label.setMinimumHeight(100)
        self.layout.addWidget(self.label)

        # Кнопка 1
        self.btn1 = QPushButton("Кнопка 1: Заменить надпись")
        self.btn1.clicked.connect(self.change_label_to_image)
        self.layout.addWidget(self.btn1)

        # Кнопка 2
        self.btn2 = QPushButton("Кнопка 2: Изменить форму окна")
        self.btn2.clicked.connect(self.change_window_shape)
        self.layout.addWidget(self.btn2)

        # Компоновка окна
        self.setLayout(self.layout)

        # Переменные состояния
        self.window_shape_pixmap = None
        self.drag_pos = None
        self.is_shape_mode = False

    # Обработчик первой кнопки (замена надписи на изображение)
    def change_label_to_image(self):
        pixmap = QPixmap("image.png")

        if pixmap.isNull():
            pixmap = QPixmap(200, 80)
            pixmap.fill(QColor(200, 255, 200))

            painter = QPainter(pixmap)
            painter.setPen(QColor(0, 100, 0))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, "Надпись - изображение")
            painter.end()

            pixmap.save("image.png", "PNG")

        pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label.setPixmap(pixmap)
        self.label.setText("")

    # Обработчик второй кнопки - изменение/восстановление формы окна
    def change_window_shape(self):
        if self.is_shape_mode:
            self.restore_original_shape()
            return

        pixmap = QPixmap("shape.png")

        if pixmap.isNull():
            pixmap = QPixmap(400, 350)
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QColor(100, 150, 255, 200))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(pixmap.rect().adjusted(0, 0, -1, -1), 50, 50)
            painter.end()

            pixmap.save("shape.png", "PNG")

        self.window_shape_pixmap = pixmap
        self.is_shape_mode = True

        self.setFixedSize(pixmap.size())
        self.btn2.setText("Кнопка 2: Вернуть форму окна")

        self.update()

    # Возвращение исходной формы окна
    def restore_original_shape(self):
        self.is_shape_mode = False
        self.window_shape_pixmap = None

        self.setFixedSize(self.original_size)
        self.btn2.setText("Кнопка 2: Изменить форму окна")

        self.update()

    # Отрисовка окна
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.is_shape_mode and self.window_shape_pixmap is not None:
            painter.drawPixmap(self.rect(), self.window_shape_pixmap)

        else:
            painter.setBrush(QColor(240, 240, 240))
            painter.setPen(QColor(150, 150, 150))
            painter.drawRect(self.rect().adjusted(0, 0, -1, -1))

        painter.end()

    # Перемещение окна мышкой
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = (event.globalPos() - self.frameGeometry().topLeft())
            event.accept()

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton and self.drag_pos is not None):
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LabWindow()
    window.show()

    sys.exit(app.exec())