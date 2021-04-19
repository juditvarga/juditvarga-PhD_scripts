# -*- coding: utf-8 -*-
"""
Created on Thu May 21 19:21:06 2020

@author: vargajv
"""

#%% DF 1: get yearly geosoc papers

def get_yearly_geosoc_ut_count(uts_df):
    
    '''
    Argument:
        
        uts_df: datafarame which contains at least 2 variables:
                
            'UT': uts of all geosocial papers
            'pub_year': publication year of UT
            
    Output:
        
        yearly_total_geosoc_df: df with 2 variables
        
            'pub_year':publication year
            'geosoc_ut_count': number of geosocial papers published in that year
    '''
    
    # import packages
    import pandas as pd

    # create dataframe
    yearly_ut = uts_df[['UT', 'pub_year']].drop_duplicates(subset = 'UT')
    yearly_total_geosoc_df = pd.DataFrame(yearly_ut.groupby('pub_year').count()).reset_index()
    yearly_total_geosoc_df.rename(columns = {'UT' : 'geosoc_ut_count'}, inplace = True)

    #print(yearly_total_geosoc_df.shape) # (12, 2)
    #print(yearly_total_geosoc_df.columns) # Index(['pub_year', 'geosoc_ut_count'], dtype='object')
    #print(yearly_total_geosoc_df.head(5)) # (2732, 2)
    
    return(yearly_total_geosoc_df)
    
#%%
#%% DF 2: count *yearly* geosoc paper count for each journal ==
# count *yearly* number of papaers published in each journal in my small dataset 

def get_yearly_geosoc_count_journals(uts_df):
    
    '''
    Argument:
        
        uts_df: datafarame which contains at least 3 variables:
                
            'UT': uts of all geosocial papers
            'pub_year': publication year of UT
            'CWTS_SO_NO': CWTS identifier of journals
            
    Output:
        
        geosoc_journals_yearly_counter_df: df with columns
        
            'CWTS_SO_NO': CWTS id of journals
            'geosoc_ut_count_<DATE>' : geosoc ut count of journals for specific years    
            
    '''
    
    # import packages
    import pandas as pd

    # create dataframe
    
    my_journals_yearly_df = uts_df[['pub_year', 'CWTS_SO_NO', 'UT']].drop_duplicates(subset = 'UT')
    #print(my_journals_yearly_df.shape) # (2732, 3)

    #print(min(my_journals_yearly_df.pub_year)) # 2008

    my_journals_yearly_counter = pd.DataFrame(my_journals_yearly_df.groupby(['pub_year', 'CWTS_SO_NO'])['UT'].count())
    my_journals_yearly_counter.reset_index(inplace = True)

    my_journals_yearly_counter.sort_values(by = 'UT', ascending = False, inplace = True)
    #print(my_journals_yearly_counter.head(5))

    #print(my_journals_yearly_counter.shape)
    #print(len(list(set(list(my_journals_yearly_counter['CWTS_SO_NO']))))) 
    
    my_journals_yearly_counter['pub_year'] = my_journals_yearly_counter['pub_year'].apply(lambda x: 'geosoc_ut_count_' + str(int(x)))

    # create wide df from long df

    geosoc_journals_yearly_counter_df = my_journals_yearly_counter.pivot(index='CWTS_SO_NO', columns='pub_year', values='UT')
    geosoc_journals_yearly_counter_df.reset_index(inplace = True)
    geosoc_journals_yearly_counter_df.sort_values(by = 'geosoc_ut_count_2019', ascending = False, inplace = True)

    # check df shapes

    #print(geosoc_journals_yearly_counter_df.shape)
    #print(geosoc_journals_yearly_counter_df.head(5))
    #print(geosoc_journals_yearly_counter_df.columns)
    
    return(geosoc_journals_yearly_counter_df)
    
#%%
#%% DF 3: yearly total ut count for each journal in my dataset from WOSdata

# get TEMPORAL data about all journals' publication count in the whole WOSKB databse 
# as opposed to my small dataset

