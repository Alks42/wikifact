import random
import re
import requests
import webbrowser
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class MyButton(QtWidgets.QPushButton):

    def __init__(self, left, right):
        super(MyButton, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setStyleSheet("QPushButton {border : outset #2d63ad; "
                                         "border-width: 3px " + str(right) + "px 3px " + str(left) + "px;"
                                         "background-color : white;"
                                         "padding: 6px 6px 6px 6px;"
                                         "color: #2d63ad}"
                           "QPushButton:hover:enabled {background-color : #2d63ad;"
                                                                "color: white}"
                            "QPushButton:pressed {font-weight: bold;}")

        self.setFont((QtGui.QFont("Arial", 12)))


class Ui_MainWindow(QtWidgets.QMainWindow):

    # main window with all buttons and stuff

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.setMinimumSize(res_x, res_y)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, res_x, res_y))

        self.gridLayoutMain = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutMain.setSpacing(0)
        self.gridLayoutMain.setContentsMargins(0, 0, 0, 0)

        self.DisplayFact = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.DisplayFact.setReadOnly(True)
        self.gridLayoutMain.addWidget(self.DisplayFact, 1, 1, 1, 7)

        self.CategoryAddField = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.gridLayoutMain.addWidget(self.CategoryAddField, 3, 3, 1, 1)

        # buttons
        self.Url = MyButton(0, 0)  # blue link
        self.gridLayoutMain.addWidget(self.Url, 2, 1, 1, 7)
        self.UrlFull = ""

        self.More = MyButton(3, 3)
        self.gridLayoutMain.addWidget(self.More, 3, 1, 1, 2)

        self.CategoryAddButton = MyButton(3, 3)
        self.gridLayoutMain.addWidget(self.CategoryAddButton, 3, 4, 1, 1)

        self.Show = MyButton(0, 3)
        self.gridLayoutMain.addWidget(self.Show, 3, 5, 1, 1)

        self.Save = MyButton(0, 3)
        self.gridLayoutMain.addWidget(self.Save, 3, 6, 1, 1)

        self.open_saved_urls = MyButton(0, 3)
        self.gridLayoutMain.addWidget(self.open_saved_urls, 3, 7, 1, 1)

        # Field with categories and delete button

        self.Delete = MyButton(3, 3)

        self.Frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.CatsLayout = QtWidgets.QGridLayout()
        self.CatsLayout.setSpacing(0)
        self.CatsLayout.setContentsMargins(0, 0, 0, 0)
        self.Frame.setLayout(self.CatsLayout)
        self.gridLayoutMain.addWidget(self.Frame, 4, 1, 1, 7)
        self.Frame.hide()

        self.state = 0

        self.setCentralWidget(self.gridLayoutWidget)

        self.setupCats()
        self.setupUi()
        self.logic()

    def setupCats(self):

        # setup ui of frame with categories:
        # clearing layout

        if self.CatsLayout.count() > 0:
            for child in self.Frame.children():
                if child != self.CatsLayout:
                    child.setParent(None)

        # reading or creating file with categories

        with open(filename, "a+") as f:
            f.seek(0)
            self.cats = f.readline().split(";")

        if self.cats == [""]:
            self.CatsLayout.addWidget(self.Delete, 0, 0, 1, 4)
            return

        # and setting checkboxes & delete button for categories

        self.checkers = []
        n = 0
        m = 0
        for cat in self.cats:
            check = QtWidgets.QCheckBox()
            check.setStyleSheet("background-color: white; border: 0px outset; padding: 6px 0px 6px 6px;")
            check.setFont((QtGui.QFont("Arial", 14)))
            check.setCheckState(2)
            check.setText(cat)
            self.checkers.append(check)
            self.CatsLayout.addWidget(check, m, n, 1, 1)
            n += 1
            if n > 3:
                n = 0
                m += 1

        self.CatsLayout.addWidget(self.Delete, m + 1, 0, 1, 4)

    def setupUi(self):

        # setting text, fonts etc

        self.setWindowTitle("WikiFact")
        self.setWindowIcon(QtGui.QIcon("wikifact.ico"))
        self.setAutoFillBackground(True)
        self.setStyleSheet("QMainWindow {background-color: white;}"
                           "QPlainTextEdit {selection-background-color: #3a7bd5}"
                           "QMenu {background-color: #F2F2F2;} QMenu::item::selected{ color: blue;}"
                           "QMessageBox {background-color: #F2F2F2;}")

        self.More.setText("   More   ")
        self.CategoryAddButton.setText("   Add field   ")
        self.Save.setText("Save")
        self.Show.setText("Show")
        self.open_saved_urls.setText("Links")
        self.CategoryAddField.setStyleSheet("border: outset #3a7bd5; border-width: 3px 0px 3px 0px")
        self.CategoryAddField.setFixedHeight(50)

        self.DisplayFact.setFont((QtGui.QFont("Times New Roman", 14)))
        self.DisplayFact.setStyleSheet("border: none")
        self.CategoryAddField.setFont((QtGui.QFont("Times New Roman", 14)))

        self.Delete.setText("Delete selected")
        self.Delete.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.Url.setFont((QtGui.QFont("Times New Roman", 10)))
        self.Url.setMinimumHeight(40)
        self.Url.setStyleSheet("background-color: white; border-style: outset; color: blue;")
        self.Url.setCursor(QtCore.Qt.PointingHandCursor)

    def logic(self):

        # connecting buttons to functions

        self.More.clicked.connect(self.getFact)
        self.CategoryAddButton.clicked.connect(self.addCategory)
        self.Url.clicked.connect(lambda x: webbrowser.open(self.UrlFull))
        self.Save.clicked.connect(self.save)
        self.Delete.clicked.connect(self.deleteCategory)
        self.Show.clicked.connect(self.showCategories)
        self.open_saved_urls.clicked.connect(lambda x: os.startfile("saved_urls.txt"))

    def getFact(self):

        self.Save.setEnabled(True)
        self.Save.setText("Save")

        if self.cats != [""]:
            self.DisplayFact.setPlainText("Connecting...")
            self.process = Process()
            self.process.start()
            self.process.update.connect(self.display)
        else:
            self.DisplayFact.setPlainText("Categories not found!")

    def display(self, args):

        # display text sent by process thread

        self.DisplayFact.setPlainText(args[0])
        if len(args) > 1:
            self.UrlFull = args[1]
            self.Url.setText(args[2])

    def save(self):

        # save current fact in file with link button

        if self.UrlFull != "":
            with open("saved_urls.txt", "ab") as f:
                f.write(str(self.DisplayFact.toPlainText()[:142] + "... - " + "\n" + self.UrlFull
                            + "\n***\n").encode("utf-8"))

            self.Save.setEnabled(False)
            self.Save.setText("Saved")

    def addCategory(self):

        if self.CategoryAddField.toPlainText() != "":
            to_add = self.CategoryAddField.toPlainText()

            # check if there is any page from the category. If category don't exist it will return Undefined Index
            # sometimes too many requests will lead to wikipedia/User_talk:Magnus_Manske page

            if to_add not in self.cats:
                url = "http://tools.wmflabs.org/magnustools/randomarticle.php"

                params = {
                    "lang": lang,
                    "project": "wikipedia",
                    "categories": to_add,
                }
                self.DisplayFact.setPlainText("Wait...")
                req = requests.get(url=url, params=params).text

                if "/User_talk:Magnus_Manske" in req:
                    self.DisplayFact.setPlainText("Something went wrong. Try again.")
                    return

                if "Undefined index" not in req:
                    with open(filename, "a+") as f:
                        f.seek(0)
                        if not f.read():
                            f.write(to_add)
                        else:
                            f.write(";" + to_add)

                    self.DisplayFact.setPlainText("ADDED")
                    self.CategoryAddField.setPlainText("")

                    self.setupCats()

                else:
                    self.DisplayFact.setPlainText("NO CATEGORY FOUND")

            else:
                self.DisplayFact.setPlainText("ADDED")

    def showCategories(self):

        # This is probably awful way to keep window size
        if self.state == 0:
            self.Frame.show()
            self.state = 1

            if self.isMaximized() == 0:
                self.resize(self.width(), self.height() + self.Frame.height())
                self.More.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
                self.More.setFocus()

        else:
            if self.isMaximized() == 0:
                self.resize(self.width(), self.height() - self.Frame.height())
            self.Frame.hide()
            self.state = 0

    def deleteCategory(self):

        if self.cats == [""]:
            return

        conf = QtWidgets.QMessageBox.question(self, 'Acceptance', "Are you sure?",
                                              QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if conf == QtWidgets.QMessageBox.No:
            return

        cats = []
        for check in self.checkers:
            if check.checkState() == 0:
                cats.append(check.text())

        if len(cats) > 0 and len(cats) != len(self.cats):
            with open(filename, "w") as f:
                f.write(cats[0])
                for i in range(1, len(cats)):
                    f.write(";" + cats[i])
            self.setupCats()

        elif len(cats) == 0:
            with open(filename, "w") as f:
                f.write("")
            self.setupCats()


class Process(QtCore.QThread):
    update = QtCore.pyqtSignal(list)

    def run(self):

        cats = []
        for check in ui.checkers:
            if check.checkState() == 2:
                cats.append(check.text())

        if len(cats) == 0:
            self.update.emit(["Select at least one category!"])
            return

        category = random.choice(cats)

        url = "http://tools.wmflabs.org/magnustools/randomarticle.php"

        params = {
            "lang": lang,
            "project": "wikipedia",
            "categories": category,
            "namespace": "0",
            "d": depth,
        }

        while True:  # to avoid short summaries (less than 200 chars) like Heart is an animal organ for pumping blood
            req = requests.get(url=url, params=params).text

            title = re.search("wiki/.*?>", req).group(0)[5:-2]
            self.update.emit(["Wait..."])

            if title != "User_talk:Magnus_Manske":  # smt many requests will lead to wikipedia/User_talk:Magnus_Manske
                req = requests.get(
                    "https://" + lang + ".wikipedia.org/api/rest_v1/page/summary/" + title + "?redirect=true").json()

                if len(req["extract"]) > 200:
                    self.update.emit([req["extract"], req["content_urls"]["desktop"]["page"],
                                      req["content_urls"]["desktop"]["page"][:50]])
                    break

            else:
                self.update.emit(["Something went wrong. Try again."])
                break


if __name__ == "__main__":
    with open("config.txt") as f:
        params = f.readlines()

    res_x = int(params[0].split(" ")[1])
    res_y = int(params[0].split(" ")[2])
    lang = params[1].split(" ")[1].rstrip()
    depth = params[2].split(" ")[1].rstrip()
    filename = lang + "_categories.txt"

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()

    ui.show()
    ui.getFact()
    sys.exit(app.exec_())
