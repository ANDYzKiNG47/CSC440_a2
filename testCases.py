from random import seed
from random import randint
import time
import os

max_x = [10000000]
max_y = [10000000]
numPoints = [4000000]
numCases = [1] 

script_dir = os.path.dirname(__file__)

for n in range(len(numPoints)):

	print("generating "+str(numCases[n])+"cases with "+str(numPoints[n])+ \
		" with max dimensions of "+str(max_x[n])+" * "+str(max_y[n])+" (max_x * max_y)")
	
	for i in range(0, numCases[n]):
		
		seed(time.time())
		points = set()

		while (len(points) < numPoints[n]):
			temp = (randint(0, max_x[n]), randint(0, max_y[n]))
			points.add(temp)

		name = "tests4/" +str(numPoints[n]) + "_points_" + str(max_x[n]) + \
			"x" + str(max_y[n]) + "_" + str(i)
		path = os.path.join(script_dir, name)
		
		with open(name+str(i), 'w') as f:
			f.write(str(points))
