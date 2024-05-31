# Lab 2 - Scheduling algorithms for Real Time Systems
## Introduction

Scheduling algorithms are fundamental to the functioning of real-time embedded systems, which are integral to numerous critical applications ranging from automotive safety systemsto  healthcare  monitoring  devices. These  systems  rely  on  precise  timing  and  immediate response  to  external  events  to  function  correctly  and  efficiently. The  role  of  scheduling algorithms is to manage the execution priorities of tasks in a way that optimizes performance and ensures timely task completion.Ineffective  scheduling  can lead  to missed deadlines, system overloads, and failures,  which in safety-critical systems could result in severe consequences.  Therefore, the application of effective scheduling algorithms is crucial for enhancing system reliability and overall performance.  By ensuring that system resources are allocated efficiently and tasks are completedwithin their time constraints, scheduling algorithms help maintain the integrity and reliability of embedded systems.

![Intro image](https://upload.wikimedia.org/wikipedia/commons/0/0c/Thread_pool.svg)
*Figure 1: A pool of tasks completed based on scheduling*
## Objective

The primary goal outlined in this task sheet is to design and implement various schedul-ing algorithms within the context of real-time systems.  This application will serve as aneducational tool, providing visual insights into how different algorithms manage tasks andresources.  Users will be able to interact with the application to modify task parameters,compare the outcomes of different scheduling strategies, and gain a deeper understandingof their advantages and limitations in real-world scenarios.Through this web-based platform, we aim to bridge theoretical knowledge and practical ap-plication, enabling learners and practitioners to visualize the dynamic processes of scheduling.

## Background 

Directed Acyclic Graph (DAG) is an incredibly valuable tool for representing and managingthe relationships and dependencies among various tasks or jobs that need to be scheduled. In such graphs, each node represents a task, and the directed edges between these nodes indicatethe precedence relationships, meaning that one task must be completed before another can begin.  In a DAG used for scheduling, each node represents an individual task or job.  These tasks  often  have  associated  attributes  like  duration,  resource  requirements,  or  deadlines.The directed edges between the nodes represent the precedence constraints.  An edge fromnode A to node B implies that task A must be completed before task B can start.  This directionality is critical for ensuring tasks are performed in the correct order.  The acyclic property of DAGs is crucial in scheduling because it guarantees that there are no circular dependencies, which would make scheduling impossible.  In practical terms, this means therecan be no situation where task A depends on task B, while task B simultaneously depends on task A, either directly or indirectly.The different scheduling algorithms are described in this section.

![My Image](./images/DAG.png)
*Figure 2: A directed acyclic graph (DAG) shows precedences, showing that process 1 must complete before processes 2 and 3 can be started, etc.*

## Tasks

 - Prepare your local environment with Python, FastAPI, NetworkX, Uvicorn, and all necessary libraries for backend development or use the requirements.txt file using the following command :
    ``` BASH
    pip install -r requirements.txt
    ```
 - Upload the provided JSON file (to visualize a pre-defined logical model) to the frontend (https://eslab2.pages.dev/), by pressing the 'Upload JSON' button in the frontend page.

 - Integration of frontend and backend : Ensure that the frontend and backend are integrated smoothly.

 - To add more nodes and edges to the existing model use 'Add Node' and 'Add edge' button and provide the details like Worst case execution time (WCET), Mean case execution time (MCET), deadline for the node etc.  The application provides a clear visualization of the logical model, making it easy to understand task dependencies.  
 
 - Implement Scheduling Algorithms:  Develop the scheduling algorithms in Python, with functionality to accept input parameters and provide outputs in JSON format. Define  Python  functions  for  each  scheduling  algorithm  (LDF, EDF, LL)  in algorithms.py file.

 - Visualize the resulting schedules in a bar graph format by pressing the 'Schedule Graph' button, providing a clear overview of the task timeline.
 
 - Debug any issues found during testing and validate the functionality of the scheduling algorithms.
 


 ## Documentation and Reporting

 As you test and optimize, document your findings.  Note down what worked, what did not,and how you adjusted your approach.  This documentation will be invaluable for your finalreport and provides a clear record of your problem solving process.  Testing and optimizationare as much a part of the learning process as the initial development.  They provide insightinto the practical challenges and the importance of iterative design.

 ### Documenting the Code

 - **Code Comments**:Include comprehensive comments throughout your python code.  Explain the purpose of functions, logic behind critical sections, and meanings of key variables.Use inline comments for complex lines of code to clarify their functionality.
 - **Readable  Structure**:Organize  your  code  logically.   Group  related  functionalities  intofunctions  or  classes  and  use  clear,  descriptive  names  for  variables  and  functions.   Ensureyour script follows a consistent coding style for ease of reading and maintenance.

 ### Writing the Lab Report

 - **Introduction**: Briefly  introduce  the  objectives  of  the  lab,  the  significance  of  scheduling strategies in single core and multi core systems.
 - **Methodology**: Detail  the  algorithm  you  developed.   Discuss  any  specific  programming techniques used.  Include diagrams or flowcharts if they help clarify your algorithm’s structure.
 - **Discussion**: Analyze the results.  Discuss any challenges faced, how you addressed them,and what you learned from the process.  Reflect on the effectiveness of your algorithm and potential improvements.
 
 - **Conclusion**:Summarize your findings and the insights you gained reading various scheduling strategies. References:Include  any  references  to  external  resources,  such  as  textbooks,  papers,  or online materials, that assisted you in the lab.

 ## Deliverables

 - algorithms.py file with scheduling algorithm implemented.
 - Lab report in pdf format.

 ## Evaluation Criterion

 - Well-structured and logically organized code.
 - Comprehensive comments explaining the purpose and logic of the code.
 - Quality of the report.




