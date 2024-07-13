"""
This module contains the scheduling algorithms used in the scheduling API.

It provides implementations for both Least Deadline First (LDF) and Earliest Deadline First (EDF) scheduling strategies, applicable in single-core and multi-core processor environments. Functions within are designed to be called with specific application and platform data structures.

Functions:
- ldf_singlecore: Schedules tasks on a single-core processor using LDF.
- edf_singlecore: Schedules tasks on a single-core processor using EDF.
- ll_singlecore: Schedules tasks on a single-core processor using LL.
- ldf_multicore: Schedules tasks on multiple cores using LDF.
- edf_multicore: Schedules tasks on multiple cores using EDF.
"""

__author__ = "Umer Rauf, Afnan Arshad"
__version__ = "2.0.0"


import networkx as nx

# Example schedule to check the frontend and backend connection
example_schedule = [
    {
        "task_id": "3",
        "node_id": 0,
        "end_time": 20,
        "deadline": 256,
        "start_time": 0,
    },
    {
        "task_id": "2",
        "node_id": 0,
        "end_time": 40,
        "deadline": 300,
        "start_time": 20,
    },
    {
        "task_id": "1",
        "node_id": 0,
        "end_time": 60,
        "deadline": 250,
        "start_time": 40,
    },
    {
        "task_id": "0",
        "node_id": 0,
        "end_time": 80,
        "deadline": 250,
        "start_time": 60,
    },
]


def ldf_single_node(application_data):
    """
    Schedule jobs on a single node using the Latest Deadline First (LDF) strategy.

    This function schedules jobs based on their latest deadlines after sorting them and considering dependencies through a directed graph representation.

    Args:
        application_data (dict): Contains jobs and messages that indicate dependencies among jobs.

    Returns:
        list of dict: Scheduling results with each job's details, including execution time, node assignment,
                      and start/end times relative to other jobs.
    """
    jobs = application_data['tasks']
    dependencies = application_data.get('messages', [])

    # Convert dependencies into a graph representation
    dependency_graph = nx.DiGraph()
    for job in jobs:
        dependency_graph.add_node(job['id'])
    for dependency in dependencies:
        dependency_graph.add_edge(dependency['sender'], dependency['receiver'])

    # Sort jobs by latest deadline first
    jobs_sorted = sorted(jobs, key=lambda x: x['deadline'], reverse=True)

    # Initialize the schedule
    schedule = []
    job_start_times = {}
    jobs_scheduled = set()

    # Schedule jobs considering dependencies
    while jobs_sorted:
        job = jobs_sorted.pop(0)
        job_id = job['id']

        # Ensure all dependencies have been scheduled
        unscheduled_dependencies = [
            dep for dep in dependency_graph.predecessors(job_id) if dep not in jobs_scheduled]
        if unscheduled_dependencies:
            jobs_sorted.append(job)  # Reinsert job at the end of the list
            # If only this job is left and still not schedulable, there's a cyclic dependency
            if len(jobs_sorted) == 1:
                raise ValueError(
                    f"Cyclic dependency detected or missing dependencies for job {job_id}.")
            continue

        # All dependencies are scheduled, schedule this job
        max_dependency_end_time = 0
        for dependency in dependency_graph.predecessors(job_id):
            max_dependency_end_time = max(max_dependency_end_time, job_start_times[dependency] + next(
                j['wcet'] for j in jobs if j['id'] == dependency))

        # Schedule the job
        job_start_time = max_dependency_end_time
        job_end_time = job_start_time + job['wcet']
        job_start_times[job_id] = job_start_time
        jobs_scheduled.add(job_id)

        schedule.append({
            'task_id': job_id,
            'node_id': 0,
            'start_time': job_start_time,
            'end_time': job_end_time,
            'deadline': job['deadline']
        })

    return {"schedule": schedule, "name": "LDF Single Node"}


