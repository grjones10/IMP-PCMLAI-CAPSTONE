## Overview

__Model Name__: Combined Space-Filling and Function Approximation Optimisation<br>
__Type__: Black-Box Optimisation Workflow enabling both space-filling sampling and surrogate modelling<br>
__Version__: 1.13<br>

## Intended use

This codebase is intended for a 

__Unsuitable__

- ?
- ?

## Details: Project is been split into 2 phases

#### __Phase 1__: Space Filling
__Aim__: Improving sampling of the space<br>

- This phase spanned most of the project and did not aim to find the function's maximum. Rather, it was focused on building the foundations for __phase 2__ by improving the sampling in the region of promise 
- Initially very explorative, with the convex hull defined around all available data points
- The approach to bounding the search space, and the exploration-exploitation balance, evolved as patterns began to appear in the data

| __Workflow__  |                                                                                                                           | 
|---------------|---------------------------------------------------------------------------------------------------------------------------|
| 1.            | Determine the bounds of the search space                                                                                  |
| 2.            | Calculate the convex hull of those bounds                                                                                 |
| 3.            | Use latin hypercube sampling with 1e6 random seeds to sample the whole domain, extract points internal to the convex hull |
| 4.            | Find the internal point with the largest distance to all current data points - the __most isolated point__                |

#### __Phase 2__: Function Maximisation
__Aim__: make use of the sampling achieved in Phase 1 to fit a Neural Network (NN) and predict the maximum values<br>

- This phase spanned the final stages was focused making use of the sampling achieved in __phase 1__ to train a neural network on the promising points and find the maximum value of the underlying function
- Since the aim was to find the maximum, only data in the vicinity of the region of promise was used in training. The rational being that the loss function would then focus on accuracy in the region that was important 

| __Workflow__  |                                                                                                               | 
|---------------|---------------------------------------------------------------------------------------------------------------|
| 1.            | Find the current maximum value                                                                                |
| 2.            | Define a search radius around that current maximum and extract all points within                              |
| 3.            | Train an NN on the extracted data points                                                                      |
| 4.            | Provide the NN with 1e6 random samples of search radius and out the maximum model-approximated function value |

#### __Summary__

| Project Phase | Objective             | Weeks     | Query Approach                                                                                            |
|---------------|-----------------------|-----------|-----------------------------------------------------------------------------------------------------------|
| 1.1           | Space Filling         | 1 - 2     | __most isolated point__ with space bound by convex hull of _all_ data points                              |
| 1.2           | Space Filling         | 3 - 5     | __most isolated point__ with space bound by convex hull of _promising_ data points                        |
| 1.3           | Space Filling         | 6 - 10    | __most isolated point__ with space bound SVM-derived decision boundary or distance from current max value |
| 2.1           | Function Maximisation | 11 - 13   | __Coordinate of model-approximated function maximum__                                                     |

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
 As mentioned above, the assumption of the peak lying within the initial dataset is a limitation - and found to be false during the project. 
 - __NN training data__
 <br>the availability of the training data used for the neural network is very limited. Despite efforts in phase 1 to improve this, the high-dimensional domains remain very coarsely sampled. This limits the accuracy, and generality, of the model used to predict the maximum

### Ethical considerations

__Transparency__<br>
- An effort has been made herein to outline the different phases of project approach and the key assumption
- Furthermore, the results/plots folder contains visual representations of the function and the new query points for transparency
- _Future Improvements_: the choice of writing the code base from scratch rather than using an existing codebase means documentation of the user-defined libraries is limited to the notes within. There is room to improve this documentation to aid understanding and reproducibility  
