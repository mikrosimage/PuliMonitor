from uuid import uuid4

from PyQt4.QtCore import Qt, QSettings, QByteArray
from PyQt4.QtGui import QMainWindow, QTabWidget, QDockWidget, QToolBar, QAction, \
    QStyle, qApp, QApplication, QMessageBox

from pulimonitor.network import requesthandler
from pulimonitor.ui.about import dialog
from pulimonitor.ui.job.panel import JobPanel
from pulimonitor.ui.pool.panel import PoolPanel
from pulimonitor.ui.rendernode.details import RenderNodeDetails
from pulimonitor.ui.rendernode.panel import RenderNodePanel
from pulimonitor.ui.rendernode.view import RenderNodeTableView
from pulimonitor.ui.serverswitch import ServerSwitchDialog


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Puli Monitor')
        self.requestHandler = requesthandler.get()

        # setup menus and toolbars
        self.initActions()
        self.initMenu()
        self.initToolbar()

        # setup docks and rendernode panels
        self.setTabPosition(Qt.TopDockWidgetArea, QTabWidget.North)
        self.addRenderNodePanel()
#         self.addPoolsPanel()
#         self.addJobPanel()
        self.restoreSettings()
        self.requestHandler.start()

    def initActions(self):
        '''
        Create and setup actions valid in the main window
        '''
        self.refreshAction = QAction(qApp.style().standardIcon(QStyle.SP_BrowserReload), "Refresh", self)
        self.refreshAction.triggered.connect(self.requestHandler.requestAll)

        self.switchServerAction = QAction("Switch Servers", self)
        self.switchServerAction.triggered.connect(self.onSwitchServer)

        self.prefsEditAction = QAction('Preferences', self)
        self.prefsEditAction.triggered.connect(self.editPreferences)
        self.prefsEditAction.setShortcut('Ctrl+p')
        self.prefsEditAction.setStatusTip('Edit application preferences')

        self.addRenderNodePanelAction = QAction("Rendernodes", self)
        self.addRenderNodePanelAction.triggered.connect(self.addRenderNodePanel)
        self.addRenderNodeDetailsPanelAction = QAction("Rendernode Details", self)
        self.addRenderNodeDetailsPanelAction.triggered.connect(self.addRenderNodeDetailsPanel)

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
        fileMenu.addAction(self.switchServerAction)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.prefsEditAction)
        windowMenu = menubar.addMenu('&Window')
        panelsMenu = windowMenu.addMenu("Panels")
        panelsMenu.addAction(self.addRenderNodePanelAction)
        panelsMenu.addAction(self.addRenderNodeDetailsPanelAction)
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
        dock = QDockWidget("rendernodes", self)
        dock.setObjectName("rendernodes-dock-{0}".format(uuid4().hex))
        dock.setWidget(RenderNodePanel(dock))
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

    def addRenderNodeDetailsPanel(self):
        focusWidget = QApplication.focusWidget()
        if isinstance(focusWidget, RenderNodeTableView):
            rnDetails = RenderNodeDetails(self)
            focusWidget.selectedRendernodesChanged.connect(rnDetails.onRendernodeChanged)
            self.addDockWidget(Qt.BottomDockWidgetArea, rnDetails)
        else:
            QMessageBox.information(self, "Rendernodes", "Please focus a"
                                    " rendernode view to attach to.")

    def addPoolsPanel(self):
        '''
        Add a pool panel to the main window. All views on the panels
        share one data model.
        '''
        dock = QDockWidget("pools", self)
        dock.setObjectName("pools-dock-{0}".format(uuid4().hex))
        poolPanel = PoolPanel(dock)
        dock.setWidget(poolPanel)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

    def addJobPanel(self):
        '''
        Add a job panel to the main window. All views on the panels
        share one data model.
        '''
        dock = QDockWidget("jobs", self)
        dock.setObjectName("jobs-dock-{0}".format(uuid4().hex))
        jobPanel = JobPanel(dock)
        dock.setWidget(jobPanel)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

    def onSwitchServer(self):
        d = ServerSwitchDialog(self)
        d.serverChanged.connect(self.requestHandler.onServerChanged)
        d.show()

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
        self.requestHandler.stop()
        self.saveSettings()
        return QMainWindow.closeEvent(self, *args, **kwargs)

    def saveSettings(self):
        '''
        Save all settings related to the main window. This is not to be confused with
        actual 'configuration' and only stores states of the ui.
        This method also notifies child widgets to save their settings.
        '''
        settings = QSettings()
        settings.beginGroup("mainwindow")
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
