from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QPointF
from PyQt5.QtGui import QBrush, QTransform
from PyQt5 import uic
from simulation import Simulation

class ApplicationWidget:

    status = "STOPPED"

    def __init__(self, params):
        self.window = uic.loadUi("src/applicationwindow.ui")
        self.simulation = Simulation(params)

        self.update_parameters()

        # Setup signals for parameter sliders and buttons
        self.window.slider_alignment.valueChanged.connect(self.sliders_updated)
        self.window.slider_cohesion.valueChanged.connect(self.sliders_updated)
        self.window.slider_separation.valueChanged.connect(self.sliders_updated)
        self.window.slider_boid_count.valueChanged.connect(self.sliders_updated)
        self.window.slider_random.valueChanged.connect(self.sliders_updated)

        self.window.btn_load.clicked.connect(self.load_parameters)
        self.window.btn_save.clicked.connect(self.save_parameters)
        self.window.btn_apply.clicked.connect(self.apply_settings)

        self.window.btn_start.clicked.connect(self.start_simulation)
        self.window.btn_pause.clicked.connect(self.pause_simulation)
        self.window.btn_stop.clicked.connect(self.stop_simulation)
        
        self.window.simulation_canvas.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.window.simulation_canvas.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.window.simulation_canvas.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.window.simulation_canvas.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.scene = self.create_scene()

        # Timer to control simulation updates
        self.timer = QTimer()
        self.timer.setInterval(1000/60)
        self.timer.timeout.connect(self.refresh_simulation)
        self.timer.start()

        # The program segfaulted when exiting due to some dark GC magic. This fixes it
        self.window.close = self.clean_exit


    def show(self):
        self.window.show()


    def create_scene(self):
        scene = QGraphicsScene()
        bgBrush = QBrush(Qt.lightGray, Qt.CrossPattern)
        bgTransform = QTransform()
        bgTransform.scale(16, 16)
        bgBrush.setTransform(bgTransform)
        scene.setBackgroundBrush(bgBrush)
        scene.sceneRect = None
        for boid in self.simulation.boids:
            scene.addItem(boid)
        
        self.window.simulation_canvas.setScene(scene)
        return scene


    @pyqtSlot()
    def clean_exit(self, obj):
        pass


    @pyqtSlot()
    def refresh_simulation(self):
        self.simulation.refresh(self.status == "RUNNING")
        self.scene.invalidate()
        self.window.simulation_canvas.fitInView(self.simulation.view_x, self.simulation.view_y, \
                self.simulation.view_w, self.simulation.view_h, Qt.KeepAspectRatio)


    @pyqtSlot()
    def sliders_updated(self):
        self.window.lab_boid_count.setText("Amount of boids: {0:3d}".format(self.window.slider_boid_count.value()))
        self.window.lab_alignment.setText("Alignment weight: {0:3d}".format(self.window.slider_alignment.value()))
        self.window.lab_cohesion.setText("Cohesion weight: {0:3d}".format(self.window.slider_cohesion.value()))
        self.window.lab_separation.setText("Separation weight: {0:3d}".format(self.window.slider_separation.value()))
        self.window.lab_random.setText("Random movement: {0:3d}".format(self.window.slider_random.value()))


    def update_parameters(self):
        self.window.slider_boid_count.setValue(self.simulation.params.boid_count)
        self.window.slider_alignment.setValue(self.simulation.params.weight_alignment)
        self.window.slider_cohesion.setValue(self.simulation.params.weight_cohesion)
        self.window.slider_separation.setValue(self.simulation.params.weight_separation)
        self.window.slider_random.setValue(self.simulation.params.random_effect)

        self.sliders_updated()


    @pyqtSlot()
    def save_parameters(self):
        self.apply_settings()
        file_name = QFileDialog.getSaveFileName()[0]
        if file_name == "":
            return
        try:
            self.simulation.params.save_to_file(file_name)
        except Exception as e:
            msg = QMessageBox(self.window)
            msg.setText("The configuration could not be saved.")
            msg.show()


    @pyqtSlot()
    def load_parameters(self):
        file_name = QFileDialog.getOpenFileName()[0]
        if file_name == "":
            return
        try:
            self.simulation.params.load_from_file(file_name)
            self.update_parameters()
        except Exception as e:
            msg = QMessageBox(self.window)
            msg.setText("The configuration could not be loaded {}".format(str(e)))
            msg.show()

    
    @pyqtSlot()
    def apply_settings(self):
        self.simulation.params.boid_count = self.window.slider_boid_count.value()
        self.simulation.params.weight_alignment = self.window.slider_alignment.value()
        self.simulation.params.weight_cohesion = self.window.slider_cohesion.value()
        self.simulation.params.weight_separation = self.window.slider_separation.value()
        self.simulation.params.random_effect = self.window.slider_random.value()

    
    @pyqtSlot()
    def start_simulation(self):
        if self.status == "STOPPED" or self.status == "PAUSED":

            self.window.btn_start.setText("Start")
            self.window.lab_status.setText("Simulation running.")
            
            self.window.btn_start.setEnabled(False)
            self.window.btn_pause.setEnabled(True)
            self.window.btn_stop.setEnabled(True)
            
            self.status = "RUNNING"
    

    @pyqtSlot()
    def pause_simulation(self):
        if self.status == "RUNNING":
            self.window.btn_start.setText("Continue")
            self.window.lab_status.setText("Simulation paused.")
            
            self.window.btn_start.setEnabled(True)
            self.window.btn_pause.setEnabled(False)
            self.window.btn_stop.setEnabled(True)

            self.status = "PAUSED"
    

    @pyqtSlot()
    def stop_simulation(self):
        self.window.btn_start.setText("Start")
        self.window.lab_status.setText("Simulation stopped.")

        self.window.btn_start.setEnabled(True)
        self.window.btn_pause.setEnabled(False)
        self.window.btn_stop.setEnabled(True)

        self.simulation.reset()
        self.scene = self.create_scene()

        self.status = "STOPPED"

