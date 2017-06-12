import sys
from PySide import QtGui, QtCore
from nodeToUQModel import nodeToUQModel
from foqus_lib.framework.listen import listen
from multiprocessing.connection import Client

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

if __name__ == '__main__':
    import imp
    #f, filename, desc = imp.find_module('foqus_lib', ['c:\\Users\\ou3.THE-LAB\\Documents\\CCSI\\foqus\\'])
    #f, filename, desc = imp.find_module('foqus_lib', ['/g/g12/ou3/ccsi/foqus/'])
    #f, filename, desc = imp.find_module('foqus_lib', ['/g/g19/ng30/ts6/foqus/'])
    f, filename, desc = imp.find_module('foqus_lib', ['c:\\CCSI\\foqus'])    
    foqus_lib = imp.load_module('foqus_lib', f, filename, desc)

from ouuSetupFrame_UI import *
from foqus_lib.framework.uq.Common import *
from foqus_lib.framework.uq.LocalExecutionModule import *
#from foqus_lib.gui.uq.Preview import *
#from InputPriorTable import InputPriorTable
from foqus_lib.gui.uq.InputPriorTable import InputPriorTable
from foqus_lib.framework.ouu.OUU import OUU

class ouuSetupFrame(QtGui.QFrame, Ui_ouuSetupFrame):
    plotSignal = QtCore.Signal(dict)

    def __init__(self, dat = None, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setupUi(self)
        self.dat = dat
        self.filesDir = ''
        self.scenariosCalculated = False
        self.result = None

        # Refresh table
        self.refresh()
        self.plotSignal.connect(self.addPlotValues)

        self.setFixed_button.setEnabled(False)
        self.setX1_button.setEnabled(False)
        self.setX2_button.setEnabled(False)
        self.setX3_button.setEnabled(False)
        self.setX4_button.setEnabled(False)

        self.input_table.setColumnHidden(3, True) # Hide scale column
        self.modelFile_edit.clear()
        self.modelFile_radio.setChecked(True)
        self.uqTab = self.tabs.widget(1)
        self.tabs.removeTab(1)
        self.tabs.setCurrentIndex(0)
        self.tabs.setEnabled(False)
        self.output_combo.setEnabled(False)
        self.mean_radio.setChecked(True)
        self.betaDoubleSpin.setValue(0)
        self.alphaDoubleSpin.setValue(0.5)
        self.primarySolver_combo.setEnabled(False)
        self.secondarySolver_combo.setCurrentIndex(0)
        self.z3_table.setRowCount(1)
        self.compressSamples_chk.setEnabled(False)
        self.calcScenarios_button.setEnabled(False)
        self.scenarioSelect_static.setEnabled(False)
        self.scenarioSelect_combo.setEnabled(False)
        self.z4NewSample_radio.setChecked(True)
        self.x4SampleScheme_combo.setCurrentIndex(0)
        self.x4SampleSize_label.setText('Sample Size')        
        self.x4SampleSize_spin.setValue(5)
        self.x4SampleSize_spin.setRange(5,1000)
        self.x4FileBrowse_button.setEnabled(False)
        self.x4SampleScheme_combo.clear()
        self.x4SampleScheme_combo.addItems([SamplingMethods.getFullName(SamplingMethods.LH),
                                            SamplingMethods.getFullName(SamplingMethods.LPTAU),
                                            SamplingMethods.getFullName(SamplingMethods.FACT)])
        self.x4RSMethod_check.setChecked(False)
        self.z4_table.setEnabled(False)
        self.z4_table.setRowCount(1)
        self.z4SubsetSize_label.setEnabled(False)
        self.z4SubsetSize_spin.setEnabled(False)
        self.run_button.setEnabled(True)
        self.summary_group.setMaximumHeight(250)
        self.progress_group.setMaximumHeight(250)

        self.setWindowTitle('Optimization Under Uncertainty (OUU)')


        # Connect signals
        self.node_radio.toggled.connect(self.chooseNode)
        self.node_combo.currentIndexChanged.connect(self.loadNodeData)
        self.modelFile_radio.toggled.connect(self.chooseModel)
        self.modelFileBrowse_button.clicked.connect(self.loadModelFileData)
        self.input_table.typeChanged.connect(self.setCounts)
        #self.input_table.typeChanged.connect(self.managePlots)
        #self.input_table.typeChanged.connect(self.manageBestValueTable)
        self.setFixed_button.clicked.connect(self.setFixed)
        self.setX1_button.clicked.connect(self.setX1)
        self.setX2_button.clicked.connect(self.setX2)
        self.setX3_button.clicked.connect(self.setX3)
        self.setX4_button.clicked.connect(self.setX4)
        self.z4NewSample_radio.toggled.connect(self.chooseZ4NewSample)
        self.z4LoadSample_radio.toggled.connect(self.chooseZ4LoadSample)
        self.x4SampleSize_spin.valueChanged.connect(self.setZ4RS)
        self.z4SubsetSize_spin.valueChanged.connect(self.setZ4RS)
        self.x3FileBrowse_button.clicked.connect(self.loadX3Sample)
        self.compressSamples_chk.toggled.connect(self.activateCompressSample)
        self.calcScenarios_button.clicked.connect(self.calcScenarios)
        self.x4SampleScheme_combo.currentIndexChanged.connect(self.setX4Label)
        self.x4FileBrowse_button.clicked.connect(self.loadX4Sample)
        self.x4RSMethod_check.toggled.connect(self.showZ4Subset)
        self.run_button.clicked.connect(self.analyze)
        self.z3_table.cellChanged.connect(self.z3TableCellChanged)
        self.z4_table.cellChanged.connect(self.z4TableCellChanged)

    def freeze(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    def semifreeze(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))

    def unfreeze(self):
        QtGui.QApplication.restoreOverrideCursor()

    def refresh(self):
        if self.dat is not None:
            nodes = sorted(self.dat.flowsheet.nodes.keys())
            items = ['Select node']
            items.extend(nodes)
            self.node_combo.clear()
            self.node_combo.addItems(items)
            self.node_radio.setChecked(True)
        else:
            self.node_radio.setEnabled(False)
            self.node_combo.setEnabled(False)
            self.modelFile_radio.setChecked(True)
        self.input_table.clearContents()
        self.input_table.setRowCount(0)
        self.modelFile_edit.clear()
        self.output_combo.clear()
        self.bestValue_table.clearContents()
        self.bestValue_table.setRowCount(2)
        self.clearPlots()

    def chooseNode(self, value):
        if value:
            self.node_combo.setEnabled(True)
            self.modelFile_edit.setEnabled(False)
            self.modelFileBrowse_button.setEnabled(False)

    def chooseModel(self, value):
        if value:
            self.node_combo.setEnabled(False)
            self.modelFile_edit.setEnabled(True)
            self.modelFileBrowse_button.setEnabled(True)

    def loadNodeData(self):
        nodeName = self.node_combo.currentText()
        if nodeName in ['', 'Select node']:
            return
        node = self.dat.flowsheet.nodes[nodeName]
        self.model = nodeToUQModel(nodeName, node)
        self.input_table.init(self.model, InputPriorTable.OUU)
        self.setFixed_button.setEnabled(True)
        self.setX1_button.setEnabled(True)
        self.setX2_button.setEnabled(True)
        self.setX3_button.setEnabled(True)
        self.setX4_button.setEnabled(True)
        self.initTabs()
        self.setCounts()

    def loadModelFileData(self):
        if platform.system() == 'Windows':
            allFiles = '*.*'
        else:
            allFiles = '*'
        fname,_ = QtGui.QFileDialog.getOpenFileName(self,
                                                   'Open Model File', self.filesDir,
                                                   'Model files (*.in *.dat *.psuade *.filtered);;All files (%s)' % allFiles)
        if fname == '':
            return
        self.filesDir, name = os.path.split(fname)
        self.modelFile_edit.setText(fname)
        self.model = LocalExecutionModule.readSampleFromPsuadeFile(fname)
        self.model = self.model.model
        self.input_table.init(self.model, InputPriorTable.OUU)
        self.setFixed_button.setEnabled(True)
        self.setX1_button.setEnabled(True)
        self.setX2_button.setEnabled(True)
        self.setX3_button.setEnabled(True)
        self.setX4_button.setEnabled(True)
        self.initTabs()
        self.setCounts()

    ##### Brenda:  Start here! #####
    def getSampleFileData(self):
        if platform.system() == 'Windows':
            allFiles = '*.*'
        else:
            allFiles = '*'

        fname,_ = QtGui.QFileDialog.getOpenFileName(self,
                                                   'Open Sample File', self.filesDir,
                                                   "Psuade Simple Files (*.smp);;CSV (Comma delimited) (*.csv);;All files (%s)" % allFiles)
        if fname == '':
            return (None, None)

        self.filesDir, name = os.path.split(fname)

        try:
            if fname.endswith('.csv'):
                data = LocalExecutionModule.readDataFromCsvFile(fname, askForNumInputs=False)
            else:
                data = LocalExecutionModule.readDataFromSimpleFile(fname, hasColumnNumbers = False)
            data = data[0]
            return (fname, data)
        except:
            import traceback
            traceback.print_exc()
            QtGui.QMessageBox.critical(self, 'Incorrect format',
                                       'File does not have the correct format! Please consult the users manual about the format.')
            return (None, None)

    def loadX3Sample(self):
        fname, data = self.getSampleFileData()
        if fname is None: return
        numInputs = data.shape[1]
        M3 = len(self.input_table.getDiscreteVariables()[0])
        if numInputs != M3:
            QtGui.QMessageBox.warning(self, "Number of variables don't match",
                                      'The number of variables from the file (%d) does not match the number of Z3 discrete variables (%d).  You will not be able to perform analysis until this is corrected.' % (numInputs, M3))
        else:
            self.compressSamples_chk.setEnabled(True)
            self.loadTable(self.z3_table, data)

    def loadTable(self, table, data):
        numSamples = data.shape[0]
        numInputs = data.shape[1]
        table.setRowCount(numSamples + 1)
        for r in xrange(numSamples):
            for c in xrange(numInputs):
                item = QtGui.QTableWidgetItem('%g' % data[r,c])
                table.setItem(r, c, item)
        table.resizeColumnsToContents()

    def z3TableCellChanged(self, row, col):
        self.randomVarTableCellChanged(self.z3_table, row, col)

    def z4TableCellChanged(self, row, col):
        self.randomVarTableCellChanged(self.z4_table, row, col)

    def randomVarTableCellChanged(self, table, row, col):
        if row == table.rowCount() - 1:
            table.setRowCount(table.rowCount() + 1)

    def writeTableToFile(self, table, fileName, numCols):
        names = {self.z3_table: 'Z3', self.z4_table: 'Z4'}
        assert(numCols <= table.columnCount())
        values = []
        for r in xrange(table.rowCount()):
            rowVals = []
            rowHasData = False
            rowFull = True
            for c in xrange(numCols):
                item = table.item(r,c)
                if not item:
                    rowFull = False
                else:
                    text = item.text()
                    if not text:
                        rowFull = False
                    else:
                        try:
                            rowVals.append(float(text))
                            rowHasData = True
                        except ValueError:
                            rowFull = False
            if not rowFull and rowHasData:
                break
            if rowFull:
                values.append(rowVals)
        if not values or (rowHasData and not rowFull):
            QtGui.QMessageBox.warning(self, "Missing data",
                                      'The %s table is missing required data!' % names[table])
            return False # Failed
        LocalExecutionModule.writeSimpleFile(fileName, values)
        return True

    def activateCompressSample(self, on):
        if on:
            rowCount = 0
            for r in self.z3_table.rowCount():
                for c in self.z3_table.columnCount():
                    rowFull = True
                    text = self.z3_table.item(r,c).text()
                    if not text:
                        rowFull = False
                        break
                    try:
                        float(text)
                    except ValueError:
                        rowFull = False
                        break
                if rowFull:
                    rowCount += 1
            if rowCount < 100:
                QtGui.QMessageBox.warning(self, "Not enough samples in file",
                                          'The file requires at least 100 samples for compression.')
                self.compressSamples_chk.setChecked(False)
                return
        self.calcScenarios_button.setEnabled(on)
        if self.scenariosCalculated:
            self.scenarioSelect_static.setEnabled(True)
            self.scenarioSelect_combo.setEnabled(True)

    def calcScenarios(self):
        self.freeze()
        self.writeTableToFile(self.z3_table, 'z3Samples.smp', len(self.input_table.getDiscreteVariables()[0]))
        self.scenarioFiles = OUU.compress('z3Samples.smp')
        if self.scenarioFiles is not None:
            self.scenarioSelect_combo.clear()
            for i, n in enumerate(sorted(self.scenarioFiles.keys())):
                self.scenarioSelect_combo.addItem(str(n))
                self.scenarioSelect_combo.setItemData(i, '%d bins per dimension' % self.scenarioFiles[n][1], QtCore.Qt.ToolTipRole)
            self.scenarioSelect_static.setEnabled(True)
            self.scenarioSelect_combo.setEnabled(True)
            self.scenariosCalculated = True
        self.unfreeze()


    def loadX4Sample(self):
        fname, inData = self.getSampleFileData()
        if fname is None: return
        numInputs = inData.shape[1]
        numSamples = inData.shape[0]
        self.z4SubsetSize_spin.setMaximum(numSamples)
        self.z4SubsetSize_spin.setValue(min(numSamples,100))
        M4 = len(self.input_table.getContinuousVariables()[0])
        if numInputs != M4:
            QtGui.QMessageBox.warning(self, "Number of variables don't match",
                                      'The number of input variables from the file (%d) does not match the number of Z4 continuous variables (%d).  You will not be able to perform analysis until this is corrected.' % (numInputs, M4))
        else:
            self.loadTable(self.z4_table, inData)

    def setX4Label(self):
        method = self.x4SampleScheme_combo.currentText()
        if method in [SamplingMethods.getFullName(SamplingMethods.LH),
                      SamplingMethods.getFullName(SamplingMethods.LPTAU)]:
            self.x4SampleSize_label.setText('Sample Size')
            numM1 = len(self.input_table.getPrimaryVariables()[0])
            self.x4SampleSize_spin.setRange(numM1 + 1,1000)
            self.x4SampleSize_spin.setValue(numM1 + 1)
            self.x4SampleSize_spin.setSingleStep(1)
        elif method == SamplingMethods.getFullName(SamplingMethods.FACT):
            self.x4SampleSize_label.setText('Number of Levels') 
            self.x4SampleSize_spin.setRange(3,100)
            self.x4SampleSize_spin.setValue(3)
            self.x4SampleSize_spin.setSingleStep(2)

    def initTabs(self):
        self.tabs.setEnabled(True)
        self.tabs.setCurrentIndex(0)
        self.output_combo.setEnabled(True)
        self.output_combo.clear()
        self.output_combo.addItems(self.model.getOutputNames())
        self.mean_radio.setChecked(True)
        self.betaDoubleSpin.setValue(0)
        self.alphaDoubleSpin.setValue(0.5)
        self.secondarySolver_combo.setCurrentIndex(0)
        self.compressSamples_chk.setChecked(False)
        self.compressSamples_chk.setEnabled(False)
        self.scenariosCalculated = False
        self.scenarioSelect_static.setEnabled(False)
        self.scenarioSelect_combo.setEnabled(False)
        self.scenarioSelect_combo.clear()
        self.x4SampleScheme_combo.setCurrentIndex(0)
        self.x4SampleSize_label.setText('Sample Size')
        self.x4SampleSize_spin.setValue(5)
        self.x4SampleSize_spin.setRange(5,1000)
        self.x4RSMethod_check.setChecked(False)
        self.run_button.setEnabled(True)      # TO DO: disable until inputs are validated

        self.bestValue_table.setColumnCount(1)
        self.bestValue_table.clearContents()
        
        # Plots
        self.plots_group = QtGui.QGroupBox()
        self.plotsLayout = QtGui.QVBoxLayout()
        self.plots_group.setLayout(self.plotsLayout)
        self.progressScrollArea.setMinimumHeight(150)
        self.progressScrollArea.setWidget(self.plots_group)
        self.plots_group.setMinimumHeight(150)
        self.objFig = Figure(
            figsize=(400,200),
            dpi=72,
            facecolor=(1,1,1),
            edgecolor=(0,0,0),
            tight_layout = True)
        self.objCanvas = FigureCanvas(self.objFig)
        self.objFigAx = self.objFig.add_subplot(111)
        self.objFigAx.set_title('OUU Progress')
        self.objFigAx.set_ylabel('Objective')
        self.objFigAx.set_xlabel('Iteration')
        self.plotsLayout.addWidget(self.objCanvas)
        self.objCanvas.setParent(self.plots_group)
        self.inputPlots = []

        self.objXPoints = []
        self.objYPoints = []
        self.objPlotPoints = None

    def manageBestValueTable(self):
        self.bestValue = None
        names, indices = self.input_table.getPrimaryVariables()
        self.bestValue_table.setRowCount(len(names) + 2)
        self.bestValue_table.setVerticalHeaderLabels(['Iteration', 'Objective Value'] + names)
        self.bestValue_table.clearContents()

    def setBestValueTable(self, iteration, objValue, inputs):
        item = self.bestValue_table.item(0, 0) #iteration
        if item is None:
            self.bestValue_table.setItem(0, 0, QtGui.QTableWidgetItem('%d' % iteration))
        else:
            item.setText('%d' % iteration)

        if self.bestValue == None or objValue < self.bestValue:
            self.bestValue = objValue
            item = self.bestValue_table.item(1, 0) #objective value
            if item is None:
                self.bestValue_table.setItem(1, 0, QtGui.QTableWidgetItem('%f' % objValue))
            else:
                item.setText('%f' % objValue)

            for i, value in enumerate(inputs):
                item = self.bestValue_table.item(i + 2, 0) #input
                if item is None:
                    self.bestValue_table.setItem(i + 2, 0, QtGui.QTableWidgetItem('%f' % value))
                else:
                    item.setText('%f' % value)
            

    def addPlotValues(self, valuesDict):
        self.addPointToObjPlot(valuesDict['objective'])
        self.addToInputPlots(valuesDict['input'])
        (iteration, objValue) = valuesDict['objective']
        self.setBestValueTable(iteration, objValue, valuesDict['input'][1:])

    def addPointToObjPlot(self, x):
        self.objXPoints.append(x[0])
        self.objYPoints.append(x[1])
        self.objFigAx.plot(self.objXPoints, self.objYPoints, 'bo')
        self.objCanvas.draw()

    def addToInputPlots(self, x):
        for i in xrange(len(self.inputPoints)):
            self.inputPoints[i].append(x[i])
            if i > 0:
                self.inputPlots[i - 1]['ax'].plot(self.inputPoints[0], self.inputPoints[i], 'bo')
                self.inputPlots[i - 1]['canvas'].draw()

    def managePlots(self):
        names, indices = self.input_table.getPrimaryVariables()
        if len(self.inputPlots) < len(names):  #add plots
            for i in xrange(len(self.inputPlots), len(names)):
                fig = Figure(
                    figsize=(400,200),
                    dpi=72,
                    facecolor=(1,1,1),
                    edgecolor=(0,0,0),
                    tight_layout = True)
                canvas = FigureCanvas(fig)
                ax = fig.add_subplot(111)
                ax.set_xlabel('Iteration')
                self.inputPlots.append({'fig': fig, 'canvas': canvas, 'ax': ax})
                self.plotsLayout.addWidget(canvas)
                canvas.setParent(self.plots_group)
        elif len(self.inputPlots) > len(names): #remove plots
            for i in xrange(len(names), len(self.inputPlots)):
                self.inputPlots[i]['fig'].clf()
                self.inputPlots[i]['canvas'].deleteLater()
                del self.inputPlots[i]

        for i, name in enumerate(names):
            self.inputPlots[i]['ax'].set_ylabel('Primary Input %s' % name)
        
        self.plots_group.setMinimumHeight(190 * (len(names) + 1))

        self.inputPoints = [[] for i in xrange(len(names) + 1)]
        self.clearPlots()
            
    def clearPlots(self):
        self.objXPoints = []
        self.objYPoints = []
        if 'objFigAx' in self.__dict__ and len(self.objFigAx.lines) > 0:
            self.objFigAx.lines = []
            self.objFigAx.relim()
            #self.objFigAx.set_xlim([0.0, 1.0])
            self.objCanvas.draw()

        if 'inputPoints' in self.__dict__:
            self.inputPoints = [[] for i in xrange(len(self.inputPoints))]
            for i in xrange(1, len(self.inputPoints)):
                if len(self.inputPlots[i - 1]['ax'].lines) > 0:
                    self.inputPlots[i - 1]['ax'].lines = []
                    self.inputPlots[i - 1]['canvas'].draw()

    def setFixed(self):
        self.input_table.setCheckedToType(0)

    def setX1(self):
        self.input_table.setCheckedToType(1)

    def setX2(self):
        self.input_table.setCheckedToType(2)

    def setX3(self):
        varNames = self.input_table.setCheckedToType(3)

    def setX4(self):
        varNames = self.input_table.setCheckedToType(4)

    def setCounts(self):
        # update counts

        M0 = len(self.input_table.getFixedVariables()[0])
        M1 = len(self.input_table.getPrimaryVariables()[0])
        M2 = len(self.input_table.getRecourseVariables()[0])
        M3Vars = self.input_table.getDiscreteVariables()[0]
        M3 = len(M3Vars)
        M4Vars = self.input_table.getContinuousVariables()[0]
        M4 = len(M4Vars)
        self.fixedCount_static.setText('# Fixed: %d' % M0)
        self.x1Count_static.setText('# Primary Opt Vars: %d' % M1)
        self.x2Count_static.setText('# Recourse Opt Vars: %d' % M2)
        self.x3Count_static.setText('# Discrete RVs: %d' % M3)
        self.x4Count_static.setText('# Continuous RVs: %d' % M4)

        hideInnerSolver = (M2 == 0)
        self.secondarySolver_label.setHidden(hideInnerSolver)
        self.secondarySolver_combo.setHidden(hideInnerSolver)

        hideZ3Group = (M3 == 0)
        hideZ4Group = (M4 == 0)
        if hideZ3Group and hideZ4Group: #Hide tab
            if self.tabs.widget(1) == self.uqTab:
                if self.tabs.currentIndex() == 1:
                    self.tabs.setCurrentIndex(0)
                self.tabs.removeTab(1)
        else: #Show tab
            if self.tabs.widget(1) != self.uqTab:
                self.tabs.insertTab(1, self.uqTab, 'UQ Setup')

        numCols = max(len(M3Vars), self.z3_table.columnCount())
        self.z3_table.setColumnCount(numCols)
        self.z3_table.setHorizontalHeaderLabels(M3Vars + ['Unused'] * (numCols - len(M3Vars)))
        numCols = max(len(M4Vars), self.z4_table.columnCount())
        self.z4_table.setColumnCount(numCols)
        self.z4_table.setHorizontalHeaderLabels(M4Vars + ['Unused'] * (numCols - len(M4Vars)))

        self.z3_group.setHidden(hideZ3Group)
        self.z4_group.setHidden(hideZ4Group)

        if self.x4SampleScheme_combo.currentText() == SamplingMethods.getFullName(SamplingMethods.FACT):
            self.x4SampleSize_spin.setMinimum(3)
        else:
            self.x4SampleSize_spin.setMinimum(M4 + 1)

        self.z4SubsetSize_spin.setMinimum(M4 + 1)

    def chooseZ4NewSample(self, value):
        if value:
            self.x4SampleScheme_label.setEnabled(True)
            self.x4SampleScheme_combo.setEnabled(True)
            self.x4SampleSize_label.setEnabled(True)
            self.x4SampleSize_spin.setEnabled(True)
            self.x4FileBrowse_button.setEnabled(False)
            self.showZ4Subset(False)
            self.setZ4RS(self.x4SampleSize_spin.value())
            self.z4_table.setEnabled(False)

    def chooseZ4LoadSample(self, value):
        if value:
            self.x4SampleScheme_label.setEnabled(False)
            self.x4SampleScheme_combo.setEnabled(False)
            self.x4SampleSize_label.setEnabled(False)
            self.x4SampleSize_spin.setEnabled(False)
            self.x4FileBrowse_button.setEnabled(True)
            self.showZ4Subset(True)
            self.setZ4RS(self.z4SubsetSize_spin.value())
            self.z4_table.setEnabled(True)

    def setZ4RS(self, value):
        if value <= 300:
            rs = ResponseSurfaces.getFullName(ResponseSurfaces.KRIGING)
        elif value <= 600:
            rs = ResponseSurfaces.getFullName(ResponseSurfaces.RBF)
        else:
            rs = ResponseSurfaces.getFullName(ResponseSurfaces.MARS)
        self.x4RSMethod_check.setText('Use Response Surface (%s)' % rs)

    def showZ4Subset(self, show):
        if show and self.x4RSMethod_check.isChecked() and self.z4LoadSample_radio.isChecked():
            self.z4SubsetSize_label.setEnabled(True)
            self.z4SubsetSize_spin.setEnabled(True)
        else:
            self.z4SubsetSize_label.setEnabled(False)
            self.z4SubsetSize_spin.setEnabled(False)


    def setupPSUADEClient(self):
        curDir = os.getcwd()
        #Copy needed files
        dest = os.path.join(curDir, 'foqusPSUADEClient.py')
        mydir = os.path.dirname(__file__)
        src = os.path.join(mydir, 'foqusPSUADEClient.py')
        shutil.copyfile(src, dest)
        os.chmod(dest, 0700)
        return dest

    def analyze(self):

        if self.run_button.text() == 'Run OUU': # Run OUU
            names, indices = self.input_table.getPrimaryVariables()
            if len(names) == 0:
                QtGui.QMessageBox.information(self, 'No Primary Variables',
                                              'At least one input must be a primary variable!')
                return

            if not self.input_table.checkValidInputs():
                QtGui.QMessageBox.information(self, 'Input Table Distributions',
                                              'Input table distributions are either not correct or not filled out completely!')
                return

            if self.compressSamples_chk.isChecked() and not self.scenariosCalculated:
                QtGui.QMessageBox.information(self, 'Compress Samples Not Calculated',
                                              'You have elected to compress samples for discrete random variables (Z3), but have not selected the sample size to use!')
                return

            Common.initFolder(OUU.dname)

            self.managePlots()
            self.clearPlots()
            self.manageBestValueTable()
            self.summary_group.setTitle('Best So Far')

            xtable = self.input_table.getTableValues()

            # get arguments for ouu()
            model = copy.deepcopy(self.model)
            inputNames = model.getInputNames()
            inputTypes = list(model.getInputTypes())
            defaultValues = model.getInputDefaults()
            for row in xtable:
                if row['type'] == 'Fixed':
                    modelIndex = inputNames.index(row['name'])
                    inputTypes[modelIndex] = Model.FIXED
                    defaultValues[modelIndex] = row['value']
            #print inputTypes
            #print defaultValues
            model.setInputTypes(inputTypes)
            model.setInputDefaults(defaultValues)
            data = SampleData(model)
            fname = 'ouuTemp.dat'
            data.writeToPsuade(fname)

            M1 = len(self.input_table.getPrimaryVariables()[0])
            M2 = len(self.input_table.getRecourseVariables()[0])
            M3 = len(self.input_table.getDiscreteVariables()[0])
            M4 = len(self.input_table.getContinuousVariables()[0])

            y = self.output_combo.currentIndex() + 1
            if self.mean_radio.isChecked():
                phi = {'type':1}
            elif self.meanWithBeta_radio.isChecked():
                beta = self.betaDoubleSpin.value()
                phi = {'type':2, 'beta':beta}
            elif self.alpha_radio.isChecked():
                alpha = self.alphaDoubleSpin.value()
                phi = {'type':3, 'alpha':alpha}
            x3sample = None
            if M3 > 0:
                if self.compressSamples_chk.isChecked():
                    selectedSamples = int(self.scenarioSelect_combo.currentText())
                    sfile = self.scenarioFiles[selectedSamples][0]
                else:
                    sfile = 'z3Samples.smp'
                    success = self.writeTableToFile(self.z3_table, sfile, M3)
                    if not success:
                        return
                    if sfile.endswith('.csv'): # Convert .csv file to simple file
                        newFileName = OUU.dname + os.sep + os.path.basename(fname)[:-4] + '.smp'
                        inData = LocalExecutionModule.readDataFromCsvFile(sfile, askForNumInputs=False)
                        LocalExecutionModule.writeSimpleFile(newFileName, inData[0])
                        sfile = newFileName

                #print 'x3 file is', sfile
                x3sample = {'file':sfile}                           # x3sample file
                data,_, numInputs, _ = LocalExecutionModule.readDataFromSimpleFile(sfile, hasColumnNumbers=False)
                if numInputs != M3:
                    QtGui.QMessageBox.critical(self, "Number of variables don't match",
                                              'The number of variables from the file (%d) does not match the number of Z3 discrete variables (%d).  You will not be able to perform analysis until this is corrected.' % (numInputs, M3))
                    return
            useRS = self.x4RSMethod_check.isChecked()
            x4sample = None
            if self.z4NewSample_radio.isChecked():
                method = self.x4SampleScheme_combo.currentText()
                method = SamplingMethods.getEnumValue(method)
                N = self.x4SampleSize_spin.value()
                if method in [SamplingMethods.LH,SamplingMethods.LPTAU]:
                    x4sample = {'method':method, 'nsamples':N}  # number of samples (range: [M1+1,1000])
                elif method == SamplingMethods.FACT:
                    x4sample = {'method':method, 'nlevels':N}   # number of levels (range: [3,100])
            else:
                sfile = 'z4Samples.smp'
                success = self.writeTableToFile(self.z4_table, sfile, M4)
                if not success:
                    return
                if len(sfile) == 0:
                    QtGui.QMessageBox.critical(self, 'Missing file',
                               'Z4 sample file not specified!')
                    return

                if sfile.endswith('.csv'): # Convert .csv file to simple file
                    newFileName = OUU.dname + os.sep + os.path.basename(fname)[:-4] + '.smp'
                    inData = LocalExecutionModule.readDataFromCsvFile(sfile, askForNumInputs=False)
                    LocalExecutionModule.writeSimpleFile(newFileName, inData[0])
                    sfile = newFileName

                inData, outData, numInputs, numOutputs = LocalExecutionModule.readDataFromSimpleFile(sfile, hasColumnNumbers=False)
                numSamples = inData.shape[0]
                if numInputs != M4:
                    QtGui.QMessageBox.critical(self, "Number of variables don't match",
                                              'The number of input variables from the file (%d) does not match the number of Z4 continuous variables (%d).  You will not be able to perform analysis until this is corrected.' % (numInputs, M4))
                    return
                if numSamples <= M4:
                    QtGui.QMessageBox.critical(self, 'Not enough samples',
                               'Z4 sample file must have at least %d samples!' % (M4 + 1))
                    return

                x4sample = {'file': sfile}                      # x4sample file, must have at least M4+1 samples

                if useRS:
                    Nrs = self.z4SubsetSize_spin.value()     # add spinbox to get number of samples to generate RS
                    x4sample['nsamplesRS'] = Nrs               # TO DO: make sure spinbox has M4+1 as min and x4sample's sample size as max

            useBobyqa = False
            if 'simulator' in self.secondarySolver_combo.currentText():
                useBobyqa = True  # use BOBYQA if driver is a simulator, not an optimizer

            self.run_button.setText('Stop')
            optDriver = None
            ensembleOptDriver = None
            if self.node_radio.isChecked():
                ensembleOptDriver = self.setupPSUADEClient()
                optDriver = ensembleOptDriver
                listener = listen.foqusListener(self.dat)
                variableNames = []
                fixedNames = []
                for row in xtable:
                    #print row
                    if row['type'] == 'Fixed':
                        fixedNames.append(row['name'])
                    else:
                        variableNames.append(row['name'])
                #print fixedNames, variableNames
                #print variableNames + fixedNames
                listener.inputNames = variableNames + fixedNames
                outputNames = self.model.getOutputNames()
                listener.outputNames = [outputNames[y-1]]
                listener.failValue = -111111
                self.listenerAddress = listener.address
                listener.start()

            # print M1, M2, M3, M4, useBobyqa
            self.OUUobj = OUU()
            try:
                if self.modelFile_radio.isChecked():
                    results = self.OUUobj.ouu(fname,y,xtable,phi,x3sample=x3sample,x4sample=x4sample,useRS=useRS,useBobyqa=useBobyqa,
                                      plotSignal = self.plotSignal, endFunction=self.finishOUU)

                elif (M3 + M4 == 0) or (M2 > 0 and useBobyqa):
                    # print 'optdriver'
                    results = self.OUUobj.ouu(fname,y,xtable,phi,x3sample=x3sample,x4sample=x4sample,useRS=useRS,useBobyqa=useBobyqa,
                                      optDriver = ensembleOptDriver, plotSignal = self.plotSignal, endFunction=self.finishOUU)
                else:
                    # print 'ensembleoptdriver'
                    results = self.OUUobj.ouu(fname,y,xtable,phi,x3sample=x3sample,x4sample=x4sample,useRS=useRS,useBobyqa=useBobyqa,
                                      ensOptDriver = ensembleOptDriver, plotSignal = self.plotSignal, endFunction=self.finishOUU)
            except:
                import traceback
                traceback.print_exc()
                if self.node_radio.isChecked():
                    # stop the listener
                    conn = Client(self.listenerAddress)
                    conn.send(['quit'])
                    conn.close()

                # enable run button
                self.run_button.setEnabled(True)
                return
        else: # Stop OUU
            self.OUUobj.stopOUU()
            self.run_button.setText('Run OUU')

    def finishOUU(self):
        if self.node_radio.isChecked():
            # stop the listener
            conn = Client(self.listenerAddress)
            conn.send(['quit'])
            conn.close()

        # enable run button
        self.run_button.setText('Run OUU')
        self.run_button.setEnabled(True)

        if not self.OUUobj.getHadError():
            self.summary_group.setTitle('Best Solution')
    #        results.replace('X','Z')
    #
    #        QtGui.QMessageBox.information(self, 'OUU Results', results)

            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle('FOQUS OUU Finished')
            msgBox.setText('Optimization under Uncertainty analysis finished')
            self.result = msgBox.exec_()

    def getResult(self):
        return self.result

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    frame = ouuSetupFrame()
    frame.show()
    app.exec_()