'''
visualization.py

Use Matplotlib to visualize data read into a Numpy ndarray from a CSV file. Visualizes the 
data in several ways, including a pair plot and a heatmap.

Execution:		>> python3 visualization.py [path_to_dataset, str] [class_column_header, str]
	Examples: 		>> python3 visualization.py 
					>> python3 visualization.py ../data/iris.csv
					>> python3 visualization.py ../data/iris.csv species

Requires Numpy and Matplotlib:
	>> pip install numpy matplotlib

@author Caitrin Eaton
@date 12/20/2021
'''

import sys							# we can retrieve command line parameters from sys.argv
import os							# helps adapt filepath formatting for your operating system
import numpy as np					# represents datasets as ndarrays (matrices)
import matplotlib.pyplot as plt		# data visualization, e.g. plot() and imshow()
from matplotlib import cm			# colormap definitions, e.g. "viridis"


def your_own_visualization_function_but_with_a_better_name( data, headers, anything_else_you_want=None ):
	''' Insert your own docstring here, using the docstrings below as a model. '''
	# Use matplotlib to create a 4th plot in any style that you want.
	# To help you get started, here is a gallery of several possible plot styles: https://matplotlib.org/stable/gallery/
	jeffery_bezos = "\n\tYOU DID IT! Congratulations!\n\n\tNext, add a 4th plotting function of your own :)\n"
	return jeffery_bezos


def scatter( data, headers, col_x, col_y, col_c=None, title="" ):
	'''
	ARGS:
	data (ndarray), dataset that contains columns with the X and Y data to be plotted
	header (list of str), the names of each feature in the data ndarray
	col_x (int), column index of the X feature within the data ndarray
	col_y (int), column index of the Y feature within the data ndarray
	col_c (int), OPTIONAL: column index of the feature to use as a marker color code
	title (str), OPTIONAL: text that will appear immediately above the plot

	RETURN:
	fig (figure reference), the figure in which the new plot appears
	'''

	# Incorporate metadata into axis labels and title
	fig, ax = plt.subplots()
	plt.suptitle( title ) 
	ax.set_xlabel( headers[ col_x ] )
	ax.set_ylabel( headers[ col_y ] )
	ax.grid( True )

	# Plot samples, color-coding if necessary
	colorcoded = (col_c != None) and (col_c < data.shape[1])
	if colorcoded:
		class_labels = np.unique( data[ :, col_c ] )	# determine if there is more than one class label present
		num_classes = len( class_labels )
		c_min = np.min( data[:,col_c] )
		c_max = np.max( data[:,col_c] )
		c_norm = ( data[:,col_c] - c_min ) / (c_max - c_min)
		
		# Plot each class (i.e. each subset of matching values in col_c) in its own color using a
		# colorblind-friendly colormap: "viridis", "plasma", "inferno", "magma", or "cividis"
		cmap = cm.get_cmap( "viridis", num_classes ) 
		for i in range( num_classes ):
			label = class_labels[ i ]
			has_lbl = data[ :, col_c ] == label
			x = data[ has_lbl, col_x ]
			y = data[ has_lbl, col_y ]
			c = cmap( c_norm[ has_lbl ] )
			ax.scatter( x=x, y=y, c=c, edgecolors='w', label=label )
		ax.legend()
	else:
		# Plot all samples in the same color
		ax.scatter( x=data[ :, col_x ], y=data[ :, col_y ] )

	return fig


