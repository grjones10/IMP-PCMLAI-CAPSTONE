## Project Overview

This Black-Box Optimisation project has the overall aim of finding the maximum of 8 different functions. The functions are unknown, and of varying dimensions. An initial set of data is provided and beyond that the functions are evaluated a further 13 times. The output of each evaluation is returned and learned from with each iteration to inform the next.

Such a process is reverent to the real-world where obtaining additional information about a particular phenomenon in industry or research comes at a cost, and only a finite number of experiments can therefore be carried out. To best model this phenomenon, the parameters of those experiments must be chosen wisely.

From a career perspective this project offers the opportunity to better understand principles studied during the course by practically applying them. The experience has provided better appreciation of the benefits and trade-offs of different modelling approaches, and can be directly applied to modelling work in my career.

#### Repository Structure

```
bbo_project/
├── .gitignore
├── pyproject.toml
├── README.md
├── DATASHEET.md
├── MODEL_CARD.md
├── requirements.txt
├── .venv/
│
├── data/
│   ├── initial_data/
│   │   └── function_1/
│   │       ├── initial_inputs.npy
│   │       └── initial_output.npy
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
│   └── phase11.ipynb
│
└── src/
    ├── __init__.py
    ├── data_loading.py
    ├── data_augmentation.py
    └── data_plotting.py
```
- The main code for running the optimisation strategy are in jupyter notebook found in notebooks/
    - This code makes use of three user-defined python libraries
        1. _data_loading.py_ 
        2. _data_augmetnation.py_
        3. _data_plotting.py_ 

## Inputs and Outputs

#### Input Dataset
There are 8 unknown functions of increasing dimensionality from 2D to 8D. Input and output data pertaining to each function (found in data/) is parsed to a pandas dataframe by calling functions in _data_loading.py_. 

The dataset for each function has two components: 

1. Initial Data Points (data/initial_data)
    - The project starts with an initial set of inputs and respective outputs for each function in .npy format. 
    - These are converted into a dataframe by the load_initial_data function within the _data_loading.py_ library where the inputs have column names containing a prefix X (e.g. X1, X2, …, Xn) and the output has the column name Y.

2. Updated Data Points (data/updated_data)
    - Each week new, updated data points are received for each function by e-mail and copied to a csv in the format shown below:


| Function | Inputs                             | Outputs      |
|----------|------------------------------------|--------------|
| F1       | [X1, X2]                           | Y1           |
| F2       | [X1, X2]                           | Y1           |
| F3       | [X1, X2, X3]                       | Y1           |
| F4       | [X1, X2, X3, X4]                   | Y1           |
| F5       | [X1, X2, X3, X4]                   | Y1           |
| F6       | [X1, X2, X3, X4, X5]               | Y1           |
| F7       | [X1, X2, X3, X4, X5, X6]           | Y1           |
| F8       | [X1, X2, X3, X4, X5, X6, X7, X8]   | Y1           |


These new data points are appended to a function’s initial dataframe by the apply_updates function in the _data_loading.py_ library

#### Code Output

The output of the code are the coordinates of the next desired function evaluation. To evaluate the function with an updated data point, each week a query is submitted to the capstone dashboard as coordinates to 6 decimal places. 

An example of a submission to function 1 is shown below:<br>
-- Function 1: 0.550501-0.050001

There is a constraint of only being able to submit 13 updated queries, so these must be chosen wisely. The response to the function evaluation is a discrete floating point number value which corresponds to the unknown function’s actual value at the location of evaluation.

## Challenge Objectives

__Objective__: Maximise each of the unknown functions

This objective is constrained by a maximum 13 updated queries per function, and a response delay while each new query is processed. Furthermore - beyond the number of dimensions - nothing is known about the function’s structure. 

For example:<br>
-- Is the maximum within the bounds of the initial data set or not? 
-- Is there more than one local maxima? 

## Technical Approach

The project has been split into 2 fundamental phases:

__Phase 1__ (Week 1 - Week 10): Space Filling<br>
    __Aim__: Improving sampling of the space – particularly in the vicinity of a promising region. 
    
The point chosen for the next function evaluation is the most isolated point within a bound search space
    -- Not attempt to maximise the function at this stage
    -- The rational is that a surrogate model based on poorly sampled training data will provide unreliable results  

- A convex hull is calculated to find the bounds of the inputs space
- Random sampling is used to efficiently fill the multi-dimensional convex hull space
- The random sample with the largest Euclidian distance to any of the input data point is chosen as the next point

Exploration and Exploitation are balanced by points that define the convex hull. Initially the convex hull is drawn around all samples (exploring whole domain). As more information became available, the search space was bound by promising regions. This region to was defined with either SVM-derived decision boundary, the distance from a peak, or the points within the upper quartile of output values (exploiting information). 

__Phase 2__ (Week 11 - Week 13): Function Maximisation<br>
_Aim__: make use of the sampling achieved in Phase 1 to fit a Neural Network and predict the maximum values

- current maximum is found, and all points within a pre-defined distance from that point are extracted
- Neural Network (NN) is trained on the data set described above 
- The trained NN is provided with random samples of the domain and returns the coordinates with the maximum output value
