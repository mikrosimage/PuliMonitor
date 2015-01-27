from uuid import uuid4

from PyQt4.QtCore import Qt, QSettings, QByteArray
from PyQt4.QtGui import QMainWindow, QTabWidget, QDockWidget, QToolBar, QAction, \
    QStyle, qApp

from network.requesthandler import getRequestHandler
from ui.about import dialog
from ui.job.panel import JobPanel
from ui.pool.panel import PoolPanel
from ui.rendernode.panel import RenderNodePanel


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Puli Monitor')

        # setup menus and toolbars
        self.initActions()
        self.initMenu()
        self.initToolbar()

        # setup docks and rendernode panels
        self.setTabPosition(Qt.TopDockWidgetArea, QTabWidget.North)
        self.addRenderNodePanel()
#         self.addJobPanel()
        self.restoreSettings()

    def initActions(self):
        '''
        Create and setup actions valid in the main window
        '''
        self.refreshAction = QAction(qApp.style().standardIcon(QStyle.SP_BrowserReload), "Refresh", self)
        self.refreshAction.triggered.connect(getRequestHandler().requestAll)

        self.prefsEditAction = QAction('Preferences', self)
        self.prefsEditAction.triggered.connect(self.editPreferences)
        self.prefsEditAction.setShortcut('Ctrl+p')
        self.prefsEditAction.setStatusTip('Edit application preferences')

        self.addRenderNodePanelAction = QAction("Rendernodes", self)
        self.addRenderNodePanelAction.triggered.connect(self.addRenderNodePanel)

        self.addPoolPanelAction = QAction("Pools", self)
        self.addPoolPanelAction.triggered.connect(self.addPoolsPanel)

        self.aboutAction = QAction('About', self)
        self.aboutAction.triggered.connect(dialog)

    def initMenu(self):
        '''
        Setup the menu bar with menus and add actions.
        '''
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.refreshAction)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.prefsEditAction)
        windowMenu = menubar.addMenu('&Window')
        panelsMenu = windowMenu.addMenu("Panels")
        panelsMenu.addAction(self.addRenderNodePanelAction)
        panelsMenu.addAction(self.addPoolPanelAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(self.aboutAction)

    def initToolbar(self):
        '''
        Add main toolbar and add actions needed for quick access.
        '''
        self.mainToolbar = QToolBar(self)
        self.mainToolbar.setObjectName("MainToolbar")
        self.mainToolbar.addAction(self.refreshAction)
        self.addToolBar(self.mainToolbar)

    def addRenderNodePanel(self):
        '''
        Add a render node panel to the main window. All views on the panels
        share one data model.
        '''
        dock = QDockWidget("Rendernodes", self)
        dock.setObjectName("rendernodes-dock-{0}".format(uuid4().hex))
        dock.setWidget(RenderNodePanel(dock))
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

    def addPoolsPanel(self):
        '''
        Add a pool panel to the main window. All views on the panels
        share one data model.
        '''
        dock = QDockWidget("Pools", self)
        dock.setObjectName("pools-dock-{0}".format(uuid4().hex))
        poolPanel = PoolPanel(dock)
        dock.setWidget(poolPanel)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

    def addJobPanel(self):
        '''
        Add a job panel to the main window. All views on the panels
        share one data model.
        '''
        dock = QDockWidget("Jobs", self)
        dock.setObjectName("jobs-dock-{0}".format(uuid4().hex))
        jobPanel = JobPanel(dock)
        dock.setWidget(jobPanel)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

    def editPreferences(self):
        '''
        Slot called to open the preferences edit dialog.
        '''
        print "Not yet implemented"

    def closeEvent(self, *args, **kwargs):
        '''
        Reimplemented from QMainWindw. Called when the main window closes.
        Saves the current widget layout and frees resources
        '''
        # TODO: implement saving settings here
        rh = getRequestHandler()
        rh.stop()
        self.saveSettings()
        return QMainWindow.closeEvent(self, *args, **kwargs)

    def saveSettings(self):
        '''
        Save all settings related to the main window. This is not to be confused with
        actual 'configuration' and only stores states of the ui.
        This method also notifies child widgets to save their settings.
        '''
        settings = QSettings()
        settings.beginGroup(self.__class__.__name__)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.endGroup()

    def restoreSettings(self):
        '''
        Restore main window and child widget settings/states.
        '''
        settings = QSettings()
        settings.beginGroup(self.__class__.__name__)
        self.restoreGeometry(settings.value("geometry", QByteArray()))
        self.restoreState(settings.value("state", QByteArray()))
        settings.endGroup()
