from DLP_program import *
from control_GUI import *
from android import *
from common_func import *
import threading

from PyQt5.QtWidgets import *
from control_GUI import Ui_MainWindow


class kwinwriter(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

def run():
    app = QApplication([])
    main_dialog = kwinwriter()
    QApplication.processEvents()
    app.exit(app.exec_())


t1 = threading.Thread(target=dlp_program_open, daemon=True)
t3 = threading.Thread(target=run)

t1.start()
t3.start()
t1.join()
t3.join()

