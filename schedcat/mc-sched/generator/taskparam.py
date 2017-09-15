'''
Saravanan Ramanathan
May 2017
'''

# Class to define taskset generation parameters
class ts:

#Path
    path="./data/in/"
    out_path="./data/out/"

# Period
    t_l=10					# Period Low
    t_h=200					# Period High
    t_log_u=0					# 0 - uniform 1 - log uniform T

# Deadline
    d_log_u=0					# 0 - uniform 1 - log uniform d

# Cores
    m=[2]					# No. of cores [2,4,8,16]

# Bound for low util
    lb_l=15					# Total Util low - 0.05
    lb_h=100					# Total Util High - 1.0
    lb_step=10					# Total Util step - 0.1

# Bound for low util
    hlb_l=15					# Total Util low - 0.05
    hlb_h=100					# Total Util High - 1.0
    hlb_step=10					# Total Util step - 0.1

# Bound for high util
    hhb_l=30					# Total Util low - 0.1
    hhb_h=100					# Total Util High - 1.0
    hhb_step=10					# Total Util step - 0.1

# Task
    numTask=5					# No. of task sets in each combination file. Exact value.
    numSet=100					# Total task set count for each utilization bound. Appx value. Generates around 100 task sets.
						# Multiple by number of p values.

# Utilization
    u_l=0.01					# Minimum utilization for any task
    u_h=1.0					# Maximum utilization for any task
    u_val=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

# Percentage of HC tasks
    #t_prob=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9] # Percentage of HC tasks in any task set
    t_prob=[0.5]

# Additional variables for plotting graphs
    count=0

    low = 0
    med = 0
    high = 0

    close = 0
    far = 0

    ulist = []
    rlist = []
