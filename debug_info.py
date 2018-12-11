from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton


# TODO: Написать пару классов для вывода всего дебага в slam_brain и для вывода требуемых графиов

class BottomDebugMenu(QWidget):
    def __init__(self, parent, geometry):
        super().__init__(parent)

        self.buildDebuger(geometry)

    def buildDebuger(self, geometry):
        self.setStyleSheet("border:3px solid rgb(0, 0, 0);")
        print(geometry[0])
        self.setFixedSize(geometry[0] + 300, geometry[1] * 0.3)

        vbox = QVBoxLayout()

        test_label = QLabel('TEST!!!')
        vbox.addWidget(test_label)

        self.setLayout(vbox)

    def mainInfo(self):
        # TODO: Колличество тактов алгоритма
        # TODO: Пройденный путь каждым роботом
        #vbox = QVBoxLayout()
        #vbox.addWidget(QLabel('Not taked'))
        #vbox.addWidget(QLabel(value))
        #vbox.addWidget(QLabel('Booked'))
        #vbox.addWidget(QLabel(value))
        #vbox.addWidget(QLabel('Progressed'))
        #vbox.addWidget(QLabel(value))
        #vbox.addWidget(QLabel('Passed'))
        #vbox.addWidget(QLabel(value))

        pause_button = QPushButton('Pause searching')
        #pause_button.clicked.connect(...)

    def robotInfo(self):
        ...


class DebugInfo(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.buildDebuger()

    def buildDebuger(self):

