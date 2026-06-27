## Overview: 

__Model Name__: Combined Space-Filling and Function Approximation Optimisation<br>
__Type__: Black-Box Optimisation Workflow enabling both sapce-filling sampling and surrogate modelling<br>
__Version__: 1.13<br>

## Intended use:

This codebase is intended for a 

__Unsuitable__

- ?
- ?

## Details: 

#### Performance

__Phase 1__ (Week 1 - Week 10): Space Filling<br>

Summary of Performance:

Metrics Used:<br>
    - Current Maximum Value<br>
    - Localisation of Upper Quartile<br>  
    - Most isolated coordinate<br>

__Phase 2__ (Week 11 - Week 13): Function Maximisation<br>

Summary of Performance:

Metrics Used:<br>
    - Current Maximum Value<br>
    - MLE<br>
    - Modelled Maximum <br>

#### Assumptions and limitations

__Assumptions__<br><br>

Bounding the initial search space with the convex hull of the initial data set built in an assumption that the peak would lie within the bounds of the initial data. This can be corrected in future version by adding the capability to bound by the overall domain 

__Limitations__<br><br>

 - Peak within initial data bounds assumption: <br>As mentioned above, the assumption of the peak lieing within the initial dataset is a limitation - and found to be false during the project. 
 - NN training data: <br>the availability of the training data used for the neural network is very limited. Despite efforts in phase 1 to improve this, the high-dimensional domains remain very coarsely sampled. This limits the accuracy, and generality, of the model used to predict the maximu

#### Ethical considerations