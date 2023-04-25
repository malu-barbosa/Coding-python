import numpy as np
import netCDF4 as nc
from pdb import set_trace

def read_data_from_netcdf(y_filename, x_filename_list, 
                          subset_function=None):
    """Read data from a netCDF file 
    Assumes that the variables in the netcdf file all have the name "variable"
    Assunes that values < -9E9, you dont want. This could be different in some circumstances.
    Arguments:

    y_filename -- a two element python list containing the name of the file and the target variable name
    x_filename_list -- a python list of filename containing the feature variables
    subset_function -- a function to be applied to each data set

    Returns:

    Y - a numpy array of the target variable
    X - an n-D numpy array of the feature variables 
    """
    
    y_dataset=nc.Dataset(y_filename[0])[y_filename[1]]
    y_dataset = np.array(y_dataset).flatten()
    # Create a new categorical variable based on the threshold
    y_dataset = np.where(y_dataset <= 0.010, 0, 1)
    #set_trace()
    #count number of 0 and 1 
    counts = np.bincount(y_dataset)
    #print(f"Number of 0's: {counts[0]}, Number of 1's: {counts[1]}")
    #set_trace()
    if subset_function is not None:
        Y=subset_function(y_dataset)
    else:
        Y=y_dataset

    n=len(Y)
    m=len(x_filename_list)
    X=np.zeros([n,m])

    for i, filename in enumerate(x_filename_list):

        x_dataset = nc.Dataset(filename[0])[filename[1]]
        x_dataset = np.array(x_dataset).flatten()
        X[:, i]=x_dataset
    
    cells_we_want = np.array([np.all(rw > -9e9) for rw in X])
    Y = Y[cells_we_want]
    X = X[cells_we_want, :]
    X = np.column_stack((X, np.ones(len(X)))) # add a column of ones to X 
    return Y, X

def read_data_from_csv(filename):
    """Read data from a file 
    """
    pass

def fit_linear_to_data(Y, X):
    """Fit equation to data
    """

    return A
    
def fit_logistic_to_data(Y, X):
    """Fit equation to data
    """

    return A

if __name__=="__main__":
    dir = "D:/Doutorado/Sanduiche/research/maxent-test/driving_and_obs_overlap/AllConFire_2000_2009/"
    y_filen = [dir +"GFED4.1s_Burned_Area_Fraction.nc", "Date"]
    
    x_filen_list=[]
    x_filen_list.append([dir + "precip.nc", "variable"])    
    x_filen_list.append([dir + "tas.nc", "variable"])    
    
    Y, X=read_data_from_netcdf(y_filen, x_filen_list)
    
    print(Y)
    print(X)
