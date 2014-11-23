#!/usr/bin/python

import sys
# import the functions
from jenks import getJenksBreaks
from jenks import getGVF


# define constants, you can change these to diff
# numbers and file names.
if len(sys.argv) == 3:
	datafile  = sys.argv[1]
	numbreaks = int(sys.argv[2])
else: 
	sys.exit("Incorrect number of arguments.")

#open the file in read mode
datafile = open(datafile, 'r')
# this splits the lines and puts them into a list
dataList_str = (datafile.read().splitlines())
# but since we read in the file, the list is full of strings
# let's convert those to floats so we can do math
# map all the elements to floats
dataList_str = map(float, dataList_str)
# filter them using a lambda funtion such that all values >= 0
dataList_str = filter(lambda x: x >= 0, dataList_str)
# now take the filter and append the results to new list
dataList_int = []
dataList_int.extend(dataList_str)

print(getJenksBreaks(dataList_int, numbreaks))
print(getGVF(dataList_int, numbreaks))

