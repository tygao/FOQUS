import sys
import os

from foqus_lib.framework.uq.Model import Model
from foqus_lib.framework.uq.SampleData import SampleData
from foqus_lib.framework.uq.Visualizer import Visualizer
from foqus_lib.framework.uq.Common import *
from foqus_lib.framework.uq.RSInference import RSInferencer
from foqus_lib.framework.sdoe import sdoe

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, \
    QAbstractItemView, QDialogButtonBox, QApplication, QTableWidgetItem
from PyQt5.QtGui import QCursor, QColor
mypath = os.path.dirname(__file__)
_sdoePreviewUI, _sdoePreview = \
        uic.loadUiType(os.path.join(mypath, "sdoePreview_UI.ui"))


class sdoePreview(_sdoePreview, _sdoePreviewUI):
    def __init__(self, data, dirname, parent=None):
        super(sdoePreview, self).__init__(parent)
        self.setupUi(self)
        self.data = data
        self.dirname = dirname

        inputTypes = data.getInputTypes()
        count = inputTypes.count(Model.FIXED)


        self.plotSdoeButton.clicked.connect(self.plotSdoe)

        self.refresh()

    def freeze(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

    def semifreeze(self):
        QApplication.setOverrideCursor(QCursor(Qt.BusyCursor))

    def unfreeze(self):
        QApplication.restoreOverrideCursor()

    class listItem(QListWidgetItem):
        def __init__(self, text, inputIndex):
            super(sdoePreview.listItem, self).__init__(text)
            self.inputIndex = inputIndex

        def getInputIndex(self):
            return self.inputIndex


    def refresh(self):

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        inputData = self.data.getInputData()
        inputTypes = self.data.getInputTypes()
        inputNames = self.data.getInputNames()
        numSamplesAdded = self.data.getNumSamplesAdded()

        # Set up table
        self.table.setColumnCount(self.data.getNumInputs())
        headers = []
        self.table.setRowCount(inputData.shape[0])
        showFixed = 0

        refinedColor = QColor(255, 255, 0, 100)

        c = 0
        for i, inputName in enumerate(inputNames):
            inputType = inputTypes[i]
            if showFixed or inputType == Model.VARIABLE:
                headers.append(inputName)
                for r in range(inputData.shape[0]):
                    item = self.table.item(r, c)
                    if item is None:
                        item = QTableWidgetItem('%g' % inputData[r][i])
                        if r >= inputData.shape[0] - numSamplesAdded:
                            item.setBackground(refinedColor)
                        self.table.setItem(r, c, item)
                    else:
                        item.setText('%g' % inputData[r][i])
                c = c + 1
                if inputType == Model.VARIABLE:
                    item = sdoePreview.listItem(inputNames[i], i)
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.resizeColumnsToContents()

        QApplication.restoreOverrideCursor()

    def plotSdoe(self):
        fname = os.path.join(self.dirname, self.data.getModelName())
        sdoe.plot(fname)
        self.setModal(True)