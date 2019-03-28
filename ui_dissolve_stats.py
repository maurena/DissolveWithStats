# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dissolve_stats.ui'
#
# Created: Thu Aug 28 13:10:26 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DissolveWithStats(object):
    def setupUi(self, DissolveWithStats):
        DissolveWithStats.setObjectName(_fromUtf8("DissolveWithStats"))
        DissolveWithStats.resize(468, 548)
        self.labelLayerList = QtWidgets.QLabel(DissolveWithStats)
        self.labelLayerList.setGeometry(QtCore.QRect(30, 20, 211, 17))
        self.labelLayerList.setObjectName(_fromUtf8("labelLayerList"))
        self.labelFieldList = QtWidgets.QLabel(DissolveWithStats)
        self.labelFieldList.setGeometry(QtCore.QRect(30, 100, 211, 17))
        self.labelFieldList.setObjectName(_fromUtf8("labelFieldList"))
        self.comboLayerList = QtWidgets.QComboBox(DissolveWithStats)
        self.comboLayerList.setGeometry(QtCore.QRect(30, 50, 401, 27))
        self.comboLayerList.setObjectName(_fromUtf8("comboLayerList"))
        self.comboFieldList = QtWidgets.QComboBox(DissolveWithStats)
        self.comboFieldList.setGeometry(QtCore.QRect(30, 130, 401, 27))
        self.comboFieldList.setEditable(False)
        self.comboFieldList.setObjectName(_fromUtf8("comboFieldList"))
        self.buttonBox = QtWidgets.QDialogButtonBox(DissolveWithStats)
        self.buttonBox.setGeometry(QtCore.QRect(260, 500, 176, 27))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.outButton = QtWidgets.QToolButton(DissolveWithStats)
        self.outButton.setGeometry(QtCore.QRect(340, 450, 91, 25))
        self.outButton.setObjectName(_fromUtf8("outButton"))
        self.outShape = QtWidgets.QLineEdit(DissolveWithStats)
        self.outShape.setEnabled(True)
        self.outShape.setGeometry(QtCore.QRect(30, 450, 291, 27))
        self.outShape.setObjectName(_fromUtf8("outShape"))
        self.labelOutput = QtWidgets.QLabel(DissolveWithStats)
        self.labelOutput.setGeometry(QtCore.QRect(30, 420, 211, 17))
        self.labelOutput.setObjectName(_fromUtf8("labelOutput"))
        self.labelFieldTable = QtWidgets.QLabel(DissolveWithStats)
        self.labelFieldTable.setGeometry(QtCore.QRect(30, 180, 261, 17))
        self.labelFieldTable.setObjectName(_fromUtf8("labelFieldTable"))
        self.tableFields = QtWidgets.QTableWidget(DissolveWithStats)
        self.tableFields.setGeometry(QtCore.QRect(30, 210, 401, 192))
        self.tableFields.setRowCount(0)
        self.tableFields.setColumnCount(4)
        self.tableFields.setObjectName(_fromUtf8("tableFields"))
        self.checkBoxAddFile = QtWidgets.QCheckBox(DissolveWithStats)
        self.checkBoxAddFile.setGeometry(QtCore.QRect(30, 500, 221, 22))
        self.checkBoxAddFile.setChecked(True)
        self.checkBoxAddFile.setObjectName(_fromUtf8("checkBoxAddFile"))

        self.retranslateUi(DissolveWithStats)
        self.comboFieldList.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(DissolveWithStats)

    def retranslateUi(self, DissolveWithStats):
        DissolveWithStats.setWindowTitle(QtWidgets.QApplication.translate("DissolveWithStats", "Dissolve with stats", None))
        self.labelLayerList.setToolTip(QtWidgets.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Choose a layer to dissolve</p></body></html>", None))
        self.labelLayerList.setText(QtWidgets.QApplication.translate("DissolveWithStats", "Choose a layer to dissolve :", None))
        self.labelFieldList.setToolTip(QtWidgets.QApplication.translate("DissolveWithStats", "<html><head/><body><p>All the geometries with the same value for this field will be merged together</p></body></html>", None))
        self.labelFieldList.setText(QtWidgets.QApplication.translate("DissolveWithStats", "Choose a dissolve field :", None))
        self.outButton.setText(QtWidgets.QApplication.translate("DissolveWithStats", "Browse", None))
        self.labelOutput.setToolTip(QtWidgets.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Click on Browse button to specify output layer</p></body></html>", None))
        self.labelOutput.setText(QtWidgets.QApplication.translate("DissolveWithStats", "Create output layer :", None))
        self.labelFieldTable.setToolTip(QtWidgets.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Choose which fields will be present in the output layer, and which statistic to calculate</p></body></html>", None))
        self.labelFieldTable.setText(QtWidgets.QApplication.translate("DissolveWithStats", "Calculate statistics on other fields :", None))
        self.checkBoxAddFile.setToolTip(QtWidgets.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Uncheck this if you do not want the output layer to be loaded in QGIS</p></body></html>", None))
        self.checkBoxAddFile.setText(QtWidgets.QApplication.translate("DissolveWithStats", "Add output layer to the map", None))