def pair_plot( data, headers, class_col=None, title="" ):
	'''
	ARGS:
	data (ndarray), dataset that contains columns with the X and Y data to be plotted
	header (list of str), the names of each feature in the data ndarray
	class_col (int), OPTIONAL: column index of the feature to use as a marker color code
	title (str), OPTIONAL: text that will appear immediately above the plot

	RETURN:
	fig (figure window reference), the figure window in which the pair plot appears
	'''

	# Set up the current axes and add grid lines
	num_features = data.shape[1]
	feature_cols = list(range(num_features))

	# Check to see if one of the features is a class category
	if class_col != None:
		feature_cols.pop( class_col )
		num_features = len(feature_cols)
		
		# Plot each class (i.e. each subset of matching values in col_c) in its own color using a
		# colorblind-friendly colormap: "viridis", "plasma", "inferno", "magma", or "cividis"
		class_labels = np.unique( data[ :, class_col ] )	# find the set of unique class labels
		num_classes = len( class_labels )
		cmap = cm.get_cmap( "viridis", num_classes )
		c_min = np.min( data[:,class_col] )
		c_max = np.max( data[:,class_col] )
		c_norm = ( data[:,class_col] - c_min ) / (c_max - c_min)

	# Populate the figure window with num_features rows * num_features columns of subplot axes
	fig, axs = plt.subplots( ncols=num_features, nrows=num_features, sharex="col", sharey="row" )
	plt.suptitle( title )
	
	# Scatterplot each possible pair of features (other than the class column, which is used for colorcoding)
	for plot_row in range( num_features ):
		for plot_col in range( num_features ):
			ax = axs[ plot_row][ plot_col ]
			ax.grid( True )

			x_col = feature_cols[ plot_col ]
			y_col = feature_cols[ plot_row ]

			# Colorcode the scatter plot by class label, if present
			if class_col != None:
				for i in range( num_classes ):
					label = class_labels[ i ]
					has_lbl = data[ :, class_col ] == label
					x = data[ has_lbl, x_col ]
					y = data[ has_lbl, y_col ]
					c = cmap( c_norm[ has_lbl ] )					
					'''
					if plot_row != plot_col:
						ax.scatter( x=x, y=y, c=c, edgecolors='w', label=label )
					else:
						ax.hist(x, facecolor=c[0,:], density=True, alpha=0.7 ) 
					'''
					ax.scatter( x=x, y=y, c=c, edgecolors='w', label=label )
			else:
				ax.scatter( x=data[:,x_col], y=data[:,y_col], edgecolors='w' )

			# Label rows along the leftmost column only
			if plot_col == 0:
				ax.set_ylabel( headers[ y_col ] )

			# Label columns along the bottom row only
			if plot_row == num_features - 1:
				ax.set_xlabel( headers[ x_col ] )

	# Show the color code to the user in only one of the subplots; the color code is always the same
	if class_col != None:
		axs[0][0].legend()

	return fig


def heatmap( data, headers, title="" ):
	'''
	Represents the data matrix as a heatmap, assigning a color to each cell. Cell annotations are included if the cells are large enough. 
	Based on https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html

	ARGS:
	data (ndarray), dataset that contains columns with the X and Y data to be plotted
	header (list of str), the names of each feature in the data ndarray
	class_col (int), OPTIONAL: column index of the feature to use as a marker color code
	title (str), OPTIONAL: text that will appear immediately above the plot

	RETURN:
	fig (figure window reference), the figure window in which the pair plot appears
	'''
	n_rows = data.shape[0]		# features
	n_cols = data.shape[1]		# samples

	# Create heatmap
	fig, ax = plt.subplots( )
	plt.set_cmap( "viridis" )	# Choose a colorblind-friendly colormap: "viridis", "plasma", "inferno", "magma", or "cividis"
	im = ax.imshow( data, interpolation='nearest', aspect='auto' )

	# Add plot title and axis labels
	plt.suptitle( title ) 
	ax.set_ylabel( "samples" )														# label rows with sample indices
	ax.set_xlabel( "features" )														# label columns wth feature names
	ax.set_xticks( np.arange(n_cols) )
	ax.set_xticklabels( headers )
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor") # Rotate the column labels and set their alignment.

	# Annotate cells only if there are few enough that the text will be legible. 
	if (n_cols < 20) and (n_rows < 20):
		for row in range( n_rows ):
			for col in range( n_cols ):
				ax.text(x=col, y=row, s=f"{data[row, col]:.2f}", ha="center", va="center", color="w")

	# Add a colorbar so that the user understands how the color of each cell relates to its value
	plt.colorbar( im )

	fig.tight_layout()
	return fig


