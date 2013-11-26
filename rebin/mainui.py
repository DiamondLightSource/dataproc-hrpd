'''
GUI for rebinner
'''
from PySide.QtGui import QMainWindow, QApplication, QFileDialog, QStringListModel, QDialog
from PySide.QtCore import Qt

from mythenui import Ui_mythen_gui

from rangeui import Ui_range_dialog

import mythen

# TODO
# add drop handling
# 
class MainWindow(QMainWindow, Ui_mythen_gui):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.add_scans.clicked.connect(self.addScanFiles)
        self.delete_selection.clicked.connect(self.deleteFiles)
        self.add_scan_numbers.clicked.connect(self.addScanNumbers)
        self.process.clicked.connect(self.processScans)
        self.scans = []
        self.scans_model = QStringListModel(self.scans, self.scans_view)
        self.scans_view.setModel(self.scans_model)
        self.scans_view.setAcceptDrops(True)

        # add years to combo
        from time import localtime
        tm = localtime()
        for i in range(tm.tm_year, 2006, -1):
            self.year_combo.addItem(str(i))

        # range dialog
        self.range_dialog = QDialog()
        self.range_ui = Ui_range_dialog()
        self.range_ui.setupUi(self.range_dialog)

    def addScanFiles(self):
        files, _selectedfilter = QFileDialog.getOpenFileNames(caption="Select scan files",
                                                              filter="Data files(*.dat)",
                                                              options=QFileDialog.ReadOnly)
        
        self.scans.extend(files)
        self.scans_model.setStringList(self.scans)
        
    def deleteFiles(self):
        rows = sorted([ i.row() for i in self.scans_view.selectedIndexes() ])
        for r in reversed(rows):
            del self.scans[r]
        self.scans_model.setStringList(self.scans)

    def addScanNumbers(self):
        result = self.range_dialog.exec_()
        if result == QDialog.Accepted:
            text = self.range_ui.range_edit.text()
            if text:
                not_found = []
                numbers = mythen.parse_range_list(text)
                vtext = self.visit_edit.toPlainText()
                visit = vtext if vtext else None
                year = None if self.year_combo.currentIndex() == 0 else self.year_combo.currentText()
                for n in numbers:
                    files = mythen.find_mythen_files(n, visit=visit, year=year)
                    if files:
                        self.scans.extend(files)
                        self.scans_model.setStringList(self.scans)
                    else:
                        not_found.append(n)
                if not_found:
                    print("The following numbers were not found:", not_found)

    def processScans(self):
        out_file, _selectedfilter = QFileDialog.getSaveFileName(caption="Save rebinned scans",
                                                              options=QFileDialog.AnyFile)
        from mythen import load_all, process_and_save
        data, files = load_all(self.scans, None, None)
        summed = True
        if self.rebin_rb.isChecked():
            summed = False
        elif self.sum_rb.isChecked():
            files = None

        process_and_save(data, self.angle_spinbox.value(), self.delta_spinbox.value(), summed, files, out_file)

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key_Delete or k == Qt.Key_Backspace:
            self.deleteFiles()

def main(args):
    app = QApplication(args)
    frame = MainWindow()
    frame.show()
    app.exec_()
