import pandas as pd
import warnings

# Excel backend with pandas
class readExcel:
	# Get the data from the excel file
	def __init__(self, file_path: str):
		with warnings.catch_warnings(record=True):
			warnings.simplefilter("always")
			# Read the excel file
			xlsx_file = pd.read_excel(file_path)
			# Convert the file to a list
			self.xlsx_file = xlsx_file.to_dict('list')
			# Get specific lists from the data
			self.times = self.xlsx_file['Time']
			self.xPositions = self.xlsx_file['xPos']
			self.yPositions = self.xlsx_file['yPos']
	