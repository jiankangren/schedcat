'''
Saravanan Ramanathan
January 2016
'''
# Function to generate multi-core task set

from taskparam import ts
import mrand as MR

from math import *
from random import *
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

import pylab
import random
import numpy


# Function to generate all task set
def run():									# Generate tasksets
    for m in ts.m:								# no. of cores
	for hhu in range(ts.hhb_l,ts.hhb_h+1,ts.hhb_step):			# Hi-Hi Utilization
		hubound=m*float(hhu)/100					# Total bound = m * hhu
		for hlu in range(ts.hlb_l,hhu,ts.hlb_step):			# Hi-Lo Utilization
			lubound=m*float(hlu)/100				# Total bound = m * hlu
			for lu in range(ts.lb_l,100-hlu+1,ts.lb_step):		# Lo task utilization
				lbound=m*float(lu)/100				# Total bound = m * lu
                    		for p in ts.t_prob:				# Prob that task is Hi-task
				   	NHmin = max(ceil(hubound/ts.u_h),m+1)	# Calculate number of hi-tasks
				    	NLmin = ceil(lbound/ts.u_h)		# Find lower bound on low criticality tasks
					if(100>=max(hhu,hlu+lu)>=30):		# condition to configure utilization range
                        		    loop(m,hhu,hlu,lu,p,hubound,lubound,lbound,NHmin,NLmin)# Generate now

# Generate task with given parameters                                
def loop(m,hhu,hlu,lu,p,hubound,lubound,lbound,NHmin,NLmin):

    print m,hhu,hlu,lu,p							# Print the parameters of task set
    prefix=str(m)+"_"+str(hhu)+"_"+str(hlu)+"_"+str(lu)+"_"+str(p)		# Prefix to write down tasks
    f = open(ts.path+"_"+prefix+".in","w")					# Open file in write mode

    cond =  1									# Loop condition variable

# Comment the next three lines if you want to generate exact number of task sets for each combination
    numSet = int(ceil(ts.numSet/len(ts.t_prob)))				# Divide by number of percentage values
    comb = 2*(max(hhu,hlu+lu)/10)-1						# Determine the number of iterations given an utilization bound range - here 0.1 divided by 10
    t_comb = comb**2								# Total combinations including nested interations
    ts.numTask = int(ceil(numSet/float(t_comb)))				# Determine the number of task sets for each combination - rounded to an integer

# Generate for total number of task sets
    for j in range(ts.numTask):						# For total number of tasksets
	ai = max(m+1,ceil(NHmin/p),ceil(NLmin/(1-p)))			# Determine the number of tasks in a task set
	#print ai,10*m
	if(ai >= 10*m):							# Restrict total tasks in a task set to 10*m - enough for all p values
		Ntotal = 10*m
	else:
		Ntotal = randint (ai, 10*m)

# If any restrictions on the number of HC tasks - e.g. 3*m HC tasks.
	#NH = int(min(max((p*Ntotal),NHmin),3*m))
	#if(NH<3*m):
	#	NL = int(max((Ntotal-NH),NLmin))
	#else:
	#	NL = int(max((((1-p)/p)*NH),NLmin))

	NH = int(min((p*Ntotal),NHmin))					# Number of HC tasks in a task set
	NL = int(max((Ntotal-NH),NLmin))				# Number of LC tasks in a task set
	#print Ntotal,NH,NL,NHmin,hubound,lubound,lbound

        while cond:
            tasks=generate(m,hubound,lubound,lbound,p,NH,NL)			# Call generate task function	
	    if tasks!=None:							# If taskset not empty
		    writeTasks(f,tasks)						# Write task set into file
		    break
        f.write("---%d\n"%(j))							# Write taskset count
    f.close()									# Close file

