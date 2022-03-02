import pandas as pd
import numpy as np

######-------------- Basics --------------###### # <editor-fold>

# (First, show difference from jupyter notebook)

# My environment includes the interactive console, variables, functions..
x = 10
print(x)

my_list = [1, 2, 3, 'Hertz', 'lab']

print(my_list[0])

my_family_dict = {'Omer': 1, 'Freddie': 4, 'Nadav': 33}

# </editor-fold>

######-------------- Basic structure: Series --------------###### # <editor-fold>

''' Structure that is a single ordered column of named values:
 Row label + value '''

''' Initialization ''' # <editor-fold>
patient_reads = pd.Series([11.8, 10.1, 14.4, np.nan, 12.9], # could have used None as well
                          index=['p1', 'p2', 'p3', 'p4', 'p5'])
print(patient_reads)

# Get index labels
print(patient_reads.index)

# Get values
print(patient_reads.values)

### Define series name
patient_reads.name = 'Hemoglobin'
print(patient_reads.name)

# We can also define name in initialization
# (helpful if we want to add / transform series to dataframe)
patient_reads = pd.Series([11.8, 10.1, 14.4, np.nan, 12.9],
                          index=['p1', 'p2', 'p3', 'p4', 'p5'],
                          name='Hemoglobin')

# What if we don't define an index?
reads_no_ind = pd.Series([11.8, 10.1, 14.4, np.nan, 12.9])
print(reads_no_ind.index) # now index label = position
print(list(reads_no_ind.index))

### Initialization from dict
patient_reads_extra = pd.Series({'p6': 13.2, 'p7': 15.3, 'p8': np.nan})
print(patient_reads_extra)

### Append
all_reads = patient_reads.append(patient_reads_extra)
print(all_reads)

# </editor-fold>

''' Get specific items - slicing ''' # <editor-fold>
# by integer location (what we are used to call 'index' in a list)
print(patient_reads.iloc[0])
print(patient_reads.iloc[2:4])

# by label (i.e. pandas index)
print(patient_reads.loc['p1'])
print(patient_reads.loc['p1':'p3'])
print(patient_reads.loc[['p1', 'p4', 'p5']])

# # another way that is not implicit -
# print(patient_reads['p1'])
# print(patient_reads[0]) # first checks if label 0 exists.
#                         # if not, looks for item in integer position 0.
#                         # So it's better not to use this way
#                         # with ints if you have ints as indexes.
#                         # it can create a mixup.
#                         # (Unless index = position as in next example.)

# </editor-fold>

''' NaNs ''' # <editor-fold>
all_reads_na = all_reads.isna() # same as .isnull().  # opposite of .notna() / .notnull()
print(all_reads_na)

# Drop NANs
all_reads_no_na = all_reads.dropna(inplace=False)
# inplace = True - changes the object itself! Function returns None
# inplace = False - function returns a changed object, without changing the original.
# all_reads.dropna(inplace=True)

# Fill NANs with a value
all_reads.fillna(-1000)

# </editor-fold>

''' Slicing by condition - boolean ''' # <editor-fold>
over_13_ind = all_reads > 13 # get boolean for each row according to condition
print(over_13_ind)

print(all_reads[over_13_ind]) # use booleans to get a subset of the data

print(~over_13_ind) # ~ = not
print(all_reads[~over_13_ind])

# </editor-fold>

''' Some more functions ''' # <editor-fold>
print(all_reads.to_dict())
print(all_reads.sum())
print(all_reads.mean())
print(all_reads.min())
print(all_reads.max())
print(all_reads.median())

# mean of subset of the data
print(all_reads[over_13_ind].mean())

# </editor-fold>

''' Numpy or other functions ''' # <editor-fold>
all_reads_sqrt = np.sqrt(all_reads)

# numpy functions support pd.Series. If they weren't, this would work:
all_reads_sqrt = all_reads.apply(np.sqrt)

all_reads_calc = all_reads - all_reads.mean()

# </editor-fold>

# more in the API documentation:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

# </editor-fold> # Series section fold

######-------------- DataFrame --------------###### # <editor-fold>

# A collection of multiple pd.Series that share an index -
# a 2-dimensional tabular structure

''' Initialization ''' # <editor-fold>
df = pd.DataFrame({'Hgb': [13.2, 10.1, 14.4, 11.8, 12.9],
                   'Age': [44, 25, 14, 33, 39],
                   'Gender': ['M', 'F', 'M', 'M', 'F']},
                  index=['p1', 'p2', 'p3', 'p4', 'p5'])
print(df)
print(df.index)
print(df.columns)

### another option (and there are more...)
examp_data = [[13.2, 44, 'M'],
              [10.1, 25, 'F'],
              [14.4, 14, 'M'],
              [11.8, 33, 'M'],
              [12.9, 39, 'F']]

df = pd.DataFrame(examp_data,
                  index=['p1', 'p2', 'p3', 'p4', 'p5'],
                  columns=['Hgb', 'Age', 'Gender'])

# </editor-fold>

''' Dataframe dimensions ''' # <editor-fold>
print(df.shape)

