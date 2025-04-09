import os
import pickle

def to_pickle(file, directory):
    """
    Function to save file to pickle file
    
    Keyword arguments:
    file -- file to save
    derictory -- directory to save file in
    """
    with open(directory, 'wb') as handle:
        pickle.dump(file, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(directory):
    """
    Function to load file from pickle file
    
    Keyword arguments:
    derictory -- directory to load file from
    
    Returns:
    file -- loaded data from pickle file
    """
    with open(directory, 'rb') as handle:
        file = pickle.load(handle)
    return file