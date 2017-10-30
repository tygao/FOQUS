'''
    mainWindows.py

    * This is the main FOQUS window

    John Eslick, Carnegie Mellon University, 2014

    This Material was produced under the DOE Carbon Capture Simulation
    Initiative (CCSI), and copyright is held by the software owners:
    ORISE, LANS, LLNS, LBL, PNNL, CMU, WVU, et al. The software owners
    and/or the U.S. Government retain ownership of all rights in the
    CCSI software and the copyright and patents subsisting therein. Any
    distribution or dissemination is governed under the terms and
    conditions of the CCSI Test and Evaluation License, CCSI Master
    Non-Disclosure Agreement, and the CCSI Intellectual Property
    Management Plan. No rights are granted except as expressly recited
    in one of the aforementioned agreements.
'''
import time
import math
import logging
import subprocess
import collections
import array
import platform
import functools
import os
from foqus_lib.framework.graph.graph import *
from foqus_lib.framework.session.session import *
from foqus_lib.framework.session.hhmmss import *
from foqus_lib.framework.sim.turbineConfiguration import *
from foqus_lib.framework import optimizer
from foqus_lib.framework.uq.Model import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QActionGroup,\
    QMenu, QAction, QToolBar
from PyQt5.QtGui import QIcon, QKeySequence
from foqus_lib.gui import icons_rc
from foqus_lib.gui.dialogs.variableBrowser import *
from foqus_lib.gui.main.Dash import *
from foqus_lib.gui.main.settingsFrame import *
from foqus_lib.gui.main.sessionDescriptionEdit import *
from foqus_lib.gui.main.saveMetadataDialog import *
from foqus_lib.gui.model.gatewayUploadDialog import *
from foqus_lib.gui.model.dmfUploadDialog import *
from foqus_lib.gui.flowsheet.drawFlowsheet import *
from foqus_lib.gui.flowsheet.nodePanel import *
from foqus_lib.gui.flowsheet.edgePanel import *
from foqus_lib.gui.flowsheet.flowsheetSettingsDialog import *
from foqus_lib.gui.flowsheet.dataBrowserDialog import *
from foqus_lib.gui.basic_data.basicDataParentFrame import *
from foqus_lib.gui.optimization.optSetupFrame import *
from foqus_lib.gui.ouu.ouuSetupFrame import *
from foqus_lib.gui.uq.uqSetupFrame import *
from foqus_lib.gui.uq.updateUQModelDialog import *
from foqus_lib.gui.help.helpBrowser import*
from foqus_lib.gui.surrogate.surrogateFrame import*
from foqus_lib.gui.heatIntegration.heatIntegrationFrame import*
from ConfigParser import *
from StringIO import StringIO
#
####
# Both the DMF and DRM builder can be conditionally imported.  Need to
# call the import functions before initializing the main window if those
# components are to be used.
#####

# Import DMF in function call to avoid importing anything if it is not
# wanted
dmf_lib = None
useDMF = False
Py4JGateway = None
Common = None
DMFBrowser = None
from dmf_lib.common.common import *
# Move this out from importDMF so that DMF lite will work without
# needing to enable the checkbox under settings
try:
    from dmf_lib.dmf_browser import DMFBrowser
except:
    logging.getLogger("foqus." + __name__)\
        .exception('Failed to import or launch DMFBrowser')
    useDMF = False


def importDMF():
    '''
        Import the dmf in a function call to allow it to be
        conditionally
    '''
    global Py4JGateway
    global Common
    global dmf_lib
    global DMFBrowser
    global useDMF
    try:
        from dmf_lib.gateway.gateway import Py4JGateway
        from dmf_lib.common.methods import Common
        useDMF = True
        err = Py4JGateway(True).startupGateway()
        if err == 0:
            startedDMF = True
            logging.getLogger("foqus." + __name__).debug(
                "Started DMF gateway.")
        else:
            logging.getLogger("foqus." + __name__).warn(
                "Not critical error: Error starting DMF gateway. "
                "Error code: {0}".format(err))
            useDMF = False
    except:
        logging.getLogger("foqus." + __name__)\
            .exception('Failed to import or launch DMF')
        useDMF = False

# Import DRM-builder, doesn't work if not in windows so can be imported
# conditionally
mainDRM = None
DRMManager = None

def importdrm():
    '''
        Import the drm builder in a function to allow it to be imported
        conditionally
    '''
    global mainDRM
    global DRMManager
    try:
        import foqus_lib.gui.drmbuilder.main_drmbuilder as mainDRM
        import foqus_lib.framework.drmbuilder.drm_manager as DRMManager
    except Exception:
        logging.getLogger("foqus." + __name__).exception(
            "Error importing D-RM builder")
        mainDRM = None
        DRMManager = None