def get_yearly_total_ut_all_journals(mydir):
    
    '''
    Argument:
        
        mydir: directory with data about journals' yearly ut count:
                these need to be separate dataframes for each year            
            
    Output:
        
        
              
    '''
    
    # import packages
    
    import os
    import pandas as pd

    # read data about yearly ut ccounts for each journal into a dictionary
    
    all_journal_counter_df_dict = {}

    for filename in os.listdir(mydir):
        if filename.endswith(".csv"): 
            try:
                # print(os.path.join(directory, filename))
                journal_csv_filename = mydir + '/' + filename
                #print(journal_csv_filename)
                journal_df = pd.read_csv(journal_csv_filename, sep = '\t', header = 0)
                year = filename[-8:-4]
                #print(year)
                # print(filename)
                # print(edge_df.columns)
                journal_df.columns = ['ut_count', 'cwts_so_no']
                journal_df = journal_df[~journal_df['ut_count'].str.contains("rows")]
                journal_df = journal_df[~journal_df['ut_count'].str.contains("Completion")]
                all_journal_counter_df_dict[year] = journal_df
                # print(edge_df.shape)
            except:
                print('no files found')
                continue

    # rename ut 'ut_count' column to also include the year

    for key, value in all_journal_counter_df_dict.items():
        col_name = 'all_ut_count_{}'.format(key)
        value.columns = [col_name, 'CWTS_SO_NO']
        #print(value.head(5)) 
   
    # create 1  dataframe with yearly ut counts for all journals  in the WOSKB database
    
    # merge the yearly ut count dataframes
    
    first = True

    for key, value in all_journal_counter_df_dict.items():
        if first:
            yearly_total_ut_all_journals_df = value
            first = False
        else:
            yearly_total_ut_all_journals_df = yearly_total_ut_all_journals_df.merge(value, on='CWTS_SO_NO', how = 'outer')

    #print(yearly_total_ut_all_journals_df.head())
    #print(yearly_total_ut_all_journals_df.shape) # (14424, 13)

    # check if any journals are dupliatced in the final dataset - no they aren't

    yearly_total_ut_all_journals_df.drop_duplicates(subset = 'CWTS_SO_NO', inplace = True)
    
    return(yearly_total_ut_all_journals_df)

#%% PART 1 OF categorise journals into disciples
# GET joined SC for SOs - requirement of categorisation according to disciplines
    
def join_SC(uts_df):
    
    '''
    Argument:
        
         uts_df: datafarame which contains at least 3 variables:
                
            'CWTS_SO_NO'
            'SC'
            'SO'
            
    Output:
        
        SO_SC_joined_df: a dataframe with 3 columns:
            
            'CWTS_SO_NO', 
            'SC', 
            'SO'
    '''
    
    # import packages
    
    import pandas as pd
    
    # get SC s for SO s

    CWTS_SO_NO_SC_df = uts_df[['CWTS_SO_NO', 'SC']]
    nrows_1 = CWTS_SO_NO_SC_df.shape[0]
    
    if CWTS_SO_NO_SC_df.SC.isnull().values.any() == True:
        print('\nTHERE ARE MISSING VALUES IN SC, the columns with missing value are being deleted')
        CWTS_SO_NO_SC_df.dropna(inplace = True) # otherwise it throws error
        
        nrows_2 = CWTS_SO_NO_SC_df.shape[0]
        
        print('\nnumber of rows deleted: ' + str((nrows_1 - nrows_2)) + '\n')

    # join SCs for each journals

    SO_SC_joined = pd.DataFrame(CWTS_SO_NO_SC_df.groupby('CWTS_SO_NO')['SC'].apply(lambda x: '; '.join(x))).reset_index()
    SO_SC_joined.rename(columns = {'SC' : 'SC_joined'}, inplace = True)
    #print(SO_SC_joined.shape) # 
    #print(SO_SC_joined.head(5)) 

    # get SO

    CWTS_SO_NO_SO_df = uts_df[['CWTS_SO_NO', 'SO']].drop_duplicates()

    SO_SC_joined_df = pd.merge(SO_SC_joined, 
                               CWTS_SO_NO_SO_df,
                               on = 'CWTS_SO_NO',
                               how = 'left')
    # check df shape
    #print(SO_SC_joined.shape) # (1069, 2)

    # print(len(list(set(SO_SC_joined['CWTS_SO_NO']))))
    #print(SO_SC_joined.columns)
    
    return(SO_SC_joined_df)
    
#%%
    
