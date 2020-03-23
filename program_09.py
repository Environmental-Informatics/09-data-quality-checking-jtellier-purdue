#!/bin/env python
# This script was modified from program_09_template.py by Joshua Tellier on 3/18/2020 as part of the lab 9 assignment for ABE65100
#Joshua Tellier, Purdue University
import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed'] #NOTE: I changed the column names because .query() would not work when referencing column names with spaces
    global DataDF #added this line to make the dataframe visible in the variable explorer
    global ReplacedValuesDF #added this line to make the dataframe visible in the variable explorer
    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data","2. Gross Error","3. Swapped","4. Range Fail"], columns=colNames[1:]) #added additional indexed rows to make adding the values later easier
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""
    
    #add your code here
    for i in range(0,len(DataDF)-1): #checks for a specific value in each cell, then replaces it with nan if it meets the criteria
        for j in range(0,3):
            if DataDF.iloc[i,j] == -999:
                DataDF.iloc[i,j]=np.nan
    
    ReplacedValuesDF.iloc[0,0]=DataDF['Precip'].isna().sum() #counts the number of "nan" values for the referenced variable, then plugs it into the correct cell in the replacedvaluesdf
    ReplacedValuesDF.iloc[0,1]=DataDF['Max Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,2]=DataDF['Min Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,3]=DataDF['Wind Speed'].isna().sum()
    
    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    for i in range(0,len(DataDF)-1): #checks for a specific range in each cell for the precip variable, then replaces it with nan if outside the range
        if 0 > DataDF['Precip'].iloc[i] or DataDF['Precip'].iloc[i] > 25:
            DataDF['Precip'].iloc[i]=np.nan
    
    for i in range(0,len(DataDF)-1): #checks for a specific range in each cell for the maxtemp variable, then replaces it with nan if outside the range
        if -25 > DataDF['Max Temp'].iloc[i] or DataDF['Max Temp'].iloc[i] > 35:
            DataDF['Max Temp'].iloc[i]=np.nan
    
    for i in range(0,len(DataDF)-1): #checks for a specific range in each cell for the mintemp variable, then replaces it with nan if outside the range
        if -25 > DataDF['Min Temp'].iloc[i] or DataDF['Min Temp'].iloc[i] > 35:
            DataDF['Min Temp'].iloc[i]=np.nan
            
    for i in range(0,len(DataDF)-1): #checks for a specific range in each cell for the windspeed variable, then replaces it with nan if outside the range
        if 0 > DataDF['Wind Speed'].iloc[i] or DataDF['Wind Speed'].iloc[i] > 10:
            DataDF['Wind Speed'].iloc[i]=np.nan
    """ the following lines count the number of nan's that resulted from ONLY this second error check"""
    ReplacedValuesDF.iloc[1,0]=DataDF['Precip'].isna().sum() - ReplacedValuesDF.iloc[0,0]
    ReplacedValuesDF.iloc[1,1]=DataDF['Max Temp'].isna().sum() - ReplacedValuesDF.iloc[0,1]
    ReplacedValuesDF.iloc[1,2]=DataDF['Min Temp'].isna().sum() - ReplacedValuesDF.iloc[0,2]
    ReplacedValuesDF.iloc[1,3]=DataDF['Wind Speed'].isna().sum() - ReplacedValuesDF.iloc[0,3]
    
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    ReplacedValuesDF.iloc[2,1]=(DataDF['Min Temp'] > DataDF['Max Temp']).sum() #Here we record how many get swapped BEFORE swapping them to get the correct count
    ReplacedValuesDF.iloc[2,2]=(DataDF['Min Temp'] > DataDF['Max Temp']).sum()
    for i in range(0,len(DataDF)-1):
        if DataDF['Min Temp'].iloc[i] > DataDF['Max Temp'].iloc[i]: #if Tmin > Tmax
            hold = DataDF['Max Temp'].iloc[i] #put Tmax value into a placeholder variable
            DataDF['Max Temp'].iloc[i] = DataDF['Min Temp'].iloc[i] #supplant Tmax value with the Tmin value
            DataDF['Min Temp'].iloc[i] = hold #supplant Tmin value with the old Tmax value (that was in the placeholder)
    
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    ReplacedValuesDF.iloc[3,1]=(DataDF['Max Temp'] - DataDF['Min Temp'] > 25).sum() #Here we count the number of days in which the temperature range was greater than 25 degrees
    ReplacedValuesDF.iloc[3,2]=(DataDF['Max Temp'] - DataDF['Min Temp'] > 25).sum() 
    for i in range(0,len(DataDF)-1):
        if DataDF['Max Temp'].iloc[i] - DataDF['Min Temp'].iloc[i] > 25: #if the difference between tmax & tmin > 25
            DataDF['Max Temp'].iloc[i] = np.nan #replace tmax w/ nan
            DataDF['Min Temp'].iloc[i] = np.nan #replace tmin w/ nan

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
"""Done modifying functions, now I will work on the rest of the lab
i.e. creating plots and file output"""
import matplotlib.pyplot as plt
#First, we import the data, assign the RAW data to a new frame so that we can plot them side-by-side, and then QC the data
ReadData('DataQualityChecking.txt')
RawData = DataDF.copy()
Check01_RemoveNoDataValues(DataDF,ReplacedValuesDF)
Check02_GrossErrors(DataDF,ReplacedValuesDF)
Check03_TmaxTminSwapped(DataDF,ReplacedValuesDF)
Check04_TmaxTminRange(DataDF,ReplacedValuesDF)