class mainWindow(QMainWindow):
    '''
        This is the FOQUS main window class
    '''
    def __init__(self,
                 title,
                 w,
                 h,
                 dat,
                 splash = None,
                 showUQ = True,
                 showOpt = True,
                 showOuu = True,
                 showDRM = True,
                 showBasicData = False,
                 ts = None):
        '''
            Main window initialization
            title: Title bar text
            w: Width (pixels)
            h: Height (pixels)
            dat: Problem information, session object
            splash: Splash screen object (also reuse for about)
            showUQ: if false the uq interface is hidden
            showOpt: if true the optimization interface is hidden
            showOuu: if true the optimization interface is hidden
        '''
        QMainWindow.__init__(self)  # call base constructor
        self.resize(w,h)
        self.setWindowTitle(title)
        self.dat = dat # This is a session object
        self.dat.mainWin = self
        self.splash = splash
        self.showOuu = showOuu
        self.showDRM = showDRM
        self.showBasicDataTab = showBasicData
        self.setIconPaths() # stores icon paths in a dict
        self.statusBar() # add a status bar to the main window
        self.statusBar().showMessage("Working Directory: {0}".format(
            os.path.abspath(os.getcwd())))
        self.mainWidget = QStackedWidget(self)
        self.setCentralWidget(self.mainWidget)
        ### Create the main window widgets for stacked widget
        #  Create the flowsheet editor/viewer
        self.flowsheetEditor = drawFlowsheet(self.dat, self)
        self.flowsheetEditor.nodeSelected.connect(self.setNodePanel)
        self.flowsheetEditor.edgeSelected.connect(self.setEdgePanel)
        self.flowsheetEditor.updateEdgeEdit.connect(
            self.applyAndUpdateEdgeEdit)
        #self.flowsheetEditor.noneSelected.connect(self.fsSelectNone)
        self.flowsheetEditor.updateFS.connect(self.refreshFlowsheet)
        self.flowsheetEditor.updateFSPos.connect(self.refreshNodeCoord)
        # Set-up dash/home widget
        self.dashFrame = dashFrame(self)
        self.dashFrame.buttonBox.rejected.connect(self.cancelSession)
        self.dashFrame.buttonBox.button(
            QDialogButtonBox.Help).clicked.connect(self.showHelp)
        #self.dashFrame.buttonBox.button(
        #    QDialogButtonBox.Cancel).setEnabled(False)
        #self.dashFrame.descriptionEditButton.clicked.connect(
        #    self.sessionDescEdit)
        # Basic Data tab
        self.basicDataFrame = basicDataParentFrame(useDMF, parent=self)
        # Set up UQ setup widget
        self.uqSetupFrame = uqSetupFrame(self.dat, self)
        # set-up opt setup widget
        self.optSetupFrame = optSetupFrame(self.dat, self)
        self.optSetupFrame.setStatusBar.connect(self.setStatus)
        self.optSetupFrame.updateGraph.connect(self.refreshFlowsheet)
        # OUU screen
        self.ouuSetupFrame = ouuSetupFrame(self.dat, self)
        # surrogate screen
        self.surFrame = surrogateFrame(self.dat, self)
        self.surFrame.setStatusBar.connect(self.setStatus)
        # heat integration screen
        self.heatIntFrame = heatIntegrationFrame(self.dat, self)
        # settings screen
        self.fsettingsFrame = settingsFrame(self.dat, self)
        self.fsettingsFrame.waiting.connect(self.setCursorWaiting)
        self.fsettingsFrame.notwaiting.connect(self.setCursorNormal)
        #Data-Browser widget
        self.dataBrowserDialog = dataBrowserDialog(self.dat, self)
        ## Add widgets to stacked widget
        self.mainWidget.addWidget(self.dashFrame)        # 0
        self.mainWidget.addWidget(self.basicDataFrame)   # 1
        self.mainWidget.addWidget(self.flowsheetEditor)  # 2
        self.mainWidget.addWidget(self.uqSetupFrame)     # 3
        self.mainWidget.addWidget(self.optSetupFrame)    # 4
        self.mainWidget.addWidget(self.ouuSetupFrame)    # 5
        self.mainWidget.addWidget(self.surFrame)         # 6
        self.mainWidget.addWidget(self.heatIntFrame)     # 7
        if showDRM and mainDRM is not None: # 8
            self.drmFrame = mainDRM.MainDRMBuilder(self.dat, self)
            self.mainWidget.addWidget(self.drmFrame)
        else: # 8
            self.drmFrame = QWidget(self)
            self.mainWidget.addWidget(self.drmFrame)
        self.mainWidget.addWidget(self.fsettingsFrame)   # 9
        # make a dictionary to look up widget indexes in stacked widget
        self.screenIndex = {
            'home': 0,
            'basicData':1,
            'flow':2,
            'uq':3,
            'opt':4,
            'ouu':5,
            'surrogate':6,
            'heatInt':7,
            'drmbuilder':8,
            'settings':9}
        ## Create toolboxes for editing nodes and edges in flowsheet
        #node editor
        self.nodeDock = nodeDock(self.dat, self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.nodeDock)
        self.nodeDock.redrawFlowsheet.connect(self.refreshFlowsheet)
        self.nodeDock.waiting.connect(self.setCursorWaiting)
        self.nodeDock.notwaiting.connect(self.setCursorNormal)
        self.nodeDock.hide()
        # Edge editor
        self.edgeDock = edgeDock(self.dat, self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.edgeDock)
        self.edgeDock.redrawFlowsheet.connect(self.refreshFlowsheet)
        self.edgeDock.hide()
        ##create help dock widget
        self.helpDock = helpBrowserDock(self, self.dat)
        self.helpDock.hideHelp.connect(self.hideHelp)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.helpDock)
        self.helpDock.hide()
        self.helpDock.showAbout.connect(self.showAbout)
        ## Center the flowsheet view on flowsheet
        self.flowsheetEditor.center()
        ## Create a variable browser dialog browser
        self.varBrowse = variableBrowser(self.dat, self)
        ## Create the toolbar and menu bar for mainwindow
        #   (there is no menu anymore)
        self.makeMainToolBar()
        self.makeDrawingToolBar()
        # Update the main window set a few things and show the window
        self.refresh()
        self.app = None  # Qt application
        self.runningSingle = False
        self.setWindowIcon(QIcon(self.iconPaths['main']))
        self.show()
        if ts is not None:
            self.tstimer = QtCore.QTimer(self)
            self.connect(self.tstimer, QtCore.SIGNAL("timeout()"),
                lambda: self.runTestScript(ts))
            self.tstimer.start(2000)
        else:
            self.tstimer = None

    def clearOldMessages(self):
        '''
            This function clears old mesages from the gui
            when loading or creating a new session.
        '''
        self.optSetupFrame.clearOld()
        self.surFrame.clearOld()

    def setStatus(self, msg):
        '''
            Set the mainwindow status bar to display msg
        '''
        self.statusBar().showMessage(msg)

    def setCursorWaiting(self):
        '''
            This changes the mouse cursor to indicate that something
            is processing and it will take some time to finish
        '''
        if self.app != None:
            self.app.setOverrideCursor(QtCore.Qt.BusyCursor)

    def setCursorNormal(self):
        '''
            This sets the mouse cursor back to normal
        '''
        if self.app != None:
            self.app.restoreOverrideCursor()

    def enable(self, b):
        '''
            This function enables or disables forms that allow editing
            of the flowsheet or other session data while something is
            running in another thread.  This is to prevent
            inconsitencies when a problem is running but the problem
            or flowsheet have been changed in the meantime
            ---args---
            b: bool true to enable false to disable
        '''
        pass

    def setIconPaths(self):
        '''
            Set the location of various icons to make it easier
            to edit later, it may be nice to have them in one place
        '''
        self.iconPaths = {
            'nodeEdit':      ':/icons/icons/nodeEditor.svg',
            'edgeEdit':      ':/icons/icons/edgeEditor.svg',
            'graphEdit':     ':icons/icons/graphEditor.svg',
            'main':          ':/icons/icons/icons_exe/foqus_icon.svg',
            'center':        ':/icons/icons/center.svg',
            'add':           ':/icons/icons/add.svg',
            'new':           ':/icons/icons/new.svg',
            'defaults':      ':/icons/icons/defaults.svg',
            'logout':        ':/icons/icons/logout.svg',
            'exit':          ':/icons/icons/exit.svg',
            'exit48':        ':/icons/icons/exit48',
            'setting':       ':/icons/icons/setting.svg',
            'settings48':    ':/icons/icons/settings48.svg',
            'load':          ':/icons/icons/load.svg',
            'save':          ':/icons/icons/save.svg',
            'select':        ':/icons/icons/select.svg',
            'edit':          ':/icons/icons/edit.svg',
            'addNode':       ':/icons/icons/addNode.svg',
            'addEdge':       ':/icons/icons/addEdge.svg',
            'delete':        ':/icons/icons/delete.svg',
            'run':           ':/icons/icons/run.svg',
            'stop':          ':/icons/icons/stop.svg',
            'up':            ':/icons/icons/up.svg',
            'down':          ':/icons/icons/down.svg',
            'left':          ':/icons/icons/left.svg',
            'right':         ':/icons/icons/right.svg',
            'help':          ':/icons/icons/help48.svg',
            'optimize':      ':/icons/icons/opt48.svg',
            'ouu':           ':/icons/icons/ouu48.svg',
            'uq':            ':/icons/icons/uq48.svg',
            'data':          ':/icons/icons/data.svg',
            'data48':        ':/icons/icons/data48.svg',
            'drm48':         ':/icons/icons/drm48.svg',
            'basicData48':   ':/icons/icons/basicData48.svg',
            'opt_run':       ':/icons/icons/opt48_run.svg',
            'uq_run':        ':/icons/icons/uq48_start.svg',
            'flow':          ':/icons/icons/fs48.svg',
            'home':          ':/icons/icons/home48.svg',
            'dash':          ':/icons/icons/dash48.svg',
            'tear':          ':/icons/icons/tear.svg',
            'model':         ':/icons/icons/model.svg',
            'model48':       ':/icons/icons/model48.svg',
            'surrogate48':   ':/icons/icons/surrogate48.svg',
            'heatEx48':      ':icons/icons/heatEx48.svg'}

    def makeMainToolBar(self):
        '''
            Make the big main window toolbar
        '''
        #Make toolbar
        self.toolbarMain = self.addToolBar('Main')
        self.toolbarMain.setIconSize(QtCore.QSize(56, 56))
        self.toolbarMain.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolbarMain.setMovable(False)
        self.mainToolbarActionGroup = QActionGroup(self)
        # Add the session button to main toolbar
        self.makeSessionMenu()
        self.homeAction = QAction(
            QIcon(self.iconPaths['home']),
            'Session',
            self)
        self.homeAction.setMenu(self.mainMenu)
        self.homeAction.triggered.connect(self.showDash)
        self.homeAction.setCheckable(True)
        self.homeAction.setChecked(True)
        self.mainToolbarActionGroup.addAction(self.homeAction)
        self.toolbarMain.addAction(self.homeAction)
        #separator
        self.toolbarMain.addSeparator()
        #Basic data action
        self.basicDataAction = QAction(
            QIcon(self.iconPaths['basicData48']),
            'Basic Data',
            self)
        self.basicDataAction.triggered.connect(self.showBasicData)
        self.basicDataAction.setCheckable(True)
        self.mainToolbarActionGroup.addAction(self.basicDataAction)
        self.toolbarMain.addAction(self.basicDataAction)
        # Flowsheet action
        self.fsEditAction = QAction(
            QIcon(self.iconPaths['flow']),
            'Flowsheet',
            self)
        self.fsEditAction.triggered.connect(self.showFlow)
        self.fsEditAction.setCheckable(True)
        self.mainToolbarActionGroup.addAction(self.fsEditAction)
        self.toolbarMain.addAction(self.fsEditAction)
        #
        # Add heat integration button
        #self.heatIntAction = QAction(
        #    QIcon(self.iconPaths['heatEx48']),
        #    'Heat Int.',
        #    self)
        #self.heatIntAction.triggered.connect(self.showHeatInt)
        #self.heatIntAction.setCheckable(True)
        #self.mainToolbarActionGroup.addAction(self.heatIntAction)
        #self.toolbarMain.addAction(self.heatIntAction)
        # UQ setup action
        self.uqSetupAction = QAction(
            QIcon(self.iconPaths['uq']),
            "Uncertainty",
            self)
        self.uqSetupAction.triggered.connect(self.showUqSetup)
        self.uqSetupAction.setCheckable(True)
        self.mainToolbarActionGroup.addAction(self.uqSetupAction)
        self.toolbarMain.addAction(self.uqSetupAction)
        # Optimization set-up action
        self.optSetupAction = QAction(
            QIcon(self.iconPaths['optimize']),
            'Optimization',
            self)
        self.optSetupAction.triggered.connect(self.showOptSetup)
        self.optSetupAction.setCheckable(True)
        self.mainToolbarActionGroup.addAction(self.optSetupAction)
        self.toolbarMain.addAction(self.optSetupAction)
        # OUU setup action
        if self.showOuu:
            self.ouuSetupAction = QAction(
                QIcon(self.iconPaths['ouu']),
                'OUU',
                self)
            self.ouuSetupAction.setToolTip(
                "Optimization Under Uncertainty")
            self.ouuSetupAction.triggered.connect(self.showOuuSetup)
            self.ouuSetupAction.setCheckable(True)
            self.mainToolbarActionGroup.addAction(self.ouuSetupAction)
            self.toolbarMain.addAction(self.ouuSetupAction)
        # Add surrogate model button
        self.surrogateAction = QAction(
            QIcon(self.iconPaths['surrogate48']),
            'Surrogates',
            self)
        self.surrogateAction.triggered.connect(self.showSurrogate)
        self.surrogateAction.setCheckable(True)
        self.mainToolbarActionGroup.addAction(self.surrogateAction)
        self.toolbarMain.addAction(self.surrogateAction)
        # Add DRM-Builder button
        if self.showDRM and mainDRM is not None:
            self.drmAction = QAction(
                QIcon(self.iconPaths['drm48']),
                'DRM-Builder',
                self)
            self.drmAction.triggered.connect(self.showDRMBuilder)
            self.drmAction.setCheckable(True)
            self.mainToolbarActionGroup.addAction(self.drmAction)
            self.toolbarMain.addAction(self.drmAction)
        #separator
        #self.toolbarMain.addSeparator()
        #Setings Action
        self.mainSettingsAction = QAction(
            QIcon(self.iconPaths['settings48']),
            'Settings',
            self)
        self.mainSettingsAction.setCheckable(True)
        self.mainToolbarActionGroup.addAction(self.mainSettingsAction)
        self.mainSettingsAction.triggered.connect(self.showSettings)
        self.toolbarMain.addAction(self.mainSettingsAction)
        # Add separator before help button
        empty1 = QWidget()
        empty2 = QWidget()
        empty1.setMinimumWidth(15)
        empty2.setMinimumWidth(15)
        empty1.setMaximumWidth(15)
        empty2.setMaximumWidth(15)
        self.toolbarMain.addWidget(empty1)
        self.toolbarMain.addSeparator()
        self.toolbarMain.addWidget(empty2)
        # Help action
        self.mainHelpAction = QAction(
            QIcon(self.iconPaths['help']),
            'Help',
            self)
        self.mainHelpAction.triggered.connect(self.helpToggle)
        self.mainHelpAction.setCheckable(True)
        self.toolbarMain.addAction(self.mainHelpAction)

    def makeDrawingToolBar(self):
        '''
            Make the toolbar for flowsheet editing
        '''
        self.toolbarDrawing = QToolBar('Drawing', self)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbarDrawing)
        self.toolbarDrawing.hide()
        self.drawingToolbarActionGroup = QActionGroup(self)
        self.flowsheetViewActionGroup = QActionGroup(self)
        self.toolbarDrawing.setIconSize(QtCore.QSize(32, 32))
        #Select Action
        self.selectAction = QAction(
            QIcon(self.iconPaths['select']),
            'Select',
            self)
        self.selectAction.triggered.connect(
            self.flowsheetEditor.setModeSelect)
        self.toolbarDrawing.addAction(self.selectAction)
        self.drawingToolbarActionGroup.addAction(self.selectAction)
        self.selectAction.setCheckable(True)
        self.selectAction.setChecked(True)
        #Add node Action
        self.addNodeAction = QAction(
            QIcon(self.iconPaths['addNode']),
            'Add Node',
            self)
        self.addNodeAction.triggered.connect(
            self.flowsheetEditor.setModeAddNode)
        self.toolbarDrawing.addAction(self.addNodeAction)
        self.drawingToolbarActionGroup.addAction(self.addNodeAction)
        self.addNodeAction.setCheckable(True)
        #Add Edge Action
        self.addEdgeAction = QAction(
            QIcon(self.iconPaths['addEdge']),
            'Add Edge',
            self)
        self.addEdgeAction.triggered.connect(
            self.flowsheetEditor.setModeAddEdge)
        self.toolbarDrawing.addAction(self.addEdgeAction)
        self.drawingToolbarActionGroup.addAction(self.addEdgeAction)
        self.addEdgeAction.setCheckable(True)
        #Center Action
        self.centerAction = QAction(
            QIcon(self.iconPaths['center']),
            'Center Flowsheet View',
            self)
        self.centerAction.triggered.connect(
            self.flowsheetEditor.center)
        self.toolbarDrawing.addAction(self.centerAction)
        #Delete Action
        self.deleteAction = QAction(
            QIcon(self.iconPaths['delete']),
            'Delete Selected',
            self)
        self.deleteAction.triggered.connect(
            self.flowsheetEditor.deleteSelected)
        self.toolbarDrawing.addAction(self.deleteAction)
        #Run flowsheet evaluation action
        self.runAction = QAction(
            QIcon(self.iconPaths['run']),
            'Start Single Flowsheet Evaluation',
            self)
        self.runAction.triggered.connect(self.runSim)
        self.toolbarDrawing.addAction(self.runAction)
        #Stop run action
        self.stopAction = QAction(
            QIcon(self.iconPaths['stop']),
            'Stop Single Flowsheet Evaluation',
            self)
        self.stopAction.triggered.connect(self.stopButton)
        self.toolbarDrawing.addAction(self.stopAction)
        self.stopAction.setEnabled(False)
        #Load default inputs action
        self.loadDefaultsAction = QAction(
            QIcon(self.iconPaths['defaults']),
            'Load deafult inputs',
            self)
        self.loadDefaultsAction.triggered.connect(
            self.loadDefaultInput)
        self.toolbarDrawing.addAction(self.loadDefaultsAction)
        #determine tear stream action
        self.tearAction = QAction(
            QIcon(self.iconPaths['tear']),
            'Determine tear streams',
            self)
        self.tearAction.triggered.connect(self.tearFlowsheet)
        self.toolbarDrawing.addAction(self.tearAction)
        # Flowsheet settings dialog
        self.fsSettingsAction = QAction(
            QIcon(self.iconPaths['setting']),
            'Flowsheet Settings',self)
        self.fsSettingsAction.triggered.connect(self.fsSettings)
        self.toolbarDrawing.addAction(self.fsSettingsAction)
        #Separator
        self.toolbarDrawing.addSeparator()
        #Add node editor toggle button
        self.toggleNodeEditorAction = QAction(
            QIcon(self.iconPaths['nodeEdit']),
            'Toggle Node Editor',
            self)
        self.toggleNodeEditorAction.setCheckable(True)
        self.toggleNodeEditorAction.triggered.connect(
            self.toggleNodePanel)
        self.toolbarDrawing.addAction(self.toggleNodeEditorAction)
        #Add edge editor toggle button
        self.toggleEdgeEditorAction = QAction(
            QIcon(self.iconPaths['edgeEdit']),
            'Toggle Edge Editor',
            self)
        self.toggleEdgeEditorAction.setCheckable(True)
        self.toggleEdgeEditorAction.triggered.connect(
            self.toggleEdgePanel)
        self.toolbarDrawing.addAction(self.toggleEdgeEditorAction)
        #Separator
        self.toolbarDrawing.addSeparator()
        # Data/Results browser View
        self.dataBrowserAction =  QAction(
            QIcon(self.iconPaths['data']),
            'Results',
            self)
        self.dataBrowserAction.triggered.connect(self.showDataBrowser)
        self.toolbarDrawing.addAction(self.dataBrowserAction)

    def makeSessionMenu(self):
        '''
            Make the menu for the session
        '''
        self.mainMenu = QMenu(self)
        # Upload FOQUS session to turbine
        self.addFoqusTurbineAction = QAction(
            QIcon(self.iconPaths['add']),
            'Add Current FOQUS Session to Turbine...',
            self)
        self.addFoqusTurbineAction.triggered.connect(self.uploadSession)
        self.mainMenu.addAction(self.addFoqusTurbineAction)
        # Add/update model in Turbine Action
        self.addTurbineModelAction = QAction(
            QIcon(self.iconPaths['add']),
            'Add\Update Model to Turbine...',
            self)
        self.addTurbineModelAction.triggered.connect(self.addTurbModel)
        self.mainMenu.addAction(self.addTurbineModelAction)
        # Add/update model in DMF Action
        self.last_dmf_repo = None
        self.last_repo_props = None
        self.addDMFModelAction = QAction(
            QIcon(self.iconPaths['add']),
            'Add\Update Model to DMF...',
            self)
        self.addDMFModelAction.triggered.connect(self.addDMFModel)
        self.mainMenu.addAction(self.addDMFModelAction)
        # New session Action
        self.newSessionAction = QAction(
            QIcon(self.iconPaths['new']),
            'New Session...',
            self)
        self.newSessionAction.setShortcut(QKeySequence("Ctrl+N"))
        self.newSessionAction.triggered.connect(self.newSession)
        self.mainMenu.addAction(self.newSessionAction)
        # Load session Action
        self.openSessionAction = QAction(
            QIcon(self.iconPaths['load']),
            'Open Session...',
            self)

        self.openSessionAction.setShortcut(QKeySequence("Ctrl+O"))
        self.openSessionAction.triggered.connect(self.loadData)
        # add and update list of recently opened files
        self.openRecentMainMenu = QMenu(
                'Open Recent', self)
        self.openRecentMainMenu.setIcon(
            QIcon(self.iconPaths['load']))
        self.mainMenu.addMenu(self.openRecentMainMenu)
        self.updateRecentlyOpened()
        #self.mainMenu.addAction(self.openSessionAction)
        # Save session action
        self.saveSessionAction = QAction(
            QIcon(self.iconPaths['save']),
            'Save Session...',
            self)
        self.saveSessionAction.setShortcut(QKeySequence("Ctrl+S"))
        self.saveSessionAction.triggered.connect(self.saveData)
        #self.mainMenu.addAction(self.saveSessionAction)
        # Save session as action
        self.saveAsSessionAction = QAction(
            QIcon(self.iconPaths['save']),
            'Save Session As...',
            self)
        self.saveAsSessionAction.triggered.connect(self.saveAsData)
        # Don't add the load, save and save as actions now, wait and
        # see if data managmanet framework (DMF) is avaialabe.
        repoProperties = []
        try:
            # We are on Windows
            if platform.system().startswith(WINDOWS):
                self.PROP_LOC = (os.environ[REPO_PROPERTIES_WIN_PATH]
                                 + WIN_PATH_SEPARATOR)
            else:
                self.PROP_LOC = (os.environ[REPO_PROPERTIES_UNIX_PATH]
                                 + UNIX_PATH_SEPARATOR)
            config = StringIO()
            # Fake properties header to allow working with configParser
            config.write('[' + PROP_HEADER + ']\n')
            # Get a list of property files for repositories
            repoProperties = [f for f in os.listdir(self.PROP_LOC)
                              if os.path.isfile(os.path.join(self.PROP_LOC, f))
                              and f.endswith(PROPERTIES_EXT)]
            if len(repoProperties) == 0:
                logging.getLogger("foqus." + __name__).debug(
                    "No properties file specified.")
            self.repoList = []
            self.propListPaths = []
            self.openSessionMapper = QtCore.QSignalMapper()
            self.saveSessionMapper = QtCore.QSignalMapper()
            self.saveAsSessionMapper = QtCore.QSignalMapper()
        except:
            logging.getLogger("foqus." + __name__)\
                .exception('Error setting up DMF: ')
        if not useDMF or not self.dat.useDmf:
            repoProperties = []

        # Create open session action for each repository
        self.openSessionMainMenu = QMenu(
            'Open Session...', self)
        self.openSessionMainMenu.setIcon(
            QIcon(self.iconPaths['load']))
        self.openSessionAction.setIcon(QIcon())
        self.openSessionAction.setText(
            'Open Session from Local Filesystem...')
        self.openSessionMainMenu.addAction(self.openSessionAction)
        self.mainMenu.addMenu(self.openSessionMainMenu)

        # For DMF lite
        openMenuName = "Open Session from " + DMF_LITE + "..."
        self.openDMFLiteSessionAction = QAction(openMenuName, self)
        self.openDMFLiteSessionAction.triggered.connect(
            self.openSessionMapper.map)
        self.openSessionMapper.setMapping(
            self.openDMFLiteSessionAction,
            self.openDMFLiteSessionAction.text())
        self.openSessionMainMenu.addAction(
            self.openDMFLiteSessionAction)

        # Create save session action for each repository
        self.saveSessionMainMenu = QMenu(
            'Save Session...', self)
        self.saveSessionMainMenu.setIcon(
            QIcon(self.iconPaths['save']))
        self.saveSessionAction.setIcon(QIcon())
        self.saveSessionAction.setText(
            'Save Session in Local Filesystem...')
        self.saveSessionMainMenu.addAction(
            self.saveSessionAction)
        self.mainMenu.addMenu(self.saveSessionMainMenu)

        # Save For DMF Lite
        saveMenuName = "Save Session in " + DMF_LITE + "..."
        self.saveDMFLiteSessionAction = QAction(saveMenuName, self)
        self.saveDMFLiteSessionAction.triggered.connect(
            self.saveSessionMapper.map)
        self.saveSessionMapper.setMapping(
            self.saveDMFLiteSessionAction,
            self.saveDMFLiteSessionAction.text())
        self.saveSessionMainMenu.addAction(
            self.saveDMFLiteSessionAction)

        # Create save session as action for each repository
        self.saveAsSessionMainMenu = QMenu(
            'Save Session As...', self)
        self.saveAsSessionMainMenu.setIcon(
            QIcon(self.iconPaths['save']))
        self.saveAsSessionAction.setIcon(
            QIcon())
        self.saveAsSessionAction.setText(
            'Save Session As in Local Filesystem...')
        self.saveAsSessionMainMenu.addAction(
            self.saveAsSessionAction)
        self.mainMenu.addMenu(self.saveAsSessionMainMenu)
        if len(repoProperties) > 0:
            for p in repoProperties:
                config.write(
                    open(self.PROP_LOC + p).read())
                config.seek(0, os.SEEK_SET)
                rcp = RawConfigParser()
                rcp.readfp(config)
                self.repo_name = rcp.get(PROP_HEADER, "repo_name")
                self.repoList.append(self.repo_name)
                self.propListPaths.append(
                    self.PROP_LOC + p)
                openMenuName = 'Open Session from '+self.repo_name+'...'
                openRepoSessionAction = QAction(openMenuName, self)
                openRepoSessionAction.triggered.connect(
                    self.openSessionMapper.map)
                self.openSessionMapper.setMapping(
                    openRepoSessionAction, openRepoSessionAction.text())
                self.openSessionMainMenu.addAction(
                    openRepoSessionAction)
                # save menu item DMF
                saveMenuName = 'Save Session in '+self.repo_name+'...'
                saveRepoSessionAction = QAction(saveMenuName, self)
                saveRepoSessionAction.triggered.connect(
                    self.saveSessionMapper.map)
                self.saveSessionMapper.setMapping(
                    saveRepoSessionAction, saveRepoSessionAction.text())
                self.saveSessionMainMenu.addAction(
                    saveRepoSessionAction)
        self.openSessionMapper.mapped['QString'].connect(
            self.loadRepoData)
        self.saveSessionMapper.mapped['QString'].connect(
            self.saveRepoData)
        self.saveAsSessionMapper.mapped['QString'].connect(
            self.saveAsRepoData)
        # Logout DMF action
        if useDMF and self.dat.useDmf:
            self.logoutAction = QAction(
                QIcon(self.iconPaths['logout']),
                'Logout from DMF Repositories...',
                self)
            self.logoutAction.triggered.connect(self.logoutDMF)
            self.mainMenu.addAction(self.logoutAction)
        # exit FOQUS action
        self.exitAction = QAction(
            QIcon(self.iconPaths['exit']),
            'Exit FOQUS...',
            self)
        self.exitAction.setShortcut(QKeySequence("Ctrl+Q"))
        self.exitAction.triggered.connect(self.close)
        self.mainMenu.addAction(self.exitAction)

    def addTurbModel(self):
        '''
            Upload a new model to Turbine
        '''
        g = gatewayUploadDialog(
            self.dat,
            self.dat.flowsheet.turbConfig,
            self)
        g.waiting.connect(self.setCursorWaiting)
        g.notwaiting.connect(self.setCursorNormal)
        try:
            g.exec_()
        except Exception as e:
            logging.getLogger("foqus." + __name__)\
                .exception('Error uploading to Turbine file: ')
        self.setCursorNormal()
        g.destroy()

    def addDMFModel(self):
        ''' Upload a new model to DMF '''
        dmf_upload_dialog = dmfUploadDialog(
            self.dat,
            self.dat.flowsheet.turbConfig,
            self)
        dmf_upload_dialog.waiting.connect(self.setCursorWaiting)
        dmf_upload_dialog.notwaiting.connect(self.setCursorNormal)
        try:
            dmf_upload_dialog.exec_()
        except Exception as e:
            logging.getLogger("foqus." + __name__)\
                .exception('Error uploading to DMF.')
        self.setCursorNormal()
        dmf_upload_dialog.destroy()

    def sessionDescEdit(self):
        '''
            This brings up an editor dialog for the FOQUS session
            description
        '''
        d = sessionDescriptionDialog(
                self,
                self.dashFrame.sessionDescription())
        ok = d.exec_()
        if ok == QDialog.Accepted:
            self.dashFrame.setSessionDescription(d.html())
            self.updateSession()

    def cancelSession(self):
        '''
            Cancels changes to session description
        '''
        self.dashFrame.setSessionDescription(self.dat.description);

    def applyAllChanges(self):
        '''
            This calls the applyChanges method on all the screens.
            mostly this is used so that all changes in GUI are applied
            before saving a session
        '''
        index = self.mainWidget.currentIndex()
        if index == self.screenIndex['home']:
            self.updateSession()
        elif index == self.screenIndex['flow']:
            self.applyNodeEdgeChanges()
        elif index == self.screenIndex['uq']:
            # may add something later
            pass
        elif index == self.screenIndex['opt']:
            self.optSetupFrame.applyChanges()
        elif index == self.screenIndex['surrogate']:
            self.surFrame.applyChanges()
        elif index == self.screenIndex['settings']:
            self.fsettingsFrame.applyChanges()

    def changeScreen(self):
        '''
            Hide special tool-bars and commit changes on the current
            screen before showing a different screen in the main window
        '''
        index = self.mainWidget.currentIndex()
        if index == self.screenIndex['home']:
            self.updateSession()
        elif index == self.screenIndex['flow']:
            self.applyNodeEdgeChanges()
            self.hideNodePanel()
            self.hideEdgePanel()
            self.toolbarDrawing.hide()
            self.varBrowse.hide()
        elif index == self.screenIndex['uq']:
            # may add something later
            pass
        elif index == self.screenIndex['opt']:
            self.optSetupFrame.applyChanges()
            self.varBrowse.hide()
        elif index == self.screenIndex['surrogate']:
            self.surFrame.applyChanges()
        elif index == self.screenIndex['settings']:
            self.fsettingsFrame.applyChanges()

    def applyNodeEdgeChanges(self):
        '''
            If the node or edge editor is shown apply whatever changes
            have been made so they are not lost when switching
            screens
        '''
        if not self.nodeDock.isHidden():
            self.nodeDock.applyChanges()
        if not self.edgeDock.isHidden():
            self.edgeDock.applyChanges()

    def hideNodeEdgePanels(self):
        self.applyNodeEdgeChanges()
        self.hideNodePanel()
        self.hideEdgePanel()

    def fsSelectNone(self):
        '''
            Hide the node and edge editors if no edege or node is
            selected.
        '''
        self.applyNodeEdgeChanges()
        self.hideNodePanel()
        self.hideEdgePanel()

    def setNodePanel(self, name=None):
        self.applyNodeEdgeChanges()
        self.nodeDock.setNodeName(name)

    def showNodePanel(self, name=None):
        '''
            If a node is selected show the node editor for it
        '''
        self.hideEdgePanel()
        self.nodeDock.updateForm()
        self.nodeDock.show()
        self.toggleNodeEditorAction.setChecked(True)
        if name!= None:
            self.nodeDock.setNodeName(name)

    def toggleNodePanel(self):
        '''

        '''
        if self.toggleNodeEditorAction.isChecked():
            self.showNodePanel()
        else:
            self.hideNodePanel()

    def toggleEdgePanel(self):
        if self.toggleEdgeEditorAction.isChecked():
            self.showEdgePanel()
        else:
            self.hideEdgePanel()

    def hideNodePanel(self):
        '''
            Hide the node editor
        '''
        self.toggleNodeEditorAction.setChecked(False)
        if not self.nodeDock.isHidden():
            self.nodeDock.applyChanges()
            self.nodeDock.hide()

    def setEdgePanel(self, index=None):
        self.applyNodeEdgeChanges()
        self.edgeDock.setEdgeIndex(index)

    def showEdgePanel(self, index=None):
        '''
            If an edge is selected show the edge editor for it
        '''
        self.hideNodePanel()
        self.toggleEdgeEditorAction.setChecked(True)
        self.edgeDock.setEdgeIndex(index)
        self.edgeDock.updateForm()
        self.edgeDock.show()

    def hideEdgePanel(self):
        '''
            Hide the edge editor
        '''
        self.toggleEdgeEditorAction.setChecked(False)
        if not self.edgeDock.isHidden():
            self.edgeDock.applyChanges()
            self.edgeDock.hide()

    def showSettings(self):
        self.changeScreen()
        self.fsettingsFrame.updateForm()
        self.mainWidget.setCurrentIndex(self.screenIndex['settings'])

    def showDash(self):
        '''
            Show the home screen
        '''
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['home'])

    def showFlow(self):
        '''
            Show the flowsheet editor
        '''
        self.changeScreen()
        self.toolbarDrawing.show()
        self.mainWidget.setCurrentIndex(self.screenIndex['flow'])

    def showUqSetup(self):
        '''
            Show the UQ screen
        '''
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['uq'])

    def showOptSetup(self):
        '''
            Show the optimization screen
        '''
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['opt'])
        self.optSetupFrame.refreshContents()

    def showOuuSetup(self):
        '''
            Show the UQ screen
        '''
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['ouu'])

    def showSurrogate(self):
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['surrogate'])
        self.surFrame.refreshContents()

    def showDRMBuilder(self):
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['drmbuilder'])

    def showHeatInt(self):
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['heatInt'])

    def showDataBrowser(self):
        '''
            Show the flowsheet results browser dialog box
        '''
        self.dataBrowserDialog.show()

    def showBasicData(self):
        self.changeScreen()
        self.mainWidget.setCurrentIndex(self.screenIndex['basicData'])

    def fsSettings(self):
        '''
            Show the flowseet settings dialog box
        '''
        fss = flowsheetSettingsDialog(self.dat, self)
        fss.exec_()

    def logoutDMF(self):
        '''
            Logout from all DMF repositories
        '''
        if platform.system().startswith(WINDOWS):  # We are on Windows
            PROP_LOC = (
                os.environ[REPO_PROPERTIES_WIN_PATH] + WIN_PATH_SEPARATOR)
        else:
            PROP_LOC = (
                os.environ[REPO_PROPERTIES_UNIX_PATH] + UNIX_PATH_SEPARATOR)
        keys = [f for f in os.listdir(PROP_LOC)
                if os.path.isfile(os.path.join(PROP_LOC, f))
                and (f.endswith(KEYS_EXT) or f.endswith(TMP_KEYS_EXT))]

        status = QDialog(self)
        status_layout = QVBoxLayout()
        status_layout.setSizeConstraint(QLayout.SetFixedSize)
        status.setLayout(status_layout)
        if len(keys) > 0:
            label = QLabel(self)
            label.setText(
                "Successfully logged out from the following repositories:")
            status_layout.addWidget(label)

            for i in range(len(keys)):
                try:
                    os.remove(PROP_LOC + keys[i])
                    label = QLabel(self)
                    label.setText('\t' + str(i + 1) + '. ' + self.repoList[i])
                    status_layout.addWidget(label)
                except OSError, e:
                    print self.__class__.__name__, PRINT_COLON, e
        else:
            label = QLabel(self)
            label.setText("There are no repositories to logout.")
            status_layout.addWidget(label)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, self)
        buttons.accepted.connect(status.accept)
        status_layout.addWidget(buttons)
        status.exec_()

    def helpToggle(self):
        if self.mainHelpAction.isChecked():
            self.showHelp()
        else:
            self.hideHelp()

    def showHelp(self):
        '''
            Show the help dock widget
        '''
        self.helpDock.showHelp()
        self.helpDock.show()
        self.mainHelpAction.setChecked(True)

    def hideHelp(self):
        '''
            Hide the help dock
        '''
        self.helpDock.hide()
        self.mainHelpAction.setChecked(False)

    def closeEvent(self, event):
        '''
            Intercept close main window close event
            make sure you really want to quit
        '''
        accept = False
        if self.splash:
            self.splash.hide()
        msgBox = QMessageBox()
        msgBox.setText(
            "Do you want to save the session before exiting?")
        msgBox.setStandardButtons(
            QMessageBox.No |
            QMessageBox.Yes |
            QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        if ret == QMessageBox.No:
            event.accept()
            accept = True
        elif ret == QMessageBox.Yes:
            if self.saveData():
                event.accept()
                accept = True
            else:
                event.ignore()
        else:
            event.ignore()
        if not accept:
            return
        self.dat.removeNewArchiveItems()
        try:
            self.applyAllChanges()
            self.dat.foqusSettings.save(newWdir = True)
        except:
            logging.getLogger("foqus." + __name__)\
                .exception('Failed to save FOQUS settings')

        # Close any open matplotlib windows
        import matplotlib.pyplot as plt
        plt.close("all")

        # Shutdown Java Gateway. This does some checking to
        # see if there is a running gateway left opened in case
        # FOQUS needs to use it.
        if useDMF:
            try:
                logging.getLogger("foqus." + __name__)\
                    .debug('Initiated DMF gateway shutdown')
                Py4JGateway(True).shutdownGateway()
                Common().deleteCachedCredentials()
            except:
                logging.getLogger("foqus." + __name__)\
                    .exception('Failed to shutdown DMF gateway')

    def showAbout(self):
        '''
            Show the about screen.  I just reused the splash
            screen for this.
        '''
        if self.splash:
            self.splash.show()

    def updateSession(self):
        '''
            Synchronize the session data with what is shown in the
            dash window.
        '''
        self.dat.name = self.dashFrame.sessionNameEdit.text()
        self.dat.version = self.dashFrame.versionBox.text()
        self.dat.confidence = self.dashFrame.confCombo.currentText()
        self.dat.description = self.dashFrame.sessionDescription()

    def applyAndUpdateNodeEdit(self):
        if not self.nodeDock.isHidden():
            self.nodeDock.applyChanges()
            self.nodeDock.updateForm()

    def applyAndUpdateEdgeEdit(self):
        if not self.edgeDock.isHidden():
            self.edgeDock.applyChanges()
            self.edgeDock.updateForm()

    def refreshFlowsheet(self):
        '''
            Update the flowsheet drawing, usually done if some change
            is made either to the structure or any node or edge
            parameter
        '''
        self.flowsheetEditor.createScene()
        if not self.nodeDock.isHidden():
            self.nodeDock.updateForm()
        if not self.edgeDock.isHidden():
            self.edgeDock.updateForm()

    def refreshNodeCoord(self):
        if not self.nodeDock.isHidden():
            self.nodeDock.updateLocation()

    def refreshDRMFrame(self):
        if not self.drmFrame.isHidden():
            self.drmFrame.update_view()

    def refresh(self):
        '''
            Update all the forms and flowsheet after reloading a file
            or some other change
        '''
        self.refreshFlowsheet()
        self.uqSetupFrame.refresh()
        self.surFrame.refreshContents()
        self.optSetupFrame.refreshContents()
        self.ouuSetupFrame.refresh()
        self.refreshDRMFrame()
        if self.dat.currentFile and self.dat.currentFile != '':
            self.setWindowTitle(
                'FOQUS - {0} - Last saved: {1}'.format(
                    self.dat.currentFile, self.dat.date))
        else:
            self.setWindowTitle('FOQUS -- [not saved yet]')
        self.dashFrame.sessionNameEdit.setText(self.dat.name)
        self.dashFrame.idBox.setText(self.dat.uid)
        self.dashFrame.creationTimeBox.setText(self.dat.creationTime)
        self.dashFrame.modTimeBox.setText(self.dat.date)
        self.dashFrame.versionBox.setText(self.dat.version)
        i = self.dashFrame.confCombo.findText(self.dat.confidence)
        if i > -1:
            self.dashFrame.confCombo.setCurrentIndex(i)
        self.dashFrame.setSessionDescription(self.dat.description)
        cltext = ""
        for m in sorted(self.dat.changeLog.keys()):
            cltext = cltext + \
                "{0}, Version: {1}, Name: {2}, ID: {3}\n{4}\n".\
                    format(
                        m,
                        self.dat.changeLog[m][0],
                        self.dat.changeLog[m][2],
                        self.dat.changeLog[m][1],
                        self.dat.changeLog[m][3])
        self.dashFrame.changeLogEdit.setPlainText(cltext)

    def newSession(self):
        '''
            Creates a new FOQUS session after asking if you are sure.
            The current session is not saved first so changes may be
            lost.
        '''
        saveSessionQuestion = QMessageBox()
        saveSessionQuestion.setText(
            "Do you want to save your current session before starting"
            " a new session?")
        saveSessionQuestion.setStandardButtons(
            QMessageBox.No|QMessageBox.Yes|\
            QMessageBox.Cancel)
        saveSessionQuestion.setDefaultButton(QMessageBox.Cancel)
        response = saveSessionQuestion.exec_()
        if response == QMessageBox.Cancel:
            return
        elif response == QMessageBox.Yes:
            if not self.saveData():
                return
        self.hideNodeEdgePanels()
        self.updateRecentlyOpened()
        self.dat.new()
        self.dat.currentFile = ""
        self.flowsheetEditor.clearSelection()
        self.refresh()
        self.clearOldMessages()

    def tearFlowsheet(self):
        '''
            Find flowsheet tears
        '''
        self.setCursorWaiting()
        self.dat.flowsheet.calculationOrder()
        self.refresh()
        self.setCursorNormal()

    def loadData(self):
        '''
            Load a saved session
        '''
        msgBox = QMessageBox()
        msgBox.setText("Do you want to save your current session"
            " before loading another session?")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setStandardButtons(
            QMessageBox.Yes|QMessageBox.No|\
            QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        response = msgBox.exec_()
        if response == QMessageBox.Cancel:
            return
        elif response == QMessageBox.Yes:
            if not self.saveData():
                return
        fileName, filtr = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "FOQUS files (*.foqus);;JSON Files (*.json);;All Files (*)")
        if fileName:
            #self.dat is a reference to the session data
            self.hideNodeEdgePanels()
            self.setCursorWaiting()
            self.dat.load(fileName)
            self.updateRecentlyOpened()
            self.setCursorNormal()
            self.flowsheetEditor.clearSelection()
            self.refresh()
            self.flowsheetEditor.center()
            self.clearOldMessages()

    def loadSessionFile(self, filename, saveCurrent=True):
        '''
            Load a FOQUS session from given filename
        '''
        if filename:
            if saveCurrent:
                msgBox = QMessageBox()
                msgBox.setText(
                    "Do you want to save your current session"
                    " before loading another session?")
                msgBox.setIcon(QMessageBox.Question)
                msgBox.setStandardButtons(
                    QMessageBox.Yes|QMessageBox.No|\
                    QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Cancel)
                response = msgBox.exec_()
                if response == QMessageBox.Cancel:
                    return
                elif response == QMessageBox.Yes:
                    self.saveData()
                    if not self.saveData():
                        return
            self.hideNodeEdgePanels()
            self.setCursorWaiting()
            self.dat.load(filename)
            self.updateRecentlyOpened()
            self.setCursorNormal()
            self.flowsheetEditor.clearSelection()
            self.refresh()
            self.flowsheetEditor.center()
            self.clearOldMessages()

    def loadRepoData(self, identifier):
        '''
            Load a FOQUS session from DMF
        '''
        msgBox = QMessageBox()
        msgBox.setText("Do you want to save your current session"
            " before loading another session?")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setStandardButtons(
            QMessageBox.Yes|QMessageBox.No|\
            QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        response = msgBox.exec_()
        if response == QMessageBox.Cancel:
            return
        elif response == QMessageBox.Yes:
            if not self.saveData():
                return
        repo_name = identifier.replace(
            'Open Session from ', '').replace('...', '')
        if repo_name == DMF_LITE:
            currentPropList = None
        else:
            index = self.repoList.index(repo_name)
            currentPropList = self.propListPaths[index]
        # Use b for desired opening of session file,
        # sim_b_ls should contain the bytestreams of associated
        # simulations (This was removed, unnecessary)
        session_b, session_path = DMFBrowser.getSession(
            self, currentPropList, repo_name)
        if session_b:
            sd = json.loads(
                session_b.decode("utf-8"),
                object_pairs_hook=collections.OrderedDict)
            dmf_prop = [currentPropList, repo_name]
            self.dat.loadDict(sd, session_path, dmf_prop=dmf_prop)
            self.refresh()
            self.flowsheetEditor.center()
            self.clearOldMessages() #clear message windows for opt and
                                    #surragate models...
        else:
            return
        #Session loaded now check on simulations
        turb_config = self.dat.flowsheet.turbConfig
        #get list of simlations session file expects in turbine
        turbine_sim_list = self.dat.flowsheet.turbineSimList()
        #get list of simulations actually in turbine
        sim_list = turb_config.getSimulationList()
        DMFBrowser.turbineSync(self, currentPropList, repo_name, turb_config,
                               turbine_sim_list, sim_list)
        '''
        #Check if a newer simulation is available
        for sim_name in turbine_sim_list:
            updateSim = False
            if not sim_name in sim_list:
                #the simulation is not in turbine go ahead and upload
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Update Simulation")
                msgBox.setText("The simulation " + sim_name +\
                    "is not available on Turbine attempting to add it "+\
                    "from the DMF")
                msgBox.exec_()
                updateSim = True
            else:
                #need to check if newer one is available
                sinter_config_id = ""
                sinterConfig = turb_config.getSinterConfig(sim_name)
                scMetaData = sinterConfig.get("CCSIFileMetaData", None)
                sim_id = None
                if scMetaData:
                    sim_id = scMetaData["Simulation ID"]
                if sim_id:
                    Latest = DMFBrowser.isLatestVersion(
                        self,
                        currentPropList,
                        repo_name,
                        sim_id)
                else:
                    Latest = False
                if Latest == False:
                    msgBox = QMessageBox()
                    msgBox.setText(
                        "A newer {0} simulation is available. Do"\
                        " you want to update Turbine?".format(sim_name))
                    msgBox.setStandardButtons(
                        QMessageBox.No|QMessageBox.Yes)
                    msgBox.setDefaultButton(QMessageBox.No)
                    ret = msgBox.exec_()
                    if ret == QMessageBox.Yes:
                        updateSim = True
            if updateSim:
                scf = DMFBrowser.getSimFileByteArrayStreamByName(
                    self,
                    currentPropList,
                    repo_name,
                    str(sim_name + "_sinter_config.json"))
                if scf:
                    sc_file = "temp/sinter_config.json"
                    with open(sc_file, 'wb') as f:
                        f.write(scf)
                    #Have the sinter config file now need to get rest
                    #of files.  The IDs should be in the sinter metadata
                    #also need to get the simulation file out of the
                    #sinter config
                    scf = json.loads(scf.decode('utf-8'))
                    sim_id = scf["CCSIFileMetaData"]["Simulation ID"]
                    input_files = scf["CCSIFileMetaData"].get(
                        "InputFiles", [])
                    sim_file, sim_resource, a = \
                        turb_config.sinterConfigGetResource(
                            sc_file, checkExists=False)
                    sim_file = os.path.join("temp", sim_file)
                    sim_bytestream = DMFBrowser.getByteArrayStreamById(
                        self,
                        currentPropList,
                        repo_name,
                        str(sim_id))
                    with open(sim_file, 'wb') as f:
                        f.write(sim_bytestream)
                    resources = []
                    resource_files = []
                    resource_bytestreams = []
                    for resource_data in input_files:
                        resource_data = resource_data["CCSIFileMetaData"]
                        rid = resource_data.get("Resource ID", None)
                        rdn = resource_data.get(
                            "Resource Display Name",
                            None)
                        if rid == None or rdn == None:
                            continue
                        resource_bytestreams.append(
                            DMFBrowser.getByteArrayStreamById(
                                self,
                                currentPropList,
                                repo_name,
                                str(rid)))
                        resource_files.append(os.path.join("temp", rdn))
                        resources.append([rdn,os.path.join("temp",rdn)])
                    for i, fname in enumerate(resource_files):
                        with open(fname, 'wb') as f:
                            f.write(resource_bytestreams[i])
                    # update files in turbine
                    turb_config.uploadSimulation(
                        sim_name,
                        sc_file,
                        update = True,
                        otherResources = resources)
        '''
    def saveAsData(self):
        '''
            Save a session
        '''
        self.applyAllChanges()
        if self.dat.name == "":
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText("You must specify the session name.")
            msgBox.exec_()
            return False
        ccheck = self.checkNameChars()
        if ccheck:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText(
                "Invalid characters in the session name: {0}".\
                    format(ccheck))
            msgBox.exec_()
            return False
        metaDataDialog = saveMetadataDialog(self.dat, self)
        ok = metaDataDialog.exec_()
        if not ok: #Cancel the save
            return False
        fileName, filtr = QFileDialog.getSaveFileName(
            self,
            "Save File",
            ".".join([self.dat.name, "foqus"]),
            "FOQUS files (*.foqus);;JSON Files (*.json);;All Files (*)")
        if fileName:
            # Move archive folders
            fullFile = os.path.abspath(fileName)
            pathName, baseName = os.path.split(fullFile)
            base, ext = os.path.splitext(baseName)
            self.dat.ID = base + time.strftime('_%y%m%d%H%M%S')
            pathName = os.path.join(pathName, '%s_files' % self.dat.ID)
            self.dat.moveArchive(pathName)
            # Delete new folders from old archive
            #  (Old folders need to be kept for old session)
            self.dat.removeNewArchiveItems()
            self.setCursorWaiting()
            self.dat.save(
                fileName,
                changeLogMsg = metaDataDialog.entry,
                bkp = "Settings",
                indent = "Settings")
            self.setCursorNormal()
            self.updateRecentlyOpened()
            self.refresh()
            return True
        else:
            return False

    def checkNameChars(self):
        invalidChars = ['\\','/','?','%','*',':','"','|','$','<','>']
        err = []
        for c in invalidChars:
            if c in self.dat.name:
                err.append(c)
        return err

    def saveData(self):
        '''
            Save a session using the current name if it hasn't been
            saved yet call save as.
        '''
        if self.dat.currentFile != "" and self.dat.currentFile != None:
            self.applyAllChanges()
            if self.dat.name == "":
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Error")
                msgBox.setText("You must specify the session name.")
                msgBox.exec_()
                return False
            ccheck = self.checkNameChars()
            if ccheck:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Error")
                msgBox.setText(
                    "Invalid characters in the session name: {0}".\
                        format(ccheck))
                msgBox.exec_()
                return False
            metaDataDialog = saveMetadataDialog(self.dat, self)
            ok = metaDataDialog.exec_()
            if not ok: #Cancel the save
                return False
            self.setCursorWaiting()
            self.dat.save(
                self.dat.currentFile,
                changeLogMsg = metaDataDialog.entry,
                bkp = "Settings",
                indent = "Settings")
            self.setCursorNormal()
            self.refresh()
            return True
        else:
            return self.saveAsData()

    def saveRepoData(self, identifier):
        '''
            Save the FOQUS session and turbine simulation files to the
            DMF.
        '''
        # if an unhandeled exception occurs it will show up in a message
        # box and in the log file so we don't really need much specuial
        # error handeling here.
        self.applyAllChanges()
        # Check that a session name has been specified if not show error
        # and cnacel save.  This forces a simulation name to be given.
        if self.dat.name == "":
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText("You must specify the session name.")
            msgBox.exec_()
            return False
        # Right now the FOQUS metadata entry box only contains a change
        # log entry.  The entry is optional but cancel button cancels
        # save.
        metaDataDialog = saveMetadataDialog(self.dat, self)
        ok = metaDataDialog.exec_()
        if not ok:  # Cancel the save
            return False
        logging.getLogger("foqus." + __name__).debug(
            "Saving session to DMF...")
        # repo name and index?
        repo_name = identifier.replace(
            'Save Session in ', '').replace('...', '')
        if repo_name == DMF_LITE:
            currentPropList = None
        else:
            index = self.repoList.index(repo_name)
            currentPropList = self.propListPaths[index]
        logging.getLogger("foqus." + __name__).debug(
            "Name of repo to save to: {n}".format(n=repo_name))
        # Get a list of simulations used in this FOQUS session
        turb_config = self.dat.flowsheet.turbConfig
        turbine_sim_list = self.dat.flowsheet.turbineSimList()
        # this is a list of file ids that the FOQUS session depends on
        # these would be the ids from the sinter config.  Sinter config
        # would depend on simulation files.  So the ids for simulation
        # and other resource files don't need to be in parents?
        parents = []
        logging.getLogger("foqus." + __name__).debug(
            "Length of turbine sim list: {s}".format(s=len(turbine_sim_list)))
        # Go through all the simulations used in this FOQUS session
        # and upload them to the DMF if they are not already there.
        for sim_name in turbine_sim_list:
            # Get sinter config and pull out metadata
            sinter_config_id = ""
            sinterConfig = turb_config.getSinterConfig(sim_name)
#            print json.dumps(sinterConfig, indent=2)
            scMetaData = sinterConfig.get("CCSIFileMetaData", None)
            sim_id = None
            if scMetaData:
                sim_id = scMetaData.get("Simulation ID", None)
            # get metadata from other files.
            scMetaData = sinterConfig.get("CCSIFileMetaData", None)
            # Get complete list of resources this is all files
            # assocciated with the simulation sinter config, simulation,
            # and any other required files.
            resourceList = turb_config.simResourceList(sim_name)
            # if no id in sinter config assume it has not been uploaded
            # to the DMF
            logging.getLogger("foqus." + __name__).debug(
                "sim ID: {s}".format(s=sim_id))
            if sim_id is None:
                # Get all simulation files from turbine
                d = {}  # dictionary of resources.  Resource name is key
                for r in resourceList:
                    d[r] = turb_config.getSimResource(sim_name, r)
                # Remove sinter config from rest of simulation files and
                # make it a bytearray
                sinter_config_bytestream = bytearray(
                    d.pop('configuration'))
                # Determine the application type for the simualtion so
                # can get the resource name for the simuatoin file then
                # remove the simualtion file from the resource dict and
                # make a bytearray
                app = turb_config.getSimApplication(sim_name)
                sim_resource = turb_config.resourceNames[app]
                sim_bytestream = bytearray(d.pop(sim_resource))
                # The files remaning in the resource dictionary are
                # extra files required by the simualtion. Make a list of
                # byte arrays and corresponding list of names.  For any
                # extra required files.
                resource_bytestream_list = []
                resource_name = []
                for r in d:
                    resource_bytestream_list.append(bytearray(d[r]))
                    resource_name.append(r)
                # Upload simulation.  Maybe this should return the
                # sinter config with new metadata.  Then I can upload
                # to turbine.  Other files should be unchanged.
                update_comment = ''
                confidence = 'experimental'
                sinter_config_name = sim_name + "_sinter_config.json"
#                print "len"
#                print len(resource_bytestream_list)
#                print len( resource_name)
                self.setEnabled(False)
                try:
                    logging.getLogger("foqus." + __name__).debug(
                        "Attributes: \n{c}\n{r}\n{sid}\n{s}\n{sc}\n{rn}\n".format(
                            c=currentPropList,
                            r=repo_name,
                            sid=sim_id,
                            s=sim_name,
                            sc=sinter_config_name,
                            rn=resource_name))
                    new_sim_id, new_sinter_config_id, \
                        sinter_config_bytestream = \
                        DMFBrowser.uploadSimulation(
                            self,
                            currentPropList,
                            repo_name,
                            sim_bytestream,
                            sim_id,
                            sim_name,
                            update_comment,
                            confidence,
                            sinter_config_bytestream,
                            sinter_config_name,
                            resource_bytestream_list,
                            resource_name)
                    parents.append(new_sinter_config_id)
                    # Upload sinter config with new metadata to turbine
                    if sinter_config_bytestream:
                        with open("temp/sinter_config.json", 'wb') as f:
                            f.write(sinter_config_bytestream)
                        turb_config.updateResource(
                            sim_name,
                            "configuration",
                            "temp/sinter_config.json")
                except Exception, e:
                    logging.getLogger("foqus." + __name__).error(
                        "Exception: {e}".format(e=str(e)))
                finally:
                    self.setEnabled(True)
            else:
                # check sinterConfigID upload if needed
                # For now only check the sinter config ID
                dmf_id_list = []
                dmf_id_list.append(sim_id)
                # You-Wei: Need to add check here to see if DM is alive
                # For each ID in dmf_id_list, a value of True (exists),
                # False (does not exist), or None (error case)
                logging.getLogger("foqus." + __name__).debug(
                    "dmf_id_list: {l}".format(l=dmf_id_list))
                does_exist_result = DMFBrowser.doFilesExist(
                    self,
                    currentPropList,
                    repo_name,
                    dmf_id_list)
                logging.getLogger("foqus." + __name__).debug(
                    "does_exist_result: {r}".format(r=does_exist_result))
                if not does_exist_result[0]:
                    # upload the simulation this is like case above,
                    # where there was no id
                    # try to get meta data for other simulation files
                    inFilesMetaData = sinterConfig.get(
                        "InputFiles", None)
                    ids = {}  # dict of ids with display name key
                    if inFilesMetaData:
                        for r in inFilesMetaData:
                            key = r["Simulation Display Name"]
                            ids[key] = r["Simulation ID"]
                    d = {}  # dictionary of resources
                    for r in resourceList:
                        d[r] = turb_config.getSimResource(sim_name, r)
                    sinter_config_bytestream = bytearray(
                        d.pop('configuration'))
                    app = turb_config.getSimApplication(sim_name)
                    sim_resource = turb_config.resourceNames[app]
                    sim_bytestream = bytearray(d.pop(sim_resource))
                    # I have the simulation ID, but I'm not quite sure
                    # what the display name would be so not sure what
                    # this should be.
                    sim_id = None
                    resource_bytestream_list = []
                    resource_name = []
                    for r in d:
                        resource_bytestream_list.append(bytearray(d[r]))
                        resource_name.append(r)
                    update_comment = ''
                    confidence = 'experimental'
                    # Use this to check is file is latest version
                    # DMFBrowser.isLatestVersion(id)
                    sinter_config_name = sim_name + "_sinter_config.json"
                    self.setEnabled(False)
                    try:
                        logging.getLogger("foqus." + __name__).debug(
                            "Attributes: \n{c}\n{r}\n{sid}\n{s}\n{sc}\n{rn}\n".format(
                                c=currentPropList,
                                r=repo_name,
                                sid=sim_id,
                                s=sim_name,
                                sc=sinter_config_name,
                                rn=resource_name))
                        new_sim_id, new_sinter_config_id, sinter_config_bytestream = \
                            DMFBrowser.uploadSimulation(
                                self,
                                currentPropList,
                                repo_name,
                                sim_bytestream,
                                sim_id,
                                sim_name,
                                update_comment,
                                confidence,
                                sinter_config_bytestream,
                                sinter_config_name,
                                resource_bytestream_list,
                                resource_name)
                        parents.append(new_sinter_config_id)
                        # Upload sinter config with new metadata to turbine
                        if sinter_config_bytestream:
                            with open("temp/sinter_config.json", 'wb') as f:
                                f.write(sinter_config_bytestream)
                            turb_config.updateResource(
                                sim_name,
                                "configuration",
                                "temp/sinter_config.json")
                    except Exception, e:
                        logging.getLogger("foqus." + __name__).error(
                            "Exception: {e}".format(e=str(e)))
                    finally:
                        self.setEnabled(True)
                else:
                    # Y-W: If simulation in DMF, pass simulation id with
                    # find sinter indicator. Assumes that sinter
                    # config lives in the same place as simulation.
                    parents.append(FIND_SINTER_INDICATOR + sim_id)

        # Get FOQUS session bytearray
        s = bytearray(json.dumps(
            self.dat.save(changeLogMsg=metaDataDialog.entry,
                          bkp="Settings",
                          indent="Settings")),
                      'utf-8')
        # Save the FOQUS session file to the DMF.
        DMFBrowser.saveByteArrayStream(
            self,
            s,
            parents,  # Add parents in here if needed
            currentPropList,
            metaDataDialog.entry,
            repo=repo_name)
        self.refresh()
        return True

    def saveAsRepoData(self, identifier):
        raise Exception("This is currently not functional.  Use Save.")

    def stopButton(self):
        '''
            This stops a flowsheet run it is just a single run
            to stop optimization or UQ they have their own ways
        '''
        if self.runningSingle:
            if self.singleRun is not None:
                self.singleRun.terminate()
            elif self.multiRun is not None:
                self.multiRun.terminate()
            self.stopSim()

    def uploadSession(self):
        """
        Uploading FOQUS session to current Turbine
        """
        self.dat.flowsheet.uploadFlowseetToTurbine(
            self.dat.name,
            dat=self.dat,
            reset=False)
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Success")
        msgBox.setText("The current FOQUS session has been uploaded to Turbine")
        msgBox.exec_()

    def runSim(self, node=None, valList=None, rows=None):
        '''
            Start simulation in a separate thread and setup a timer
            to monitor it.  If node is set to a node name only a single
            node given by the name is evaluated
        '''
        turb_config = self.dat.flowsheet.turbConfig
        turb_sim_list = self.dat.flowsheet.turbineSimList()
        self.applyNodeEdgeChanges()
        if node in self.dat.flowsheet.nodes:
            self.dat.flowsheet.onlySingleNode = node
            self.setStatus(
                "Running Single Node ({0}) Simulation...".format(node))
        elif valList is not None:
            self.dat.flowsheet.onlySingleNode = None
            self.setStatus("Running Flowsheet Set...")
        else:
            self.dat.flowsheet.onlySingleNode = None
            self.setStatus("Running Single Flowsheet Simulation...")
        if self.dat.foqusSettings.runFlowsheetMethod == 0:
            # run in FOQUS
            if valList is not None:
                self.multiRun = self.dat.flowsheet.runListAsThread(
                    valList)
                self.singleRun = None
            else:
                self.singleRun = self.dat.flowsheet.runAsThread()
                self.multiRun=None
        elif self.dat.foqusSettings.runFlowsheetMethod == 1:
            # Submit to Turbine <-> FOQUS consumer
            # first save a session file (need to upload to turbine)
            self.dat.flowsheet.uploadFlowseetToTurbine(
                self.dat.name,
                dat=self.dat,
                reset=False)
            if valList is not None:
                self.multiRun = self.dat.flowsheet.runListAsThread(
                    valList,
                    useTurbine=True)
                self.singleRun = None
            else:
                self.singleRun = self.dat.flowsheet.runAsThread(
                    useTurbine=True)
                self.multiRun = None
        self.refreshFlowsheet()
        self.stopAction.setEnabled(True)
        self.runAction.setEnabled(False)
        self.nodeDock.runButton.setEnabled(False)
        self.nodeDock.stopButton.setEnabled(True)
        self.runningSingle = True
        self.startTime = time.time()
        self.replaceRows = rows
        self.multiRunDone = {}
        if rows is not None:
            for row in rows: self.multiRunDone[row] = False
        self.multiSuccess = 0
        self.multiError = 0
        delay = 500 # time in ms between checking simulation status
        self.timer = QtCore.QTimer(self)
        self.connect(
            self.timer,
            QtCore.SIGNAL("timeout()"),
            self.checkSim)
        self.timer.start(delay)

    def checkSim(self):
        '''
            Check if a single simulation is done.  If it is call
            stopSim to read results and finish up. Also update
            the status bar with the elapsed time.
        '''
        if self.singleRun is not None:
            if not self.singleRun.is_alive():
                self.stopSim()
            else:
                self.setStatus(
                    "Running Single Simulation... Elapsed Time: {0}".format(
                        hhmmss(int(time.time() - self.startTime))))
        elif self.multiRun is not None:
            gt = self.multiRun
            res = self.dat.flowsheet.results
            # Monitor in here to show progress
            goagain = gt.is_alive() #still running, keep waiting
            #see what's done
            with gt.resLock:
                for i, row in enumerate(self.replaceRows):
                    if self.multiRunDone[row]: continue
                    if gt.res_fin[i] != -1:
                        #A run new finished read results
                        self.multiRunDone[row] = True
                        r =  res.rlist[row]
                        res.rlist[row] = res.addFromSavedValues(
                            setName = r[res.headMap['SetName']],
                            name = r[res.headMap['ResultName']],
                            tags = r[res.headMap['Tags']],
                            valDict=gt.res[i], append=False)
                        if gt.res_fin[i] == 0: self.multiSuccess += 1
                        else: self.multiError += 1
            self.setStatus(
                "Running Simulation Set... Success: {0}/{1} Error: {2}/{1} Elapsed Time: {3}".format(
                    self.multiSuccess, len(gt.res), self.multiError, hhmmss(int(time.time() - self.startTime))))
            if not goagain: self.stopSim()

    def stopSim(self):
        '''
            If a single simulation has been started with runSim, this
            will stop it and read the results. The simulation can be
            stopped before it is finished; this will put -1 error codes
            in the graph and nodes indicating that the simulation
            wasn't run or finished.  Stopping the simulation will
            terminate anything running in turbine.  It will kill the
            worker thread/process (hopefully) although that may take
            some time.
        '''
        self.timer.stop()
        self.stopAction.setEnabled(False)
        # Next will wait for the single run thread to close down all the
        # way and save the results.  This may delay stopping a bit
        if self.multiRun is not None:
            gt = self.multiRun
            gt.join(10)
            self.runAction.setEnabled(True)
            self.nodeDock.runButton.setEnabled(True)
            self.nodeDock.stopButton.setEnabled(False)
            self.setStatus(
                "Stopped Simulation Set... Success: {0}/{1} Error: {2}/{1} Elapsed Time: {3}".format(
                    self.multiSuccess, len(gt.res), self.multiError, hhmmss(int(time.time() - self.startTime))))
        elif self.singleRun is not None:
            self.singleRun.join(10)
            self.runAction.setEnabled(True)
            self.nodeDock.runButton.setEnabled(True)
            self.nodeDock.stopButton.setEnabled(False)
            if self.singleRun.res[0]:
                self.dat.flowsheet.loadValues(self.singleRun.res[0])
                self.dat.flowsheet.results.headersFromGraph()
                self.dat.flowsheet.results.addFromSavedValues(
                    'Single_runs',
                    'single_{0}'.format(self.dat.flowsheet.singleCount),
                    None,
                    self.singleRun.res[0])
            else:
                self.dat.flowsheet.setErrorCode(20)
                logging.getLogger("foqus." + __name__).error(
                    "to results graph thread was likely terminated")
            self.refresh()
            if not self.dataBrowserDialog.isHidden():
                self.dataBrowserDialog.dataFrame.refreshContents()
            err = self.dat.flowsheet.errorStat
            errText = self.dat.flowsheet.errorLookup(err)
            self.runningSingle = False
            self.dat.flowsheet.onlySingleNode = None
            if err == 0:
                QMessageBox.information(
                    self,
                    "Finished in " + hhmmss(int(self.dat.flowsheet.solTime)),
                    "The simulation completed successfully.")
                self.setStatus(
                    "Finished Single Simulation... Success in " +
                    hhmmss(int(self.dat.flowsheet.solTime)))
            elif err == 100:
                QMessageBox.information(
                    self,
                    "Finished in " + hhmmss(int(self.dat.flowsheet.solTime)) + "s",
                    "The single node simulation completed successfully.")
                self.setStatus(
                    "Finished Single Node Simulation... Success in " +
                    hhmmss(int(self.dat.flowsheet.solTime)))
            else:
                QMessageBox.critical(
                    self,
                    "Error in " + hhmmss(int(self.dat.flowsheet.solTime)) + "s",
                    "The simulation completed with an error " +
                        str(err) +
                        ", " +
                        errText)
                self.setStatus(
                    "Error Single Simulation in " +
                    hhmmss(int(self.dat.flowsheet.solTime)) + " ... " +
                    str(err) +
                    ", " +
                    errText)

    def loadDefaultInput(self):
        '''
            Return inputs to default values
        '''
        msgBox = QMessageBox()
        msgBox.setText("Load Defaults?")
        msgBox.setInformativeText(
            ("Do you want replace current "
            "input values with the defaults?"))
        msgBox.setStandardButtons(
            QMessageBox.No | QMessageBox.Yes)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        if ret == QMessageBox.Yes:
            self.applyNodeEdgeChanges()
            self.dat.flowsheet.loadDefaults()
            self.refresh()

    def testSCC(self):
        [
            sccNodes,
            sccEdges,
            outEdges,
            inEdges,
            sccOrder
        ] = self.dat.flowsheet.stronglyConnectedSubGraphs(True)
        print "Strongly connected component test\n"
        print "nodes"
        print sccNodes
        print "\nedges\n"
        print sccEdges
        print "\nOrder\n"
        print sccOrder

    def testTear(self):
        [tearSets, ub1, ub2] = self.dat.flowsheet.selectTear()
        self.dat.flowsheet.setTearSet(tearSets[0])
        self.flowsheetEditor.createScene()
        self.setupTimer(None, tearSets, len(tearSets), 2000)

    def testCalcOrder(self):
        [tearSets, ub1, ub2] = self.dat.flowsheet.selectTear()
        self.dat.flowsheet.setTearSet(tearSets[0])
        self.flowsheetEditor.createScene()
        order = self.dat.flowsheet.calculationOrder()
        self.setupTimer(order, None, len(order), 1000)

    def testCycles(self):
        [cycles, edges] = self.dat.flowsheet.allCycles()
        print "Found " + str(len(cycles)) + " cycles"
        self.setupTimer(cycles, edges, len(cycles), 1000)

    def testObjCalc(self):
        print self.dat.flowsheet.calcObjective()

    def setupTimer(self, nodeLists, edgeLists, nFrames, delay=1000):
        self.nodes = nodeLists
        self.edges = edgeLists
        self.index = 0
        self.endIndex = nFrames
        if self.nodes == None:
            self.nodes = []
            for i in range(0,nFrames):
                self.nodes.append([])
        if self.edges == None:
            self.edges = []
            for i in range(0,nFrames):
                self.edges.append([])
        self.timer = QtCore.QTimer(self)
        self.connect(
            self.timer,
            QtCore.SIGNAL("timeout()"),
            self.highlight)
        self.timer.start(delay)

    def highlight(self):
        print self.index
        if self.index == self.endIndex:
            self.timer.stop()
            self.flowsheetEditor.sc.selectedNodes = []
            self.flowsheetEditor.sc.selectedEdges = []
            self.flowsheetEditor.createScene()
            return
        try:
            self.flowsheetEditor.sc.selectedNodes = list(
                self.nodes[self.index])
        except:
            self.flowsheetEditor.sc.selectedNodes = []
        try:
            self.flowsheetEditor.sc.selectedEdges = list(
                self.edges[self.index])
        except:
            self.flowsheetEditor.sc.selectedEdges = []
        self.flowsheetEditor.createScene()
        self.index += 1

    def updateRecentlyOpened(self):
        '''
            Update recent file menu
        '''
        if self.dat.currentFile != "":
            self.dat.foqusSettings.addRecentlyOpenedFile(
                self.dat.currentFile)
        self.openRecentMainMenu.clear()
        self.openRecentAction = []
        for i, f in enumerate(
            self.dat.foqusSettings.getRecentlyOpendFiles()):
            self.openRecentAction.append(QAction(f, self))
            self.openRecentAction[i].setIcon(QIcon())
            self.openRecentAction[i].triggered.connect(
                functools.partial(self.loadSessionFile,f))
            self.openRecentMainMenu.addAction(
                self.openRecentAction[i])

    def runTestScript(self, fileName):
        '''
            This function is use to automatically run a UI test script
            when FOQUS starts.
        '''
        if self.tstimer is not None:
            self.tstimer.stop()
        self.helpDock.loadDbgCode(fileName)
        self.helpDock.runDebugCode()
