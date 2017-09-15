'''
Saravanan Ramanathan
Updated: November 2016
'''

from random import *		# Import for random number generation
from math import *		# Import for math functions
import pdb			# Import for enabling trace
from copy import *		# Import for copying objects from another file
import sys
import numpy as np
import numpy.matlib

# Function to generate uniformly distributed utilization values for multi-core
def randfixedsum(n,m,s,a,b):
	
	v=[]
	# Check the arguments
	if((m<0) or (n<1)):
		print "N must be greater than 1 or M a non-negative integer"
		return None,None
	elif((s<n*a) or (s>n*b) or (a>=b)):
		print "Inequalities n*a <= s <= n*b and a < b must hold"
		return None,None

	# Rescale to a unit cube: 0 <= x(i) <= 1
	s = (s-n*a)/(b-a)
	
	# Construct the transition probability table, t.
	# t(i,j) will be utilized only in the region where j <= i + 1
	k = int(max(min(floor(s),n-1),0))					# Must have 0 <= k <= n-1
	s = max(min(s,k+1),k)							# Must have k <= s <= k+1
	s1=[s-(k-i) for i in range(n)]						# s1 & s2 will never be negative
	s2=[(k+n-i)-s for i in range(n)]
	w = [[0.0 for x in range(n+1)] for x in range(n)]
	w[0][1] = sys.float_info.max						# Scale for full 'double' range
	t = [[0.0 for x in range(n)] for x in range(n-1)]
	tiny = 2**(-1074)							# The smallest positive matlab 'double' no.
	
	for i in range(2,n+1):
		tmp1 = np.multiply(w[i-2][1:i+1],s1[0:i])/i
		tmp2 = np.multiply(w[i-2][0:i],s2[n-i:n])/i
		w[i-1][1:i+1] = np.add(tmp1,tmp2)
		tmp3 = np.add(w[i-1][1:i+1],tiny)				# In case tmp1 & tmp2 are both 0
		tmp4 = np.greater(s2[n-i:n],s1[0:i])				# then t is 0 on left & 1 on right
		t[i-2][0:i] = np.multiply(np.divide(tmp2,tmp3),tmp4) + np.multiply((1-np.divide(tmp1,tmp3)),(~tmp4))


	# Derive the polytope volume v from the appropriate
	# element in the bottom row of w.
	v.append(n**(3/float(2))*(w[n-1][k+1]/sys.float_info.max)*(b-a)**(n-1))

	# Now compute the matrix x.
	xl = [[0.0 for x in range(m)] for x in range(n)]
	if (m == 0):								# If m is zero, quit with x = []
		return None,None

	rt = np.matlib.rand(n-1, m)						# For random selection of simplex typ
	rs = np.matlib.rand(n-1, m)						# For random location within a simplex
	#rt=[[[0.4387,0.7952]],[[0.3816,0.1869]],[[0.7655,0.4898]]]
	#rs=[[[0.4456,0.7547]],[[0.6463,0.2760]],[[0.7094,0.6797]]]
	s = np.matlib.repmat(s,1,m)
	j = np.matlib.repmat(k+1,1,m)						# For indexing in the t table
	sm = np.zeros((1,m))
	pr = np.ones((1,m))							# Start with sum zero & product 1
	td = [0.0 for x in range(m)]

	for i in reversed(range(1,n)):						# Work backwards in the t table
		j = list(numpy.array(j).reshape(-1,))
		for x in range(len(j)):
			td[x] = t[i-1][j[x]-1]
		e = np.less_equal(rt[n-i-1][:],td[:])				# Use rt to choose a transition
		#print "e",e
		sx = np.power(rs[n-i-1][:],(1/float(i)))			# Use rs to compute next simplex coord
		#print "sx",sx
		sm = np.add(sm,np.multiply((1-sx),np.multiply(pr,s)/float(i+1)))# Update sum
		#print "sm",sm
		pr = np.multiply(sx,pr)						# Update product
		#print "pr",pr
		xl[n-i-1][:] = np.add(sm,np.multiply(pr,e))			# Calculate x using simplex coords.
		#print "xl",xl[n-i-1][:]
		s = s - e
		j = j - e 							# Transition adjustment
		#print "s,j",s,j

	xl[n-1][:] = np.add(sm,np.multiply(pr,s))				# Compute the last x

	xl = list(numpy.array(xl).reshape(-1,))

	# Randomly permute the order in the columns of x and rescale.
	rp = np.matlib.rand(n,m)						# Use rp to carry out a matrix 'randperm'
	rp = numpy.array(rp)
	#rp=[[[0.6551],[0.9597]],[[0.1626],[0.3404]],[[0.1190],[0.5853]],[[0.4984],[0.2238]]]
	for i in range(m):
		pxl = sorted(range(len(rp)), key=lambda k: rp[k][i])
		pxl = numpy.array(pxl)
		pxl = pxl[:,None]
		#px = list(numpy.array(px).reshape(-1,))
		pxl = list(numpy.array(np.add(pxl,np.matlib.repmat([n*i],n,1))).reshape(-1,))
		for d in range(n):
			xl[pxl[d]] = (b-a)*xl[pxl[d]]+a			# Permute & rescale x
	xl = np.reshape(xl, (-1, m))
	return xl,v

# Sample Test Run
#u,vl= randfixedsum(5,1,2,0,1)