# Function to generate task
def generate(m,hubound,lubound,lbound,p,NH,NL):

    Ull = 0									# Lo - lo U vector
    Uhh = 0									# Hi - hi U vector
    Uhl = 0									# Hi - lo U vector

    num = 0									# Count tasks
    temp_task = []								# Temporary task set

    qh,q1= MR.randfixedsum(NH,1,hubound,ts.u_l,ts.u_h)				# randfixessum to calculate uiH of Hi-tasks
    ql,q1 = pick_low_util(qh,NH,lubound,hubound,ts.u_l)				# Calculate uiL of Hi-tasks

    for j in range(NH):								# For all Hi-tasks

	uh = qh[j]								# Pick Hi utilization from list
        ul = ql[j]			        				# Pick Lo utilization from list

	if(ts.t_log_u==0):
		#T = int(uniform(ts.t_l,ts.t_h))					# Pick uniform period in range (pl, ph)
		T = int(uniform(max(ceil(2/float(ul)),ts.t_l),ts.t_h))
	else:
		T = int(floor((exp(uniform(log(max(ceil(2/float(ul))+ts.t_l,ts.t_l)),log(ts.t_h+ts.t_l))))/ts.t_l)*ts.t_l)	# Pick log-uniform period in range (pl, ph)

	crit = 1								# Define criticality

        c_lo = ul*T								# Compute execution time
        c_hi = uh*T

	if (c_lo < 2 or c_hi < 2):
		print c_lo,c_hi,ceil(2/float(ul))
		print "Errrrr"
		c = raw_input("Enter")
		#return None

        if (c_lo > c_hi+0.000001):							# Return error if CiL > CiH
		print c_lo,c_hi
		print "Errrrr"
		c = raw_input("Enter")

	Uhl+=float(c_lo)/T							# Add utilization in U vector
	Uhh+=float(c_hi)/T

	if (ceil(c_hi) < T):
	    if(ts.d_log_u==0):
		d=randint(ceil(c_hi),T)						# Compute uniform constrained deadline
	    else:
		d=int(floor((exp(uniform(log(ceil(c_hi)),log(T))))/ceil(c_hi))*ceil(c_hi))				# Compute log-uniform deadline
	else:
		d=T

	if ((Uhh>hubound+0.000001) or (Uhl>lubound+0.000001)):					# If Util greater than bound then break
		print "BErrrrr"
		c = raw_input("Enter")

	if(c_hi<=0 or c_lo<=0):							# Append task if execut. requirement is > 0
		print "CErrrrr"
		c = raw_input("Enter")
	
	temp_task.append((T,c_lo,c_hi,crit,d))				# Append period, exe.time, crit, deadline

        num = num + 1								# Total no. of tasks


    x,xl= MR.randfixedsum(NL,1,lbound,ts.u_l,ts.u_h)  				# Use randfixedsum - uiL of Lo-tasks
    #print x
    for j in range(NL):

		uh = x[j]							# Pick Lo utilization from list
		ul = uh								# Assign Lo utilization = Hi utilization

		if(ts.t_log_u==0):
			#T = int(uniform(ts.t_l,ts.t_h))				# Pick uniform period in  range (pl, ph)
			T = int(uniform(max(ceil(2/float(ul))+ts.t_l,ts.t_l),ts.t_h))
		else:
			T = int(floor((exp(uniform(log(max(ceil(2/float(ul)),ts.t_l)),log(ts.t_h+ts.t_l))))/ts.t_l)*ts.t_l)	# Pick log-uniform period in range (pl, ph)


		crit = 0							# Define criticality

        	c_lo = ul*T							# Compute execution time
        	c_hi = uh*T

		if (c_lo < 2 or c_hi < 2):
			print c_lo,c_hi,ceil(2/float(ul))
			print "Errrrr"
			c = raw_input("Enter")
			#return None

		Ull+=float(c_lo)/T						# Add utilization in U vector

		if (ceil(c_hi) < T):
			if(ts.d_log_u==0):
				d=randint(ceil(c_hi),T)				# Compute uniform constrained deadline
	    		else:
				d=int(floor((exp(uniform(log(ceil(c_hi)),log(T))))/ceil(c_hi))*ceil(c_hi)) 		# Compute log-uniform deadline
		else:
			d=T

        	if (Ull>lbound+0.000001):						# If Util greater than bound then break
			print "BErrrrr"
			c = raw_input("Enter")

		if(c_lo<=0):
			print "CErrrrr"
			c = raw_input("Enter")

		temp_task.append((T,c_lo,c_hi,crit,d))			# Append period, exe.time, crit, deadline

        	num = num + 1							# Total no. of tasks

    if ((Uhh<hubound-m*float(ts.hhb_step)/100) or (Uhl<lubound-m*float(ts.hlb_step)/100) or (Ull<lbound-m*float(ts.lb_step)/100)):					# Max uilization error
	#print temp_task
        return None								# Return none
    
    return temp_task								# Return task set



def pick_low_util(qh,NH,lubound,hubound,u_l):
	
	#print "qh",qh
	B = lubound
	Basign = 0
	Nrem = NH-1
	Hrem = hubound
	#lh = sorted(qh,reverse=True)						# Sort list in decreasing order
	lh=list(numpy.array(qh).reshape(-1,))
	ql=lh
	for i in range(NH):
		Hrem -= lh[i]
		ql[i] = uniform(max(u_l,B-Hrem),min((B-(Nrem*u_l)),lh[i]))
		Nrem -= 1
		B -= ql[i]
	#ql[NH-1] = B

	for i in range(NH):
		Basign += ql[i]

	#print "B,lubound",Basign,lubound
	#print "qh",qh
	#print "ql",ql
	if(Basign > lubound+0.000001):
		c = raw_input("Enter +")
	if(Basign < lubound-0.000001 ):
		c = raw_input("Enter -")

	return ql,1


# Function to write taskset into file
def writeTasks(f,tasks):
    for task in tasks:
        f.write("%d %f %f %d %d\n"%(task[0],task[1],task[2],task[3],task[4]))   # Ordering of writing


def main():									# Main function
	run()
	#tset = generate(2,1.4,0.5,0.7,0.5,3,2)
	#print tset
	#r = test.ECDF(tset)
	#print r

main()										# Call main()
