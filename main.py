import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QComboBox, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QAction, QMessageBox,
    QDialog, QLineEdit, QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt


# Окно для ввода произвольного SQL-запроса
class QueryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод SQL-запроса")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(450, 150)

        self.layout = QFormLayout(self)

        self.query_edit = QLineEdit()
        self.query_edit.setPlaceholderText(
            "Например: SELECT * FROM sqlite_master WHERE type='table'"
        )
        self.layout.addRow("SQL-запрос:", self.query_edit)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def get_query(self):
        return self.query_edit.text().strip()


# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №3 — Таблицы и SQL")
        self.resize(900, 600)

        # Состояние приложения
        self.connection = None
        self.current_db_path = None
        self.current_table = None
        self.current_columns = []

        self._init_ui()
        self._init_menu()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        control_layout = QHBoxLayout()

        self.lbl_status = QLabel("База данных не подключена")
        self.lbl_status.setStyleSheet("color: gray; font-weight: bold;")
        control_layout.addWidget(self.lbl_status)

        control_layout.addStretch()

        self.combo_column = QComboBox()
        self.combo_column.setMinimumWidth(180)
        self.combo_column.setEnabled(False)
        control_layout.addWidget(QLabel("Колонка:"))
        control_layout.addWidget(self.combo_column)

        self.bt1 = QPushButton("bt1: SELECT name")
        self.bt2 = QPushButton("bt2: Таблица в Tab4")
        self.bt3 = QPushButton("bt3: Таблица в Tab5")
        self.btn_custom = QPushButton("Произвольный SQL...")

        for btn in (self.bt1, self.bt2, self.bt3, self.btn_custom):
            btn.setEnabled(False)
            control_layout.addWidget(btn)

        main_layout.addLayout(control_layout)

        self.tabs = QTabWidget()
        self.tab1 = QTableWidget()
        self.tab2 = QTableWidget()
        self.tab3 = QTableWidget()
        self.tab4 = QTableWidget()
        self.tab5 = QTableWidget()

        self.tabs.addTab(self.tab1, "Tab1")
        self.tabs.addTab(self.tab2, "Tab2")
        self.tabs.addTab(self.tab3, "Tab3")
        self.tabs.addTab(self.tab4, "Tab4")
        self.tabs.addTab(self.tab5, "Tab5")

        main_layout.addWidget(self.tabs)

        self.bt1.clicked.connect(self.on_bt1_clicked)
        self.bt2.clicked.connect(self.on_bt2_clicked)
        self.bt3.clicked.connect(self.on_bt3_clicked)
        self.btn_custom.clicked.connect(self.on_custom_query)
        self.combo_column.currentTextChanged.connect(self.on_column_changed)

    def _init_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")

        act_open = QAction("Set connection", self)
        act_open.setShortcut("Ctrl+O")
        act_open.triggered.connect(self.set_connection)
        file_menu.addAction(act_open)

        act_close = QAction("Close connection", self)
        act_close.setShortcut("Ctrl+W")
        act_close.triggered.connect(self.close_connection)
        file_menu.addAction(act_close)

        file_menu.addSeparator()

        act_exit = QAction("Выход", self)
        act_exit.setShortcut("Ctrl+Q")
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)

    def set_connection(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл базы данных SQLite",
            "",
            "SQLite файлы (*.db *.sqlite *.sqlite3);;Все файлы (*)"
        )
        if not file_path:
            return

        try:
            self.connection = sqlite3.connect(file_path)
            self.current_db_path = file_path
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться:\n{e}")
            return

        self.lbl_status.setText(f"Подключено: {file_path}")
        self.lbl_status.setStyleSheet("color: green; font-weight: bold;")

        for btn in (self.bt1, self.bt2, self.bt3, self.btn_custom):
            btn.setEnabled(True)
        self.combo_column.setEnabled(True)

        self._execute_to_tab("SELECT * FROM sqlite_master", self.tab1)
        self.tabs.setCurrentWidget(self.tab1)

        self._fill_tables_combo()

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.Error:
                pass
            self.connection = None

        self.current_db_path = None
        self.current_table = None
        self.current_columns = []

        for tab in (self.tab1, self.tab2, self.tab3, self.tab4, self.tab5):
            tab.clear()
            tab.setRowCount(0)
            tab.setColumnCount(0)

        self.combo_column.clear()
        self.combo_column.setEnabled(False)
        for btn in (self.bt1, self.bt2, self.bt3, self.btn_custom):
            btn.setEnabled(False)

        self.lbl_status.setText("База данных не подключена")
        self.lbl_status.setStyleSheet("color: gray; font-weight: bold;")

    def _fill_tables_combo(self):
        self.combo_column.blockSignals(True)
        self.combo_column.clear()
        try:
            cursor = self.connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = [row[0] for row in cursor.fetchall()]
            self.combo_column.addItems(tables)
            if tables:
                self.current_table = tables[0]
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Предупреждение", str(e))
        self.combo_column.blockSignals(False)

    def _execute_to_tab(self, query, table_widget):
        """Выполнение SQL-запроса и вывод результата в QTableWidget."""
        table_widget.clear()
        table_widget.setRowCount(0)
        table_widget.setColumnCount(0)

        try:
            cursor = self.connection.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка SQL", str(e))
            return

        table_widget.setColumnCount(len(columns))
        table_widget.setHorizontalHeaderLabels(columns)
        table_widget.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else "")
                table_widget.setItem(r, c, item)

        table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

    def on_bt1_clicked(self):
        """bt1: выборочный запрос SELECT name FROM sqlite_master → Tab2."""
        self._execute_to_tab(
            "SELECT name FROM sqlite_master", self.tab2
        )
        self.tabs.setCurrentWidget(self.tab2)

    def on_bt2_clicked(self):
        """bt2: вывод выбранной таблицы в Tab4."""
        if not self.current_table:
            return
        self._execute_to_tab(
            f"SELECT * FROM [{self.current_table}]", self.tab4
        )
        self.tabs.setCurrentWidget(self.tab4)

    def on_bt3_clicked(self):
        """bt3: вывод количества строк выбранной таблицы в Tab5."""
        if not self.current_table:
            return
        self._execute_to_tab(
            f"SELECT COUNT(*) AS row_count FROM [{self.current_table}]",
            self.tab5
        )
        self.tabs.setCurrentWidget(self.tab5)

    def on_column_changed(self, table_name):
        """При выборе таблицы из QComboBox — запрос в Tab3."""
        if not table_name or not self.connection:
            return
        self.current_table = table_name
        self._execute_to_tab(
            f"PRAGMA table_info([{table_name}])", self.tab3
        )
        self.tabs.setCurrentWidget(self.tab3)

    def on_custom_query(self):
        """Бонус: модальное окно для ввода произвольного SQL-запроса."""
        dlg = QueryDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            query = dlg.get_query()
            if query:
                # Результат произвольного запроса — в активную вкладку
                current = self.tabs.currentWidget()
                self._execute_to_tab(query, current)

    def closeEvent(self, event):
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.Error:
                pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())