""" Precipitation comparison figure"""
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
ax1.scatter(x=DataDF.index.values, y=RawData['Precip'], s=3, c='b', marker='s', label="Raw Data")
ax1.scatter(x=DataDF.index.values, y=DataDF['Precip'], s=3, c='r', marker='o', label='QC Data')
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.legend(loc = 'lower left')
plt.savefig('Precipitation_Raw_vs_QC.pdf')
plt.close()

"Max temp comparison figure"""
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.scatter(x=DataDF.index.values, y=RawData['Max Temp'], s=3, c='b', marker='s', label="Raw Data")
ax2.scatter(x=DataDF.index.values, y=DataDF['Max Temp'], s=3, c='r', marker='o', label='QC Data')
plt.xlabel('Date')
plt.ylabel('Maximum Temperature (degrees Celsius)')
plt.legend(loc = 'lower left')
plt.savefig('Maxtemp_Raw_vs_QC.pdf')
plt.close()

"""Min temp comparsion figure"""
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.scatter(x=DataDF.index.values, y=RawData['Min Temp'], s=3, c='b', marker='s', label="Raw Data")
ax2.scatter(x=DataDF.index.values, y=DataDF['Min Temp'], s=3, c='r', marker='o', label='QC Data')
plt.xlabel('Date')
plt.ylabel('Minimum Temperature (degrees Celsius)')
plt.legend(loc = 'lower left')
plt.savefig('Mintemp_Raw_vs_QC.pdf')
plt.close()

"""Wind speed comparison figure"""
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
ax2.scatter(x=DataDF.index.values, y=RawData['Wind Speed'], s=3, c='b', marker='s', label="Raw Data")
ax2.scatter(x=DataDF.index.values, y=DataDF['Wind Speed'], s=3, c='r', marker='o', label='QC Data')
plt.xlabel('Date')
plt.ylabel('Wind Speed (m/s)')
plt.legend(loc = 'upper right')
plt.savefig('Windspeed_Raw_vs_QC.pdf')
plt.close()

""" Data output """
DataDF.to_csv('Quality_Checked_Data.txt', sep='\t', index=True) #writing the corrected data to a tab-delimited text file
ReplacedValuesDF.to_csv('ReplacedValueInfo.txt', sep='\t', index=True) #writing the correctio info to a tab-delimited text file
