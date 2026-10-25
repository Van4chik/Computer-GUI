from PyQt5.QtCore import pyqtSignal, QObject


class _SignalWrapper(QObject):
    mySignal = pyqtSignal(float)


_wrapper_instance = _SignalWrapper()
mySignal = _wrapper_instance.mySignal


def func():
    import main
    try:
        newOne = main.Data()
        newList = newOne.getData()
        newList.append("Данные инициализированы в cl1")
        print("cl1: func() — данные инициализированы:", newList)
    except Exception as e:
        print(f"cl1: ошибка в func(): {e}")