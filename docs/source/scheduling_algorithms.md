
# Scheduling Algorithms

This document explains the four scheduling algorithms implemented in this project. It provides guidance on how to use these algorithms with a JSON logical model of jobs, messages, and nodes.

## Overview

The scheduling algorithms covered are:
1. Latest Deadline First (LDF) for Multi-Node
2. Earliest Deadline First (EDF) for Multi-Node
3. Latest Deadline First (LDF) for Single-Node
4. Earliest Deadline First (EDF) for Single-Node

## JSON Logical Model

The JSON logical model consists of:
- **Tasks**: Represent the tasks to be scheduled.
- **Messages**: Represent dependencies between jobs.
- **Nodes**: Represent the processors or cores where jobs can be executed or the switches and routers in the network.
- **Links**: Represent the communication links between nodes and has the bandwidth and latency information.

Note the units of time are arbitrary but same across all properties.

### Example JSON Model

```json
{
  "application": {
    "Tasks": [
      {
        "id": "1",
        "wcet": 5,
        "mcet": 3,
        "deadline": 10
      },
      {
        "id": "2",
        "wcet": 3,
        "mcet": 2,
        "deadline": 25
      }
    ],
    "messages": [
      {
        "id": 1,
        "sender": 1,
        "receiver": 2,
        "size": 2,
      }
    ]
  },
  "platform": {
    "nodes": [
      {
        "id": 1,
        "type": "compute"
      },
      {
        "id": 2,
        "type": "compute"
      }
    ],
        }
    "links": [
	    {
      "id": 1,  
		  "start_node": 1,
		  "end_node": 2,
      "link_delay": 2,
      "bandwidth": 100,
      "type": "ethernet",
	    }
    ]
  }

}
```
### Example Scheduling Algorithms Output
Given the example JSON model, the output of scheduling algorithms should be as follows:

``` json
{
    "schedule": [
        {
            "task_id": "1",
            "node_id": "1",
            "start_time": 0,
            "end_time": 5,
            "deadline": 10
        },
        {
            "task_id": 2,
            "node_id": 2,
            "start_time": 7,
            "end_time": 10,
            "deadline": 25
        }
    ]
}
```
## Latest Deadline First (LDF) for Multi-Node

The Latest Deadline First (LDF) algorithm schedules jobs based on the latest deadlines. 
It aims to delay job execution as much as possible while still meeting deadlines, to allow more urgent jobs to execute first. Among these leaf nodes, the one with the latest deadline is selected to be scheduled last. Last process to execute is the one on which no other process depends that has the latest deadline.   Proceed  each  time  choosing  from  among  the  processes  whose  dependents  have already been scheduled.  LDF schedule respects all precedences and meets all deadlines.


### Usage

``` PYTHON
schedule = ldf_multicore(application_data, platform_data)
```
### Example


## Earliest Deadline First (EDF) for Multi-Node

The Earliest Deadline First (EDF) algorithm schedules jobs based on the earliest deadlines. 
It prioritizes jobs with the nearest deadlines to ensure that all deadlines are met as soon as possible. EDF scheduling gives priority to tasks based on the imminence of their deadlines.  The task with the closest deadline is scheduled first.  Given n independent processes with deadlines, d1, . . . , dn, schedule them to minimize the maximum lateness, defined by the following equation,
                                    
![alt text](image.png)


where f<sub>i</sub> is the finishing time of process 'i'.  Note that the above equation is negative if all deadlines are  met.   EDF  is  widely  used  in  systems  where  meeting  deadlines  is  crucial,  such  as  in multimedia systems for audio/video processing to ensure smooth streaming without delays. EDF ensures that tasks with the earliest deadlines are executed first. By prioritizing tasks based on their deadlines, EDF minimizes the chances of missing deadlines and helps meet real time  requirements.   EDF  maximizes  CPU  utilization  by  allowing  tasks  to  execute as soon as their deadlines arrive, as long as the  CPU is available. EDF provides predictability in terms of task execution times and deadlines.  The scheduling decisions are deterministic and can be analyzed and predicted in advance, which is crucial for real-time systems.  EDF can handle both periodic and aperiodic tasks, making it suitable for a wide range of real-time systems. It allows for dynamic task creation and scheduling without disrupting the execution of existing tasks.
## EDF and LDF for Single-Node
The Earliest Deadline First (EDF) and Latest Deadline First (LDF) algorithms for single-core systems schedules jobs similarly to the multi-core version but considers only one processor. 
The Least Deadline First (LDF) scheduling strategy starts by identifying the endpoint of the schedule.  The LDF scheduling strategy builds a schedule backwards.  Given a DAG, choose  the  leaf  node  with  the  latest  deadline  to  be  scheduled  last,  and  work  backwards. 

![alt text](edf_and_ldf.PNG)
*Figure 3: The LDF scheduling strategy in single core,the leaf node with the latest deadline to be scheduled last,and work backwards.  In EDF, the task with the closest deadline is scheduled first.*

EDF  optimizes  the  use  of system resources by minimizing idle time.  EDF provides a high level of responsiveness for time-critical  tasks.   It  ensures  that  tasks  are  scheduled  and  executed  promptly, reducing response times and improving system performance.

## Least Laxity

Laxity in scheduling algorithms is defined as the difference between a task’s deadline and therequired CPU time to complete it.  This metric is crucial in dynamic preemptive schedulingwhere priorities are  adjusted dynamically based on current  task states and requirements.The Least Laxity First (LLF) algorithm, which operates under the same assumptions as RateMonotonic Scheduling (RMS), exemplifies this approach by assigning the highest priority tothe task with the shortest laxity.  This means that tasks closer to their deadlines, with lessremaining time relative to their CPU demands, are prioritized. The task with the least laxitygets  the  highest  priority.   In  uniprocessor  systems,  this  scheduling  strategy  is  consideredoptimal because it effectively minimizes the likelihood of deadline misses by focusing CPUresources on the most time-critical tasks.  LL is not optimal in multiprocessor systems.


