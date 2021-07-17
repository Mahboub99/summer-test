from plotter import Window
from PySide2 import QtCore
import pytest


@pytest.fixture
def app(qtbot):
    tester = Window()
    tester.show_error_alert = False
    qtbot.addWidget(tester)
    return tester


def test_empty(app, qtbot):
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: All fileds are required"

    app.function_x.setText("5*X^2+3*X")
    app.min_x.setText("-20")
    app.max_x.setText("")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: All fileds are required"

    app.function_x.setText("5*X^2+3*X")
    app.min_x.setText("")
    app.max_x.setText("20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: All fileds are required"

    app.function_x.setText("")
    app.min_x.setText("-20")
    app.max_x.setText("20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: All fileds are required"


def test_invalid_function(app, qtbot):
    app.function_x.setText("5*y^2+2*x")
    app.min_x.setText("-20")
    app.max_x.setText("20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: enter a valid function"

    app.function_x.setText("y")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: you have to use only numbers , variable x and supported operators[+ - / * ^]"


def test_invalid_limits(app, qtbot):
    app.function_x.setText("5*X^2+2%x")

    app.min_x.setText("test")
    app.max_x.setText("20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: enter valid lower limmit"

    app.min_x.setText("-20")
    app.max_x.setText("test")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error:enter valid upper limmit"

    
    app.min_x.setText("20")
    app.max_x.setText("-20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == "error: Lower limit must be less than the upper limit"



def test_valid_function_1(app, qtbot):
    app.function_x.setText("5*X^2")
    app.min_x.setText("-20")
    app.max_x.setText("20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == None


def test_valid_function_2(app, qtbot):
    app.function_x.setText("20^X+50*x+40")
    app.min_x.setText("-20")
    app.max_x.setText("20")
    qtbot.mouseClick(app.plot_button, QtCore.Qt.LeftButton)
    assert app.error_messag == None

