#test_construct.py coding utf-8
import sys
import pandas
import pyqtgraph as pg
import pyqtgraph.exporters

from calculation import calculation_sequence
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, \
QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QStackedLayout, QWidget, QStyle, QMessageBox

class MainWindow(QMainWindow):
	"""Мой вариант основного окна приложения"""
	def __init__(self):
		super().__init__()

		self.setWindowTitle('Tehyco')

		self.main_font = pg.Qt.QtGui.QFont()
		self.main_font.setPixelSize(30)

		#self.setFixedSize(QSize(300, 500))
		self.plot_window = False
		self.label_water_pressure = QLabel('Water inlet pressure, [MPa]')
		self.label_steam_pressure = QLabel('Steam pressure, [MPa]')
		self.label_water_temperature_in = QLabel(
			'Water inlet temperature, [K]')
		self.label_water_mass_flow = QLabel(
			'Water mass flow, [kg/second]')
		self.label_tubes_amount = QLabel('Amount of tubes, [integer]')
		self.label_din = QLabel('Inside tube diameter, [mm]')
		self.label_dout = QLabel('Outside tube diameter, [mm]')
		self.label_steam_velocity = QLabel(
			'Average steam velocity, [m/s]')
		self.label_partitions = QLabel(
			'Distance behind partitions as in example, [m]')
		self.label_pass = QLabel('Amount of passes by water, [integer]')
		self.label_roughness = QLabel('Surface roughness, [mm]')
		self.label_thermcond = QLabel('Thermal Conductivity, [W/K*m**2]')
		self.label_depth = QLabel('Depth of the curve, [mm]')
		self.label_step = QLabel('Step between the curves, [mm]')
		self.label_line_number = QLabel('Number of curved lines, [integer]')



		self.button_save = QPushButton('SAVE')
		self.button_save.setCheckable(True)
		self.button_save.clicked.connect(self.save_results)

		self.button_calculate = QPushButton('CALCULATE')
		self.button_calculate.setCheckable(True)
		self.button_calculate.clicked.connect(self.calculate)

		self.input_water_pressure = QLineEdit('1')
		self.input_steam_pressure = QLineEdit('0.206')
		self.input_water_temperature_in = QLineEdit('343.15')
		self.input_water_mass_flow = QLineEdit('416.67')
		self.input_tubes_amount = QLineEdit('963')
		self.input_din = QLineEdit('17')
		self.input_dout = QLineEdit('19')
		self.input_steam_velocity = QLineEdit('7')
		self.input_partitions = QLineEdit('0.35/0.35/0.45/0.6/0.6/0.6/0.6/0.6/0.472')
		self.input_pass = QLineEdit('2')
		self.input_roughness = QLineEdit('0.001')
		self.input_thermcond = QLineEdit('129.2')
		self.input_depth = QLineEdit('0.5')
		self.input_step = QLineEdit('9')
		self.input_line_number = QLineEdit('3')


		layout = QGridLayout()
		layout.addWidget(self.label_water_pressure, 0, 0)
		layout.addWidget(self.input_water_pressure, 0, 1)
		layout.addWidget(self.label_steam_pressure, 1, 0)
		layout.addWidget(self.input_steam_pressure, 1, 1)
		layout.addWidget(self.label_water_temperature_in)
		layout.addWidget(self.input_water_temperature_in)
		layout.addWidget(self.label_water_mass_flow)
		layout.addWidget(self.input_water_mass_flow)
		layout.addWidget(self.label_tubes_amount)
		layout.addWidget(self.input_tubes_amount)
		layout.addWidget(self.label_din)
		layout.addWidget(self.input_din)
		layout.addWidget(self.label_dout)
		layout.addWidget(self.input_dout)
		layout.addWidget(self.label_steam_velocity)
		layout.addWidget(self.input_steam_velocity)
		layout.addWidget(self.label_partitions)
		layout.addWidget(self.input_partitions)
		layout.addWidget(self.label_pass)
		layout.addWidget(self.input_pass)
		layout.addWidget(self.label_roughness)
		layout.addWidget(self.input_roughness)
		layout.addWidget(self.label_thermcond)
		layout.addWidget(self.input_thermcond)
		layout.addWidget(self.label_depth)
		layout.addWidget(self.input_depth)
		layout.addWidget(self.label_step)
		layout.addWidget(self.input_step)
		layout.addWidget(self.label_line_number)
		layout.addWidget(self.input_line_number)
		layout.addWidget(self.button_save)
		layout.addWidget(self.button_calculate)

		if self.plot_window:
			layout.addWidget(self.plot_window)


		container = QWidget()
		container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
		self.setCentralWidget(container)
	def get_values(self):
		try:
			self.water_pressure = float(self.input_water_pressure.text()) * (10**6)
			self.steam_pressure = float(self.input_steam_pressure.text()) * (10**6)
			self.water_mass_flow = float(self.input_water_mass_flow.text())
			self.inlet_water_temperature = float(self.input_water_temperature_in.text())
			self.tubes_amount = int(self.input_tubes_amount.text())
			self.din = float(self.input_din.text()) / 1000
			self.dout = float(self.input_dout.text()) / 1000
			self.steam_velocity = float(self.input_steam_velocity.text())
			self.passes = int(self.input_pass.text())
			self.roughness = float(self.input_roughness.text()) / 1000
			self.thermcond = float(self.input_thermcond.text())
			self.depth = float(self.input_depth.text()) / 1000
			self.step = float(self.input_step.text()) / 1000
			self.line_number = int(self.input_line_number.text())

			partitions = self.input_partitions.text().split(sep = '/')
			partitions = [float(item) for item in partitions]
			self.partitions = []
			reversed_partitions = partitions[::-1]
			for i in range(1, self.passes + 1):
				if i % 2 == 0:
					self.partitions.extend(reversed_partitions)
				else:
					self.partitions.extend(partitions)
		except TypeError('Fuck you!'):
			raise TypeError('Fuck you!')

	def get_results(self):
		self.get_values()
		self.results = calculation_sequence(self.inlet_water_temperature, self.water_pressure, \
			self.water_mass_flow, self.steam_pressure, self.partitions, self.tubes_amount, \
			self.din, self.dout, self.steam_velocity, self.roughness, self.depth, self.step, self.line_number)
		growing_length = 0
		self.bundle = []
		for elem in self.partitions:
			growing_length += elem
			self.bundle.append(growing_length)

	def present_results(self):
		result_vocabulary = {'Температура воды на входе, K': self.results[:, 0],
		 'Температура воды на выходе, К': self.results[:, 1],
		  'Коэффициент теплопередачи, Вт/(К*м**2)': self.results[:, 2],
		   'Температура стенки, К': self.results[:, 3],
		    'Теплоотдача воды':self.results[:, 6],
		     'Теплоотдача пара':self.results[:, 7],
		      'dt_log':self.results[:, 8],
		      'Развернутая длина пучка, м': self.bundle,
		      'Тепловая мощность секции, Вт': self.results[:, 5]}#678
		result_df = pandas.DataFrame(result_vocabulary)
		result_df.to_excel('./res.xlsx', index = True)

	def save_results(self):
		self.get_values()
		#self.calculate()
		if self.plot_window:
			exporter = pg.exporters.ImageExporter(self.plot_window.plotItem)
			exporter.parameters()['width'] = 1600
			exporter.export('Graph.png')
			exporter = pg.exporters.ImageExporter(self.plot_dt.plotItem)
			exporter.parameters()['width'] = 1600
			exporter.export('Graph_dt.png') 
			exporter = pg.exporters.ImageExporter(self.plot_he.plotItem)
			exporter.parameters()['width'] = 1600
			exporter.export('Graph_he.png')
		self.present_results()
		self.wind_ok = QMessageBox()
		#self.wind_ok.setIcon(QMessageBox.Information)
		self.wind_ok.setText('Succesfully saved')
		self.wind_ok.setWindowTitle('Saving')
		self.wind_ok.show()
		print('Tried to save!')
		


	def get_plot_temps(self):
		pass

	def get_plot_dt(self):
		self.plot_dt = pg.plot()
		self.plot_dt.addLegend()
		self.plot_dt.plot(self.bundle, self.results[:, 8], name= 'dtlog, K', symbol= 'x', pen = {'color': 0.4, 'width': 2})
		self.plot_dt.showGrid(x = True, y = True)
		self.plot_dt.setWindowTitle('Изменение температурного напора по развернутой длине пучка')
		self.plot_dt.setLabel('bottom', text = 'Развернутая длина трубного пучка, м')
		self.plot_dt.setLabel('left', text = 'Температура, К')
		

	def get_plot_heat_exchange(self):
		self.plot_he = pg.plot()
		self.plot_he.addLegend()
		self.plot_he.plot(self.bundle, self.results[:, 2],
		 name='HTC, W/(K*m**2)', symbol='o',
		 pen = {'color': 0.4, 'width': 2})
		self.plot_he.plot(self.bundle, self.results[:, 6], 
			name='Alpha water, W/(K*m**2)', symbol='o', 
			pen = {'color': 0.8, 'width': 2})
		self.plot_he.plot(self.bundle, self.results[:, 7], 
			name='Alpha steam, W/(K*m**2)', symbol='o', 
			pen = {'color': 1, 'width': 2})
		self.plot_he.showGrid(x = True, y = True)
		self.plot_he.setWindowTitle('Коэффициент теплопередачи и теплоотдачи по развернутой длине пучка')
		self.plot_he.setLabel('bottom', text = 'Развернутая длина трубного пучка, м')
		self.plot_he.setLabel('left', text='W/(K*m**2)')


	def calculate(self):
		self.get_results()
		print('Tried to calculate')
		print(self.results)
		self.plot_window = pg.plot()
		self.plot_window.addLegend() #offset = (x,y) дает расположить легенду куда хочется
		self.plot_window.plot(self.bundle, self.results[:, 0], 
			name= 'Температура воды на входе, К', symbol= 'o', 
			pen = {'color': 1, 'width': 2})
		self.plot_window.plot(self.bundle, self.results[:, 1], 
			name= 'Температура воды на выходе, К', symbol= 'o', 
			pen = {'color': 0.8, 'width': 2})
		self.plot_window.plot(self.bundle, self.results[:, 3], 
			name= 'Температура стенки, К', symbol= 'x', 
			pen = {'color': 0.2, 'width': 2})
		#self.plot_window.plot(self.bundle, self.results[:, 8], name= 'dtlog, K', symbol= 'x', pen = {'color': 0.4, 'width': 2})
		self.plot_window.showGrid(x = True, y = True)
		self.plot_window.setWindowTitle('Изменение температур по развернутой длине пучка')
		self.plot_window.setLimits(yMin = min(self.results[:, 0]) - 5, xMin = 0, yMax = max(self.results[:, 3]) + 10, xMax = max(self.bundle) + 0.5)
		self.text = pg.TextItem(text = 'Развернутая длина трубного пучка, м', color = (250, 20, 20), angle = 0)
		self.text.moveBy(self.bundle[len(self.bundle) - 1] - 2, 1)
		self.plot_window.addItem(self.text)
		#self.plot_window.setStyle(font = self.main_font)
		self.plot_window.setLabel('left', text = 'Температура, К')
		self.plot_window.setLabel('bottom', text = 'Развернутая длина трубного пучка, м')
		self.get_plot_heat_exchange()
		self.get_plot_dt()
		

app = QApplication(sys.argv)
#app.setStyle("Breeze")
window = MainWindow()

window.show()

app.exec() 

