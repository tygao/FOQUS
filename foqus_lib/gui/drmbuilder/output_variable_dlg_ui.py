# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output_variable_dlg.ui'
#
# Created: Fri Oct 09 15:14:18 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_outputVariableDlg(object):
    def setupUi(self, outputVariableDlg):
        outputVariableDlg.setObjectName("outputVariableDlg")
        outputVariableDlg.resize(624, 355)
        self.gridLayout_3 = QtGui.QGridLayout(outputVariableDlg)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_OutputList = QtGui.QLabel(outputVariableDlg)
        self.label_OutputList.setObjectName("label_OutputList")
        self.gridLayout_3.addWidget(self.label_OutputList, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidget_OutputList = QtGui.QListWidget(outputVariableDlg)
        self.listWidget_OutputList.setObjectName("listWidget_OutputList")
        self.gridLayout_2.addWidget(self.listWidget_OutputList, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_Up = QtGui.QPushButton(outputVariableDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Up.sizePolicy().hasHeightForWidth())
        self.pushButton_Up.setSizePolicy(sizePolicy)
        self.pushButton_Up.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_Up.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_Up.setObjectName("pushButton_Up")
        self.gridLayout.addWidget(self.pushButton_Up, 0, 0, 1, 1)
        self.pushButton_Down = QtGui.QPushButton(outputVariableDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Down.sizePolicy().hasHeightForWidth())
        self.pushButton_Down.setSizePolicy(sizePolicy)
        self.pushButton_Down.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_Down.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_Down.setObjectName("pushButton_Down")
        self.gridLayout.addWidget(self.pushButton_Down, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(13, 182, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 1, 1, 1)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.lineEdit_NumberOfVariedVariables = QtGui.QLineEdit(outputVariableDlg)
        self.lineEdit_NumberOfVariedVariables.setEnabled(False)
        self.lineEdit_NumberOfVariedVariables.setReadOnly(True)
        self.lineEdit_NumberOfVariedVariables.setObjectName("lineEdit_NumberOfVariedVariables")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_NumberOfVariedVariables)
        self.label_NumberOfVariedVariables = QtGui.QLabel(outputVariableDlg)
        self.label_NumberOfVariedVariables.setObjectName("label_NumberOfVariedVariables")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_NumberOfVariedVariables)
        self.groupBox_ForSelected = QtGui.QGroupBox(outputVariableDlg)
        self.groupBox_ForSelected.setObjectName("groupBox_ForSelected")
        self.formLayout = QtGui.QFormLayout(self.groupBox_ForSelected)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_Name = QtGui.QLabel(self.groupBox_ForSelected)
        self.label_Name.setObjectName("label_Name")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_Name)
        self.lineEdit_Name = QtGui.QLineEdit(self.groupBox_ForSelected)
        self.lineEdit_Name.setEnabled(False)
        self.lineEdit_Name.setObjectName("lineEdit_Name")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_Name)
        self.label_Unit = QtGui.QLabel(self.groupBox_ForSelected)
        self.label_Unit.setObjectName("label_Unit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_Unit)
        self.lineEdit_Unit = QtGui.QLineEdit(self.groupBox_ForSelected)
        self.lineEdit_Unit.setEnabled(False)
        self.lineEdit_Unit.setObjectName("lineEdit_Unit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_Unit)
        self.label_Description = QtGui.QLabel(self.groupBox_ForSelected)
        self.label_Description.setObjectName("label_Description")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_Description)
        self.lineEdit_Description = QtGui.QLineEdit(self.groupBox_ForSelected)
        self.lineEdit_Description.setObjectName("lineEdit_Description")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_Description)
        self.checkBox_VariesWithTime = QtGui.QCheckBox(self.groupBox_ForSelected)
        self.checkBox_VariesWithTime.setObjectName("checkBox_VariesWithTime")
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.checkBox_VariesWithTime)
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.SpanningRole, self.groupBox_ForSelected)
        self.gridLayout_3.addLayout(self.formLayout_2, 1, 2, 1, 1)
        self.pushButton_Cancel = QtGui.QPushButton(outputVariableDlg)
        self.pushButton_Cancel.setAutoDefault(False)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.gridLayout_3.addWidget(self.pushButton_Cancel, 2, 0, 1, 1)
        self.pushButton_OK = QtGui.QPushButton(outputVariableDlg)
        self.pushButton_OK.setAutoDefault(False)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.gridLayout_3.addWidget(self.pushButton_OK, 2, 2, 1, 1)

        self.retranslateUi(outputVariableDlg)
        QtCore.QMetaObject.connectSlotsByName(outputVariableDlg)
        outputVariableDlg.setTabOrder(self.listWidget_OutputList, self.lineEdit_Description)
        outputVariableDlg.setTabOrder(self.lineEdit_Description, self.checkBox_VariesWithTime)
        outputVariableDlg.setTabOrder(self.checkBox_VariesWithTime, self.pushButton_Up)
        outputVariableDlg.setTabOrder(self.pushButton_Up, self.pushButton_Down)
        outputVariableDlg.setTabOrder(self.pushButton_Down, self.pushButton_Cancel)
        outputVariableDlg.setTabOrder(self.pushButton_Cancel, self.pushButton_OK)
        outputVariableDlg.setTabOrder(self.pushButton_OK, self.lineEdit_NumberOfVariedVariables)
        outputVariableDlg.setTabOrder(self.lineEdit_NumberOfVariedVariables, self.lineEdit_Name)
        outputVariableDlg.setTabOrder(self.lineEdit_Name, self.lineEdit_Unit)

    def retranslateUi(self, outputVariableDlg):
        outputVariableDlg.setWindowTitle(QtGui.QApplication.translate("outputVariableDlg", "Output Variable Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_OutputList.setText(QtGui.QApplication.translate("outputVariableDlg", "Output Variable List", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Up.setText(QtGui.QApplication.translate("outputVariableDlg", "˄", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Down.setText(QtGui.QApplication.translate("outputVariableDlg", "˅", None, QtGui.QApplication.UnicodeUTF8))
        self.label_NumberOfVariedVariables.setText(QtGui.QApplication.translate("outputVariableDlg", "Number of Time Dependent Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_ForSelected.setTitle(QtGui.QApplication.translate("outputVariableDlg", "For Selected Output Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Name.setText(QtGui.QApplication.translate("outputVariableDlg", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Unit.setText(QtGui.QApplication.translate("outputVariableDlg", "Unit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Description.setText(QtGui.QApplication.translate("outputVariableDlg", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_VariesWithTime.setText(QtGui.QApplication.translate("outputVariableDlg", "Included in DRM", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("outputVariableDlg", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("outputVariableDlg", "OK", None, QtGui.QApplication.UnicodeUTF8))
