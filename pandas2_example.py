import pandas as pd
import numpy as np


''' @ 1. Import from excel file ''' # <editor-fold>
path = 'C:/Users/liel-/Dropbox/PyCharm/PycharmProjectsNew/Python-classes/'

df = pd.read_excel(path + 'example_data_FLU09.xlsx',
                   sheet_name='FLU09 plasma',
                   index_col='ID')

# from csv - pd.read_csv(...)
# from tsv - pd.read_csv(..., delimiter='\t')

# </editor-fold>

''' @ Importing from the code folder: ''' # <editor-fold>
''' Place the file in the folder where your code is at,
so that python will recognize it without having to write
the entire path.
If you're working with the pycharm console, you may have
to manually change the working directory to the
folder where your code is at: '''


import os
print(os.getcwd()) # this is the current working directory of the environment
os.chdir(path) # here we are changing it

df = pd.read_excel('ex11_FLU09_data.xlsx',
                   sheet_name='FLU09 plasma',
                   index_col='ID')

# </editor-fold>

''' 2. Let's view our dataframe ''' # <editor-fold>

# Open in SciView, or:
print(df.head())

# </editor-fold>

''' 3. Are indices unique? ''' # <editor-fold>

print(df.index.is_unique) #

# </editor-fold>

''' 4. How many subjects are there? ''' # <editor-fold>
print(df.shape)
# </editor-fold>

''' We were told we are not allowed to use data 
of subjects 3200, 3388! '''

### 5. Lets look at subject 3200 data. how? # <editor-fold>
df.loc[3200] # looks for 3200 in the index
df.loc[3200, :] # same

# </editor-fold>

#### 6. now, let's delete 3200, 3388 # <editor-fold>
df.drop(index=[3200, 3388], inplace=True)
print(df.shape)
# df.loc[3200] # what will happen?

# </editor-fold>

''' 7. Add column age in years, & delete old ''' # <editor-fold>
df['Age'] = df['Age_months'] / 12
df.drop(columns=['Age_months'], inplace=True)

# </editor-fold>

''' 8. Rename 'Influenza_test_result_positive' to 'Flu_positive' ''' # <editor-fold>
df = df.rename({'Influenza_test_result_positive': 'Flu_positive'}, axis=1)
df = df.rename(columns={'Influenza_test_result_positive': 'Flu_positive'}) # same

# </editor-fold>

''' 9. Let's add '_Plasma' to all cytokine column names. ''' # <editor-fold>

# Let's create a dict of all cytokine original col names (keys) + new names (vals).
cy_cols_new_names = {}
for name in df.columns:
    if name not in ['Gender', 'Flu_positive', 'Age']:
        cy_cols_new_names[name] = name + '_Plasma'

# Change the names
df.rename(cy_cols_new_names, axis=1, inplace=True) # axis 1 = columns, axis 0 = rows

# </editor-fold>

''' 10. Assign the Gender column value counts to a new variable.
Then, using this variable, calculate the percentage of Females 
out of all patients in df (float between 0-100). ''' # <editor-fold>

df_gender_count = df['Gender'].value_counts()
print(df_gender_count)

df_females_per  = 100 * df_gender_count['Female'] / df_gender_count.sum()
print(df_females_per)

# </editor-fold>

''' @ 11. Manipulating with functions: log transform values ''' # <editor-fold>

# Create df_log - a copy of df in which all cytokine columns are log transformed (using np.log10)
df_log = df.copy() # if we'd do df_log = df, df_log will just point to df!
col_names_cy = list(cy_cols_new_names.values())
df_log[col_names_cy] = np.log10(df[col_names_cy])

# make sure transformation was done correctly
print(df_log.loc[3202, 'EGF_Plasma'])
print(np.log10(df.loc[3202, 'EGF_Plasma']))
print(df_log.loc[3202, 'EGF_Plasma'] == np.log10(df.loc[3202, 'EGF_Plasma']))

np.allclose(np.log10(df[col_names_cy]),
            df_log[col_names_cy],
            equal_nan=True)
# read about assertion in python.

# </editor-fold>


''' Analyzing a subset of rows using condition ''' # <editor-fold>

# Get booleans for indices, by the condition that 'Flu_positive' == True.

# ind_sick = df_log.Flu_positive == True # better not to use this. what if you have a column named sum, mean?
ind_sick = df_log['Flu_positive'] == True

# Looking at the 'Flu_positive' of the sick subjects only
print(df_log.loc[ind_sick, 'Flu_positive'])

# Gender counts of the sick subjects
print(df_log.loc[ind_sick, 'Gender'].value_counts())

# Mean IP10_Plasma of the subjects negative with influenza
print(df.loc[~ind_sick, 'IP10_Plasma'].mean())

# Mean IP10_Plasma of the subjects positive with influenza
print(df.loc[ind_sick, 'IP10_Plasma'].mean())

# Change specific values by indices
df_log.loc[ind_sick, 'Flu_positive'] = 1
df_log.loc[~ind_sick, 'Flu_positive'] = 0

# Get list of indices by condition
ind_numbers_sick = df_log[ind_sick].index

# </editor-fold>

''' @ Change values using map and dictionary + unique ''' # <editor-fold>

df_log['Flu_positive'].unique()

df_log['Flu_positive'] = df_log['Flu_positive'].map({1: True, 0: False}) # map - only for series

# </editor-fold>

''' @ Sort by column ''' # <editor-fold>

df_log.sort_values(by='Age', ascending=False, inplace=True)

# </editor-fold>

''' @ Write df to file ''' # <editor-fold>

df_log.to_csv(path + 'df_log_21_06_03.csv')

df_log.to_excel(path + 'df_log_21_06_03.xlsx')

# </editor-fold>

''' @ Join ''' # <editor-fold>

df_log['log EGF+GRO'] = df_log['EGF_Plasma'] + df_log['GRO_Plasma']

df = df.join(df_log['log EGF+GRO'])

df = df.join(df_log['EGF_Plasma'], rsuffix='_log')

# </editor-fold>

''' @ Apply functions ''' # <editor-fold>

def magic_calc(num):
    log_num = np.log10(num)
    inverse_num = 1 / num
    return log_num / np.sqrt(inverse_num)

df['magic EGF'] = df['EGF_Plasma'].apply(magic_calc)

df['1/EGF'] = df['EGF_Plasma'].apply(lambda value: 1/value)

df['EGF calc'] = df['EGF_Plasma'].apply(lambda value: 10 if value > 10 else 4)

df['EGF GRO calc'] = df.apply(lambda row: row['EGF_Plasma'] + 1/row['GRO_Plasma'], axis=1)

def EGF_adjust_by_gender_age(row):
    if row['Gender'] == 'Female':
        result = row['EGF_Plasma'] / row['Age']
    else:
        result = (1 + row['EGF_Plasma']) / (0.7 * row['Age'])

    return round(result, 4)


df['EGF_adjusted'] = df.apply(lambda row: row['EGF_Plasma'] + 1/row['GRO_Plasma'], axis=1)

# </editor-fold>


# group by

df.shape
df[df['Flu_positive'] == True]