def create_all_so_sc_df(df_1_path, df_2_path, df_3_path):
    
    '''
    Arguments
    
    Outputs
    '''
    
    import pandas as pd
    
    list_of_dfs = [] # list which contains all 3 dataframes
    list_of_dfs_no_na = [] # list which contains all 3 dataframes. with NAN deleted
    
    # laod data whcih contains SO and CWTS_SO_NO
    all_SO_df = pd.read_csv(df_1_path, sep = '\t')
    list_of_dfs.append(all_SO_df)
    
    # laod data whcih contains cwts_so_no, cwts_sc_no, weight
    SO_NO_SC_NO_df = pd.read_csv(df_2_path, sep = '\t')
    list_of_dfs.append(SO_NO_SC_NO_df)
    
    # # laod data whcih contains CWTS_SC_NO, SC
    SC_NO_SC_df = pd.read_csv(df_3_path, sep = '\t')
    list_of_dfs.append(SC_NO_SC_df)
    
    # check dfs
    
    for df in list_of_dfs:
        #print(df.head(5))
        #print(df.shape) # (19935, 2)
        #print(df.isna().sum())
        
        # drop na
        df_2 = df.dropna()
        
        # add non na df to list
        list_of_dfs_no_na.append(df_2)
        
    # change data type of cwys_sc_no so I can merge dataframes
    # have to do 2 rounds because some column names are capitals, others are lower case
    counter = 0
    for df in list_of_dfs_no_na:
        print(counter)
        try:
           df.cwts_sc_no = df.cwts_sc_no.astype(int)
           print('changed var type 1')
        except:
            print('')
            
        counter += 1
   
    counter_2 = 0       
    for df in list_of_dfs_no_na:
        print(counter_2)
        try:
           df.CWTS_SC_NO = df.CWTS_SC_NO.astype(int)
           print('changed var type 2')
        except:
            print('')
            
        counter_2 += 1
        
    
    # merge dataframes
    
    merged_1 = pd.merge(list_of_dfs_no_na[0], list_of_dfs_no_na[1], 
                        left_on = 'CWTS_SO_NO', right_on = 'cwts_so_no',
                        how = 'left')
    
    merged_2 = pd.merge(merged_1, list_of_dfs_no_na[2], 
                        left_on = 'cwts_sc_no', right_on = 'CWTS_SC_NO',
                        how = 'left')
    
    return(merged_2)
    
    
#%% DF 4: GET YEARLY GEOSOC UT COUNT FOR EACH DISCIPLINARY GROUP

def disc_yearly_ut_counter(SO_SC_cat_df, journals_yearly_counter_df):
    
    '''
    Arguments:
        
         SO_SC_cat_df: datafarame which contains at least the following variables:
                
            'CWTS_SO_NO'
            'SO'
            + disciplinary categories columns
            
            e.g. output by SC_categorise_for_timeline_with_names function 
            
       journals_yearly_counter_df: a dataframe which contains at least the following columns:
           
           'CWTS_SO_NO'
           + columns which specifcy how many papers were published in these journals each year
            
    Output:
        
        disc_yearly_counter_dict: a dictionary , whose
            
            keys = disciplinary categores
            items = yearly ut counter dataframes 
    '''

    # geosoc_journals_yearly_counter_df

    import pandas as pd

    # change column type to make sure it works when merging
    journals_yearly_counter_df.CWTS_SO_NO = journals_yearly_counter_df.CWTS_SO_NO.astype(float)

    # 1.
    # create dictionary where keys are disciplinary categories
    # and items are dfs which include ['CWTS_SO_NO']

    disciplines_journals_dict = {} 

    for column in SO_SC_cat_df.columns[3:]:
        disciplines_journals_dict[column] = SO_SC_cat_df.loc[SO_SC_cat_df[column] == 1]

    # remove unnecessary columns

    for key, item in disciplines_journals_dict.items():
        #print(key)
        item.drop(columns = ['SC_joined', 'computational', 'social', 'SO',
                             'multi_inter', 'all_geo', 'phys_geo', 'non_phys_geo',
                             'non_cat', 'only_social',
                             'only_non_phys_geo', 'only_computational', 'comp_soc',
                             'comp_non_phys_geo', 'health', 'biol_env',
                             'arts_humanities', 'econ_bus_trans'], inplace = True)
        #print(item.shape)


   
    # 2.     
    # create dictionary where keys are disciplinary categories
    # and items are yearly journal counters

    disc_journals_geosoc_yearly_counter_dict = {} 

    for key, item in disciplines_journals_dict.items():
        #print(item.shape)
        
        # change column type to make sure it works when merging
        item.CWTS_SO_NO = item.CWTS_SO_NO.astype(float)
        
        merged_df = pd.merge(journals_yearly_counter_df,
                             item,
                             on = 'CWTS_SO_NO', 
                             how = 'right')
    
        disc_journals_geosoc_yearly_counter_dict[key] = merged_df
    
    # check
    
    #for key, item in disc_journals_geosoc_yearly_counter_dict.items():
        #print(item.columns)
        #print(item.shape)


        
    # 3.     
    # create dictionary where keys are disciplinary categories
    # and items are yearly geosoc ut count (df)
    disc_yearly_counter_dict = {} 

    for key, item in disc_journals_geosoc_yearly_counter_dict.items():
        item_2 = item.drop(columns = ['CWTS_SO_NO'])
        #print(item_2.columns)
        item_2.fillna(0, inplace = True) # fillna
        item_2 = item_2.astype('int32') # change data type to inteher so that I can for sure sum
        disc_yearly_counter = pd.DataFrame(item_2.sum(axis = 0)).reset_index()
        #print(disc_yearly_counter)
        disc_yearly_counter.columns = ['year', 'ut_count'] # rename columns
    
        # get year as integer
        disc_yearly_counter['year'] = disc_yearly_counter['year'].apply(lambda x: int(x.split('_')[-1]))
    
        # save df
        disc_yearly_counter_dict[key] = disc_yearly_counter
    
    
    # check
    #for key, item in disc_geosoc_yearly_counter_dict.items():
        #print(type(item))
        #print(item.columns)
        #print(key)
        #print(item)
        
    return(disc_yearly_counter_dict)
    
