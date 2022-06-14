import PySimpleGUI as sg
import matplotlib 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Matplotlib backend with TkAgg
class mpl:
	# Initialize the window and plot
	def __init__(self, window: sg.Window):
		# Create a figure
		self.fig = matplotlib.figure.Figure(figsize=(5,4))
		# Create a subplot (create a graph)
		self.fig.add_subplot(111).plot([],[])

		# set aspect equal
		self.fig.axes[0].set_aspect('equal')
		# add grid
		self.fig.axes[0].grid(True, which='both')
		# add axis lines
		self.fig.axes[0].axhline(y=0, color='k')
		self.fig.axes[0].axvline(x=0, color='k')
		# set graph title
		self.fig.axes[0].set_title('WAFFLE VISION', fontsize=20, color="#0066ff")
		# set x and y labels
		self.fig.axes[0].set_xlabel('X', fontsize=16, color="#0066ff")
		self.fig.axes[0].set_ylabel('Y', fontsize=16, color="#0066ff")
		
		# Add plot to window canvas
		self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, window['-CANVAS-'].TKCanvas)
		# Draw the plot
		self.figure_canvas_agg.draw()
		self.figure_canvas_agg.get_tk_widget().pack()

		# Set points to none
		self.points = None
	
	# Update the plot
	def update_figure(self, xList: list[int], yList: list[int], rotation: float):
		# Get the axes
		self.axes = self.fig.axes
		# Clear the plot
		if self.points is not None:
			for point in self.points:
				point.remove()
	
		# Create a list of points that are rotated based on the rotation parameter
		newListX = []
		newListY = []
		for n, x in enumerate(xList):
			newX = x * math.cos(rotation) - yList[n] * math.sin(rotation)
			newY = yList[n] * math.cos(rotation) + x * math.sin(rotation)
			newListX.append(newX)
			newListY.append(newY)
			# xList[n] = newX
			# yList[n] = newY

		# Plot the points
		self.points = self.axes[0].plot(newListX, newListY, 'C1-.')

		# Draw the plot
		self.figure_canvas_agg.draw()
		self.figure_canvas_agg.get_tk_widget().pack()

	# Save the plot
	def save_figure(self, path, name):
		self.fig.savefig(f'{path}/{name}.png')
