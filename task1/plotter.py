from PySide2.QtWidgets import QApplication, QDialog, QWidget, QLineEdit, QLabel, QGridLayout, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2.QtGui import QIcon , QPalette ,QColor
from matplotlib import pyplot as plt
import numpy as np
import sys
import re

plt.style.use('ggplot')


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()

        self.widget = QWidget(self)
        self.setWindowTitle("Plotter")
        self.setWindowIcon(QIcon("function.png"))
        self.setMinimumSize(1000, 800)

        self.error_messag = ""
        self.show_error_alert = True
        self.error_alert = QMessageBox

        self.set_layout()

    # creates the function input text box
    def set_function_Input(self):
        self.function_x = QLineEdit(self)
        self.function_x.setPlaceholderText("enter funtion like 5*x^3 + 2*x")
        self.function_x_label = QLabel("F(x)")
        font = self.function_x.font()
        font.setPointSize(15)
        self.function_x.setFont(font)

    #creates the text inputs for min and max values
    def set_limits_Input(self):
        self.min_x = QLineEdit(self)
        self.min_x.setPlaceholderText("enter min value like -20")
        self.min_x_label = QLabel("min x")

        self.max_x = QLineEdit(self)
        self.max_x.setPlaceholderText("enter max value like 20")
        self.max_x_label = QLabel("max x")

        font_min = self.min_x.font()
        font_min.setPointSize(15)
        self.min_x.setFont(font_min)

        font_max = self.max_x.font()
        font_max.setPointSize(15)
        self.max_x.setFont(font_max)

    # creates the plot button 
    def set_plot_button(self):
        self.plot_button = QPushButton("Plot", self)
        self.plot_button.clicked.connect(self.draw)
    
    # creates the plot figure
    def set_graph_canvas(self):
        self.graph = plt.figure()
        self.axes = self.graph.add_subplot(111)
        self.axes.set_title("Plotter")
        self.canvas = FigureCanvas(self.graph)
        self.toolbar = NavigationToolbar(self.canvas, self)

    # calls all layout elements
    def set_layout_elements(self):
        self.set_function_Input()
        self.set_limits_Input()
        self.set_plot_button()
        self.set_graph_canvas()

    #styles the App 
    def set_styles(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(94, 67, 82))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        fonts = "font-family:Arial; font: bold; color: #f56476; font-size: 20px"
        self.min_x_label.setStyleSheet(fonts)
        self.max_x_label.setStyleSheet(fonts)
        self.plot_button.setStyleSheet(fonts)
        self.function_x_label.setStyleSheet(fonts)

        input = "border-radius:8px; padding:1px 10px ; background: #e7e9eb"
        self.function_x.setStyleSheet( input)
        self.min_x.setStyleSheet( input)
        self.max_x.setStyleSheet( input)

        button_style = "font-family:Snell Roundhand, cursive; background:#f56476; color:#2C313A;  border-radius:8px; font-size:20px; padding:5px 5px;"
        self.plot_button.setStyleSheet(button_style)






    # creates all layout    
    def set_layout(self):
        self.set_layout_elements()
        self.layout = QGridLayout(self.widget)
        self.layout.addWidget(self.function_x_label, 0, 0)
        self.layout.addWidget(self.function_x, 0, 1)
        self.layout.addWidget(self.min_x_label, 1, 0)
        self.layout.addWidget(self.min_x, 1, 1)
        self.layout.addWidget(self.max_x_label, 2, 0)
        self.layout.addWidget(self.max_x, 2, 1)
        self.layout.addWidget(self.plot_button, 3, 1)
        self.layout.addWidget(self.toolbar, 4, 0, 1, 4)
        self.layout.addWidget(self.canvas, 5, 0, 1, 4)
        self.setLayout(self.layout)
        self.set_styles()

    # calls error alert if exists
    def set_user_warnings(self):
        if self.show_error_alert:
            self.error_alert.warning(self, "error", self.error_messag)

    # validates inputs
    def set_input_validation(self, function_x, min_x, max_x):
        if function_x == "" or min_x == "" or max_x == "":
            self.error_messag = "error: All fileds are required"
            self.set_user_warnings()
            return False

        funcution_x_regex = "(?:[0-9-+ * / ^ () x])+"
        limit_regex = "(?:[0-9-])+"

        self.error_messag = ''
        if not bool(re.findall(funcution_x_regex, function_x)):
            self.error_messag = "error: you have to use only numbers , variable x and supported operators[+ - / * ^]"
            self.set_user_warnings()
            return False

        if not bool(re.match(limit_regex, min_x)) :
            self.error_messag = "error: enter valid lower limmit"
            self.set_user_warnings()
            return False

        
        if not bool(re.match(limit_regex, max_x)) :
            self.error_messag = "error:enter valid upper limmit"
            self.set_user_warnings()
            return False    

        return True

    # make main logic for the app
    def set_app_logic(self):
        function_x = self.function_x.text().lower()
        min_x = self.min_x.text()
        max_x = self.max_x.text()

        valid = self.set_input_validation(function_x, min_x, max_x)
        x = []
        y = []

        if valid:
            function_x = function_x.replace(" ", "")
            function_x = function_x.replace("^", "**")
            

            try:
                min_x = float(min_x)
                max_x = float(max_x)
                if max_x <= min_x:
                    self.error_messag = "error: Lower limit must be less than the upper limit"
                    self.set_user_warnings()
                    return x, y, False
            except:
                self.error_messag = "error: enter valid limits"
                self.set_user_warnings()
                return x, y, False

            try:
                x = np.linspace(min_x, max_x, 100)
                y = eval(function_x)
            except:
                self.error_messag = "error: enter a valid function"
                self.set_user_warnings()
                return x, y, False

            try:
                len(y)
            except:
                y = np.full(len(x), y)

        return x, y, valid

    def draw(self):
        x, y, valid = self.set_app_logic()
        if not valid:
            return

        self.axes.clear()
        self.axes.plot(x, y)
        self.axes.set_title("Plotter")
        self.canvas.draw()
        self.error_messag = None


def run():
    application = QApplication(sys.argv)
    window = Window()
    window.show()
    application.exec_()


if __name__ == "__main__":
    run()
