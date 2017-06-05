from Stiffness import Stiffness
from PyQt4.uic import loadUiType

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)

Ui_MainWindow, QMainWindow = loadUiType("mainwindow.ui")

class Main(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.calculateButton.clicked.connect(self.handleCalculate)
        self.pointedForceButton.clicked.connect(self.handleAddForce)
        self.pointedMomentButton.clicked.connect(self.handleAddMoment)
        self.clearForceTableButton.clicked.connect(self.handleRemoveForce)
        self.clearMomentsTableButton.clicked.connect(self.handleRemoveMoment)
        self.basic_user_forces = {}
        self.basic_user_moments = {}
        self.user_forces = {}
        self.user_moments = {}

    def setData(self):
        self.user_length = float(str(self.lengthValue.text()))
        self.user_width = float(str(self.widthValue.text()))
        self.user_height = float(str(self.heightValue.text()))
        self.user_quantity_bars = float(str(self.quantityValue.text()))
        self.user_diameter_bars = 0.001 * float(str(self.diameterValue.text()))
        self.user_placement_bars = 0.001 * float(str(self.steelPlacementValue.text()))
        self.user_moe_concrete = 1000 * float(str(self.moeConcreteValue.text()))
        self.user_moe_steel = 1000 * float(str(self.moeSteelValue.text()))
        self.user_cracking_moment = float(str(self.crackingValue.text()))
        self.user_load = float(str(self.uniformLoadValue.text()))
        self.user_forces = self.basic_user_forces
        self.user_moments = self.basic_user_moments

    def clearData(self):
        self.user_length = 0
        self.user_width = 0
        self.user_height = 0
        self.user_quantity_bars = 0
        self.user_diameter_bars = 0
        self.user_placement_bars = 0
        self.user_moe_concrete = 0
        self.user_moe_steel = 0
        self.user_cracking_moment = 0
        self.user_load = 0
        self.resultMomentsTable.setRowCount(0)
        self.resultStiffnessTable.setRowCount(0)

    def addMomentsPlot(self, fig):
        self.canvas_m = FigureCanvas(fig)
        for i in reversed(range(self.verticalLayoutMoments.count())):
            self.verticalLayoutMoments.itemAt(i).widget().setParent(None)
        self.verticalLayoutMoments.addWidget(self.canvas_m)
        self.canvas_m.draw()

    def addStiffnessPlot(self, fig):
        self.canvas_s = FigureCanvas(fig)
        for i in reversed(range(self.verticalLayoutStiffness.count())):
            self.verticalLayoutStiffness.itemAt(i).widget().setParent(None)
        self.verticalLayoutStiffness.addWidget(self.canvas_s)
        self.canvas_s.draw()

    def addMomentsValuesTable(self, stiffness):
        for step in range(0, 101, 1):
            self.resultMomentsTable.setRowCount(self.resultMomentsTable.rowCount() + 1)
            currentRow = self.resultMomentsTable.rowCount() - 1
            currentLocation = (self.user_length / 100) * step
            self.resultMomentsTable.setItem(currentRow, 0, QtGui.QTableWidgetItem(str(round(currentLocation, 3))))
            self.resultMomentsTable.setItem(currentRow, 1,
                                            QtGui.QTableWidgetItem(
                                                str(round(stiffness.rc_element.moments_values[step], 3))))

    def addStiffnessValuesTable(self, stiffness):
        for step in range(0, 101, 1):
            self.resultStiffnessTable.setRowCount(self.resultStiffnessTable.rowCount() + 1)
            currentRow = self.resultStiffnessTable.rowCount() - 1
            currentLocation = (self.user_length / 100) * step
            self.resultStiffnessTable.setItem(currentRow, 0, QtGui.QTableWidgetItem(str(round(currentLocation, 3))))
            self.resultStiffnessTable.setItem(currentRow, 1,
                                              QtGui.QTableWidgetItem(str(round(stiffness.stiffness_values[step], 3))))

    def handleCalculate(self):
        self.clearData()
        self.setData()

        stiffness = Stiffness(self.user_length, self.user_width, self.user_height, self.user_quantity_bars,
                              self.user_diameter_bars, self.user_placement_bars, self.user_moe_concrete,
                              self.user_moe_steel,self.user_load, self.user_forces,self.user_moments,
                              self.user_cracking_moment)
        stiffness.uncracked_compressive_zone_height_calculation()
        stiffness.cracked_compressive_zone_height_calculation()
        stiffness.uncracked_moment_of_inertia_calculation()
        stiffness.cracked_moment_of_inertia_calculation()
        stiffness.stiffness_calculation()
        figure1 = Figure()
        plot1 = figure1.add_subplot(111)
        plot1.plot(stiffness.rc_element.moments_values)
        self.addMomentsPlot(figure1)
        figure2 = Figure()
        plot2 = figure2.add_subplot(111)
        plot2.plot(stiffness.stiffness_values)
        self.addStiffnessPlot(figure2)
        self.addMomentsValuesTable(stiffness)
        self.addStiffnessValuesTable(stiffness)

    def handleAddForce(self):
        self.pointedForceTable.setRowCount(self.pointedForceTable.rowCount() + 1)
        currentRow = self.pointedForceTable.rowCount() - 1
        self.pointedForceTable.setItem(currentRow, 0, QtGui.QTableWidgetItem(self.pointedForceValue.text()))
        self.pointedForceTable.setItem(currentRow, 1, QtGui.QTableWidgetItem(self.pointedForceLocation.text()))
        self.basic_user_forces[self.pointedForceLocation.text()] = self.pointedForceValue.text()

    def handleAddMoment(self):
        self.pointedMomentTable.setRowCount(self.pointedMomentTable.rowCount()+1)
        currentRow = self.pointedMomentTable.rowCount() - 1
        self.pointedMomentTable.setItem(currentRow, 0, QtGui.QTableWidgetItem(self.pointedMomentValue.text()))
        self.pointedMomentTable.setItem(currentRow, 1, QtGui.QTableWidgetItem(self.pointedMomentLocation.text()))
        self.basic_user_moments[self.pointedMomentLocation.text()] = self.pointedMomentValue.text()

    def handleRemoveForce(self):
        self.basic_user_forces = {}
        self.pointedForceTable.clearContents()
        self.pointedForceTable.setRowCount(0)


    def handleRemoveMoment(self):
        self.basic_user_moments = {}
        self.pointedMomentTable.clearContents()
        self.pointedMomentTable.setRowCount(0)


if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


