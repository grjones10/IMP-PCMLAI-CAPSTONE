## Section 1: Project Overview

This Black-Box Optimisation project has the overall aim of finding the maximum of 8 different functions. The functions are unknown, and of varying dimensions. An initial set of data is provided and beyond that the functions are evaluated a further 10 times. The output of each evaluation is returned and learned from with each iteration.

Such a process is reverent to the real-world where obtaining additional information about a particular phenomenon in industry or research comes at a cost and only a finite amount of experiments can therefore be carried out. To best model this phenomenon, the parameters of those experiments must be chosen wisely.

From a career perspective this project provides the opportunity to better understand principles studied during the course by practically applying them. Through this, better appreciation of benefits and trade-offs of different modelling approaches and the impact of uncertainty will be achieved, and directly applied to modelling work in my career.

## Section 2: Inputs and Outputs

To parse the input and output data I have written a library of functions called data_loading found in the src folder. 

Data Set:

There are 8 unknown functions of increasing dimensionality from 2D to 8D. The dataset for each function has two components: 

1. Initial Data Points
The project starts with an initial set of inputs and respective outputs for each function in .npy format. These are converted into a dataframe by the load_initial_data function within the data_loading library where the inputs have column names containing a prefix X (e.g. X1, X2, …, Xn) and the output has the column name Y.

2. Updated Data Points
Each week new, updated data points are received for each function by e-mail and copied to a csv in the format shown below:

function name   inputs	                            outputs
function_1	    [X1, X2]                            Y
function_2	    [X1, X2]                            Y
:
function_3	    [X1, X2, X3, X4, X5, X6, X7, X8]    Y 

These new data points are appended to a function’s initial dataframe by the apply_updates function in the data_loading library

Function Evaluation:

To evaluate the function with an updated datapoint, each week a query is submitted to the capstone dashboard as coordinates to 6 decimal places. An example of a submission to function 1 is shown below:

Function 1: 0.550501-0.050001

There is a constraint of only being able to submit 10 updated queries, so these must be chosen wisely. The response to the function evaluation is a discrete floating point number value which corresponds to the unknown function’s actual value at the location of evaluation.

## Section 3: Challenge Objectives

Objective: Maximise each of the unknown functions
This objective is constrained by a maximum 10 updated queries per function, and a response delay while each new query is processed. Furthermore - beyond the number of dimensions - nothing is known about the function’s structure. 

For example:
-- Is the maximum within the bounds of the initial data set or not? 
-- Is there more than one local maxima? 

## Section 4: Technical Approach

The main principal of the first few weeks of the project it is better populate the sample space before trying to models.

1. Week 1
This first week takes a purely explorative approach by looking for the most isolated point within the input domain and choosing that as the coordinate of the next point 
-- A convex hull is calculated to find the bounds of the inputs space
-- Random sampling is used to efficiently fill the multi-dimensional space
-- The random sample with the largest Euclidian distance to any of the input data point is chosen as the next point

2. Week 2

This week takes a more balanced approach to exploration-exploitation, with a bias to exploration. Unlike week 1, I considered the output-input relationship. I still explore the sample space by looking for a "most isolated point", but this time I manually define a bounding box for that search based on observations from the input-output relationships
-- functionality was added to scatter the output "Y" as a function of each input variable independently 
-- where clear trends were present, I used the bounding box to exclude regions of the domain where a maximum looked highly unlikely 

3. Week 3

This extends the boundary box approach from week 2. Rather than manually specifying a bounding box from inspection of the input-output scatter, this code classifies the data with a binary "promising" channel.  
-- Data points with an output in the upper quartile of values are given a "promising" value of 1, others are 0 
-- A convex hull is then drawn around the subset of points defined as being "promising" 
-- This convex hull is then searched for the most-isolated point as in week 1, but the search region is now concentrated around points that appear to be close to the maximum

bbo_project/
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
├── .venv/
│
├── data/
│   ├── initial_data/
│   │   └── function_1/
│   │       ├── initial_inputs.npy
│   │       ├── initial_output.npy
│   │
│   └── updated_data/
│       ├── new_data_points_wk1.csv
│       └── ...
│
├── results/
│   ├── week_1/
│   │   └── plots/
│   │       ├── function_1/
│   │       └── ...
│   ├── wk1_submission.csv
│   └── ...
│
├── notebooks/
│   └── main_week1.ipynb
│
└── src/
    ├── __init__.py
    ├── data_loading.py
    ├── data_augmentation.py
    └── data_plotting.py
