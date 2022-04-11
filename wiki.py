import random
import re
import requests
import webbrowser
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class MyButton(QtWidgets.QPushButton):

    def __init__(self):
        super(MyButton, self).__init__()
        self.setFont((QtGui.QFont("Arial", 14)))


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

        # buttons

        self.More = MyButton()
        self.gridLayoutMain.addWidget(self.More, 3, 1, 1, 2)

        self.CategoryAddField = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.gridLayoutMain.addWidget(self.CategoryAddField, 3, 3, 1, 1)

        self.CategoryAddButton = MyButton()
        self.gridLayoutMain.addWidget(self.CategoryAddButton, 3, 4, 1, 1)

        self.Url = MyButton()   # the one with blue link
        self.gridLayoutMain.addWidget(self.Url, 2, 1, 1, 7)
        self.UrlFull = ""

        self.open_saved_urls = MyButton()
        self.gridLayoutMain.addWidget(self.open_saved_urls, 3, 7, 1, 1)

        self.Save = MyButton()
        self.gridLayoutMain.addWidget(self.Save, 3, 6, 1, 1)

        self.Show = MyButton()
        self.gridLayoutMain.addWidget(self.Show, 3, 5, 1, 1)

        # Field with categories and delete button

        self.Delete = MyButton()

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

        # reading or editing file with categories

        if os.path.isfile(filename):
            with open(filename) as f:
                self.cats = f.readline().split(";")

        if not os.path.isfile(filename) or self.cats == [""]:
            with open(filename, "w") as f:
                f.write(def_cat)
            self.cats = [def_cat]

        # and setting checkboxes for categories

        self.checkers = []
        n = 0
        m = 0
        for cat in self.cats:
            check = QtWidgets.QCheckBox()
            check.setStyleSheet("background-color: white; border: 1px solid; color: Black; padding: 6px 6px 6px 6px;")
            check.setFont((QtGui.QFont("Arial", 14)))
            check.setCheckState(2)
            check.setText(cat)
            self.checkers.append(check)
            self.CatsLayout.addWidget(check, m, n, 1, 1)
            n += 1
            if n > 3:
                n = 0
                m += 1

        self.CatsLayout.addWidget(self.Delete, m, n, 1, 4 - n)

    def setupUi(self):

        # setting all text, fonts etc

        self.setWindowTitle("WikiFact")
        self.setWindowIcon(QtGui.QIcon("wikifact.png"))

        self.More.setText("More")
        self.CategoryAddButton.setText("Add field")
        self.CategoryAddButton.setMinimumWidth(180)
        self.Save.setText("Save")
        self.Show.setText("Show")
        self.open_saved_urls.setText("Links")
        self.CategoryAddField.setFixedSize(250, 40)

        self.DisplayFact.setFont((QtGui.QFont("Times New Roman", 14)))
        self.DisplayFact.setStyleSheet("border: none")
        self.CategoryAddField.setFont((QtGui.QFont("Times New Roman", 12)))

        self.Delete.setText("Delete selected")

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
        self.DisplayFact.setPlainText("Connecting...")

        self.Save.setEnabled(True)
        self.Save.setText("Save")

        self.process = Process()
        self.process.start()
        self.process.update.connect(self.display)

    def display(self, args):

        # display text sent by process thread

        self.DisplayFact.setPlainText(args[0])
        if len(args) > 1:
            self.UrlFull = args[1]
            self.Url.setText(args[2])

    def save(self):

        # save current fact in file with link

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
            # sometimes too many requests will lead to WinError or to wikipedia/User_talk:Magnus_Manske page

            if to_add not in self.cats:
                url = "http://tools.wmflabs.org/magnustools/randomarticle.php"

                params = {
                    "lang": lang,
                    "project": "wikipedia",
                    "categories": to_add,
                }

                while True:
                    try:
                        req = requests.get(url=url, params=params).text
                        break
                    except WindowsError:
                        pass

                if "/User_talk:Magnus_Manske" in req:
                    self.DisplayFact.setPlainText("Something went wrong. Try again.")
                    return

                if "Undefined index" not in req:
                    with open(filename, "a") as f:
                        f.write(";" + to_add)

                    self.DisplayFact.setPlainText("ADDED!")
                    self.CategoryAddField.setPlainText("")

                    self.setupCats()

                else:
                    self.DisplayFact.setPlainText("NO SUCH CATEGORY")

            else:
                self.DisplayFact.setPlainText("ALREADY IN")

    def showCategories(self):

        if self.state == 0:
            self.Frame.show()
            self.state = 1

            if self.isMaximized() == 0:
                self.resize(self.width(), self.height() + self.Frame.height())

        else:
            if self.isMaximized() == 0:
                self.resize(self.width(), self.height() - self.Frame.height())
            self.Frame.hide()
            self.state = 0

    def deleteCategory(self):

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

        # sometimes too many requests will lead to WinError or to wikipedia/User_talk:Magnus_Manske page

        while True:
            try:
                req = requests.get(url=url, params=params).text

                title = re.search("wiki/.*?>", req).group(0)[5:-2]
                self.update.emit(["Wait..."])

                if title != "User_talk:Magnus_Manske":
                    req = requests.get(
                        "https://" + lang + ".wikipedia.org/api/rest_v1/page/summary/" + title + "?redirect=true").json()

                    if len(req["extract"]) > 200:
                        self.update.emit([req["extract"], req["content_urls"]["desktop"]["page"],
                                          req["content_urls"]["desktop"]["page"][:50]])
                        break

                else:
                    self.update.emit(["Something went wrong. Try again."])
                    break

            except WindowsError:
                self.update.emit(["Something went wrong. Try again."])


if __name__ == "__main__":

    with open("config.txt") as f:
        params = f.readlines()

    res_x = int(params[0].split(" ")[1])
    res_y = int(params[0].split(" ")[2])
    lang = params[1].split(" ")[1].rstrip()
    def_cat = params[2].split(" ")[1].rstrip()
    depth = params[3].split(" ")[1].rstrip()
    filename = lang + "_categories.txt"

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()

    ui.show()
    ui.getFact()
    sys.exit(app.exec_())
