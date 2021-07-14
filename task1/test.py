from PySide2 import QtCore
from plotter import Window
import pytest


@pytest.fixture
def app(qtbot):
    tester = Window()
    tester.show_err = False
    qtbot.addWidget(tester)
    return tester


def empty_test(app, qtbot):
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "All fileds are required"

    app.f_x.setText("5*X^2+3*X")
    app.min_x.setText("-10")
    app.max_x.setText("")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "All fileds are required"

    app.f_x.setText("5*X^2+3*X")
    app.min_x.setText("")
    app.max_x.setText("10")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "All fileds are required"

    app.f_x.setText("")
    app.min_x.setText("-10")
    app.max_x.setText("10")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "error: All fileds are required"


def invalid_function(app, qtbot):
    app.f_x.setText("5*y^2+2*x")
    app.min_x.setText("-10")
    app.max_x.setText("10")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "error: enter a valid function"

    app.f_x.setText("y")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "error: Only numbers, operators (+, -, *, /) and the variable x are allowed"


def invalid_limits(app, qtbot):
    app.f_x.setText("5*X^2+2%x")

    app.min_x.setText("test")
    app.max_x.setText("20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "error: enter valid limits"

    app.min_x.setText("--20")
    app.max_x.setText("20test")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == "error: enter valid limit numbers"


def valid_function_1(app, qtbot):
    app.f_x.setText("5*X^2")
    app.min_x.setText("-10")
    app.max_x.setText("10")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == None


def valid_function_2(app, qtbot):
    app.f_x.setText("20^X+50*x+40")
    app.min_x.setText("-10")
    app.max_x.setText("10")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.err == None

