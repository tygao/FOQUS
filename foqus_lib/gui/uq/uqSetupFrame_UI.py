# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uq\uqSetupFrame_UI.ui'
#
# Created: Mon Aug 10 09:15:37 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_uqSetupFrame(object):
    def setupUi(self, uqSetupFrame):
        uqSetupFrame.setObjectName("uqSetupFrame")
        uqSetupFrame.resize(1450, 813)
        uqSetupFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        uqSetupFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout_11 = QtGui.QGridLayout(uqSetupFrame)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.groupBox = QtGui.QGroupBox(uqSetupFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_14 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addSimulationButton = QtGui.QPushButton(self.groupBox)
        self.addSimulationButton.setMinimumSize(QtCore.QSize(5, 5))
        self.addSimulationButton.setObjectName("addSimulationButton")
        self.horizontalLayout.addWidget(self.addSimulationButton)
        self.loadSimulationButton = QtGui.QPushButton(self.groupBox)
        self.loadSimulationButton.setObjectName("loadSimulationButton")
        self.horizontalLayout.addWidget(self.loadSimulationButton)
        self.cloneSimulationButton = QtGui.QPushButton(self.groupBox)
        self.cloneSimulationButton.setMinimumSize(QtCore.QSize(5, 5))
        self.cloneSimulationButton.setObjectName("cloneSimulationButton")
        self.horizontalLayout.addWidget(self.cloneSimulationButton)
        self.deleteSimulationButton = QtGui.QPushButton(self.groupBox)
        self.deleteSimulationButton.setObjectName("deleteSimulationButton")
        self.horizontalLayout.addWidget(self.deleteSimulationButton)
        self.saveSimulationButton = QtGui.QPushButton(self.groupBox)
        self.saveSimulationButton.setObjectName("saveSimulationButton")
        self.horizontalLayout.addWidget(self.saveSimulationButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_14.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.infoGroupBox = QtGui.QGroupBox(self.groupBox)
        self.infoGroupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.infoGroupBox.setObjectName("infoGroupBox")
        self.gridLayout_7 = QtGui.QGridLayout(self.infoGroupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.infoTable = QtGui.QTableWidget(self.infoGroupBox)
        self.infoTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.infoTable.setObjectName("infoTable")
        self.infoTable.setColumnCount(1)
        self.infoTable.setRowCount(4)
        item = QtGui.QTableWidgetItem()
        self.infoTable.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.infoTable.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.infoTable.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.infoTable.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.infoTable.setHorizontalHeaderItem(0, item)
        self.infoTable.horizontalHeader().setVisible(False)
        self.gridLayout_7.addWidget(self.infoTable, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.infoGroupBox, 0, 1, 2, 1)
        self.dockWidget = QtGui.QDockWidget(self.groupBox)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.dataTabs = QtGui.QTabWidget(self.dockWidgetContents)
        self.dataTabs.setProperty("sizeHint", QtCore.QSize(745, 282))
        self.dataTabs.setObjectName("dataTabs")
        self.deleteTab = QtGui.QWidget()
        self.deleteTab.setObjectName("deleteTab")
        self.gridLayout_6 = QtGui.QGridLayout(self.deleteTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.delete_static = QtGui.QLabel(self.deleteTab)
        self.delete_static.setObjectName("delete_static")
        self.gridLayout_6.addWidget(self.delete_static, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.resetDeleteTable_button = QtGui.QPushButton(self.deleteTab)
        self.resetDeleteTable_button.setObjectName("resetDeleteTable_button")
        self.horizontalLayout_2.addWidget(self.resetDeleteTable_button)
        self.delete_button = QtGui.QPushButton(self.deleteTab)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_2.addWidget(self.delete_button)
        self.changeOutputs_button = QtGui.QPushButton(self.deleteTab)
        self.changeOutputs_button.setObjectName("changeOutputs_button")
        self.horizontalLayout_2.addWidget(self.changeOutputs_button)
        self.gridLayout_6.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.delete_table = QtGui.QTableWidget(self.deleteTab)
        self.delete_table.setObjectName("delete_table")
        self.delete_table.setColumnCount(0)
        self.delete_table.setRowCount(0)
        self.gridLayout_6.addWidget(self.delete_table, 1, 0, 1, 2)
        self.dataTabs.addTab(self.deleteTab, "")
        self.filterTab = QtGui.QWidget()
        self.filterTab.setObjectName("filterTab")
        self.gridLayout_12 = QtGui.QGridLayout(self.filterTab)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.filterOutput_radio = QtGui.QRadioButton(self.filterTab)
        self.filterOutput_radio.setObjectName("filterOutput_radio")
        self.gridLayout_12.addWidget(self.filterOutput_radio, 0, 1, 1, 1)
        self.filter_button = QtGui.QPushButton(self.filterTab)
        self.filter_button.setToolTip("")
        self.filter_button.setObjectName("filter_button")
        self.gridLayout_12.addWidget(self.filter_button, 0, 2, 2, 1)
        self.filterInputBox = QtGui.QGroupBox(self.filterTab)
        self.filterInputBox.setTitle("")
        self.filterInputBox.setObjectName("filterInputBox")
        self.gridLayout_5 = QtGui.QGridLayout(self.filterInputBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.filterInputMax_static = QtGui.QLabel(self.filterInputBox)
        self.filterInputMax_static.setObjectName("filterInputMax_static")
        self.gridLayout_5.addWidget(self.filterInputMax_static, 2, 0, 1, 1)
        self.filterInputMin_static = QtGui.QLabel(self.filterInputBox)
        self.filterInputMin_static.setObjectName("filterInputMin_static")
        self.gridLayout_5.addWidget(self.filterInputMin_static, 1, 0, 1, 1)
        self.horizontalLayout_filterInput = QtGui.QHBoxLayout()
        self.horizontalLayout_filterInput.setObjectName("horizontalLayout_filterInput")
        self.filterInput_static = QtGui.QLabel(self.filterInputBox)
        self.filterInput_static.setObjectName("filterInput_static")
        self.horizontalLayout_filterInput.addWidget(self.filterInput_static)
        self.filterInput_combo = QtGui.QComboBox(self.filterInputBox)
        self.filterInput_combo.setObjectName("filterInput_combo")
        self.horizontalLayout_filterInput.addWidget(self.filterInput_combo)
        self.gridLayout_5.addLayout(self.horizontalLayout_filterInput, 0, 0, 1, 2)
        self.filterInputMin_edit = QtGui.QLineEdit(self.filterInputBox)
        self.filterInputMin_edit.setObjectName("filterInputMin_edit")
        self.gridLayout_5.addWidget(self.filterInputMin_edit, 1, 1, 1, 1)
        self.filterInputMax_edit = QtGui.QLineEdit(self.filterInputBox)
        self.filterInputMax_edit.setObjectName("filterInputMax_edit")
        self.gridLayout_5.addWidget(self.filterInputMax_edit, 2, 1, 1, 1)
        self.gridLayout_12.addWidget(self.filterInputBox, 1, 0, 2, 1)
        self.filterOutputBox = QtGui.QGroupBox(self.filterTab)
        self.filterOutputBox.setTitle("")
        self.filterOutputBox.setObjectName("filterOutputBox")
        self.gridLayout_13 = QtGui.QGridLayout(self.filterOutputBox)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.horizontalLayout_filterOutput = QtGui.QHBoxLayout()
        self.horizontalLayout_filterOutput.setObjectName("horizontalLayout_filterOutput")
        self.filterOutput_static = QtGui.QLabel(self.filterOutputBox)
        self.filterOutput_static.setObjectName("filterOutput_static")
        self.horizontalLayout_filterOutput.addWidget(self.filterOutput_static)
        self.filterOutput_combo = QtGui.QComboBox(self.filterOutputBox)
        self.filterOutput_combo.setObjectName("filterOutput_combo")
        self.horizontalLayout_filterOutput.addWidget(self.filterOutput_combo)
        self.gridLayout_13.addLayout(self.horizontalLayout_filterOutput, 0, 0, 1, 2)
        self.filterOutputMin_static = QtGui.QLabel(self.filterOutputBox)
        self.filterOutputMin_static.setObjectName("filterOutputMin_static")
        self.gridLayout_13.addWidget(self.filterOutputMin_static, 1, 0, 1, 1)
        self.filterOutputMin_edit = QtGui.QLineEdit(self.filterOutputBox)
        self.filterOutputMin_edit.setObjectName("filterOutputMin_edit")
        self.gridLayout_13.addWidget(self.filterOutputMin_edit, 1, 1, 1, 1)
        self.filterOutputMax_static = QtGui.QLabel(self.filterOutputBox)
        self.filterOutputMax_static.setObjectName("filterOutputMax_static")
        self.gridLayout_13.addWidget(self.filterOutputMax_static, 2, 0, 1, 1)
        self.filterOutputMax_edit = QtGui.QLineEdit(self.filterOutputBox)
        self.filterOutputMax_edit.setObjectName("filterOutputMax_edit")
        self.gridLayout_13.addWidget(self.filterOutputMax_edit, 2, 1, 1, 1)
        self.gridLayout_12.addWidget(self.filterOutputBox, 1, 1, 2, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 86, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem1, 2, 2, 1, 1)
        self.filterInput_radio = QtGui.QRadioButton(self.filterTab)
        self.filterInput_radio.setObjectName("filterInput_radio")
        self.gridLayout_12.addWidget(self.filterInput_radio, 0, 0, 1, 1)
        self.dataTabs.addTab(self.filterTab, "")
        self.gridLayout.addWidget(self.dataTabs, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.gridLayout_14.addWidget(self.dockWidget, 2, 0, 1, 2)
        self.simulationTable = QtGui.QTableWidget(self.groupBox)
        self.simulationTable.setMinimumSize(QtCore.QSize(5, 5))
        self.simulationTable.setBaseSize(QtCore.QSize(0, 0))
        self.simulationTable.setStyleSheet("selection-background-color: rgb(192, 192, 255);\n"
"selection-color: rgb(0, 0, 0);")
        self.simulationTable.setObjectName("simulationTable")
        self.simulationTable.setColumnCount(7)
        self.simulationTable.setRowCount(2)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.simulationTable.setHorizontalHeaderItem(6, item)
        self.simulationTable.horizontalHeader().setDefaultSectionSize(100)
        self.simulationTable.horizontalHeader().setMinimumSectionSize(35)
        self.simulationTable.verticalHeader().setVisible(False)
        self.simulationTable.verticalHeader().setMinimumSectionSize(25)
        self.gridLayout_14.addWidget(self.simulationTable, 1, 0, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(uqSetupFrame)
        self.dataTabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(uqSetupFrame)

    def retranslateUi(self, uqSetupFrame):
        uqSetupFrame.setWindowTitle(QtGui.QApplication.translate("uqSetupFrame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("uqSetupFrame", "Uncertainty Quantification Simulation Ensembles", None, QtGui.QApplication.UnicodeUTF8))
        self.addSimulationButton.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Click to generate a new ensemble.", None, QtGui.QApplication.UnicodeUTF8))
        self.addSimulationButton.setText(QtGui.QApplication.translate("uqSetupFrame", "Add New...", None, QtGui.QApplication.UnicodeUTF8))
        self.loadSimulationButton.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Click to load an existing ensemble\n"
"saved as a PSUADE file.", None, QtGui.QApplication.UnicodeUTF8))
        self.loadSimulationButton.setText(QtGui.QApplication.translate("uqSetupFrame", "Load from File...", None, QtGui.QApplication.UnicodeUTF8))
        self.cloneSimulationButton.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Click to clone ensemble.", None, QtGui.QApplication.UnicodeUTF8))
        self.cloneSimulationButton.setText(QtGui.QApplication.translate("uqSetupFrame", "Clone Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteSimulationButton.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Click to delete ensemble.", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteSimulationButton.setText(QtGui.QApplication.translate("uqSetupFrame", "Delete Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.saveSimulationButton.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Click to save ensemble as a PSUADE file.", None, QtGui.QApplication.UnicodeUTF8))
        self.saveSimulationButton.setText(QtGui.QApplication.translate("uqSetupFrame", "Save Selected...", None, QtGui.QApplication.UnicodeUTF8))
        self.infoGroupBox.setTitle(QtGui.QApplication.translate("uqSetupFrame", "Ensemble Info", None, QtGui.QApplication.UnicodeUTF8))
        self.infoTable.verticalHeaderItem(0).setText(QtGui.QApplication.translate("uqSetupFrame", "# Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.infoTable.verticalHeaderItem(1).setText(QtGui.QApplication.translate("uqSetupFrame", "# Outputs", None, QtGui.QApplication.UnicodeUTF8))
        self.infoTable.verticalHeaderItem(2).setText(QtGui.QApplication.translate("uqSetupFrame", "Sample Design", None, QtGui.QApplication.UnicodeUTF8))
        self.infoTable.verticalHeaderItem(3).setText(QtGui.QApplication.translate("uqSetupFrame", "Sample Size", None, QtGui.QApplication.UnicodeUTF8))
        self.infoTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("uqSetupFrame", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_static.setText(QtGui.QApplication.translate("uqSetupFrame", "Select Variables (columns) and/or Sample Points (rows) for Deletion.\n"
"Type new values for outputs in the appropriate cells. ", None, QtGui.QApplication.UnicodeUTF8))
        self.resetDeleteTable_button.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Undo uncommitted changes.", None, QtGui.QApplication.UnicodeUTF8))
        self.resetDeleteTable_button.setText(QtGui.QApplication.translate("uqSetupFrame", "Reset\n"
"Table", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Delete rows/columns and save.", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setText(QtGui.QApplication.translate("uqSetupFrame", "Perform Deletion then\n"
"Save as New Ensemble", None, QtGui.QApplication.UnicodeUTF8))
        self.changeOutputs_button.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Commit all changes. ", None, QtGui.QApplication.UnicodeUTF8))
        self.changeOutputs_button.setText(QtGui.QApplication.translate("uqSetupFrame", "Make Output Value\n"
"Changes Permanent", None, QtGui.QApplication.UnicodeUTF8))
        self.dataTabs.setTabText(self.dataTabs.indexOf(self.deleteTab), QtGui.QApplication.translate("uqSetupFrame", "Inspection / Deletion / Output Value Modification", None, QtGui.QApplication.UnicodeUTF8))
        self.filterOutput_radio.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Choose this to filter your data based on output values.", None, QtGui.QApplication.UnicodeUTF8))
        self.filterOutput_radio.setText(QtGui.QApplication.translate("uqSetupFrame", "Filter output", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_button.setText(QtGui.QApplication.translate("uqSetupFrame", "Perform Filtering then\n"
"Save as New Ensemble", None, QtGui.QApplication.UnicodeUTF8))
        self.filterInputMax_static.setText(QtGui.QApplication.translate("uqSetupFrame", "Upper Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.filterInputMin_static.setText(QtGui.QApplication.translate("uqSetupFrame", "Lower Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.filterInput_static.setText(QtGui.QApplication.translate("uqSetupFrame", "Choose Input:", None, QtGui.QApplication.UnicodeUTF8))
        self.filterOutput_static.setText(QtGui.QApplication.translate("uqSetupFrame", "Choose Output:", None, QtGui.QApplication.UnicodeUTF8))
        self.filterOutputMin_static.setText(QtGui.QApplication.translate("uqSetupFrame", "Lower Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.filterOutputMax_static.setText(QtGui.QApplication.translate("uqSetupFrame", "Upper Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.filterInput_radio.setToolTip(QtGui.QApplication.translate("uqSetupFrame", "Choose this to filter your data based on input values.", None, QtGui.QApplication.UnicodeUTF8))
        self.filterInput_radio.setText(QtGui.QApplication.translate("uqSetupFrame", "Filter Input", None, QtGui.QApplication.UnicodeUTF8))
        self.dataTabs.setTabText(self.dataTabs.indexOf(self.filterTab), QtGui.QApplication.translate("uqSetupFrame", "Filtering", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.verticalHeaderItem(0).setText(QtGui.QApplication.translate("uqSetupFrame", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.verticalHeaderItem(1).setText(QtGui.QApplication.translate("uqSetupFrame", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("uqSetupFrame", "Ensemble", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("uqSetupFrame", "Run Status", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("uqSetupFrame", "Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("uqSetupFrame", "Launch", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("uqSetupFrame", "Analyze", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("uqSetupFrame", "Descriptor", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTable.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("uqSetupFrame", "Turbine Session", None, QtGui.QApplication.UnicodeUTF8))