def edf_single_node(application_data):
    """
    Schedule jobs on single node using the Earliest Deadline First (EDF) strategy.

    This function processes application data to schedule jobs based on the earliest
    deadlines. It builds a dependency graph and schedules accordingly, ensuring that jobs with no predecessors are
    scheduled first, and subsequent jobs are scheduled based on the minimum deadline of available nodes.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.
    """
    jobs = application_data['tasks']
    dependencies = application_data.get('messages', [])

    # Convert dependencies into a graph representation
    dependency_graph = nx.DiGraph()
    for job in jobs:
        dependency_graph.add_node(job['id'])
    for dependency in dependencies:
        dependency_graph.add_edge(dependency['sender'], dependency['receiver'])

    # Sort jobs by earliest deadline first
    jobs_sorted = sorted(jobs, key=lambda x: x['deadline'])

    # Initialize the schedule
    schedule = []
    job_start_times = {}
    jobs_scheduled = set()

    # Schedule jobs considering dependencies
    while jobs_sorted:
        job = jobs_sorted.pop(0)
        job_id = job['id']

        # Ensure all dependencies have been scheduled
        unscheduled_dependencies = [
            dep for dep in dependency_graph.predecessors(job_id) if dep not in jobs_scheduled]
        if unscheduled_dependencies:
            jobs_sorted.append(job)  # Reinsert job at the end of the list
            # If only this job is left and still not schedulable, there's a cyclic dependency
            if len(jobs_sorted) == 1:
                raise ValueError(
                    f"Cyclic dependency detected or missing dependencies for job {job_id}.")
            continue

        # All dependencies are scheduled, schedule this job
        max_dependency_end_time = 0
        for dependency in dependency_graph.predecessors(job_id):
            max_dependency_end_time = max(max_dependency_end_time, job_start_times[dependency] + next(
                j['wcet'] for j in jobs if j['id'] == dependency))

        # Schedule the job
        job_start_time = max_dependency_end_time
        job_end_time = job_start_time + job['wcet']
        job_start_times[job_id] = job_start_time
        jobs_scheduled.add(job_id)

        schedule.append({
            'task_id': job_id,
            'node_id': 0,
            'start_time': job_start_time,
            'end_time': job_end_time,
            'deadline': job['deadline']
        })

    return {"schedule": schedule, "name": "EDF Single Node"}


def ll_multinode(application_data, platform_data):
    """
    Schedule jobs on a distributed system with multiple compute nodes using the Least Laxity (LL) strategy.
    This function schedules jobs based on their laxity, with the job having the least laxity being scheduled first.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.
        platform_data (dict): Contains information about the platform, nodes and their types, the links between the nodes and the associated link delay.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.
    """
    jobs = application_data['tasks']
    dependencies = application_data.get('messages', [])
    nodes = platform_data['nodes']

    # Convert dependencies into a graph representation
    dependency_graph = nx.DiGraph()
    for job in jobs:
        dependency_graph.add_node(job['id'])
    for dependency in dependencies:
        dependency_graph.add_edge(dependency['sender'], dependency['receiver'])

    # Initialize the schedule
    schedule = []
    job_start_times = {}
    job_end_times = {}
    jobs_scheduled = set()
    # Current time for each node
    current_time = {node['id']: 0 for node in nodes}

    def calculate_laxity(job, current_time):
        return job['deadline'] - (current_time + job['wcet'])

    # Helper function to find a node with the minimum current time
    def find_available_node(current_time):
        return min(current_time, key=current_time.get)

    # Schedule jobs considering dependencies
    while jobs:
        # Filter out jobs that are ready to be scheduled (all dependencies met)
        ready_jobs = [job for job in jobs if all(
            dep in jobs_scheduled for dep in dependency_graph.predecessors(job['id']))]

        if not ready_jobs:
            raise ValueError(
                "Cyclic dependency detected or missing dependencies among jobs.")

        # Sort ready jobs by laxity
        ready_jobs.sort(key=lambda x: calculate_laxity(
            x, current_time[find_available_node(current_time)]))

        # Get the job with the least laxity
        job_to_schedule = ready_jobs[0]
        job_id = job_to_schedule['id']

        # Find an available node to schedule the job
        node_id = find_available_node(current_time)

        # Ensure the job starts after all its dependencies have finished
        max_dependency_end_time = 0
        for dependency in dependency_graph.predecessors(job_id):
            max_dependency_end_time = max(
                max_dependency_end_time, job_end_times.get(dependency, 0))

        # Schedule the job
        job_start_time = max(current_time[node_id], max_dependency_end_time)
        job_end_time = job_start_time + job_to_schedule['wcet']
        job_start_times[job_id] = job_start_time
        job_end_times[job_id] = job_end_time
        jobs_scheduled.add(job_id)
        current_time[node_id] = job_end_time

        schedule.append({
            'task_id': job_id,
            'node_id': node_id,
            'start_time': job_start_time,
            'end_time': job_end_time,
            'deadline': job_to_schedule['deadline']
        })

        # Remove the scheduled job from the list of jobs
        jobs = [job for job in jobs if job['id'] != job_id]

    return {"schedule": schedule, "name": "LL Multi Node"}


