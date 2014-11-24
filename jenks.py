# Functions to calculate Jenks' Natural Breaks
#
# Author	=> Daniel J. Lewis
# Date		=> 06.07.2010
# Modified	=> Sean Hellebusch | sahellebusch@gmail.com
# Date		=> 11.24.2014

# For the examples, I am using the following input:
# datalist is of length ten, 3 breaks.
def getJenksBreaks( dataList, numClass ):
	
	dataList.sort()
	
	# These first two for loop blocks simply instantiate 
	# two 2D matrices.  They are (datalist.length + 1) x (num_classes + 1)
	# They look like this:
	# [ [0, 0, 0, 0],
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0] ]
	
	mat1 = []
	for i in range(0,len(dataList)+1): 
		temp = []
		for j in range(0,numClass+1):
			temp.append(0)
		mat1.append(temp)
	
	mat2 = []
	for i in range(0,len(dataList)+1):
		temp = []
		for j in range(0,numClass+1):
			temp.append(0)
		mat2.append(temp)
	
	#This initializes the following:
	# sets the second array in mat1 to ones.
	# sets all arrays but the first in mat2 to infinity.
	# This is what they look like.
	# mat1: 
	# [ [0, 0, 0, 0],
	# 	[1, 1, 1, 1], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0], 
	# 	[0, 0, 0, 0] ]
	# mat2:
	# [[0, 0, 0, 0], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf], 
	#  [inf, inf, inf, inf] ]

	for i in range(0,numClass+1):
		mat1[1][i] = 1
		mat2[1][i] = 0
		for j in range(1,len(dataList)+1):
			mat2[j][i] = float('inf')
	
	v = 0.0
	for l in range(2,len(dataList)+1):
		curr_list_sum = 0.0
		curr_sqr_sum = 0.0
		w  = 0.0
		for m in range(1,l+1):
			# this is iterating through and grabbing each element
			# in the sorted dataList in this pattern
			# 2, 1, 3, 2, 1, 4, 3, 2, 1, 5, 4, 3, 2, 1, ....
			i3 = l - m + 1
			
			val = float(dataList[i3-1])
			curr_sqr_sum += val * val
			curr_list_sum += val
			
			w += 1
			# calculate the variance
			variance = curr_sqr_sum - (curr_list_sum * curr_list_sum) / w
			i4 = i3 - 1
			 
			# now it compares
			if i4 != 0:
				for j in range(2,numClass+1):
					if mat2[l][j] >= (variance + mat2[i4][j - 1]):
							mat1[l][j] = i3
							mat2[l][j] = variance + mat2[i4][j - 1]
				mat1[l][1] = 1
				mat2[l][1] = variance
						
	# this last section here compares standard deviations between classes (SDBC) and decides if
	# it should move one unit fron the lagest SDBC to the class with the lowest SDBC
	k = len(dataList)
	kclass = []
	for i in range(0,numClass+1):
		kclass.append(0)
			
	kclass[numClass] = float(dataList[len(dataList) - 1])
			
	countNum = numClass
	while countNum >= 2:
		id = int((mat1[k][countNum]) - 2)
		
		kclass[countNum - 1] = dataList[id]
		k = int((mat1[k][countNum] - 1))
		countNum -= 1

	return kclass

def getGVF( dataList, numClass ):
	"""
	The Goodness of Variance Fit (GVF) is found by taking the 
	difference between the squared deviations
	from the array mean (SDAM) and the squared deviations from the 
	class means (SDCM), and dividing by the SDAM
	"""
	breaks = getJenksBreaks(dataList, numClass)
	dataList.sort()
	listMean = sum(dataList)/len(dataList)
	print("Data Mean:  {0}".format(listMean))
	SDAM = 0.0
	for i in range(0,len(dataList)):
		sqDev = (dataList[i] - listMean)**2
		SDAM += sqDev
	
	SDCM = 0.0
	classListCount = 0
	for i in range(0,numClass):
		if breaks[i] == 0:
			classStart = 0
		else:
			classStart = dataList.index(breaks[i])
			classStart += 1
		classEnd = dataList.index(breaks[i+1])
		classList = dataList[classStart:classEnd+1]

		classMean = sum(classList)/len(classList)
		classListCount += 1
		print("Class {0} Mean: {1}".format(classListCount,classMean))
		preSDCM = 0.0
		for j in range(0,len(classList)):
			sqDev2 = (classList[j] - classMean)**2
			preSDCM += sqDev2
	
		SDCM += preSDCM
	return (SDAM - SDCM)/SDAM
