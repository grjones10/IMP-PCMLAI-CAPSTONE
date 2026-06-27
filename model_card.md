## Overview

__Model Name__: Combined Space-Filling and Function Approximation Optimisation<br>
__Type__: Black-Box Optimisation Workflow enabling both sapce-filling sampling and surrogate modelling<br>
__Version__: 1.13<br>

## Intended use

This codebase is intended for a 

__Unsuitable__

- ?
- ?

## Details:

The project has been split into 2 fundamental phases:

__Phase 1__: Space Filling
- __Aim__: Improving sampling of the space – particularly in the vicinity of a promising region
__Phase 2__: Function Maximisation
- __Aim__: make use of the sampling achieved in Phase 1 to fit a Neural Network and predict the maximum values

| Project Phase | Objective             | Weeks     | Query Approach                                                                        |
|---------------|-----------------------|-----------|---------------------------------------------------------------------------------------|
| 1.1           | Space Filling         | 1 - 2     | __most isolated point__ with space bound by convex hull of _all_ data points          |
| 1.2           | Space Filling         | 3 - 5     | __most isolated point__ with space bound by convex hull of _promising_ data points    |
| 1.3           | Space Filling         | 6 - 10    | __most isolated point__ with space bound by convex hull of _promising_ data points    |
| 2.1           | Function Maximisation | 11 - 13   | __Coordinate of model-approximated function maximum__                                 |

### Performance

__Phase 1__ (Week 1 - Week 10): Space Filling<br>

Summary of Performance:

Metrics Used:<br>
    - Current Maximum Value<br>
    - Localisation of Upper Quartile<br>
    - Most isolated coordinate

__Phase 2__ (Week 11 - Week 13): Function Maximisation<br>

Summary of Performance:

Metrics Used:<br>
    - Current Maximum Value<br>
    - MLE<br>
    - Modelled Maximum 

### Assumptions and limitations

__Assumptions__<br>

Bounding the initial search space with the convex hull of the initial data set built in an assumption that the peak would lie within the bounds of the initial data. This can be corrected in future version by adding the capability to bound by the overall domain 

__Limitations__<br>

 - __Peak within initial data bounds assumption___ <br>
 As mentioned above, the assumption of the peak lieing within the initial dataset is a limitation - and found to be false during the project. 
 - __NN training data__
 <br>the availability of the training data used for the neural network is very limited. Despite efforts in phase 1 to improve this, the high-dimensional domains remain very coarsely sampled. This limits the accuracy, and generality, of the model used to predict the maximu

### Ethical considerations