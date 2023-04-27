import numpy as np
import netCDF4 as nc
from pdb import set_trace
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def read_variable_from_netcdf(filename, dir = None, subset_function=None,):
    """Read data from a netCDF file 
    Assumes that the variables in the netcdf file all have the name "variable"
    Assunes that values < -9E9, you dont want. This could be different in some circumstances.
    Arguments:

    filename -- a two element python list containing the name of the file and the target variable name
    dir -- directory file is in. Path can be in "filename" and None means no additional directory path needed.
    subset_function -- a function to be applied to each data set

    Returns:

    Y - a numpy array of the target variable
    X - an n-D numpy array of the feature variables 
    """
    
    dataset = nc.Dataset(filename[0])[filename[1]]
    dataset = np.array(dataset).flatten()
    
    if subset_function is not None:
        dataset = subset_function(dataset)
    
    return dataset

def read_all_data_from_netcdf(y_filename, x_filename_list, add_1s_columne = False, y_threshold = None, *args, **kw):
    """Read data from netCDF files 
    Assunes that values < -9E9, you dont want. This could be different in some circumstances.
    Arguments:

    y_filename -- a two element python list containing the name of the file and the target variable name
    x_filename_list -- a python list of filename containing the feature variables
    y_threshold -- if converting y into boolean, the threshold we use to spit into 0's and 1's
    add_1s_columne --useful for if using for regressions. Adds a variable of just 1's t rperesent y = SUM(a_i * x_i) + c
    see read_variable_from_netcdf comments for *arg and **kw.

    Returns:

    Y - a numpy array of the target variable
    X - an n-D numpy array of the feature variables 
    """
    Y = read_variable_from_netcdf(y_filename, *args, **kw)
    # Create a new categorical variable based on the threshold
    if y_threshold is not None:
        Y = np.where(Y >= y_threshold, 0, 1)
        #count number of 0 and 1 
        counts = np.bincount(Y)
        print(f"Number of 0's: {counts[0]}, Number of 1's: {counts[1]}")
    
    n=len(Y)
    m=len(x_filename_list)
    X=np.zeros([n,m])

    for i, filename in enumerate(x_filename_list):
        X[:, i]=read_variable_from_netcdf(filename)
    
    cells_we_want = np.array([np.all(rw > -9e9) for rw in np.column_stack((X, Y))])
    Y = Y[cells_we_want]
    X = X[cells_we_want, :]

    if add_1s_columne: 
        X = np.column_stack((X, np.ones(len(X)))) # add a column of ones to X 

    return Y, X

def read_data_from_csv(filename):
    """Read data from a file 
    """
    pass

def fit_linear_to_data(Y, X):
    """Use scikit learn to fit a linear equation.

    Arguments:

    Y -- numpy array of target variables 
    X -- numpy array of feature space variabels

    Returns.

    regr.coef_ -- regression coefficients
    Y_pred -- model prediction of the Y values

    **OR**
    regr -- return the regression model
    """


    regr = linear_model.LinearRegression()
    
    regr.fit(X, Y)

    Y_pred = regr.predict(X)

 

    #return regr.coef_, Y_pred

    return regr

def fit_logistic_to_data(Y, X):
    """Use scikit learn to fit a linear equation.

    Arguments:

    Y -- numpy array of target variables 
    X -- numpy array of feature space variabels

    Returns.

    logr.coef_ -- regression coefficients
    Y_pred -- model prediction of the Y values

    **OR**
    logr -- return the regression model
    """
    
   
    # Split data into train and test sets
    #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
    logr = LogisticRegression()
    logr.fit(X, Y)

    y_pred = logr.predict(X)

    return logr
   

if __name__=="__main__":
    dir = "D:/Doutorado/Sanduiche/research/maxent-test/driving_and_obs_overlap/AllConFire_2000_2009/"
    dir = "../ConFIRE_attribute/isimip3a/driving_data/GSWP3-W5E5-20yrs/Brazil/AllConFire_2000_2009/"
    y_filen = [dir +"GFED4.1s_Burned_Fraction.nc", "Date"]
    
    x_filen_list=[]
    x_filen_list.append([dir + "precip.nc", "variable"])    
    x_filen_list.append([dir + "tas.nc", "variable"]) 
    
    Y, X=read_all_data_from_netcdf(y_filen, x_filen_list, add_1s_columne = True,
                                   y_threshold = 0.01)
    
    #reg = fit_linear_to_data(Y, X)
    #plt.plot(Y, reg.predict(X), '.')
    
    logr = fit_logistic_to_data(Y, X)
    plt.plot(logr.predict_proba(X)[:,1],Y, '.')
    

    
    plt.show()
    print(Y)
    print(X)

