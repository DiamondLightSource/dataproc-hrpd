'''
GUI for rebinner
'''
try:
    import sip
    sip.setapi('QString', 2)
    from PyQt4.QtGui import QMainWindow, QApplication, QFileDialog, QStringListModel, QDialog, QProgressDialog, QErrorMessage
    from PyQt4.QtCore import Qt
except:
    from PySide.QtGui import QMainWindow, QApplication, QFileDialog, QStringListModel, QDialog, QProgressDialog, QErrorMessage
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
        base = self.getBaseDirectory(False)
        files, _selectedfilter = QFileDialog.getOpenFileNames(caption="Select scan files",
                                                              filter="Data files(*.dat)",
                                                              dir=base,
                                                              options=QFileDialog.ReadOnly)
        files = [ f for f in files if f not in self.scans ]
        self.scans.extend(files)
        self.scans_model.setStringList(self.scans)

    def deleteFiles(self):
        rows = sorted([ i.row() for i in self.scans_view.selectedIndexes() ])
        for r in reversed(rows):
            del self.scans[r]
        self.scans_model.setStringList(self.scans)

    def getYearAndVisit(self):
        year = None if self.year_combo.currentIndex() == 0 else self.year_combo.currentText()
        vtext = self.visit_edit.toPlainText()
        visit = vtext if vtext else None
        return year, visit

    def getBaseDirectory(self, processing=False, scans=None):
        import os.path as path
        base = None
        if scans:
            base = path.dirname(scans[0])
            if processing:
                base = path.join(base, 'processing')
            if not path.exists(base):
                base = None

        if base is None:
            year, visit = self.getYearAndVisit()
            base = mythen.DEFAULT_BL_DIR
            if year is not None:
                base = path.join(base, year)
                if visit is not None:
                    if processing:
                        base = path.join(base, visit, 'processing')
                    else:
                        base = path.join(base, visit)
        return base

    def addScanNumbers(self):
        result = self.range_dialog.exec_()
        if result == QDialog.Accepted:
            text = self.range_ui.range_edit.text()
            if text:
                not_found = []
                numbers = mythen.parse_range_list(text)
                year, visit = self.getYearAndVisit()
                progress = QProgressDialog("Locating scan files from numbers...", "Stop", 0, len(numbers), self)
                progress.setWindowModality(Qt.WindowModal)
                progress.forceShow()
                progress.setValue(0)
                for n in numbers:
                    progress.setValue(progress.value() + 1)
                    if progress.wasCanceled():
                        break
                    
                    files = mythen.find_mythen_files(n, visit=visit, year=year) # FIXME needs to be in separate thread(!)
                    if files:
                        files = [ f for f in files if f not in self.scans ]
                        self.scans.extend(files)
                        self.scans_model.setStringList(self.scans)
                    else:
                        not_found.append(n)

                progress.setValue(progress.maximum())

                if not_found:
                    error = QErrorMessage(self)
                    msg = "The following numbers were not found: "
                    for n in not_found:
                        msg = msg + str(n) + ", "
                    error.showMessage(msg[:-2])

    def processScans(self):
        base = self.getBaseDirectory(True, self.scans)
        out_file, _selectedfilter = QFileDialog.getSaveFileName(caption="Save rebinned scans",
                                                                dir=base,
                                                                options=QFileDialog.AnyFile)

        if not out_file:
            return

        progress = QProgressDialog("Process scans...", "Stop", 0, 2*len(self.scans), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.forceShow()
        progress.setValue(0)
        from mythen import load_all, process_and_save, report_processing
        data, files = load_all(self.scans, None, None, progress=progress)
        summed = True
        rebinned = True
        if self.rebin_rb.isChecked():
            summed = False
        elif self.sum_rb.isChecked():
            rebinned = False

        process_and_save(data, self.angle_spinbox.value(), self.delta_spinbox.value(),
                rebinned, summed, files, out_file, progress=progress, weights=self.weight_cb.isChecked())
        report_processing(files, out_file, self.angle_spinbox.value(), [self.delta_spinbox.value()])
        progress.setValue(progress.maximum())

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key_Delete or k == Qt.Key_Backspace:
            self.deleteFiles()

def main(args=None):
    if args is None:
        import sys
        args = sys.argv
    app = QApplication(args)
    frame = MainWindow()
    frame.show()
    app.exec_()
