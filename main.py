import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QPushButton, QFileDialog,
                             QVBoxLayout, QWidget,
                             QMessageBox, QDesktopWidget)
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from AutoPlot import plotter


class CsvPlotterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CSV Plotter')

        self.setMinimumSize(400, 200)
        self.setMaximumSize(600, 400)

        self.setGeometry(100, 100, 300, 150)
        self.app_center()

        # 主窗口的布局
        layout = QVBoxLayout()

        # 导入CSV文件按钮
        self.importCsvBtn = QPushButton('Input the .csv file 导入 CSV 文件', self)
        self.importCsvBtn.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: #F0F0F0;
                border: 2px solid #AAADB6;
                padding: 15px; /*增加内边距*/
                font-size: 16px; /*字体大小，根据需要调整*/
                font-weight: bold;
                color: black; /*字体颜色，根据需要调整*/
            }
            QPushButton:hover {
                background-color: #D4E2FF;
                border: 2px solid #3574F0;
            }
        """)

        self.importCsvBtn.clicked.connect(self.importCsv)
        layout.addWidget(self.importCsvBtn)

        # 选择导出文件夹的按钮
        self.exportFolderBtn = QPushButton('Choose the output folder选择导出文件夹', self)
        self.exportFolderBtn.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: #F0F0F0;
                border: 2px solid #AAADB6;
                padding: 15px; /*增加内边距*/
                font-size: 16px; /*字体大小，根据需要调整*/
                font-weight: bold;
                color: black; /*字体颜色，根据需要调整*/
            }
            QPushButton:hover {
                background-color: #D4E2FF;
                border: 2px solid #3574F0;
            }
        """)
        self.exportFolderBtn.clicked.connect(self.selectExportFolder)
        layout.addWidget(self.exportFolderBtn)

        # 确定按钮
        self.plotBtn = QPushButton('Confirm 确定', self)
        self.plotBtn.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: #F0F0F0;
                border: 2px solid #AAADB6;
                padding: 15px; /*增加内边距*/
                font-size: 16px; /*字体大小，根据需要调整*/
                font-weight: bold;
                color: black; /*字体颜色，根据需要调整*/
            }
            QPushButton:hover {
                background-color: #D4E2FF;
                border: 2px solid #3574F0;
            }
        """)
        self.plotBtn.clicked.connect(self.plot)
        layout.addWidget(self.plotBtn)

        # 中央小部件
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 用于存储文件路径和导出路径的变量
        self.file_path = ''
        self.export_path = ''

    def app_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def importCsv(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Input the .csv file 导入 CSV 文件", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            self.file_path = fileName

    def selectExportFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose the output folder 选择导出文件夹")
        if folder:
            self.export_path = folder

    def plot(self):
        if self.file_path:
            plotter(self.file_path, self.export_path)
            QMessageBox.information(self, "Finished 完成", "Plot successfully 绘图成功")
        else:
            print("PLease input the .csv file first! 请先导入CSV文件！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CsvPlotterApp()
    mainWindow.show()
    sys.exit(app.exec_())