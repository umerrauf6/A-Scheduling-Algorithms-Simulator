# Scheduling Algorithms

This document explains the four scheduling algorithms implemented in this project. It provides guidance on how to use these algorithms with a JSON logical model of jobs, messages, and nodes.

## Overview

The scheduling algorithms covered are:
1. Latest Deadline First (LDF) for Multi-Core
2. Earliest Deadline First (EDF) for Multi-Core
3. Latest Deadline First (LDF) for Single-Core
4. Earliest Deadline First (EDF) for Single-Core

## JSON Logical Model

The JSON logical model consists of:
- **Jobs**: Represent the tasks to be scheduled.
- **Messages**: Represent dependencies between jobs.
- **Nodes**: Represent the processors or cores where jobs can be executed or the switches and routers in the network.
- **Links**: Represent the communication links between nodes and has the bandwidth and latency information.

Note the units of time are arbitrary but same across all properties.

### Example JSON Model

```json
{
  "application": {
    "jobs": [
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
      "timetriggered": 1
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
```
### Example Scheduling Algorithms Output
Given the example JSON model, the output of scheduling algorithms should be as follows:

``` json
{
    "schedule": [
        {
            "job_id": "1",
            "node_id": "1",
            "start_time": 0,
            "end_time": 5,
            "deadline": 10
        },
        {
            "job_id": 2,
            "node_id": 2,
            "start_time": 7,
            "end_time": 10,
            "deadline": 25
        }
    ]
}
```
## Latest Deadline First (LDF) for Multi-Core

The Latest Deadline First (LDF) algorithm schedules jobs based on the latest deadlines. 
It aims to delay job execution as much as possible while still meeting deadlines, to allow more urgent jobs to execute first.

### Usage

``` PYTHON
schedule = ldf_multicore(application_data, platform_data)
```
### Example


## Earliest Deadline First (EDF) for Multi-Core

The Earliest Deadline First (EDF) algorithm schedules jobs based on the earliest deadlines. 
It prioritizes jobs with the nearest deadlines to ensure that all deadlines are met as soon as possible.

### Usage

``` PYTHON
schedule = edf_multicore(application_data, platform_data)
```
### Example
## EDF and LDF for Single-Core
The Earliest Deadline First (EDF) and Latest Deadline First (LDF) algorithms for single-core systems schedules jobs similarly to the multi-core version but considers only one processor.


