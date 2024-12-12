# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mythen.ui'
#
# Created: Sat Nov  9 20:19:59 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from customui import DropListView

try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PySide import QtCore, QtGui


class Ui_mythen_gui(object):
    def setupUi(self, mythen_gui):
        mythen_gui.setObjectName("mythen_gui")
        mythen_gui.resize(640, 422)
        self.centralwidget = QtGui.QWidget(mythen_gui)
        self.centralwidget.setObjectName("centralwidget")
        self.parameter_group = QtGui.QGroupBox(self.centralwidget)
        self.parameter_group.setGeometry(QtCore.QRect(380, 170, 241, 111))
        self.parameter_group.setObjectName("parameter_group")
        self.angle_spinbox = QtGui.QDoubleSpinBox(self.parameter_group)
        self.angle_spinbox.setGeometry(QtCore.QRect(90, 30, 62, 31))
        self.angle_spinbox.setDecimals(3)
        self.angle_spinbox.setMaximum(180.0)
        self.angle_spinbox.setObjectName("angle_spinbox")
        self.delta_spinbox = QtGui.QDoubleSpinBox(self.parameter_group)
        self.delta_spinbox.setGeometry(QtCore.QRect(90, 70, 62, 31))
        self.delta_spinbox.setDecimals(3)
        self.delta_spinbox.setMaximum(1.0)
        self.delta_spinbox.setSingleStep(0.001)
        self.delta_spinbox.setProperty("value", 0.001)
        self.delta_spinbox.setObjectName("delta_spinbox")
        self.label = QtGui.QLabel(self.parameter_group)
        self.label.setGeometry(QtCore.QRect(10, 40, 57, 14))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.parameter_group)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 57, 14))
        self.label_2.setObjectName("label_2")
        self.dls_group = QtGui.QGroupBox(self.centralwidget)
        self.dls_group.setGeometry(QtCore.QRect(380, 20, 241, 141))
        self.dls_group.setObjectName("dls_group")
        self.label_3 = QtGui.QLabel(self.dls_group)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 57, 14))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(self.dls_group)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 57, 14))
        self.label_4.setObjectName("label_4")
        self.visit_edit = QtGui.QTextEdit(self.dls_group)
        self.visit_edit.setGeometry(QtCore.QRect(90, 20, 104, 31))
        self.visit_edit.setAcceptRichText(False)
        self.visit_edit.setObjectName("visit_edit")
        self.add_scan_numbers = QtGui.QPushButton(self.dls_group)
        self.add_scan_numbers.setGeometry(QtCore.QRect(40, 110, 141, 25))
        self.add_scan_numbers.setObjectName("add_scan_numbers")
        self.year_combo = QtGui.QComboBox(self.dls_group)
        self.year_combo.setGeometry(QtCore.QRect(90, 70, 83, 29))
        self.year_combo.setObjectName("year_combo")
        self.year_combo.addItem("")
        self.scan_group = QtGui.QGroupBox(self.centralwidget)
        self.scan_group.setGeometry(QtCore.QRect(20, 20, 331, 371))
        self.scan_group.setObjectName("scan_group")
        self.scans_view = DropListView(self.scan_group)
        self.scans_view.setGeometry(QtCore.QRect(10, 30, 311, 271))
        self.scans_view.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.scans_view.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.scans_view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.scans_view.setObjectName("scans_view")
        self.add_scans = QtGui.QPushButton(self.scan_group)
        self.add_scans.setGeometry(QtCore.QRect(10, 320, 131, 31))
        self.add_scans.setObjectName("add_scans")
        self.delete_selection = QtGui.QPushButton(self.scan_group)
        self.delete_selection.setGeometry(QtCore.QRect(190, 320, 131, 31))
        self.delete_selection.setObjectName("delete_selection")
        self.output_group = QtGui.QGroupBox(self.centralwidget)
        self.output_group.setGeometry(QtCore.QRect(380, 280, 241, 121))
        self.output_group.setObjectName("output_group")
        self.rebin_rb = QtGui.QRadioButton(self.output_group)
        self.rebin_rb.setGeometry(QtCore.QRect(10, 30, 109, 26))
        self.rebin_rb.setObjectName("rebin_rb")
        self.sum_rb = QtGui.QRadioButton(self.output_group)
        self.sum_rb.setGeometry(QtCore.QRect(10, 60, 109, 26))
        self.sum_rb.setObjectName("sum_rb")
        self.both_rb = QtGui.QRadioButton(self.output_group)
        self.both_rb.setGeometry(QtCore.QRect(10, 90, 109, 26))
        self.both_rb.setChecked(True)
        self.both_rb.setObjectName("both_rb")
        self.process = QtGui.QPushButton(self.output_group)
        self.process.setGeometry(QtCore.QRect(130, 40, 91, 71))
        self.process.setObjectName("process")
        self.weight_cb = QtGui.QCheckBox(self.output_group)
        self.weight_cb.setGeometry(QtCore.QRect(110, 10, 131, 22))
        self.weight_cb.setObjectName("weight_cb")
        mythen_gui.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(mythen_gui)
        self.statusbar.setObjectName("statusbar")
        mythen_gui.setStatusBar(self.statusbar)

        self.retranslateUi(mythen_gui)
        QtCore.QMetaObject.connectSlotsByName(mythen_gui)

    def retranslateUi(self, mythen_gui):
        mythen_gui.setWindowTitle(
            QtGui.QApplication.translate(
                "mythen_gui",
                "Mac/Mythen Rebinner",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.parameter_group.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "<html><head/><body><p>Count data is rebinned into larger angle bins specified by the leading edge value (start) and the width (size) in units of degrees</p></body></html>",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.parameter_group.setTitle(
            QtGui.QApplication.translate(
                "mythen_gui",
                "Bin angle parameters (degrees)",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.label.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Start", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.label_2.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Size", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.dls_group.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "<html><head/><body><p>Diamond Light Source specific information</p></body></html>",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.dls_group.setTitle(
            QtGui.QApplication.translate(
                "mythen_gui", "DLS info", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.label_3.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Visit ID", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.label_4.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Year", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.visit_edit.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "<html><head/><body><p>A visit ID is a combination of two letters (village), four numbers (proposal) followed by a dash and a visit number in a year (eg. &quot;cm1234-2&quot;). Leave empty for all visits</p></body></html>",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.add_scan_numbers.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "<html><head/><body><p>Add to list of scan files using given scan numbers and visit information</p></body></html>",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.add_scan_numbers.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Add scans...", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.year_combo.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "<html><head/><body><p>Year of visit</p></body></html>",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.year_combo.setItemText(
            0,
            QtGui.QApplication.translate(
                "mythen_gui", "All years", None, QtGui.QApplication.UnicodeUTF8
            ),
        )
        self.scan_group.setTitle(
            QtGui.QApplication.translate(
                "mythen_gui", "Scan files", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.scans_view.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui", "List of scan files", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.add_scans.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Sans Serif\'; font-size:9pt;">Add scan files to list from file selector</span></p></body></html>',
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.add_scans.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Add files...", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.delete_selection.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "<html><head/><body><p>Delete selected files from list</p></body></html>",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.delete_selection.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Delete", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.output_group.setTitle(
            QtGui.QApplication.translate(
                "mythen_gui", "Output", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.rebin_rb.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Rebin only", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.sum_rb.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Sum only", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.both_rb.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "Both", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.process.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "<html><head/><body><p>Rebin the count data from the given scan files according to the bin parameters set and save as indicted using chosen directory and summarise in chosen filename</p></body></html>",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.process.setText(
            QtGui.QApplication.translate(
                "mythen_gui",
                "Process\n" "and\n" "save...",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.weight_cb.setToolTip(
            QtGui.QApplication.translate(
                "mythen_gui",
                "Include weight (number of bins used) as 4th column of output",
                None,
                QtGui.QApplication.UnicodeUTF8,
            )
        )
        self.weight_cb.setText(
            QtGui.QApplication.translate(
                "mythen_gui", "include weight", None, QtGui.QApplication.UnicodeUTF8
            )
        )
