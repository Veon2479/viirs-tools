import os
os.system('pyuic6 ./mainwindow.ui -o ./mainwindow.py')  # build ui

import sys
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QSettings
import mainwindow

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

import re
from datetime import datetime
import rasterio
import numpy as np
from math import nan

import viirs_tools.NightMask as NM
import viirs_tools.CloudMask as CM
import viirs_tools.Fires as F
import viirs_tools.LST as LST
import viirs_tools.Water as W
import viirs_tools.Utils as U

# os.environ["CUDA_VISIBLE_DEVICES"] = "" # force use CPU by masking CUDA devices
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import load_model

model = load_model('./89-0.9206-0.1881-best_val_loss.model.keras')

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # Init window geometry
        self.showMaximized()
        self.setFixedSize(self.size())

        # Custom variables
        self.fig_save_dir = './figs'
        self.raster_save_dir = './rasters'

        self.roots = []
        self.files = []
        self.timestamps = []

        self.selected_ts_index = 0
        self.selected_file_index = 0

        self.working_directory = None
        self.working_directory_input = None

        # Init buttons
        self.bind_buttons()

        # Select working directory
        self.restore_settings()
        self.show_directory_dialog()
        while (self.working_directory_input is None):
            self.show_directory_dialog()
        self.working_directory = self.working_directory_input

        # Load UI data from working directory
        self.ready = self.try_load_dir()

        # Activate initial selecting features
        self.ui.tsListView.selectionModel().selectionChanged.connect(self.on_ts_selection_changed)
        self.update_file_model()

        self.control_universal_algs(True)
        if self.is_day_selected():
            self.control_night_algs(False)
            self.control_day_algs(True)
        elif self.is_night_selected():
            self.control_day_algs(False)
            self.control_night_algs(True)

    # Utils
    def load_raster(self, root, file):
        path = os.path.join(root, file)
        data = None
        with rasterio.open(path) as src:
            data = src.read()[0]
            profile = src.profile
        return data, profile
    def is_night_selected(self):
        res = True
        if 'i01_ref.tiff' in self.ts_files:
            res = False
        if 'i02_ref.tiff' in self.ts_files:
            res = False
        if 'i03_ref.tiff' in self.ts_files:
            res = False
        if 'i04_bt.tiff' not in self.ts_files:
            res = False
        if 'i05_bt.tiff' not in self.ts_files:
            res = False
        return res
    def is_day_selected(self):
        res = True
        if 'i01_ref.tiff' not in self.ts_files:
            res = False
        if 'i02_ref.tiff' not in self.ts_files:
            res = False
        if 'i03_ref.tiff' not in self.ts_files:
            res = False
        if 'i04_bt.tiff' not in self.ts_files:
            res = False
        if 'i05_bt.tiff' not in self.ts_files:
            res = False
        return res
    def get_raster_info(self):
        ti = self.selected_ts_index
        root = self.roots[ti]
        ts = self.timestamps[ti]
        return root, ts
    def get_i1(self, root):
        return self.load_raster(root, 'i01_ref.tiff')
    def get_i2(self, root):
        return self.load_raster(root, 'i02_ref.tiff')
    def get_i3(self, root):
        return self.load_raster(root, 'i03_ref.tiff')
    def get_i4(self, root):
        return self.load_raster(root, 'i04_bt.tiff')
    def get_i5(self, root):
        return self.load_raster(root, 'i05_bt.tiff')

    # Handling buttons actions
    def bind_buttons(self):
        self.ui.saveJpgBtn.clicked.connect(self.handle_saveJpgBtn)
        self.ui.saveTiffBtn.clicked.connect(self.handle_saveTiffBtn)
        self.ui.naiveNmBtn.clicked.connect(self.handle_naiveBtn)
        self.ui.wbBtn.clicked.connect(self.handle_wbBtn)
        self.ui.rCmBtn.clicked.connect(self.handle_rcmBtn)
        self.ui.fireCmBtn.clicked.connect(self.handle_firemaskBtn)
        self.ui.ndviBtn.clicked.connect(self.handle_ndviBtn)
        self.ui.monoLstBtn.clicked.connect(self.handle_monolstBtn)
        self.ui.monoMaskedLstBtn.clicked.connect(self.handle_maskedMonoLstBtn)
        self.ui.ActiveFireBtn.clicked.connect(self.handle_activefireBtn)
        self.ui.cmMlBtn.clicked.connect(self.handle_cmMlBtn)

    def control_night_algs(self, state):
        self.ui.cmMlBtn.setEnabled(state)
    def control_day_algs(self, state):
        self.ui.rCmBtn.setEnabled(state)
        self.ui.monoLstBtn.setEnabled(state)
        self.ui.monoMaskedLstBtn.setEnabled(state)
        self.ui.wbBtn.setEnabled(state)
        self.ui.ndviBtn.setEnabled(state)
    def control_universal_algs(self, state):
        self.ui.fireCmBtn.setEnabled(state)
        self.ui.naiveNmBtn.setEnabled(state)
        self.ui.ActiveFireBtn.setEnabled(state)

    def handle_saveJpgBtn(self):
        if not os.path.exists(self.fig_save_dir):
            os.makedirs(self.fig_save_dir)
        self.figure.savefig(
            os.path.join(
                self.fig_save_dir, f'{self.rendered_title} {self.rendered_ts}'
            )
        )
    def handle_saveTiffBtn(self):
        if not os.path.exists(self.raster_save_dir):
            os.makedirs(self.raster_save_dir)
        path = os.path.join(
            self.raster_save_dir, f'{self.rendered_title} {self.rendered_ts}'
        )
        with rasterio.open(path, 'w', **self.rendered_profile) as dst:
            dst.write(self.rendered_data, 1)
    def handle_naiveBtn(self):
        root, ts = self.get_raster_info()
        bi4, p = self.get_i4(root)
        ri1 = None
        if self.is_night_selected():
            ri1 = np.where(bi4 > 1, nan, nan)
        else:
            ri1, p = self.get_i1(root)
        nm = NM.naive(ri1, bi4)
        self.render_raster(nm, 'Night Mask', ts, p)
    def handle_wbBtn(self):
        root, ts = self.get_raster_info()
        ri1, p = self.get_i1(root)
        ri2, p = self.get_i2(root)
        ri3, p = self.get_i3(root)
        water = W.water_bodies_day(ri1, ri2, ri3)
        self.render_raster(water, 'Water Bodies', ts, p)
    def handle_rcmBtn(self):
        root, ts = self.get_raster_info()
        ri1, p = self.get_i1(root)
        ri2, p = self.get_i2(root)
        ri3, p = self.get_i3(root)
        bi4, p = self.get_i4(root)
        bi5, p = self.get_i5(root)
        cm = CM.rsnpp_day_img(ri1, ri2, ri3, bi4, bi5)
        self.render_raster(cm, "Rapid CM", ts, p)
    def handle_firemaskBtn(self):
        root, ts = self.get_raster_info()
        bi4, p = self.get_i4(root)
        bi5, p = self.get_i5(root)
        ncm = CM.fire_night_img(bi4, bi5)
        cm = None
        if self.is_day_selected():
            ri1, p = self.get_i1(root)
            ri2, p = self.get_i2(root)
            dcm = CM.fire_day_img(ri1, ri2, bi5)
            nm = NM.naive(ri1, bi4)
            cm = U.merge_day_night(dcm, ncm, nm)
        else:
            cm = ncm
        self.render_raster(cm, "Fire CM", ts, p)
    def handle_ndviBtn(self):
        root, ts = self.get_raster_info()
        ri1, p = self.get_i1(root)
        ri2, p = self.get_i2(root)
        ndvi = U.ndvi(ri2, ri1)
        self.render_raster(ndvi, 'NDVI', ts, p)
    def handle_monolstBtn(self):
        root, ts = self.get_raster_info()
        ri1, p = self.get_i1(root)
        ri2, p = self.get_i2(root)
        bi5, p = self.get_i5(root)
        ndvi = U.ndvi(ri2, ri1)
        lst = LST.mono_window_i05(bi5, ndvi)
        self.render_raster(lst, 'LST (unmasked)', ts, p)
    def handle_maskedMonoLstBtn(self):
        root, ts = self.get_raster_info()
        ri1, p = self.get_i1(root)
        ri2, p = self.get_i2(root)
        ri3, p = self.get_i3(root)
        bi4, p = self.get_i4(root)
        bi5, p = self.get_i5(root)
        ndvi = U.ndvi(ri2, ri1)
        cm = CM.rsnpp_day_img(ri1, ri2, ri3, bi4, bi5)
        lst = LST.mono_window_i05(bi5, ndvi, cmask=cm)
        self.render_raster(lst, 'LST (masked)', ts, p)
    def handle_activefireBtn(self):
        root, ts = self.get_raster_info()
        bi4, p = self.get_i4(root)
        bi5, p = self.get_i5(root)
        ri1 = None
        ri2 = None
        ri3 = None
        ncm = CM.fire_night_img(bi4, bi5)
        cm = None
        if self.is_day_selected():
            ri1, p = self.get_i1(root)
            ri2, p = self.get_i2(root)
            ri3, p = self.get_i3(root)
            dcm = CM.fire_day_img(ri1, ri2, bi5)
            nm = NM.naive(ri1, bi4)
            cm = U.merge_day_night(dcm, ncm, nm)
        else:
            stub = np.where(bi4 > 0, nan, nan)
            ri1 = stub
            ri2 = stub
            ri3 = stub
            cm = ncm
        nm = NM.naive(ri1, bi4)
        af = F.active_fires(ri1, ri2, ri3, bi4, bi5, nm, cm)
        af = np.where(af >= 1, 1, nan)
        self.render_raster(af, 'Active Fires', ts, p)
    def handle_cmMlBtn(self):
        root, ts = self.get_raster_info()
        bi4, p = self.get_i4(root)
        bi5, p = self.get_i5(root)
        bi4 = (bi4 - 208) / (362 - 208)
        bi5 = (bi5 - 150) / (424 - 150)
        bi4 = bi4 * 0.5 + 0.5
        bi5 = bi5 * 0.5 + 0.5
        bi4 = np.where(bi4 is nan, 0, bi4)
        bi5 = np.where(bi5 is nan, 0, bi5)
        data = np.array([bi4, bi5])
        data = np.transpose(data, (1, 2, 0))
        o = model.predict(np.expand_dims(data, axis=0))
        data = np.transpose(o[0], (2, 0, 1))
        self.render_raster(data[0], "Predicted Mask", ts, p)

    # Handle selecting input
    def on_ts_selection_changed(self, selected, deselected):
        indexes = self.ui.tsListView.selectedIndexes()
        if indexes:
            self.selected_ts_index = indexes[0].row()
            self.update_file_model()
            if self.is_day_selected():
                self.control_night_algs(False)
                self.control_day_algs(True)
            elif self.is_night_selected():
                self.control_day_algs(False)
                self.control_night_algs(True)
    def on_file_selection_changed(self, selected, deselected):
        indexes = self.ui.fileListView.selectedIndexes()
        if indexes:
            self.selected_file_index = indexes[0].row()
            self.show_raster()


    # Rendering figures
    def render_raster(self, data, title, ts, profile):
        self.figure = Figure()
        canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(1, 1, 1)

        ax.set_title(title)
        cax = ax.imshow(data, interpolation='none')
        self.figure.colorbar(cax, ax=ax)

        canvas.draw()
        width, height = canvas.get_width_height()
        image = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8).reshape(height, width, 4)
        qimage = QImage(image.data, width, height, QImage.Format.Format_RGBX8888)
        pixmap = QPixmap.fromImage(qimage)

        self.ui.figureLabel.setPixmap(pixmap)
        self.ui.saveJpgBtn.setEnabled(True)
        self.ui.saveTiffBtn.setEnabled(True)

        self.rendered_data = data
        self.rendered_title = title
        self.rendered_ts = ts
        self.rendered_profile = profile
    def show_raster(self):
        ti = self.selected_ts_index
        fi = self.selected_file_index
        root = self.roots[ti]
        files = self.files[ti]
        ts = self.timestamps[ti]
        file = files[fi]
        d, p = self.load_raster(root, file)
        title = "Data"
        if file == 'mvcm.tiff':
            title = "MVCM"
        elif file == 'i01_ref.tiff':
            title = "Reflectance at I01"
        elif file == 'i02_ref.tiff':
            title = "Reflectance at I02"
        elif file == 'i03_ref.tiff':
            title = "Reflectance at I03"
        elif file == 'i04_bt.tiff':
            title = "BT at I04"
        elif file == 'i05_bt.tiff':
            title = "BT at I05"
        self.render_raster(d, title, ts, p)


    # Loading UI data
    def show_directory_dialog(self):
        if self.working_directory is None:
            path = os.path.expanduser("~")
        else:
            path = self.working_directory
        working_directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Working Directory", path
        )
        if working_directory:
            self.working_directory_input = working_directory
    def try_load_dir(self):
        path = self.working_directory
        failed = True
        for root, dirs, files in os.walk(path):
            if dirs == []:
                tiffs = []
                for file in files:
                    if '.tiff' in file:
                        tiffs.append(file)
                if len(tiffs) > 0:
                    ts = re.search(r'A\d{7}\.\d{4}', root)
                    if ts is not None:
                        ts = ts[0]
                        timestamp = datetime.strptime(ts, 'A%Y%j.%H%M').strftime("%Y-%m-%d %H-%M")
                        self.timestamps.append(timestamp)
                        self.roots.append(root)
                        self.files.append(tiffs)
                        failed = False
        if not failed:
            self.update_ts_model()
        return False


    # Updating data models
    def update_ts_model(self):
        timestamps_model = QtCore.QStringListModel(self.timestamps)
        self.ui.tsListView.setModel(timestamps_model)
    def update_file_model(self):
        self.ts_files = self.files[self.selected_ts_index]
        file_model = QtCore.QStringListModel(self.ts_files)
        self.ui.fileListView.setModel(file_model)

        self.selected_file_index = 0
        self.ui.fileListView.selectionModel().selectionChanged.connect(self.on_file_selection_changed)


    # Setting handling
    def save_settings(self):
        settings = QSettings("viirs-demo")
        settings.setValue("path", self.working_directory)
    def restore_settings(self):
        settings = QSettings("viirs-demo")
        self.working_directory = settings.value("path")
    def closeEvent(self, event):
        self.save_settings()
        event.accept()


app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec())
