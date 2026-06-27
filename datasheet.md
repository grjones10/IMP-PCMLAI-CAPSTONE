## Motivation
__Pbjective__: Find the maximum of unknown mathmatical functions<br><br>
This dataset was generated as part of a Black-Box Optimisation task for Imperial College London's _Professional Certificate in Machine Learning and AI Capstone Project_. 

## Composition
  
 There are 8 different datasets within corresponding to 8 different functions (F1, F2, ..., F8)
 - The datasets for each function are composed of initially provided data points, and the queries requested during the project. These are distinguished with a binary "new_point" channel in the dataframe when loading the data
    <br> -- original datasets are store in their original .npy format and parsed into a dataframe using the data_loading library
    <br> -- new data points are stored as weekly .csv files in the results folder and parsed into the dataframe using the data_loading library
 - data is stored as floating point numbers to 6 decimal places

| Data Table                                                           |
| Function | Dimensions | Number of Points | Max Value | Min Value     |
|----------|-----------|---------------|---------------|---------------|
| F1       | 2D        | 20            | 0.037891      | -0.006092     |
| F2       | 2D        | 20            | 0.666604      | -0.132547     |
| F3       | 3D        | 25            | 0.006003      | -0.398926     |
| F4       | 4D        | 40            | -3.810608     | -32.625660    |
| F5       | 4D        | 28            | 4170.668432   | 0.112940      | 
| F6       | 5D        | 30            | -0.499612     | -2.571170     |
| F7       | 6D        | 39            | 1.869530      | 0.002701      |  
| F8       | 8D        | 50            | 9.833484      | 5.592193      | 

## Collection process

Each function was queried once a week, following evaluation of the available data up to that point. The coordinate of each query was determined by the code related to that phase of the strategy. 

<br> -- Phase 1: Queries were the most isolated point within a bound search space. The space was bound by regions of promise - and SVM-derived decision boundary, distance from a peak or samples in the upper quartile of outputs
<br> -- Phase 2: Queries were a Neural Networks approximation of maximum values

## Preprocessing and uses

Outputs were scaled to be within 0 - 1, and where absolute values are less than 1e-6, they are considered 0 owing to the 6 decimal place precision. 

## Distribution and maintenance

- all data is available within this repository. For repository structure, see README.md
- Data was generated over the duration of the capstone project (Q2 2026). It was maintained by the owner of the repository - Gareth Jones