from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import cl1
import cl2
import cl3


class Some(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛР №2 Сигналы-Слоты: Конвертер валют")
        self.resize(600, 150)

        self.usd_edit = QLineEdit()
        self.rub_edit = QLineEdit()
        self.eur_edit = QLineEdit()

        validator = QDoubleValidator(0.0, 9999999.99, 4)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.usd_edit.setValidator(validator)
        self.rub_edit.setValidator(validator)
        self.eur_edit.setValidator(validator)

        layout = QFormLayout()
        layout.addRow("Доллар (USD):", self.usd_edit)
        layout.addRow("Рубль (RUB):", self.rub_edit)
        layout.addRow("Евро (EUR):", self.eur_edit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Курс валют на 25.10.2026
        self.usd_to_rub = 80.5381
        self.eur_to_rub = 90.2429

        # Сигналы из модулей cl1, cl2, cl3
        self.myClsig = cl1.mySignal    # RUB
        self.myDolsig = cl2.mySignal   # EUR
        self.myUsdsig = cl3.mySignal   # USD

        self.myClsig.connect(self.on_rub_signal)
        self.myDolsig.connect(self.on_dolar_signal)
        self.myUsdsig.connect(self.on_usd_signal)

        # Сигналы от полей ввода
        self.usd_edit.textChanged.connect(self.usd_changed)
        self.rub_edit.textChanged.connect(self.rub_changed)
        self.eur_edit.textChanged.connect(self.eur_changed)

        self.updating = False

    def usd_changed(self, text):
        if self.updating:
            return
        try:
            usd = float(text) if text else 0.0
            self.updating = True
            rub = usd * self.usd_to_rub
            eur = rub / self.eur_to_rub
            self.rub_edit.setText(f"{rub:.4f}")
            self.eur_edit.setText(f"{eur:.4f}")
            self.updating = False

            self.myUsdsig.emit(usd)
        except ValueError:
            pass

    def rub_changed(self, text):
        if self.updating:
            return
        try:
            rub = float(text) if text else 0.0
            self.updating = True
            usd = rub / self.usd_to_rub
            eur = rub / self.eur_to_rub
            self.usd_edit.setText(f"{usd:.4f}")
            self.eur_edit.setText(f"{eur:.4f}")
            self.updating = False

            self.myClsig.emit(rub)
        except ValueError:
            pass

    def eur_changed(self, text):
        if self.updating:
            return
        try:
            eur = float(text) if text else 0.0
            self.updating = True
            rub = eur * self.eur_to_rub
            usd = rub / self.usd_to_rub
            self.usd_edit.setText(f"{usd:.4f}")
            self.rub_edit.setText(f"{rub:.4f}")
            self.updating = False

            self.myDolsig.emit(eur)
        except ValueError:
            pass

    def on_rub_signal(self, value):
        print(f"[Сигнал из cl1] Зафиксировано изменение рублей: {value}")

    def on_dolar_signal(self, value):
        print(f"[Сигнал из cl2] Зафиксировано изменение евро: {value}")

    def on_usd_signal(self, value):
        print(f"[Сигнал из cl3] Зафиксировано изменение долларов: {value}")


class Data:
    def __init__(self):
        self.myData = []

    def getData(self):
        return self.myData


if __name__ == "__main__":
    cl1.func()
    app = QApplication(sys.argv)
    window = Some()
    window.show()
    sys.exit(app.exec_())