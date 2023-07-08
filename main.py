# Libraries
import pandas as pd
import numpy as np

# Proyect libraries
import functions as fn
import data

## Market Making Bot
ob = data.read_file(file_name = "orderbooks_05jul21.json", folder_route = "files/")
ob