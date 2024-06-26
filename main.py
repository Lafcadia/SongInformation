from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtCore import Qt
import sys, os

# def BabyMode():
#     os.system('pip3 install mutagen')

QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Ceil)

def setSongInfo(songfilepath, songtitle, songartist, songalbum, songpicpath):
    audio = ID3(songfilepath)
    img = open(songpicpath,'rb')
    audio.update_to_v23() #把可能存在的旧版本升级为2.3
    audio['APIC'] = APIC( #插入专辑图片
                    encoding=3,
                    mime='image/jpeg',
                    type=3, 
                    desc=u'Cover',
                    data=img.read()
                )
    audio['TIT2'] = TIT2( #插入歌名
                    encoding=3,
                    text=[songtitle]
                )
    audio['TPE1'] = TPE1( #插入第一演奏家、歌手、等
                    encoding=3,
                    text=[songartist]
                )
    audio['TALB'] = TALB( #插入专辑名称
                    encoding=3,
                    text=[songalbum]
                )
    audio.save() #记得要保存
    img.close()



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.LoadJPG.clicked.connect(self.JPGloader)
        self.ui.LoadMP3.clicked.connect(self.MP3loader)
        self.ui.Start.clicked.connect(self.doer)
        
    def JPGloader(self):
        self.JPG = QtWidgets.QFileDialog.getOpenFileName(self,  "Load JPG","./", "All Files (*)")[0]
        self.ui.image.setPixmap(QPixmap(self.JPG))
    
    def MP3loader(self):
        self.MP3 = QtWidgets.QFileDialog.getOpenFileName(self,  "Load MP3","./", "All Files (*)")[0]
    
    def doer(self):
        SingerName = self.ui.SingerName.toPlainText()
        SongName = self.ui.SongName.toPlainText()
        AlbumName = self.ui.AlbumName.toPlainText()
        setSongInfo(self.MP3, SongName, SingerName, AlbumName, self.JPG)
        QMessageBox.information(self, "Done!","The file is overrided.")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())