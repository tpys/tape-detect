import matplotlib.pyplot as plt
import numpy as np
import struct
import os
import random 
import math

def read_signal(file_name, max_length = 600):
	signal = []
	for byte in bytes_from_file(file_name):
		signal.append(struct.unpack('1B',byte)[0])
	return signal[:max_length]


def bytes_from_file(file_name, chunk_size = 256):
	with open(file_name,'rb') as f:
		while True:
			chunk = f.read(chunk_size)
			if chunk:
				for b in chunk:
					yield b
			else:
				break

def preprocess_signal(signal):
	# cut signal
	pass



def smooth(signal):
	signal_smooth = []
	for idx, val in enumerate(signal[2:-2]):
		val_smooth = (signal[idx]*6 + (signal[idx-1] + signal[idx+1])*4 + (signal[idx-2]+signal[idx+2]))/16;
		signal_smooth.append(val_smooth)
	return signal_smooth




def fit_line(signal, low_thresh = 55, high_thresh = 90):
	points = [ (x, y) for x, y in enumerate(signal) if y > low_thresh and y < high_thresh ]
	num = len(points)

	inliers_count = 0
	inliers_record = []

	outliers_count = 0
	distance_record = []

	for i in range(20):
		sample_points = random.sample(points,2)
		a = sample_points[1][1] - sample_points[0][1] 
		b = sample_points[0][0] - sample_points[1][0]
		c = sample_points[1][0]*sample_points[0][1] - sample_points[1][1]*sample_points[0][0]

		inliers = 0
		outliers  = 0
		distance = []
		for p in points:
			d = compute_distance(p[0],p[1],a,b,c)
			if d<5:
				inliers = inliers + 1
			if d>8 and (b*(a*p[0] + b*p[1] +c))>0:
				outliers = outliers + 1
				distance.append(d)

		if inliers_count < inliers:
			inliers_count = inliers
			inliers_record = sample_points
			outliers_count = outliers
			distance_record = distance

	score = 0
	for d in distance_record:
		score = score + d	

	print outliers_count, score, True if score>=10 else False

	return inliers_record



def compute_distance(x,y,a,b,c):
	return abs(a*x+b*y+c)/math.sqrt(a*a+b*b)



def display(signal):
	x = range(len(signal))
	plt.plot(x,signal)
	plt.show()



def batch_process(root_path = "/home/tpys/work/tape-signal/with"):
	for f in os.listdir(root_path):
		full_name = os.path.join(root_path,f)
		# print full_name
		signal =  read_signal(full_name)
		signal_smooth = smooth(signal)
		display(signal_smooth)




def main():
	# good response 2-1, 2-3, 2-5, 2-6, 2-7, 4-2, 4-3 
	tape_signal =  read_signal("/home/tpys/work/tape-signal/with/ir_tape_up2_7.dat")
	tape_signal_smooth = smooth(tape_signal)

	line = fit_line(tape_signal_smooth)
	slop = float(line[1][1] - line[0][1])/(line[1][0] -  line[0][0])
	x_border = [0, len(tape_signal_smooth)]
 	y_border = [line[0][1] + slop*(x - line[0][0]) for x in x_border]

	x = range(len(tape_signal_smooth))
	plt.plot(x,tape_signal_smooth)
	plt.plot(x_border, y_border,'r')
	plt.show()



if __name__ == '__main__':
	main()