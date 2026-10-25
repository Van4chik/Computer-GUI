from PyQt5.QtCore import pyqtSignal, QObject


class _SignalWrapper(QObject):
    mySignal = pyqtSignal(float)


_wrapper_instance = _SignalWrapper()
mySignal = _wrapper_instance.mySignal