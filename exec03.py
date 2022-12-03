#Program umożliwia użytkownikowi otwarcie obaz z dysku lokalnego i obejrzenie. Można zmieniać skalę

from PyQt6.QtCore import QDir
from PyQt6.QtGui import QAction, QImage, QPalette, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image = QImage()
        self.scaleFactor = 1.778

        self.imageViewer = QLabel()
        self.imageViewer.setBackgroundRole(QPalette.ColorRole.Base)
        mp = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageViewer.setSizePolicy(mp)
        self.imageViewer.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.ColorRole.Shadow)
        self.scrollArea.setWidget(self.imageViewer)
        self.setCentralWidget(self.imageViewer)

        openAct = QAction('&Otwórz...', self)
        openAct.triggered.connect(self.open)
        openAct.setShortcut('Ctrl+O')
        exitAct = QAction('&Zakończ', self)
        exitAct.triggered.connect(self.quit)
        exitAct.setShortcut('Ctrl+Q')

        fileMenu = QMenu('&Plik', self)
        fileMenu.addAction(openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        self.menuBar().addMenu(fileMenu)

        self.statusBar().showMessage('Wybierz obraz do obejrzenia')

        self.setWindowTitle('Przeglądarka obrazów')
        w = 800
        h = int(800 / self.scaleFactor)
        self.resize(w, h)

    def resizeEvent(self, event):
        if not self.image.isNull():
            self.updateView()

    def updateView(self):
        '''Obsługa zdarzenia zmiany rozmiaru okna zapewnia, że proporcje obrazu nie będą się zmieniać.'''
        if self.scaleFactor < 1:
            self.imageViewer.resize(int(self.height() * self.scaleFactor), self.height())
        else:
            self.imageViewer.resize(self.width(), round(int(self.width() / self.scaleFactor)))
        self.statusBar().showMessage(str(self.width()) + 'x' + str(self.height()))
        self.resize(self.imageViewer.width(), self.imageViewer.height())

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Wybierz obraz',
                                                  QDir.homePath(), 'Pliki obrazów (*.png *.xpm *.jpg *.bmp *.pdf)')
        if fileName:
            self.filename = fileName
            self.loadFile(self.filename)

    def loadFile(self, fileName):
        if self.filename:
            self.image = QImage(self.filename)
            if self.image.isNull():
                QMessageBox.information(self, 'Błąd',
                                        'Nie udało się załadować pliku')
                return
            self.imageViewer.setPixmap(QPixmap.fromImage(self.image))
            self.scaleFactor = int(self.image.width()) / int(self.image.height())
            f = round(self.scaleFactor, 3)
            self.statusBar().showMessage('Skala: ' + str(f), 3000)
            if self.scaleFactor < 1:
                self.resize(int(600 * self.scaleFactor), 600)
            else:
                self.resize(600, int(600 / self.scaleFactor))

    def quit(self):
        self.close()

app = QApplication([])
mainWindow = MainWindow()
mainWindow.show()
app.exec()