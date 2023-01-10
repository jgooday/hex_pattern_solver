from math import ceil, sqrt
from tkinter import N
import matplotlib.pyplot as plt
import numpy as np

def plot_pattern(r, R, X, Y, ps, d, inclusion_mask):
	fig, ax = plt.subplots()

	for i in range(0, ps.shape[1]):
		x = ps[0, i]
		y = ps[1, i]
		if inclusion_mask[i]:
			c = plt.Circle((x, y), r, fill=False, color='g')
		else:
			c = plt.Circle((x, y), r, fill=False, color='r')
		ax.add_artist(c)

	c = plt.Circle((X, Y), R, fill=False)
	ax.add_artist(c)

	# plot centroid of pattern
	ax.plot(X, Y, 'kx')

	# plot centroid of closest cell
	ax.plot(ps[0, np.argmin(d)], ps[1, np.argmin(d)], 'bx')

	ax.set_aspect(1)
	ax.set_xlim(-r, 2*R+2*r)
	ax.set_ylim(-sqrt(3)*r, 2*R+2*r)
	plt.title('Honeycomb circle solver')
	plt.show()

def solve(R, r, precision):
	"""
	solves the problem
	R - radius of your container
	r - radius of your cell
	precision - precision of solution (% of radius of container)
	"""

	# create a matrix of the position of small circles
	# this needs to be bigger than the big circle

	x1s = np.arange(0, R*2+r*2, r*2)					# x positions of cells on 1st, 3rd... rows
	x2s = np.arange(r, R*2+r*2, r*2)					# corresponding y positions
	y1s = np.arange(0, R*2+r*2, 2*sqrt(3)*r)			# x positions of cells on 2nd, 4th... rows
	y2s = np.arange(sqrt(3)*r, R*2+r*2, 2*sqrt(3)*r)	# corresponding y positions

	p1x, p1y = np.meshgrid(x1s, y1s)				# first set of individual x values
	p2x, p2y = np.meshgrid(x2s, y2s)				# y values
	p1 = np.array([p1x.flatten(), p1y.flatten()])	# second set...
	p2 = np.array([p2x.flatten(), p2y.flatten()])
	ps = np.concatenate([p1, p2], axis=1)			# 2 by n maxtix of (x, y) values of n cells

	# loop till you find the best one
	X_init = R+r			# start in the middle
	Y_init = R+r
	dx = R*precision			# step change to simulate
	X_best = None
	Y_best = None
	n_best = 0
	dsum_best = None
	X_test = np.arange(X_init-2*r, X_init+2*r, dx)						# test points to move the container to
	Y_test = np.arange(Y_init-2*sqrt(3)*r, Y_init+2*sqrt(3)*r, dx)

	for X in X_test:
		for Y in Y_test:
			# calculate distance matrix and determine which ones are inside
			d = ((X-ps[0,:])**2 + (Y-ps[1,:])**2)**0.5
			dsum = sum(d)
			inclusion_mask = d+r<R
			n = sum(inclusion_mask)		# number of cells inside container
			#print(X, Y, n)
			if n>n_best:
				X_best = X
				Y_best = Y
				n_best = n
				dsum_best = dsum
				print(f'n_best={n_best}')
			elif n==n_best and dsum<dsum_best:
				X_best = X
				Y_best = Y
				n_best = n
				dsum_best = dsum
				print(f'  dsum_best={dsum_best}')

	X = X_best
	Y = Y_best
	d = ((X-ps[0,:])**2 + (Y-ps[1,:])**2)**0.5
	inclusion_mask = d+r<R

	return X, Y, d, inclusion_mask, ps

if __name__=="__main__":

	# settings
	R = (368.3-5)/2			# internal radius of tube
	r = 18.5/2			# radius of cell
	precision = 0.01	# simulation step dimenison

	# solve
	X, Y, d, inclusion_mask, ps = solve(R, r, precision)

	# determine coords to nearest cell (used for CAD location of pattern)
	dx = ps[0, np.argmin(d)] - X
	dy = ps[1, np.argmin(d)] - Y

	# plot the pattern
	print(f'Can fit {sum(inclusion_mask)} cells in this container')
	#print(f'min(d)={min(d)}, ps[:, np.argmin(d)]={ps[:, np.argmin(d)]}')
	#print(f'X={X}, Y={Y}')
	print(f'dx={dx} dy={dy}')
	#plot_pattern(r, R, X, Y, ps, d, inclusion_mask)

	