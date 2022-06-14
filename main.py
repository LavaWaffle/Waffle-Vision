from time import sleep
import PySimpleGUI as sg
from pathlib import Path
from mpl import mpl
from readExcel import readExcel

# Constants
PI = 3.14
SLIDER_SCALE = 10

# UI Theme
sg.theme('DarkGray2')
# Table Content (contains time, x, and y when a file is opened)
table_content = []
# Menu bar layout
menu_layout = [
	['File', ['Open', '---', 'Exit']],
	['Tools', ['Screen Shot']],
]

# UI Layout
layout = [
	# First row is the menu bar
	[sg.Menu(menu_layout)],
	# Second row is the filename, checkbox, and slider
	[
		sg.Text('Click "File" -> "Open" to begin', key='-FILENAME-', font=('Helvetica', 16)), 
		sg.Push(), 
		sg.Checkbox('Auto rotate', key='-AUTOROTATE-', default=False, font=('Helvetica 16')),
		sg.Push(),
		sg.Text('{Slider val}', key='-SLIDER_VAL-'),
		sg.Slider(
			range=(0, 2*PI*SLIDER_SCALE),
			default_value=PI*SLIDER_SCALE,
			tick_interval=PI*SLIDER_SCALE/2,
			orientation='horizontal',
			font=('Helvetica 12'),
			enable_events=True,
			key='-SLIDER-',
			disable_number_display=True
		)
	],
	# Third row is the table and plot (canvas)
	[
		sg.Table(
			headings = ['Time', 'X', 'Y'],
			values = table_content,
			auto_size_columns = True,
			expand_x = True,
			expand_y = True,
			key='-TABLE-'
		),
		sg.Canvas(key='-CANVAS-',size=(400,450))
	]
]

# Create a window
window = sg.Window('WAFFLE VISION', layout, finalize=True, size=(800, 450))

# Create a plot from the window
plot = mpl(window)

# Update the slider value text
def update_slider_val(values):
	slider_val = values['-SLIDER-']
	slider_val = round(slider_val/SLIDER_SCALE/PI, 2)
	window['-SLIDER_VAL-'].update(f'{slider_val} pi')

# Main loop
def main():
	while True:
		# Get events and values from the window
		# Timeout means that if nothing happens for x ms, the loop will be ran through again
		# Without timeout, the loop will only be ran when events occur
		event, values = window.read(timeout=10)

		# When user clicks x button or the exit button, exit the program
		if event in (sg.WIN_CLOSED, 'Exit'):
			break

		# When user clicks the open file button, get a file path, and then display it through matplotlib
		if event == 'Open':
			# Get file path
			# Only allow excel files
			file_path = sg.popup_get_file('Open File', no_window=True, file_types=(('excel', '*.xlsx'), ('All Files', '*.*')))
			# User entered a file vs user cancelled
			if file_path:
				# User entered a file!
				# Read the file
				file = Path(file_path)
				# Set the filename text to the file name
				window['-FILENAME-'].update(file.name)
				excelData = readExcel(file_path)
				# Update the table with the data
				plot.update_figure(excelData.xPositions, excelData.yPositions, values['-SLIDER-']/SLIDER_SCALE)

				# Update the table with the data
				table_content = []
				for i, x in enumerate(excelData.xPositions):
					time = excelData.times[i]
					x = x
					y = excelData.yPositions[i]
					table_content.append([round(time), round(x, 2), round(y, 2)])
				window['-TABLE-'].update(table_content)

		# When user clicks the screen shot button, take a screenshot of the plot
		if event == 'Screen Shot':
			# Get file path
			path = sg.popup_get_folder('Save Screen Shot', no_window=True)
			# Get file name
			name = sg.popup_get_text('Filename')
			# User entered file and file path vs cancelled
			if path != None and name != None and name != '':
				# User entered file and file path!
				print('path: ', path, 'name: ', name)
				# Save plot screenshot
				plot.save_figure(path, name)
			else:
				# User cancelled
				sg.popup_error('Please select a folder and enter a filename')
			
		# When the user moves the slider (rotation), update the plot
		if event == '-SLIDER-':
			# Update the slider value text
			update_slider_val(values)
			
			# Update the plot
			plot.update_figure(excelData.xPositions, excelData.yPositions, values['-SLIDER-']/SLIDER_SCALE)
		
		# When the Auto Rotate checkbox is checked, update the plot
		if values['-AUTOROTATE-']:
			# Get the current slider value
			slider_val = values['-SLIDER-']
			# Add one
			slider_val += 1
			# If value is greater than 2pi, reset to 0
			if slider_val > 2*PI*SLIDER_SCALE:
				slider_val = 0

			# Update the slider 
			window['-SLIDER-'].Update(value=slider_val)
			# Update the slider value text
			update_slider_val(values)
			# Update the plot
			plot.update_figure(excelData.xPositions, excelData.yPositions, values['-SLIDER-']/SLIDER_SCALE)
			# Refresh the window
			window.refresh()
			# Sleep to slow down the loop
			sleep(0.025)
	
	# Close the window when the program ends
	window.close()

# Run the main loop
if __name__ == '__main__':
	main()