from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont

# TODO: Написать пару классов для вывода всего дебага в slam_brain и для вывода требуемых графиов

class BottomDebugMenu(QWidget):
    def __init__(self, parent, geometry, robot_value):
        super().__init__(parent)

        self.robot_value = robot_value
        self.progress_bars = []
        self.main_geometry = geometry
        self.buildDebuger()

    def buildDebuger(self):
        self.setStyleSheet("border:3px solid rgb(0, 0, 0);")
        self.setFixedSize(self.main_geometry[0] + 300, self.main_geometry[1] * 0.3)

        #vbox = QVBoxLayout()

        hbox = self.robotInfo()
        test_label = QLabel('TEST!!!')
        #vbox.addLayout(hbox)

        self.setLayout(hbox)

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
        hbox = QHBoxLayout()
        for x in range(self.robot_value):
            vbox = QVBoxLayout()

            vbox.addWidget(QLabel('Robot {0}'.format(x)))
            new_progress_bar = ProgressBar()
            new_progress_bar.setFixedSize(150, self.main_geometry[1] * 0.28)
            self.progress_bars.append(new_progress_bar)
            vbox.addWidget(new_progress_bar)
            hbox.addLayout(vbox)

        return hbox


class DebugInfo(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.buildDebuger()

    def buildDebuger(self):
        ...


class ProgressBar(QFrame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setMinimumSize(20, 35)
        self.value = 0
        self.num = [15, 10, 5]
        self.font_size = round((self.width() + self.height()) / 100)
        self.paint_font = QFont('Serif', self.font_size, QFont.Light)

    def setValue(self, value):
        self.value = value
        self.repaint()

    def incrementValue(self):
        self.value += 1
        self.repaint()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawBar(qp)
        qp.end()

    def drawBar(self, qp):
        qp.setFont(self.paint_font)

        w = self.width()
        h = self.height()

        line_step = int(round(h / 4))
        qp.setPen(QPen(QColor(255, 255, 255)))
        qp.setBrush(QColor(60, 179, 113))

        cur_heigth = self.value * (h / (self.num[0] + self.num[2]))
        if h / self.num[0] + self.num[2] > 1:
            drow_heigth = h - cur_heigth
            qp.drawRect(0, drow_heigth, w, cur_heigth)

        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(1, 0, w - 2, h - 1)

        i = 0
        for step in range(line_step, line_step * 4, line_step):
            if step - self.font_size < h - cur_heigth < step + self.font_size:
                pass
            else:
                self.drawMetric(qp, step, str(self.num[i]), w)
            i += 1

        qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        self.drawMetric(qp, h - cur_heigth, str(self.value), w)

        # Переназначение максимума бара
        if self.value > (self.num[0] + self.num[2]) * 0.8:
            self.num = [x * 4 for x in self.num]

    def drawMetric(self, qp, heigth, text, w):
        qp.drawLine(0, heigth + 1, int(w * 0.1), heigth + 1)
        qp.drawLine(w, heigth + 1, int(w * 0.9), heigth + 1)
        metrics = qp.fontMetrics()
        fw = metrics.width(text)
        qp.drawText(w / 2 - fw / 2, heigth + self.font_size / 1.7, text)

