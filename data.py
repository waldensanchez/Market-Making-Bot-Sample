
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import json
import pandas as pd

def read_file(file_name:str=None, folder_route:str=None) -> dict:
    """
    Read data from a local file

    Parameters
    ----------

    file_name: str, (default=None)
        name of the file to be read

    folder_route: str, (default=None)
        Relative or full path to the file

    Returns
    -------

    A json object with the contents of the file
    
    """
    
    # Opening JSON file
    if folder_route == None:
        f = open(file_name)
    else:
        f=open(folder_route+file_name)
    
    # Returns JSON object as a dictionary
    orderbooks_data=json.load(f)

    return orderbooks_data


def read_data(file_name:str=None, folder_route:str=None):
    """
    Read data from a local file

    Parameters
    ----------

    file_name: str, (default=None)
        name of the file to be read

    folder_route: str, (default=None)
        Relative or full path to the file

    Returns
    -------

    A DatFrame with the contents of the file
    
    """
    
    # Read PARQUET file
    if folder_route == None:
        parquet_data=pd.read_parquet(file_name+'.parquet')
    else:
        parquet_data=pd.read_parquet(folder_route+file_name+'.parquet')

    return parquet_data