def ldf_multinode(application_data, platform_data):
    """
    Schedule jobs on a distributed system with multiple compute nodes using the Latest Deadline First (LDF) strategy.
    This function schedules jobs based on their periods and deadlines, with the shortest period job being scheduled first.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.
        platform_data (dict): Contains information about the platform, nodes and their types, the links between the nodes and the associated link delay.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.
    """
    jobs = application_data['tasks']
    dependencies = application_data.get('messages', [])
    nodes = platform_data['nodes']

    # Convert dependencies into a graph representation
    dependency_graph = nx.DiGraph()
    for job in jobs:
        dependency_graph.add_node(job['id'])
    for dependency in dependencies:
        dependency_graph.add_edge(dependency['sender'], dependency['receiver'])

    # Sort jobs by latest deadline first
    jobs_sorted = sorted(jobs, key=lambda x: x['deadline'], reverse=True)

    # Initialize the schedule
    schedule = []
    job_start_times = {}
    jobs_scheduled = set()
    # Current time for each node
    current_time = {node['id']: 0 for node in nodes}

    # Helper function to find a node with the minimum current time
    def find_available_node(current_time):
        return min(current_time, key=current_time.get)

    # Schedule jobs considering dependencies
    while jobs_sorted:
        job = jobs_sorted.pop(0)
        job_id = job['id']

        # Ensure all dependencies have been scheduled
        unscheduled_dependencies = [
            dep for dep in dependency_graph.predecessors(job_id) if dep not in jobs_scheduled]
        if unscheduled_dependencies:
            jobs_sorted.append(job)  # Reinsert job at the end of the list
            # If only this job is left and still not schedulable, there's a cyclic dependency
            if len(jobs_sorted) == 1:
                raise ValueError(
                    f"Cyclic dependency detected or missing dependencies for job {job_id}.")
            continue

        # Find an available node to schedule the job
        node_id = find_available_node(current_time)

        # Ensure the job starts after all its dependencies have finished
        max_dependency_end_time = 0
        for dependency in dependency_graph.predecessors(job_id):
            max_dependency_end_time = max(max_dependency_end_time, job_start_times[dependency] + next(
                j['wcet'] for j in jobs if j['id'] == dependency))

        # Schedule the job
        job_start_time = max(current_time[node_id], max_dependency_end_time)
        job_end_time = job_start_time + job['wcet']
        job_start_times[job_id] = job_start_time
        jobs_scheduled.add(job_id)
        current_time[node_id] = job_end_time

        schedule.append({
            'task_id': job_id,
            'node_id': node_id,
            'start_time': job_start_time,
            'end_time': job_end_time,
            'deadline': job['deadline']
        })

    return {"schedule": schedule, "name": "LDF Multi Node"}


def edf_multinode(application_data, platform_data):
    """
    Schedule jobs on a distributed system with multiple compute nodes using the Earliest Deadline First (EDF) strategy.
    This function processes application data to schedule jobs based on the earliest
    deadlines.

    Args:
        application_data (dict): Job data including dependencies represented by messages between jobs.
        platform_data (dict): Contains information about the platform, nodes and their types, the links between the nodes and the associated link delay.

    Returns:
        list of dict: Contains the scheduled job details, each entry detailing the node assigned, start and end times,
                      and the job's deadline.
    """
    jobs = application_data['tasks']
    dependencies = application_data.get('messages', [])
    nodes = platform_data['nodes']

    # Convert dependencies into a graph representation
    dependency_graph = nx.DiGraph()
    for job in jobs:
        dependency_graph.add_node(job['id'])
    for dependency in dependencies:
        dependency_graph.add_edge(dependency['sender'], dependency['receiver'])

    # Sort jobs by earliest deadline first
    jobs_sorted = sorted(jobs, key=lambda x: x['deadline'])

    # Initialize the schedule
    schedule = []
    job_start_times = {}
    jobs_scheduled = set()
    # Current time for each node
    current_time = {node['id']: 0 for node in nodes}

    # Helper function to find a node with the minimum current time
    def find_available_node(current_time):
        return min(current_time, key=current_time.get)

    # Schedule jobs considering dependencies
    while jobs_sorted:
        job = jobs_sorted.pop(0)
        job_id = job['id']

        # Ensure all dependencies have been scheduled
        unscheduled_dependencies = [
            dep for dep in dependency_graph.predecessors(job_id) if dep not in jobs_scheduled]
        if unscheduled_dependencies:
            jobs_sorted.append(job)  # Reinsert job at the end of the list
            # If only this job is left and still not schedulable, there's a cyclic dependency
            if len(jobs_sorted) == 1:
                raise ValueError(
                    f"Cyclic dependency detected or missing dependencies for job {job_id}.")
            continue

        # Find an available node to schedule the job
        node_id = find_available_node(current_time)

        # Ensure the job starts after all its dependencies have finished
        max_dependency_end_time = 0
        for dependency in dependency_graph.predecessors(job_id):
            max_dependency_end_time = max(max_dependency_end_time, job_start_times[dependency] + next(
                j['wcet'] for j in jobs if j['id'] == dependency))

        # Schedule the job
        job_start_time = max(current_time[node_id], max_dependency_end_time)
        job_end_time = job_start_time + job['wcet']
        job_start_times[job_id] = job_start_time
        jobs_scheduled.add(job_id)
        current_time[node_id] = job_end_time

        schedule.append({
            'task_id': job_id,
            'node_id': node_id,
            'start_time': job_start_time,
            'end_time': job_end_time,
            'deadline': job['deadline']
        })

    return {"schedule": schedule, "name": "EDF Multi Node"}
