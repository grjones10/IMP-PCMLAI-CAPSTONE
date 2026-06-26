import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull, Delaunay
import bbo_project.data_plotting as data_plotting

def subset_volume(df,input_cols,threshold):

    import math
    
    upper_q = df[df["YScaled"] >= threshold]
    non_upper_q = df[df["YScaled"] < threshold]

    # Centre of upper quartile points
    centre = upper_q[input_cols].mean()

    # Radius needed to enclose all upper quartile points
    upper_distances = np.linalg.norm(upper_q[input_cols] - centre, axis=1)
    radius = upper_distances.max()

    dims = len(input_cols)
    volume_fraction = (math.pi**(dims / 2) / math.factorial(dims // 2)) * radius**dims


    # Distances of ALL points from the centre
    all_distances = np.linalg.norm(df[input_cols] - centre, axis=1)

    # Which points fall inside the radius?
    inside_volume = all_distances <= radius

    # Count non-upper-quartile points inside
    non_upper_inside = (
        inside_volume & (df["YScaled"] < threshold)
    ).sum()
    upper_inside = (
        inside_volume & (df["YScaled"] > threshold)
    ).sum()

    return volume_fraction*100, non_upper_inside, upper_inside

def compute_convex_hull(data):


    points = data.to_numpy()

    if points.ndim != 2:
        raise ValueError("Input must be a 2D array of shape (m, n)")

    if points.shape[0] <= points.shape[1]:
        raise ValueError(
            "Need at least n+1 points in n-dimensional space to form a convex hull"
        )

    hull = ConvexHull(points)

    return hull, points

import numpy as np
from scipy.spatial import Delaunay

def most_isolated_point_new(points, hull, n_samples=10000, seed=42, bounds=None):
    """
    Finds the most isolated point.

    If bounds is provided:
        → search inside bounding box ONLY

    If bounds is None:
        → search inside convex hull
    """

    rng = np.random.default_rng(seed)

    points = np.asarray(points)
    dim = points.shape[1]

    # ----------------------------
    # Distance computation target
    # ----------------------------
    # (can be changed later for boundary exclusion etc.)
    target_points = points

    # ----------------------------
    # CASE 1: bounded box search (NO hull)
    # ----------------------------
    if bounds is not None:

        mins = np.asarray(bounds["lowers"])
        maxs = np.asarray(bounds["uppers"])

        if len(mins) != dim or len(maxs) != dim:
            raise ValueError("Bounds dimensionality does not match data.")

        candidates = rng.uniform(mins, maxs, size=(n_samples, dim))

    # ----------------------------
    # CASE 2: convex hull search
    # ----------------------------
    else:
        delaunay = Delaunay(points[hull.vertices])

        mins = points.min(axis=0)
        maxs = points.max(axis=0)

        candidates = rng.uniform(mins, maxs, size=(n_samples, dim))

        inside_mask = delaunay.find_simplex(candidates) >= 0
        candidates = candidates[inside_mask]

        if len(candidates) == 0:
            raise ValueError("No sampled points fell inside convex hull.")

    # ----------------------------
    # Compute isolation (vectorised)
    # ----------------------------
    dists = np.linalg.norm(
        target_points[:, None, :] - candidates[None, :, :],
        axis=2
    )

    min_dists = dists.min(axis=0)

    best_idx = np.argmax(min_dists)

    best_point = candidates[best_idx]
    best_dist = min_dists[best_idx]

    return best_point, best_dist

def most_isolated_point(points, hull, n_samples=10000, seed=42):
    """
    Finds the point inside the convex hull that is farthest from dataset points.

    If exclude_boundary=True, hull vertices are excluded from distance calculation.
    """

    print("\tgenerating random seeds...")
    rng = np.random.default_rng(seed)
    points = np.asarray(points)
    dim = points.shape[1]

    # ----------------------------
    # Build hull test (still uses full hull geometry)
    # ----------------------------
    delaunay = Delaunay(points[hull.vertices])

    # ----------------------------
    # Sample bounding box
    # ----------------------------

    mins = points.min(axis=0)
    maxs = points.max(axis=0)

    candidates = rng.uniform(mins, maxs, size=(n_samples, dim))

    # ----------------------------
    # Keep only points inside hull
    # ----------------------------
    print("\tfinding internal points...")
    inside_mask = delaunay.find_simplex(candidates) >= 0
    inside_points = candidates[inside_mask]

    if len(inside_points) == 0:
        raise ValueError("No sampled points fell inside the convex hull.")

    # ----------------------------
    # Compute isolation
    # ----------------------------
    best_point = None
    best_dist = -np.inf

    print("\tlooking for furthest points...")
    for p in inside_points:
        dists = np.linalg.norm(points - p, axis=1)
        min_dist = np.min(dists)

        if min_dist > best_dist:
            best_dist = min_dist
            best_point = p

    return best_point, best_dist

def minmax_scale(Y):
    Y = np.asarray(Y)
    
    if Y.ndim == 1:
        Y_min, Y_max = Y.min(), Y.max()
        return (Y - Y_min) / (Y_max - Y_min if Y_max != Y_min else 1)

    Y_min = Y.min(axis=0)
    Y_max = Y.max(axis=0)
    range_ = Y_max - Y_min
    range_[range_ == 0] = 1

    return (Y - Y_min) / range_

import itertools

def filter_points_in_bounding_box(df_other, bounds_info):
    lows = bounds_info["lowers"]
    highs = bounds_info["uppers"]

    mask = np.ones(len(df_other), dtype=bool)

    for i, col in enumerate(df_other.columns):
        mask &= (df_other[col].values >= lows[i]) & (df_other[col].values <= highs[i])

    return df_other[mask]

def compute_hypercube_corners(X):

    n_points, n_features = X.shape

    while True:
        try:

            parts = input(
                f"Enter bounds per dimension (e.g. 0,1;0.2,0.8 for {n_features}D): "
            ).split(";")

            if len(parts) != n_features:
                print("Wrong number of dimensions.")
                continue

            lows = []
            highs = []

            for i, p in enumerate(parts):
                l, u = map(float, p.split(","))

                if l >= u:
                    raise ValueError(f"Invalid bounds in dimension {i+1}: {l} >= {u}")

                lows.append(l)
                highs.append(u)

            lows = np.array(lows)
            highs = np.array(highs)

            # ----------------------------
            # Generate hypercube corners
            # ----------------------------
            corners = np.array(
                list(itertools.product(*zip(lows, highs)))
            )

            # ----------------------------
            # Convert to DataFrame
            # ----------------------------
            col_names = [f"X{i+1}" for i in range(n_features)]
            corners_df = pd.DataFrame(corners, columns=col_names)

            bounds_info = {
                "lowers": lows,
                "uppers": highs,
                "corners": corners_df
            }

            break

        except Exception as e:
            print("Invalid format.")

    return corners_df, bounds_info

from scipy.stats import qmc

def generate_lhc(n_dims, n_samples=100000, seed=42):
    """
    Generates LHS samples in [0.05, 0.95]^n
    """

    sampler = qmc.LatinHypercube(d=n_dims, seed=seed)
    unit_samples = sampler.random(n=n_samples)

    lows = np.full(n_dims, 0.05)
    highs = np.full(n_dims, 0.95)

    samples = qmc.scale(unit_samples, lows, highs)

    return samples

from sklearn import svm, metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import copy


def k_folds(data, k):
    """
    Stratified k-fold split preserving class imbalance as closely as possible.
    """

    # Shuffle full dataset
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    # Split by class
    df_zero = data[data["promising"] == 0]
    df_one = data[data["promising"] == 1]

    n0 = len(df_zero)
    n1 = len(df_one)

    # Compute exact counts per fold
    n0_per_fold = [n0 // k + (i < n0 % k) for i in range(k)]
    n1_per_fold = [n1 // k + (i < n1 % k) for i in range(k)]

    # Shuffle each class
    df_zero = df_zero.sample(frac=1, random_state=42).reset_index(drop=True)
    df_one = df_one.sample(frac=1, random_state=42).reset_index(drop=True)

    folds = []
    idx0 = 0
    idx1 = 0

    for i in range(k):
        fold_zero = df_zero.iloc[idx0:idx0 + n0_per_fold[i]]
        fold_one = df_one.iloc[idx1:idx1 + n1_per_fold[i]]

        idx0 += n0_per_fold[i]
        idx1 += n1_per_fold[i]

        fold = pd.concat([fold_zero, fold_one])
        fold = fold.sample(frac=1, random_state=42).reset_index(drop=True)

        folds.append(fold)

    return folds

def fit_and_predict_SVM(train, validate, x_columns,g,c):

    X_train = train[x_columns].to_numpy()
    y_train = train['promising'].to_numpy()
    X_val = validate[x_columns].to_numpy()

    # counts = train["promising"].value_counts()
    # class_weight={1: int(np.divide(counts[0],counts[1])), 0: 1}

    SVM = svm.SVC(kernel='rbf', gamma = g, C = c,  class_weight="balanced")
    SVM.fit(X_train, y_train)


    return SVM.predict(X_val)

def accuracy(prediction, true):

    cm = confusion_matrix(true, prediction)
    acc = accuracy_score(true, prediction)

    return acc

def cross_validation(folds,x_columns,g,c):


    import copy
    folds = copy.copy(folds) #This creates a new variable, which is a copy of folds

    accuracy_SVM = []  #This is a list to collect the RMSEs for each fold for the KRR

    for i, fold in enumerate(folds):

        ############################
        #Write code to create the training and validation sets as data frames

        train = pd.concat(folds[:i]+folds[(i+1):])
#         train = pd.concat([folds.pop(i)])
        validate = fold

        ############################

        ############################
        #Use the fit_and_predict function to create new columns in the validation set for the predictions
        #for KRR model with the heading ['KRR_predictions'].

        validate['SVM_predictions'] = fit_and_predict_SVM(train, validate, x_columns,g,c)

        ############################

        ############################
        #Calculate the RMSE and append it to rmses_KRR

        accuracy_SVM.append(accuracy(validate['SVM_predictions'].to_numpy(), validate['promising'].to_numpy()))

        ############################

    RMSE_SVM = np.mean(accuracy_SVM) # calculate the average RMSEs for kernel ridge regression
    STD_SVM = np.std(accuracy_SVM) # calculate the average RMSEs for kernel ridge regression

    return RMSE_SVM,STD_SVM

def svm_hyperparameter_tuning(df,input_cols,save_path):

    grid_params = np.arange(0,10,0.2)
    grid_params += 0.01

    folds =  k_folds(df, 5)

    G, C, A = list(),list(),list()

    for gam in grid_params:
        for pen in grid_params:

            RMSE_SVM,STD_SVM = cross_validation(copy.copy(folds),input_cols, gam, pen)

            G.append(gam)
            C.append(pen)
            A.append(RMSE_SVM)

    svm_cross_validation = pd.DataFrame({
    "gamma": G,
    "C": C,
    "Accuracy": A
    })

    C_best, gamma_best, max_val = data_plotting.plot_hyperparameter_surface(svm_cross_validation,save_path)

    return C_best, gamma_best, max_val, STD_SVM

def fit_svm(df, g, c, input_cols):

    X = df[input_cols].to_numpy()
    y = df["promising"].to_numpy().ravel()

    weight = int(1/np.divide(len(df[df["promising"] == 1]),len(df)))

    SVM = svm.SVC(kernel='rbf', gamma = g, C = c, class_weight={0: weight, 1: 1})
    SVM.fit(X, y)

    return SVM.predict(X), SVM

def augment_with_svm(df,df_sampled,samples,input_cols,save_path):

    print("\t\ttuning hyperparameters...")

    c, g, val_acc, val_std = svm_hyperparameter_tuning(df,input_cols,save_path)

    print("\t\tHyperparamters Parameters:")
    print("\t\t\tC =", c)
    print("\t\t\tgamma =", g)
    print("\t\t\tValidation Accuracy =", val_acc)
    print("\t\t\tValidation Standard Deviation =", val_std)

    print("\t\tfitting final SVM model...")
    df["prediction"], model = fit_svm(df, g, c, input_cols)

    all_acc = accuracy(df['prediction'].to_numpy(), df['promising'].to_numpy())

    print("\t\t\tFull Model Accuracy =", all_acc)

    print(f"Extracting points from Latin Hypercube on promising side of decision boundary ...")
    df_sampled["promising"] = model.predict(samples)
    df_sampled = df_sampled[df_sampled["promising"] == 1]

    return df_sampled

def extract_distance_from_max(df, variable, input_cols, min_points):

    max_idx = df[variable].idxmax()
    max_point = df.loc[max_idx]

    center = max_point[input_cols].values.astype(float)

    input_points = df[input_cols].values.astype(float)

    r = 0.1
    num_points_inside = 0

    if len(input_cols) <= 4:
        while num_points_inside < min_points:
            r += 0.02
            distances = np.linalg.norm(input_points - center, axis=1)

            # Points inside n-dimensional sphere
            inside_mask = distances <= r
            # region_of_interest = df[inside_mask]
            region_of_interest = df.loc[inside_mask].copy()
            num_points_inside = len(region_of_interest)
    else:
        while num_points_inside < (len(input_cols)*2):

            r += 0.02
            distances = np.linalg.norm(input_points - center, axis=1)

            # Points inside n-dimensional sphere
            inside_mask = distances <= r
            region_of_interest = df[inside_mask]
            num_points_inside = len(region_of_interest)
        
    return region_of_interest

def seed_convex_hull(points, hull, n_samples=10000000, seed=42):

    from scipy.spatial import Delaunay

    rng = np.random.default_rng(seed)

    points = np.asarray(points)
    dim = points.shape[1]

    target_points = points

    delaunay = Delaunay(points[hull.vertices])

    mins = points.min(axis=0)
    maxs = points.max(axis=0)

    candidates = rng.uniform(mins, maxs, size=(n_samples, dim))

    inside_mask = delaunay.find_simplex(candidates) >= 0
    candidates = candidates[inside_mask]

    return candidates