# How can I get number of rows, number of columns?

# </editor-fold>

''' Slicing ''' # <editor-fold>

# Slicing columns
df_age = df['Age'] # slice entire column
print(type(df_age)) # single column = pd.Series!

# print(patient_df['Age', 'Hgb'])
print(df[['Age', 'Hgb']]) # for multiple columns, use names list
print(type(df[['Age', 'Hgb']]))

# Slicing rows - data[start:stop]
print(df[0:2]) # only works with int - row position
# It's better not to use this, may be confusing.

# Like in series:
# iloc - get by row position
# loc - get by row label

print(df.iloc[0, 1]) # int
print(df.iloc[0:3, 0:2]) # int

print(df.loc['p1', 'Age']) # label
print(df.loc[['p1', 'p4'], ['Hgb', 'Gender']]) # label
print(df.loc['p1':'p4', 'Age':]) # label   # same as patient_df.loc['p1':'p4']

# </editor-fold>

''' Replace values ''' # <editor-fold>
df.iloc[0, 1] = 888
df.iloc[0:2, 1] = [99, 100]
df.loc['p2', ['Gender', 'Hgb']] = ['Unknown', 1.11111]

# With .loc/.iloc, you will modify the original
# DataFrame and not a copy of it...

# </editor-fold>

''' View vs. Copy ''' # <editor-fold>
df_age = df['Age']

df_age.loc['p1'] = 5000
# SettingWithCopyWarning warning! why?


df_age2 = df['Age'].copy()

df_age2.loc['p2'] = 10000 # Now the original won't change

# Back to changing values -

# Chaining:
print(df[['Hgb', 'Age']][0:1]) # get df with 'Hgb' and 'Age', then get value of row 0


'''
Value assignment to an existing pd.DataFrame:
Assigning to the product of chained indexing has
inherently unpredictable results. 
Chained indexing sometimes creates a copy, and sometimes
just creates a view (like a pointer to the original DataFrame). 
When selecting a single column from a DataFrame, 
it creates a view and not a copy.
But the rules for this are a bit ambiguous (see link 1 which contains an explanation from one of Pandas writers)
To make an assignment, it's better not to use chained indexing.
Use .loc in a single call.

More on that:
https://stackoverflow.com/questions/23296282/what-rules-does-pandas-use-to-generate-a-view-vs-a-copy
https://medium.com/dunder-data/selecting-subsets-of-data-in-pandas-part-4-c4216f84d388
'''

# Don't use chaining to modify values!
# Usually chaining returns a copy so the original
# will not change. (SettingWithCopyWarning warning: https://realpython.com/pandas-settingwithcopywarning/)
# Use .loc/.iloc

df[df['Hgb'] > 10]['Age'] = 99 # Don't do this!!! or similar to this


# </editor-fold>

''' Manipulating index ''' # <editor-fold>

df.index[2]
# what if I want to change the row label?
# df.index[2] = 'p20' # won't work
df.rename(index={'p3': 'p20'}, inplace=True)
print(df)

print(df.set_index('Hgb')) # make column values into index. notice that default for inplace is False
print(df)

df.index = [1, 2, 3, 4, 5] # change all indices
print(df)

df.index = 'p' + df.index.astype(str) # back to original       can also do .to_series()
print(df)

# </editor-fold>

''' Drop ''' # <editor-fold>

df.drop(['p3'], inplace=False) # default - drops row
# df.drop(['Gender'], inplace=True) # Why won't it work?

# write explicitly - index / columns
df.drop(index=['p2'], inplace=False)
df.drop(columns=['Gender'], inplace=False)
print(df)

# </editor-fold>

''' Simple calculations ''' # <editor-fold>

df['Hgb+100'] = df['Hgb'] + 100
print(df)

df['Hgb-adjusted'] = df['Hgb'] - df['Hgb'].min()
print(df)

df['Hgb*Age'] = df['Hgb'] * df['Age']
print(df)

# </editor-fold>

''' Value counts ''' # <editor-fold>

df_gender_count = df['Gender'].value_counts()
print(df_gender_count)

# </editor-fold>

''' Functions ''' # <editor-fold>

print(df.sum())

print(df.sum(axis=1))

df_log = np.log(df[['Age', 'Hgb']]) # numpy functions - can execute over entire column

# More on example 2

# </editor-fold>

''' Add single row ''' # <editor-fold>

df_log.loc['p10'] = [1.5 ,2]
df_log.loc['p11'] = {'Age': 4,'Hgb': 5}
print(df_log)

# </editor-fold>

''' Sort by column ''' # <editor-fold>

df.sort_values(by='Age', ascending=False, inplace=True)

# </editor-fold>

''' Join ''' # <editor-fold>

# I'd like to add the 'Gender' column from df to df_log.
df_log = df_log.join(df['Gender'])
# fix nans?

# Now I'd like to add the log 'Hgb' from df_log to df.
df = df.join(df_log['Hgb'])

df2 = df.join(df_log, rsuffix='_log', how='outer')

# </editor-fold>

# </editor-fold> # pd.Dataframe fold