def remove_nans( data, headers ):
	''' Remove entirely non-numeric features and rows with missing values. 
	Return the clean dataset and updated headers (non-numeric feature names removed. 
	
	INPUT: 
	data -- ndarray, with a datum in each row a feature in each column
	headers -- list of strings, each the name of a feature (column). 
	
	OUTPUT:
	complete_data -- ndarray, a subset of data that is numeric and contains no rows with missing values.
	complete_headers -- list of strings, the names of features retained in the numeric dataset 
					(non-numeric features removed).
	''' 

	# Remove columns that contain entirely non-numeric features, e.g. the date
	numeric_cols = ~np.isnan( data ).all( axis=0 )
	numeric_data = data[ : , numeric_cols ]
	numeric_headers = headers[:]
	for col in range(len(headers)-1,-1,-1):
		if numeric_cols[ col ] == False:
			numeric_headers.pop( col )
	print("Original data shape:", data.shape)
	print("Numeric data shape: ", numeric_data.shape)
	print(numeric_data.shape[1] - data.shape[1], "non-numeric features culled from raw dataset")


	# Remove incomplete rows with any missing values (NaNs)
	complete_rows = ~np.isnan( numeric_data ).any( axis=1 )
	complete_data = numeric_data[complete_rows, :]
	print("Complete data shape:", complete_data.shape)
	print(numeric_data.shape[0] - complete_data.shape[0], "NaN and/or outlier rows culled from numeric dataset")

	return complete_data, numeric_headers


def read_csv( filepath, delimiter="," ):
	'''
	ARGS:
	filepath (str), relative or absolute path to the target data file
	delimieter (str), OPTIONAL: the character that separates adjacent columns in the dataset

	RETURN:
	data (ndarray), 2D collection of values extracted from the file
	headers (list of str), the names of each feature in the file
	title (str), the name of the file
	'''
	
	# Grab the title from the file name
	title = filepath.split("\\")[-1]
	title = title.split("/")[-1]
	title = title.split(".")[-2]

	# Grab the metadata from the first line of the file
	headers=[]
	with open( filepath, 'r' ) as infile:
		line = infile.readline()

		# Break the line up into individual headers and strip whitespace
		headers = line.split( delimiter )
		for col in range(len(headers)):
			headers[col] = headers[col].strip()

		'''
		# Test for non-numeric fields
		line = infile.readline()
		row = line.split( delimiter )
		for col in range(len(row)):
			if 
			row[col] = row[col].strip()
		'''
		infile.close()

	# Grab the data from the remaining rows in the file
	data = np.genfromtxt( filepath, skip_header=1, delimiter=delimiter )
	#data, headers = np.genfromtxt( filepath, names=True, delimiter=delimiter )
	
	return data, headers, title #, class_labels


def main( argv ):
	''' Parse command line arguments: 
		-- argv[0] is always the name of the program run from the terminal
		-- argv[1] should be the path of a data file (e.g. *.DATA or *.CSV) to read into a Pandas DataFrame
	'''

	# Determne the input file's path: either it was supplied in the commandline, or we should use iris as a default
	if len(argv) > 1:
		filepath = argv[1].strip()
	else:
		#filepath = "../data/iris_preproc.csv"
		current_directory = os.path.dirname(__file__)
		filepath = os.path.join(current_directory, "..", "data", "iris_preproc.csv")

	# Read the dataset into a numpy ndarray object (a matrix)
	data, headers, title = read_csv( filepath )
	
	# Let the user name a feature that they want to use as the class color code in the plots below
	class_col = None
	if len(argv) > 2:
		try: 
			# Find the column that contains the user's chosen feature name 
			class_col = headers.index( argv[2] )	# CAUTION: this will crash if the user's input does not match any element in the list of headers
		except:
			print( f"\nWARNING: '{argv[2]}' not found in the headers list: {headers}. No class color coding applied.\n" )

	# If your plots are coming up empty, you may need to remove NaN ("Not a Number") elements like missing values
	# and non-numeric columns from your data matrix. You can accomplish that by uncommenting the next line:
	# data, headers = remove_nans( data, headers )

	scatter( data, headers, col_x=0, col_y=1, col_c=class_col, title=title )	# pick any X and Y columns you want
	pair_plot( data, headers, class_col=class_col, title=title )				
	heatmap( data, headers, title=title )
	congrats = your_own_visualization_function_but_with_a_better_name( data, headers )
	print( congrats )

	plt.show()


if __name__=="__main__":
	main( sys.argv )

