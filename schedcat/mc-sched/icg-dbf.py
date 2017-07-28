import sys
from audsley import audsley
from taskset import taskset

class icg_dbf(audsley):
    """Speed up bound and schedulability check for ICG"""
    
    def __init__(self, taskset):
        self.taskset = taskset
        self.graph = {}

    def __get_task_with_minimum_edge_weight(self, task):
        """Among the active edges of given task find the task with minimum 
        edge weight"""
        node = self.graph[task.index]
        weight = task.b_lo
        for t in node["edges"]:
            weight = min(weight, t.b_lo)
        return weight

    def __create_new_node(self, t):
        """Create a new node to be inserted in the graph.
        Each node consists of a vertex, which is the task t, a set of
        edges representing the tasks which t can interfer with and edge 
        weight, which is budget of the current task in criticality level of target
        task(if edge from t_i to t_j, weight is C_i in criticality level of t_j ).
        """
        node = {
                "vertex":t,
                "edges": [],
                }
        self.graph[task.index] = node

    def __asign_task_priorities(self):
        """Use audsley priority assignment on given taskset."""
        taskset = self.assign_priorities(self.taskset)
        if len(taskset):
            self.taskset = taskset

    def __calculate_min_speed_up(self, task):
        """Calculate the minimum speed up factor."""
        pass

    def __get_response_time(self, task):
        """Get the worst case response time for the given task.
        RTA calculation as per algorithm 1 in paper. 
        """
        RTA_i = task.b_hi
        tasks_high_prio = self.taskset.get_high_prio(task)
        for t in tasks_high_prio:
            sigma_i_j = 0  # interference on j from i
            sigma_j_i = 0  # interference on i from j
            if task.crit == 'high':
                sigma_j_i = t.b_hi
            else:
                sigma_j_i = t.b_lo

            if t.crit == 'high':
                sigma_i_j = task.b_hi
            else:
                sigma_i_j = task.b_lo
            
            RTA_i += math.ceil(R_i/t.t_lo) * min(sigma_i_j, sigma_j_i)
        return RTA_i

    def interference_minimization(self):
        """Iteratively minimize the interference in the task graph."""
        pass

    def dbf_icg(self):
        """Calculate the demand bound for the task."""
        pass

    def icg_schedulability(self):
        """ICG schedulability test based on graph based representation with
        interference allowed."""
        
        

# Edge modification and addition api set.
    def __calculate_graph_edges(self):
        """Each high critical task is to have a default edge to all low
        crit task."""

# Auxiliary functions to determine the speedup factor of given tasks.

    def __get_scheduling_points(self, task, taskset):
        """Get the scheduling points as per lehocsky's approach.'"""
        schedule_points = []
        for i in range(1, task.prio):
            k_range = task.d_lo / taskset[i].t_lo
            for k in range(1, math.floor(k_range)):
                schedule_points.append(k * taskset[i].t_lo)
        return schedule_points

    def __get_critical_scaling_factor(self, task, taskset):
        """Determine critical speed up factor for given task."""
        scale_factor = 0
        schedule_points = self.__get_scheduling_points(task)
        for t in schedule_points:
            iter_scale = 0
            for i in range(t):
                C_j_i = 0
                T_j_i = 0
                if task.crit == 'high':
                    C_j_i = taskset[i].c_hi
                    T_j_i = taskset[i].t_hi
                else:
                    C_j_i = taskset[i].c_lo
                    T_j_i = taskset[i].t_lo
                iter_scale += (C_j_i/t) * math.ceil(t/T_j_i)
            scale_factor = min(scale_factor, iter_scale)
        return 1/scale_factor

    def __speed_modulation(self, priority_count = 0):
        """Determine maximum scaling factor."""
        critical_speedup = 0
        if priority_count == 0:
            raise ValueError("No of priorities should not be non zero.\n")
        taskset_local = copy.copy(self.taskset)
        taskset_prio_assigned = []
        is_not_picked = lambda x, y: return x.index == y.index

        for i in reversed(range(priority_count, 1)):
            task_vestal = None
            for task in taskset_local:
                if task_vestal is None:
                    task_vestal = task
                    critical_speedup = self.__get_critical_scaling_factor(task, taskset_local)
                else:
                    crit_speed_prev = self.__get_critical_scaling_factor(task_vestal, taskset_local)
                    crit_speed_curr = self.__get_critical_scaling_factor(task, taskset_local)
                    if crit_speed_prev < crit_speed_factor:
                        task_vestal = task
            task.prio = i
            # Remove the picked task from next iteration loop and add to new priority list.
            taskset_local[:] = [x for x in taskset_local if is_not_picked(x, task_vestal)]
            taskset_prio_assigned.append(task_vestal)
            
            # Recalculate the critical speedup factor again with new task list.
            new_crit_speedup = self.__get_critical_scaling_factor(task, taskset_local)
            if new_crit_speedup < critical_speedup:
                critical_speedup = new_crit_speedup
        return (critical_speedup, taskset_prio_assigned)