#%%#%% DF 4: GET YEARLY GEOSOC UT COUNT FOR EACH DISCIPLINARY GROUP

def cumulative_yearly_ut_counter(journals_yearly_counter_df):
    
    '''
    Arguments:
            
       journals_yearly_counter_df: a dataframe which contains at least the following columns:
           
           'CWTS_SO_NO'
           + columns which specifcy how many papers were published in these journals each year
            
    Output:
        
    '''

    # geosoc_journals_yearly_counter_df

    import pandas as pd

    # change column type to make sure it works when merging
    journals_yearly_counter_df.CWTS_SO_NO = journals_yearly_counter_df.CWTS_SO_NO.astype(float)

    # 1.
    # create dictionary where keys are disciplinary categories
    # and items are dfs which include ['CWTS_SO_NO']

    disciplines_journals_dict = {} 

    for column in SO_SC_cat_df.columns[3:]:
        disciplines_journals_dict[column] = SO_SC_cat_df.loc[SO_SC_cat_df[column] == 1]

    # remove unnecessary columns

    for key, item in disciplines_journals_dict.items():
        #print(key)
        item.drop(columns = ['SC_joined', 'computational', 'social', 'SO',
                             'multi_inter', 'all_geo', 'phys_geo', 'non_phys_geo',
                             'non_cat', 'only_social',
                             'only_non_phys_geo', 'only_computational', 'comp_soc',
                             'comp_non_phys_geo', 'health', 'biol_env',
                             'arts_humanities', 'econ_bus_trans'], inplace = True)
        #print(item.shape)


   
    # 2.     
    # create dictionary where keys are disciplinary categories
    # and items are yearly journal counters

    disc_journals_geosoc_yearly_counter_dict = {} 

    for key, item in disciplines_journals_dict.items():
        #print(item.shape)
        
        # change column type to make sure it works when merging
        item.CWTS_SO_NO = item.CWTS_SO_NO.astype(float)
        
        merged_df = pd.merge(journals_yearly_counter_df,
                             item,
                             on = 'CWTS_SO_NO', 
                             how = 'right')
    
        disc_journals_geosoc_yearly_counter_dict[key] = merged_df
    
    # check
    
    #for key, item in disc_journals_geosoc_yearly_counter_dict.items():
        #print(item.columns)
        #print(item.shape)


        
    # 3.     
    # create dictionary where keys are disciplinary categories
    # and items are yearly geosoc ut count (df)
    disc_yearly_counter_dict = {} 

    for key, item in disc_journals_geosoc_yearly_counter_dict.items():
        item_2 = item.drop(columns = ['CWTS_SO_NO'])
        #print(item_2.columns)
        item_2.fillna(0, inplace = True) # fillna
        item_2 = item_2.astype('int32') # change data type to inteher so that I can for sure sum
        disc_yearly_counter = pd.DataFrame(item_2.sum(axis = 0)).reset_index()
        #print(disc_yearly_counter)
        disc_yearly_counter.columns = ['year', 'ut_count'] # rename columns
    
        # get year as integer
        disc_yearly_counter['year'] = disc_yearly_counter['year'].apply(lambda x: int(x.split('_')[-1]))
    
        # save df
        disc_yearly_counter_dict[key] = disc_yearly_counter
    
    
    # check
    #for key, item in disc_geosoc_yearly_counter_dict.items():
        #print(type(item))
        #print(item.columns)
        #print(key)
        #print(item)
        
    return(disc_yearly_counter_dict)