## Modeling The States of Liquid Phase Change Pouch Actuators by Reservoir Computing

First, [install][1] the $\it{PhysRes}$ framework.

Load the [.npy file][2] (in a script created in your PhysRes/examples folder) containing the OptiTrack data for all 5 markers to create an array of 416 experiments, 19588 time steps, and 15 coordinates: 

    import numpy as np
    np.random.seed(42) #for reproducibility
    from prc import model
    from scripts import utils

    sample = 1 #downsample if need e.g. sample = 10
    Y_ = np.load(data_out_interp)[:,::sample,:-1] #load all coordinates, except for the last column, representing the on/off signal, not needed for modeling the states

Some experiments should be discarded, for example when containing erroneous labeling (as stated in the [OptiTrack documentation][3], "multiple non-unique Rigid Bodies may lead to mislabeling errors" in the auto-labeling feature), resulting in a final number of 399 experiments:


    # Discard error-proned files
    pruned = [28, 29, 30, 31, 97, 98, 99, 135, 144, 198, 328, 369, 408, 409, 410, 411, 412]
    Y_ = np.delete(Y_, pruned, axis=0)
    Y_ = np.nan_to_num(Y_,nan=0)

    L = Y_.shape[0]
    total_frames = Y_.shape[1]
    M = Y_.shape[2]


The collected data are then randomized and divided into a training set (70% of the data, i.e., 279 experiments) and a test set (30%, or 120 experiments) so that the model does not learn patterns specific to the data collection’s sequential nature. We initialize the $\it{PhysRes}$ model with the default hyperparameters. The input to the network consists of shifted coordinates by half of the points in the original Y_ array, while the other half indexes the target for model estimations (i.e., the input shifted ahead in time by 9,794 steps, half the total number of time steps). Then, the model is trained to reconstruct the pouch’s target state. Note that the input needs to be reshaped in a 2d array to be accepted by the model, such that its columns represent a concatenation of all coordinates, and its rows represent the experiment index. The network estimations will therefore be over all points, for each experiment. Consequently, a target 9,784 steps ahead does not just represent a time-delay of the input, but may also represent a coordinate shift, from one axis to the next, or from one marker's last axis to the next marker's first axis. Such matrix of re-ordered coordinates is what we define as "the state(s) of the system".

    permutation = np.random.permutation(L)
    Y_ = Y_[permutation]

    order = 'F' #Reshape for the network matrices shape requirement
    Y = Y_.reshape(L,-1,order=order)

    N = 1000  #Reservoir size (number of nodes, , type: int)
    alpha = 1  #Alpha (scaling hyperparam, type: float)
    lamda = 1  #latency (type: int). Note: "lambda" is already taken in python builtins (the anonymous lambda function)
    tau = 1  #Tau (state delay, generally set to 1, type: int)
    x0 = 0  #Initial condition (type: float)
    steps_ahead = int((total_frames/2))
    physres = model.PhysRes(Y[:,:-steps_ahead], N, x0, lamda, alpha, tau)  #Instantiate
    X = physres.Run(verbose=False, save_operand=False)  #Run
    Y_test, Ypred, split = physres.TrainTest(0.7, Y[:,steps_ahead:])

We now reshape the target and estimation to retrieve the initial array shape.

    L_test = Y_test.shape[0]
    total_points = Y.shape[1]
    test_points = total_points - steps_ahead

    Y_test_ = np.zeros((L_test, total_points))
    Y_test_[:,:test_points] = Y_test
    Y_test_ = Y_test_.reshape(L_test,-1,M,order=order)

    Ypred_ = np.zeros((L_test, total_points))
    Ypred_[:,:test_points] = Ypred
    Ypred_ = Ypred_.reshape(L_test,-1,M,order=order)

Y_test_ and Ypred_ represent the ground truth state and estimated state of the system, respectively.
Finally, we compute the model's estimation errors (normalized root mean squared errors or NRMSE) wrt to the target along each column, and their mean, standard deviation, and median.

    errors = np.asarray( [
        [
            utils.computeEr( Y_test_[File_, :, coor_], Ypred_[File_, :, coor_] )
            for coor_ in range(M)
        ]
        for File_ in range(L_test)
    ] ).T

    print(np.mean(errors))
    print(np.std(errors))
    print(np.median(errors))

[1]: https://github.com/KawaharaLab/PhysRes
[2]: https://drive.google.com/file/d/1xwKmGbU0_p_Dro_v88EjaXGeZlishxr7/view?usp=share_link
[3]: https://docs.optitrack.com/motive/rigid-body-tracking
