# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DissolveWithStatsDialog
                                 A QGIS plugin
 Group entities with same value for one field, calculate statistics on the other fields
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-02-19
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Julie Pierson, UMR 5319 Passages, CNRS
        email                : julie.pierson@cnrs.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import uic, QtWidgets, QtCore
#from PyQt5 import QtGui
from qgis.core import QgsMessageLog, Qgis, QgsProviderRegistry
#from qgis.gui import QgsMessageBar
from qgis.utils import iface


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dissolve_stats_dialog_base.ui'))


class DissolveWithStatsDialog(QtWidgets.QDialog, FORM_CLASS):
    # Define constants of the TableWidget
    _listHeaders = ["name", "type", "stat", "dest name"]
    _listHeadersWidths = [120, 80, 100, 120]

    # Contructor
    def __init__(self, parent=None):
        """Constructor."""
        super(DissolveWithStatsDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        # input layer combobox must show only vector layers
        providers = QgsProviderRegistry.instance().providerList()
        vector_providers = ['ogr', 'memory', 'postgres', 'spatialite', 'virtual']
        providers = [i for i in providers if i not in vector_providers]
        self.mMapLayerComboBox.setExcludedProviders(providers)
        
        # connect changed index signal in comboLayerList
        self.mMapLayerComboBox.currentIndexChanged[int].connect(self.onChangedValueLayer)
        # connect changed index signal in comboFieldList
        self.mFieldComboBox.currentIndexChanged[int].connect(self.onChangedValueField)
        # connect click on browse button for output to display file dialog for output file
        self.outButton.clicked.connect(self.outFile)
        # connect add all fields button for include a row for each field except dissolve
        self.allFields.clicked.connect(self.onClickAllFieldsButton)
        # connect remove all fields except dissolve
        self.noFields.clicked.connect(self.onClickNoFieldsButton)
        # connect OK button with validation test for input paramaters
        self.buttonBox.accepted.connect(self.validation)

        # populate field combobox and table
        self.onChangedValueLayer(self.mMapLayerComboBox.currentIndex())
        # populate the table header
        self.tableWidget.setHorizontalHeaderLabels(self._listHeaders)
        # set column widths for table 
        for i in range(len(self._listHeadersWidths)):
            self.tableWidget.setColumnWidth(i, self._listHeadersWidths[i])

    # check if all the dialog parameters are valid
    def validation(self):
        # testing for input layer
        if not self.mMapLayerComboBox.currentLayer():
            iface.messageBar().pushMessage("Error", "Please select a valid vector layer for input", level=Qgis.Critical)
        # testing for output layer
        if not self.outLayerName.text():
            iface.messageBar().pushMessage("Error", "Please choose a path and a name for output layer", level=Qgis.Critical)
        # input layer must have at least one field
        if self.mFieldComboBox.currentIndex() == -1:
            iface.messageBar().pushMessage("Error", "Input layer must have at least one column", level=Qgis.Critical)
        # at least one field must be kept for output layer (not needed to test because the dissolve field is always filled)
        # test if all destName are filled (remember that last row must be empty)
        for i in range(1, self.tableWidget.rowCount() - 1):
            if len(self.tableWidget.item(i, 2).text()) == 0:
                iface.messageBar().pushMessage("Error", "Output field names must have at least one character", level=Qgis.Critical)
        # test if all destName are different (a duplicate field+stat)
        if len(set([self.tableWidget.item(i, 2).text() for i in range(self.tableWidget.rowCount() - 1)])) != self.tableWidget.rowCount() - 1:
            iface.messageBar().pushMessage("Error", "Duplicate field and stats provided. Please remove one of them", level=Qgis.Critical)
    
    # refresh fields
    def _refreshFields(self):
        selectedLayer = self.mMapLayerComboBox.currentLayer()
        fields = selectedLayer.fields()
        return fields

    # if selected value in comboLayerList changes :
    # actualize the values in comboFieldList and in tableFields
    def onChangedValueLayer(self, index):
        # get selected layer from combobox if one
        if index != -1:
            selectedLayer = self.mMapLayerComboBox.currentLayer()
            # if selected layer is loaded (name selected in combobox from canvas layers)
            if selectedLayer:
                QgsMessageLog.logMessage('selectedLayer : ' + str(selectedLayer.name()))
            # populate field combobox from selected layer fields
            self.mFieldComboBox.setLayer(selectedLayer)
            
            # add the two rows: first for dissolve field, second to include more fields stats (automatically)
            self.addTableWidgetRow()

            # select first field (this triggers populating row 0 and creating row 1)
            fields = selectedLayer.fields()
            if len(fields) > 0:
                self.mFieldComboBox.setField(fields[0].name())
            # we disable first row because is the field used for dissolve
            self.tableWidget.cellWidget(0, 0).setEnabled(False)
            self.tableWidget.cellWidget(0, 2).setEnabled(False)

    # add an empty row with selection
    def addTableWidgetRow(self):
        # retrieve selected layer fields
        fields = self._refreshFields()
        previousRowCount = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(previousRowCount + 1)
        comboFields = QtWidgets.QComboBox()
        fieldList = [' '] + [i.name() for i in fields]
        comboFields.setProperty('row', previousRowCount)
        comboFields.setFixedWidth(self._listHeadersWidths[0])
        comboFields.addItems(fieldList)
        comboFields.currentIndexChanged[int].connect(self.onChangedFieldRow)
        self.tableWidget.setCellWidget(previousRowCount, 0, comboFields)

    # Fill a row of the table with all information of the selected field    
    def populateTableWidgetRow(self, row):
        # fill basic info of the layer
        index = self.tableWidget.cellWidget(row, 0).currentIndex()
        fields = self._refreshFields()
        # second column: type of field (not editable)
        typeitem = QtWidgets.QTableWidgetItem(fields[index - 1].typeName())
        typeitem.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(row, 1, typeitem)
        # third column : stat (editable) and triggers fillProposedName (order of insertion is important becuase of the
        # triggered function!!)
        combo = QtWidgets.QComboBox()
        combo.setProperty('row', row)
        self.tableWidget.setCellWidget(row, 2, combo)
        combo.setFixedWidth(self._listHeadersWidths[2])
        combo.currentIndexChanged[int].connect(self.fillProposedName)
        combo.addItems(self.availableStatistics(fields[index - 1]))
        
        # fourth column: final name (except for the first row is a combination of original field and stat)
        # automatically filled when combo is created and set
    
    # fill proposed name column
    def fillProposedName(self, index):
        # Determine the row
        combo = self.sender()
        row = combo.property('row')
        # Row 0 represents the dissolve field. Its value and stat is fixed so its name.
        if row == 0:
            nameitem = QtWidgets.QTableWidgetItem(self.tableWidget.cellWidget(row,0).currentText())
            self.tableWidget.setItem(row, 3, nameitem)
            return    
        # Rest of rows
        nameitem = QtWidgets.QTableWidgetItem(self.tableWidget.cellWidget(row,0).currentText() + "_" + self.tableWidget.cellWidget(row,2).currentText())
        nameitem.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(row, 3, nameitem)

    # if changed the field of a row we must fill the rest of columns
    def onChangedFieldRow(self, index):
        # First locate selected row
        combo = self.sender()
        row = combo.property('row')
        self.populateTableWidgetRow(row)
        # Add a new row if the current combo value is not "" in other case remove this row if is upper than 2
        if index == 0:
            if row > 1:
                self.tableWidget.removeRow(row)
                self.tableWidget.setRowCount(self.tableWidget.rowCount() - 1)
            else:
                self.tableWidget.setCellWidget(row, 1, None)
                self.tableWidget.setCellWidget(row, 2, None)
        else:
            # Create a new row to allow including more fields if the row is the last one
            if row == self.tableWidget.rowCount() - 1:
                self.addTableWidgetRow()

    # if selected value in comboFieldList changes :
    # re-enable the stats list for ex-selected value if one, disable it for selected value
    def onChangedValueField(self, index):
        # We change the value at first combobox
        self.tableWidget.cellWidget(0, 0).setCurrentIndex(index + 1)

    # function to add all fields similar to previous version of DissolveWithStats
    def onClickAllFieldsButton(self):
        # update fields
        fields = self._refreshFields()
        # add all fields except the first in the table
        for i in fields:
            if i.name() != self.tableWidget.cellWidget(0, 0).currentText():
                index = self.tableWidget.cellWidget(self.tableWidget.rowCount() - 1, 0).findText(i.name())
                if index != -1:
                    self.tableWidget.cellWidget(self.tableWidget.rowCount() - 1, 0).setCurrentIndex(index)
    
    # function to remove all fields except the dissolve field
    def onClickNoFieldsButton(self):
        # remove all rows except first (dissolve fields) and second (to add more fields)
        self.tableWidget.setRowCount(2)
        self.tableWidget.cellWidget(1, 0).setCurrentIndex(0)
        # clear rest of row (remove texts if exists)
        self.tableWidget.setItem(1, 1, None)
        self.tableWidget.setItem(1, 3, None)
    
    # return available statistics for a given field (i.e mean can only be calculated for a numeric field)
    def availableStatistics(self, field):
        # if field is numeric (works also for PostGIS data, fix by DelazJ, and for int64 and double, fix by A. Ferraton)
        if field.type() in [QtCore.QVariant.Int, QtCore.QVariant.Double, 2, 4, 6]:
            statList = ["Count", "First", "Last", "Max", "Mean", "Median", "Min", "Standard deviation", "Sum"]
        else:
        # if field is not numeric (string)
            statList = ["Count", "Concatenation", "First", "Last", "Uniquification"]
        return statList
    
    # get output file path
    def outFile(self):
        # display file dialog for output file
        outFile = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', '', "Shapefile (*.shp);;GeoPackage (*.gpkg)")
        # get file format, for example : .shp
        outFileFormat = outFile[1].split('*')[-1][:-1]
        # get file name, for example /path/to/file.shp
        outFileName = outFile[0]
        if not outFileName.endswith(outFileFormat):
            outFileName = outFileName + outFileFormat
        # populate QLineEdit widget with output file path
        self.outLayerName.setText(outFileName)
        return outFileName
        