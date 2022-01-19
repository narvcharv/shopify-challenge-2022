from tkinter import Tk
from tkinter.filedialog import askopenfilename #lets user graphically select file
import pandas as pd #to read data from csv, use DataFrame
from scipy import stats #to remove outliers elegantly
import numpy as np #for absolute value function


def read_in(file_location):
    return pd.read_csv(file_location) #returns all data from .csv

def clean_data(dataset):
    dataset = dataset.drop(labels=['order_id', 'user_id', 'payment_method', 'created_at'], axis = 1) #sets index to shop_id, removes order and user id, payment method, time
    dataset = dataset.set_index('shop_id') #indexes by shop id
    dataset_no_outliers = dataset[(np.abs(stats.zscore(dataset['total_items'])) < 3)] #removes outlier transcations by checking if values are within 3 of std from mean
    dataset_no_outliers = dataset_no_outliers[(np.abs(stats.zscore(dataset_no_outliers['order_amount'])) < 3)]
    return dataset_no_outliers

def sort_by_store(dataset):
    dataset = dataset.rename(columns={"order_amount": "avg_order_amount", "total_items": "avg_total_items"})
    return dataset.groupby(['shop_id']).mean() #calculates averages of each data point by store
    

if __name__ == "__main__":
    print("Please select .csv:")
    Tk().withdraw()
    file_location = askopenfilename() #asks user for file location
    data = read_in(file_location) #reads data from given data set, stores to var data
    pd.set_option("display.max_rows", None, "display.max_columns", None) #makes all rows of pandas DataFrames print

    data = clean_data(data) #removes outliers, indexes by store
    aov = data.order_amount.mean() #classical aov
    print("AOV without outliers is:" , aov)
    avg_spend_per_pair = sum(data.order_amount) / sum(data.total_items) #total money spent over total pairs bought
    print("Average spend per pair is:" , avg_spend_per_pair)

    data_per_store = sort_by_store(data) #gets average of each data point by store
    data_per_store['shoe_price'] = data_per_store.avg_order_amount / data_per_store.avg_total_items #calculates shoe price at each store, adds to DataFrame
    data_per_store['relative_value'] = data_per_store.shoe_price / avg_spend_per_pair
    data_per_store['target_aov'] = data_per_store.relative_value * aov
    print("Data per shop:")
    print(data_per_store)