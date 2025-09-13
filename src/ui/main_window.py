"""
Main window module for the Tolerance Visualizer application.
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMenuBar, QToolBar,
    QStatusBar, QMessageBox, QFileDialog, QSplitter,
    QTextEdit, QLabel, QPushButton)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon
import pandas as pd
from pathlib import Path

class MainWindow(QMainWindow):
    """Main application window"""

    #Signals
    data_imported = Signal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.current_data = None
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Tolerance Chain Visualizer")
        self.setGeometry(100, 100, 1200, 800)

        #create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        #create splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        #left panel - data table
        self.setup_data_panel(splitter)

        #right panel - analysis result
        self.setup_analysis_panel(splitter)

        #setup menu, toolbar, status bar
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()

        #set splitter proportions
        splitter.setSizes([700, 500])

    def setup_data_panel(self, parent):
        """Setup the data panel"""
        data_widget = QWidget()
        layout = QVBoxLayout(data_widget)

        #header
        header_layout = QHBoxLayout()
        data_label = QLabel("📊 Tolerance Data")
        data_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        header_layout.addWidget(data_label)
        header_layout.addStretch()

        #hmport button
        self.import_btn = QPushButton("📁 Import Data")
        self.import_btn.setToolTip("Import tolerance data from CSV or Excel file")
        header_layout.addWidget(self.import_btn)

        layout.addLayout(header_layout)

        #data table
        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        layout.addWidget(self.data_table)

        parent.addWidget(data_widget)

    def setup_analysis_panel(self, parent):
        """Setup the analysis result panel"""
        analysis_widget = QWidget()
        layout = QVBoxLayout(analysis_widget)

        #header
        analysis_label = QLabel("🔍 Analysis Results")
        analysis_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        layout.addWidget(analysis_label)

        #results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlainText("Import tolerance data to begin analysis...")
        layout.addWidget(self.results_text)

        #analysis buttons
        button_layout = QHBoxLayout()
        self.analyze_btn = QPushButton("🧮 Analyze Tolerances")
        self.analyze_btn.setEnabled(False)
        self.export_btn = QPushButton("💾 Export Results")
        self.export_btn.setEnabled(False)

        button_layout.addWidget(self.analyze_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        parent.addWidget(analysis_widget)
    
    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()

        #file menu
        file_menu = menubar.addMenu("&File")

        import_action = QAction("&Import Data...", self)
        import_action.setShortcut("Ctrl+0")
        import_action.setStatusTip("Import tolerance data from file")
        file_menu.addAction(import_action)

        export_action = QAction("&Export Results...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.setStatusTip("Export analysis results")
        export_action.setEnabled(False)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        #tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        analyze_action = QAction("&Analyze Tolerances", self)
        analyze_action.setShortcut("Ctrl+A")
        analyze_action.setStatusTip("Perform tolerance chain analysis")
        analyze_action.setEnabled(False)
        tools_menu.addAction(analyze_action)

        #help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Store actions for later use
        self.import_action = import_action
        self.export_action = export_action
        self.analyze_action = analyze_action
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Tolerance Chain Visualizer",
            """<h3>Tolerance Chain Visualizer v0.1.0</h3>
            <p>A learning project for tolerance analysis and visualization.</p>
            <p>Built with PySide6 and Pandas</p>
            <p><b>Author:</b> Diana Husanu</p>
            <p><b>Purpose:</b> Just for fun :) </p>"""
        )

    def setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Add actions to toolbar
        toolbar.addAction(self.import_action)
        toolbar.addSeparator()
        toolbar.addAction(self.analyze_action)
        toolbar.addAction(self.export_action)

    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Import data to begin", 5000)

    def setup_connections(self):
        """Connect signals and slots"""
        self.import_btn.clicked.connect(self.import_data)
        self.import_action.triggered.connect(self.import_data)
        self.analyze_btn.clicked.connect(self.analyze_data)
        self.analyze_action.triggered.connect(self.analyze_data)

    def import_data(self):
        """Import data from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Tolerance Data",
            str(Path.home()),
            "Data files (*.csv *.xlsx *.xls);;CSV files (*.csv);;Excel files (*.xlsx *.xls)"
        )
        
        if not file_path:
            return
            
        try:
            # Load data based on file extension
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
                
            self.load_data_to_table(df)
            self.current_data = df
            self.data_imported.emit(df)
            
            # Enable analysis controls
            self.analyze_btn.setEnabled(True)
            self.analyze_action.setEnabled(True)
            
            self.status_bar.showMessage(f"Imported {len(df)} rows from {Path(file_path).name}", 3000)
            self.results_text.setPlainText(f"✅ Data imported successfully!\n\nRows: {len(df)}\nColumns: {list(df.columns)}\n\nReady for analysis...")
            
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import data:\n{str(e)}")
            self.status_bar.showMessage("Import failed", 3000)
            
    def load_data_to_table(self, df):
        """Load DataFrame into the table widget"""
        self.data_table.setRowCount(len(df))
        self.data_table.setColumnCount(len(df.columns))
        self.data_table.setHorizontalHeaderLabels(df.columns.tolist())
        
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                self.data_table.setItem(row, col, item)
                
        self.data_table.resizeColumnsToContents()
        
    def analyze_data(self):
        """Perform tolerance analysis"""
        if self.current_data is None:
            QMessageBox.warning(self, "No Data", "Please import data first.")
            return
            
        # Placeholder analysis - will be implemented later
        results = f"""🔍 TOLERANCE ANALYSIS RESULTS

Data Summary:
• Total components: {len(self.current_data)}
• Columns: {', '.join(self.current_data.columns)}

Basic Statistics:
{self.current_data.describe() if len(self.current_data.select_dtypes(include=['number']).columns) > 0 else 'No numeric columns found'}

⚠️ Advanced tolerance calculations will be implemented in next phase.
        """
        
        self.results_text.setPlainText(results)
        self.export_btn.setEnabled(True)
        self.export_action.setEnabled(True)
        self.status_bar.showMessage("Analysis completed", 3000)