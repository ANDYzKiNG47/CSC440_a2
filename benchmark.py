import copy
from convexhull import computeHull
import os
import ast
import time

for filename in os.listdir('tests4'):
	f = open("tests4/"+filename)
	points = list(ast.literal_eval(f.read()))
	f.close()
	print("tests/"+str(filename))
	start = time.time()
	computeHull(list(points))
	end = time.time()
	print(end-start)

