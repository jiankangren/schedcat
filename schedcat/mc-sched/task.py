"""Task class"""


class Task:
    """Abstract representation of the task."""

    def __init__(self, crit, bgt_lo, bgt_hi, prio_lo, prio_hi,
                 d_lo, d_hi, pr_lo, pr_hi):
        """Initialize task params."""
        self.index = None  # Use for iteration
        self.crit = crit  # System criticality.
        self.c_lo = float(bgt_lo)  # Low crit budget.
        self.c_hi = float(bgt_hi)  # High crit budget.
        self.prio_lo = float(prio_lo)  # Low crit priority.
        self.prio_hi = float(prio_hi)  # High crit priority.
        self.d_lo = float(d_lo)  # Low crit deadline.
        self.d_hi = float(d_hi)  # High crit deadline.
        self.t_lo = float(pr_lo)  # Low crit period.
        self.t_hi = float(pr_hi)  # High crit period.

    def task_util(self, mode="low"):
        """Get task utilization for low or high mode."""
        util = None
        if mode == "low":
            util = self.c_lo / self.t_lo
        elif mode == "high":
            util = self.c_hi / self.t_hi
        else:
            raise AttributeError("Undefined mode input provided.\n")
        return util

    def task_attrib(self, mode="low"):
        """Retrieve task attribute for low or high mode."""
        attrib = None
        if mode == "low":
            attrib = (self.c_lo, self.prio_lo, self.t_lo, self.d_lo)
        elif mode == "high":
            attrib = (self.c_hi, self.prio_hi, self.t_hi, self.d_hi)
        else:
            raise ValueError("Undefined mode input provided.\n")
        return attrib

    def __getattr__(self, name=None):
        """Override the attribute keyword"""
        attrib = None
        if name == "pd_l":
            attrib = self.t_lo
        elif name == "pd_h":
            attrib = self.t_hi
        elif name == "dl_l":
            attrib = self.d_lo
        elif name == "dl_h":
            attrib = self.d_hi
        elif name == "b_l":
            attrib = self.c_lo
        elif name == "b_h":
            attrib = self.c_hi
        elif name == "p_l":
            attrib = self.prio_lo
        elif name == "p_h":
            attrib = self.prio_hi
        elif name == "c":
            attrib = self.crit
        else:
            raise AttributeError("Invalid attribute name provided as input.")
        return attrib

    def __str__(self):
        """Print task information."""
        return "Crit:{0}, period-low:{1}, period-high:{2}, \
                budget-low:{3}, budget-high:{4}, deadline-low:{5},\
                deadline-high:{6}\n".format(self.crit, self.t_l,
                                            self.t_hi, self.c_lo, self.c_hi,
                                            self.d_lo, self.d_hi)
