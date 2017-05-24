"""Task class"""
class Task:
    """Abstract representation of the task."""
    def __init__(self, crit, bgt_lo, bgt_hi, prio_lo, prio_hi,
            dl_lo, dl_hi, pr_lo, pr_hi):
        """Initialize task params."""
        self.__crit = crit      #System criticality.
        self.__bgt_lo = float(bgt_lo)    #Low crit budget.
        self.__bgt_hi = float(bgt_hi)    #High crit budget.
        self.__prio_lo = float(prio_lo)   #Low crit priority.
        self.__prio_hi = float(prio_hi)   #High crit priority.
        self.__dl_lo = float(dl_lo)     #Low crit deadline.
        self.__dl_hi = float(dl_hi)     #High crit deadline.
        self.__pr_lo = float(pr_lo)     #Low crit period.
        self.__pr_hi = float(pr_hi)     #High crit period.

    def task_util(self, mode="low"):
        """Get task utilization for low or high mode."""
        util = None
        if mode == "low":
            util = self.__bgt_lo/ self.__pr_lo
        elif mode == "high":
            util = self.__bgt_hi/ self.__pr_hi
        else:
            raise AttributeError("Undefined mode input provided.\n")
        return util

    def task_attrib(self, mode="low"):
        """Retrieve task attribute for low or high mode."""
        attrib = None
        if mode == "low":
            attrib = (self.__bgt_lo, self.__prio_lo, self.__pr_lo, self.__dl_lo)
        elif mode == "high":
            attrib = (self.__bgt_hi, self.__prio_hi, self.__pr_hi, self.__dl_hi)
        else:
            raise ValueError("Undefined mode input provided.\n")
        return attrib

    def __getattr__(self, name=None):
        """Override the attribute keyword"""
        attrib = None
        if name == "pd_l":
            attrib = self.__pr_lo
        elif name == "pd_h":
            attrib = self.__pr_hi
        elif name == "dl_l":
            attrib = self.__dl_lo
        elif name == "dl_h":
            attrib = self.__dl_hi
        elif name == "b_l":
            attrib = self.__bgt_lo
        elif name == "b_h":
            attrib = self.__bgt_hi
        elif name == "p_l":
            attrib = self.__prio_lo
        elif name == "p_h":
            attrib = self.__prio_hi
        elif name == "c":
            attrib = self.__crit
        else:
            raise AttributeError("Invalid attribute name provided as input.")
        return attrib

    def __str__(self):
        """Print task information."""
        return "Crit:{0}, period-low:{1}, period-high:{2}, \
                budget-low:{3}, budget-high:{4}, deadline-low:{5},\
                deadline-high:{6}\n".format(self.__crit, self.__pr_low,
                        self.__pr_hi, self.__bgt_lo, self.__bgt_hi,
                        self.__dl_lo, self.__dl_hi)


