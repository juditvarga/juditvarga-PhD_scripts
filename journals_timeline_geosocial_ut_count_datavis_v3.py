# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:42:22 2020

@author: vargajv
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:21:47 2019

@author: vargajv
"""

#%% ALGORITHM

"""

GOAL

norm method 1:
    
    what percentage of geosocial papers are published by different disciplines?

    for each disciplinary group:
        geosoc_ut_count(discipline) / all_geosoc_ut_count
 

norm method 2:
    
    what percentage of publications within the disciplines delineated by
    journals which publish geosocial research are geosocial papers?
    
    categorise journals and sum up geosoc_ut_percentages of the journals within them
    
    for each group:
        geosoc_ut_count(group) / all_uts(journals_in_group_for_same_time_period)


norm method 3:
    
    what percentage of publications within these 'disciplines' are geosocial papers?
    
    for each group:
        geosoc_ut_count(group) / all_uts(all_journals_in_WOS_with_same_disciplinary_classification_for_same_time_period)
 

ALGORITHM 


# data needed for interim steps
## DATA NEEDED FOR FINAL CALCULATIONS

for data vis 1 & 2 & 3:

    1. create dataframes
    
        ## YEARLY TOTAL GEOSOCOC UT COUNT
            DONE: yearly_total_geosoc_df

        # yearly geosoc ut count for each journal in my dataset (== journals which publish geosocial papers)
            DONE: geosoc_journals_yearly_counter_df

        # yearly total ut count for each journal in WOSKB (== all journals)
            DONE: yearly_total_ut_all_journals_df
            
        # SC of all journals (CWTS_SO_NO) from WOSKB (for vis 3)
            DONE: all_so_sc_df
            
    
    2. categorise journals into discplines
    
        # in my small dataset into disciplinary categories (for vis 1 & 2)
            DONE: SO_SC_cat_df
            
        # in all WOSKB into disciplinary categories (for vis 3)
            DONE: all_journals_SO_SC_cat_df
    
    3. create data
    
        ## YEARLY GEOSOC UT COUNT FOR EACH DISCIPLINARY GROUP
            DONE: disc_geosoc_yearly_ut_counter_dict, a dictionary where
                    keys = disciplinary groups
                    items = dataframes, yearly geosoc ut count 
        
        ## YEARLY TOTAL UT COUNT FOR EACH DISCIPLINARY GROUP based on subset of journals which publish geosocial papers
            DONE: disc_total_yearly_ut_counter_dict_subset_journals, a dictionary where
                    keys = disciplinary groups
                    items = dataframes, yearly total ut count of journals which publish geosoc papers
            
        ## YEARLY TOTAL UT COUNT FOR EACH DISCIPLINARY GROUP based on all journals
            DONE: disc_total_yearly_ut_counter_dict
    
    4. calculate norm 1, norm 2 and norm 3
    
        # norm 1: YEARLY GEOSOC UT COUNT FOR EACH DISCIPLINARY GROUP / yearly_total_geosoc_df
            DONE
        
        # norm 2: YEARLY GEOSOC UT COUNT FOR EACH DISCIPLINARY GROUP / YEARLY TOTAL UT COUNT FOR EACH DISCIPLINARY GROUP based on subset of journals which publish geosocial papers
            TO DO
            
        # norm3: YEARLY GEOSOC UT COUNT FOR EACH DISCIPLINARY GROUP / YEARLY TOTAL UT COUNT FOR EACH DISCIPLINARY GROUP based on all journals
            TO DO
    
    5. visualise norm 1 AND norm 2 AND norm 3

"""
#%% 

#%% read in nodes (papers) with info, pub_year already filtered
import os
import pandas as pd

# change working directory
os.chdir("P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/")
print("Current Working Directory " , os.getcwd())

from load_csv_data import load_ut_nodes

all_nodes_df = load_ut_nodes()

print(all_nodes_df.shape) # (17774, 14)

print(all_nodes_df.columns)

#Index(['UT', 'ti', 'ab', 'de', 'id', 'pub_year', 'CWTS_SO_NO', 'CWTS_SC_NO',
#       'SC', 'WEIGHT', 'SO', 'AU_COUNT', 'AU_NO', 'AU'],
#      dtype='object')

# plot pub_year of papers

print(min(all_nodes_df.pub_year)) # 2008
print(max(all_nodes_df.pub_year)) # 2009

# fill NaN in 'AU' columns
# to avoid # ValueError: cannot index with vector containing NA / NaN values

all_nodes_df['AU'].fillna('0', inplace = True)

#%% get all SC for methods chapter

all_SC = pd.DataFrame(all_nodes_df[['UT', 'SC']].groupby('SC').count()).reset_index().sort_values(by = 'UT', ascending = False)
print(all_SC)
all_SC.rename(columns = {'SC' : 'subject_category', 'UT': 'number of papers'}, inplace = True)
all_SC.to_excel("P:/thesis/thesis_final_data/produced_data/geosoc_papers_all_SC.xlsx", index = False)

#%%
#%% DF 1: get yearly geosoc papers

from disciplines_timeline_functions import get_yearly_geosoc_ut_count

yearly_total_geosoc_df = get_yearly_geosoc_ut_count(all_nodes_df)

print(yearly_total_geosoc_df.shape) # (12, 2)
print(yearly_total_geosoc_df.columns) # Index(['pub_year', 'geosoc_ut_count'], dtype='object')



# create cumulative geosoc ut count variable
cum_yearly_total_geosoc_df = yearly_total_geosoc_df.copy()
geosoc_counts_list = list(cum_yearly_total_geosoc_df.geosoc_ut_count)

newlist_1 = [geosoc_counts_list[0]]
maxi = (len(geosoc_counts_list)) -1
newlist_2 = [geosoc_counts_list[0] + sum(geosoc_counts_list[1:i + 2]) for i in list(range(0, maxi))]

print(sum(yearly_total_geosoc_df.geosoc_ut_count))
print(yearly_total_geosoc_df.geosoc_ut_count)

newlist = newlist_1 + newlist_2

cum_yearly_total_geosoc_df['cumulative_geosoc_ut_count'] = newlist 

print(cum_yearly_total_geosoc_df)


#%% DF 2: count *yearly* geosoc paper count for each journal ==
# count *yearly* number of papaers published in each journal in my small dataset 

from disciplines_timeline_functions import get_yearly_geosoc_count_journals

geosoc_journals_yearly_counter_df = get_yearly_geosoc_count_journals(all_nodes_df)

print(geosoc_journals_yearly_counter_df.shape) # (1069, 13)
print(geosoc_journals_yearly_counter_df.head(5))
print(geosoc_journals_yearly_counter_df.columns)

#Index(['CWTS_SO_NO', 'geosoc_ut_count_2008', 'geosoc_ut_count_2009',
#       'geosoc_ut_count_2010', 'geosoc_ut_count_2011', 'geosoc_ut_count_2012',
#       'geosoc_ut_count_2013', 'geosoc_ut_count_2014', 'geosoc_ut_count_2015',
#       'geosoc_ut_count_2016', 'geosoc_ut_count_2017', 'geosoc_ut_count_2018',
#       'geosoc_ut_count_2019'],
#      dtype='object', name='pub_year')

geosoc_journals_yearly_counter_df.to_csv('P:/thesis/thesis_final_data/produced_data/journal_pub_count_dfs/yearly_geosoc_ut_all_journals.csv')


# get cumulative

geosoc_journals_yearly_counter_df_2 = geosoc_journals_yearly_counter_df.copy()
geosoc_journals_yearly_counter_df_2.index = geosoc_journals_yearly_counter_df_2.CWTS_SO_NO
geosoc_journals_yearly_counter_df_2.drop(columns = ['CWTS_SO_NO'], inplace = True)
print(geosoc_journals_yearly_counter_df_2.columns)
geosoc_journals_yearly_counter_df_2.fillna(0, inplace = True)

print(geosoc_journals_yearly_counter_df_2.dtypes)

geosoc_journals_yearly_counter_df_cum = geosoc_journals_yearly_counter_df_2.cumsum(axis = 1)

# re-add 'CWTS_SO_NO' column
geosoc_journals_yearly_counter_df_cum.reset_index(inplace = True)
print(geosoc_journals_yearly_counter_df_cum.columns)

# check
print(geosoc_journals_yearly_counter_df[['geosoc_ut_count_2010', 'geosoc_ut_count_2011']].head(5))
print(geosoc_journals_yearly_counter_df_cum[['geosoc_ut_count_2010', 'geosoc_ut_count_2011']].head(5))
#%% DF 3 yearly total ut count for each journal in my dataset from WOSdata

# get TEMPORAL data about all journals' publication count in the whole WOSKB databse 
# as opposed to my small dataset

mydir = 'P:/thesis/thesis_final_data/collected_data/csv/4_yearly_journal_ut_counts_csv/'

from disciplines_timeline_functions import get_yearly_total_ut_all_journals

yearly_total_ut_all_journals_df = get_yearly_total_ut_all_journals(mydir)

print(yearly_total_ut_all_journals_df.shape) # (14646, 13)
print(yearly_total_ut_all_journals_df.columns)

#Index(['all_ut_count_2010', 'CWTS_SO_NO', 'all_ut_count_2009',
#       'all_ut_count_2011', 'all_ut_count_2012', 'all_ut_count_2013',
#       'all_ut_count_2014', 'all_ut_count_2015', 'all_ut_count_2016',
#       'all_ut_count_2017', 'all_ut_count_2018', 'all_ut_count_2019',
#       'all_ut_count_2008'],
#      dtype='object')

#print(yearly_total_ut_all_journals_df.head(5))

yearly_total_ut_all_journals_df.to_csv('P:/thesis/thesis_final_data/produced_data/journal_pub_count_dfs/yearly_total_ut_all_journals.csv')



# get cumulative ut counts

#reorder columns
yearly_total_ut_all_journals_df_2 = yearly_total_ut_all_journals_df[['CWTS_SO_NO', 'all_ut_count_2008', 
                                                                     'all_ut_count_2009',
                                                                     'all_ut_count_2010', 
                                                                     'all_ut_count_2011', 
                                                                     'all_ut_count_2012', 
                                                                     'all_ut_count_2013',
                                                                     'all_ut_count_2014', 
                                                                     'all_ut_count_2015',
                                                                     'all_ut_count_2016',
                                                                     'all_ut_count_2017', 
                                                                     'all_ut_count_2018', 
                                                                     'all_ut_count_2019']]
    
yearly_total_ut_all_journals_df_2.index = yearly_total_ut_all_journals_df_2.CWTS_SO_NO
yearly_total_ut_all_journals_df_2.drop(columns = ['CWTS_SO_NO'], inplace = True)
yearly_total_ut_all_journals_df_2.fillna(0, inplace = True)

print(yearly_total_ut_all_journals_df_2.columns)

print(yearly_total_ut_all_journals_df_2.dtypes)

yearly_total_ut_all_journals_df_2 = yearly_total_ut_all_journals_df_2.astype('float64')

print(yearly_total_ut_all_journals_df_2.dtypes)


yearly_total_ut_all_journals_df_cum = yearly_total_ut_all_journals_df_2.cumsum(axis = 1)
print(yearly_total_ut_all_journals_df_cum.columns)

# re-add 'CWTS_SO_NO' column
yearly_total_ut_all_journals_df_cum.reset_index(inplace = True)
print(yearly_total_ut_all_journals_df_cum.columns)


# check
print(yearly_total_ut_all_journals_df[['all_ut_count_2008', 'all_ut_count_2019']].head(5))
print(yearly_total_ut_all_journals_df_cum[['all_ut_count_2008', 'all_ut_count_2019']].head(5))

#%% DF 4 SC s of all SO from WOSKB

from disciplines_timeline_functions import create_all_so_sc_df

# directory which contains data files with information about all SO from WOSKB
all_SO_dir = 'P:/thesis/thesis_final_data/collected_data/csv/5_all_journals_so_sc_csv/all_so_woskb.csv'
SO_NO_SC_NO_dir = 'P:/thesis/thesis_final_data/collected_data/csv/5_all_journals_so_sc_csv/all_so_cwts_sc_no_woskb.csv'
SC_NO_SC_dir = 'P:/thesis/thesis_final_data/collected_data/csv/5_all_journals_so_sc_csv/all_so_cwts_sc_no_woskb_2.csv'


# laod data whcih contains SO and CWTS_SO_NO

all_so_sc_df = create_all_so_sc_df(all_SO_dir,SO_NO_SC_NO_dir, SC_NO_SC_dir)

print(all_so_sc_df['SC'].head(10))
print(all_so_sc_df.columns)
print(all_so_sc_df.shape)
print(all_so_sc_df['CWTS_SO_NO'].head(10))
print(all_so_sc_df.SC.isnull().values.any())

#%%
#%% 
#%% CATEGORISE SC S INTO DISCIPLINES
#%% PART 1 OF categorise JOURNALS WHICH PUBLISH GEOSOCIAL RESEARCH into disciplinary groups:
# GET joined SC for SOs - requirement of categorisation according to disciplines

from disciplines_timeline_functions import join_SC

SO_SC_joined_df = join_SC(all_nodes_df)

print(SO_SC_joined_df.columns) # Index(['CWTS_SO_NO', 'SC_joined', 'SO'], dtype='object')
#print(SO_SC_joined_df['SC_joined'].head(5))


#%% categorise JOURNALS WHICH PUBLISH GEOSOCIAL RESEARCH based on disciplines
# create indicator variables
# ENDED UP USING THE DICTIONARY BASED SOLUTION BELOW

#from SC_categories_function import SC_categorise_for_timeline_with_names # not good function
#SO_SC_cat_df =  SC_categorise_for_timeline_with_names(SO_SC_joined_df)
#catf = 'catf_withnames'

#from SC_categories_function import SC_categories_4
#SO_SC_cat_df =  SC_categories_4(SO_SC_joined_df)
#catf = 'catf4'
##
#
#from SC_categories_function import SC_categories_4_copy
#SO_SC_cat_df =  SC_categories_4_copy(SO_SC_joined_df)
#catf = 'catf4_copy'

from SC_categories_function import SC_categories_7
SO_SC_cat_df =  SC_categories_7(SO_SC_joined_df)
catf = 'catf7'

#from SC_categories_function import SC_categories_6
#SO_SC_cat_df =  SC_categories_6(SO_SC_joined_df)
#catf = 'catf6'
#
#from SC_categories_function import SC_categories_5
#SO_SC_cat_df =  SC_categories_5(SO_SC_joined_df)
#catf = 'catf5'

print(SO_SC_cat_df.columns)

#Index(['CWTS_SO_NO', 'SC_joined', 'SO', 'SC_comp', 'SC_soc', 'SC_multi_inter',
#       'SC_all_geo', 'SC_phys_geo', 'SC_non_phys_geo', 'SC_non_cat', 'SC_only_soc',
#       'SC_only_non_phys_geo', 'SC_only_comp', 'SC_comp_soc',
#       'SC_comp_non_phys_geo'],
#      dtype='object')

# questions: medical informatincs, information and library science, VETERINARY science, DEVELOPMENT studies
print('')
noncat_1 = SO_SC_cat_df.loc[SO_SC_cat_df['non_cat'] == 1]
print(set(list(noncat_1.SC_joined)))

#%%
#%% PART 1 OF categorise ALL JOURNALS

from disciplines_timeline_functions import join_SC

print(all_so_sc_df.columns)

#Index(['CWTS_SO_NO', 'SO', 'cwts_so_no', 'cwts_sc_no', 'weight', 'CWTS_SC_NO', 'SC'], dtype='object')
all_journals_SO_SC_joined_df = join_SC(all_so_sc_df)
print(all_journals_SO_SC_joined_df.columns) # Index(['CWTS_SO_NO', 'SC_joined', 'SO'], dtype='object')
#print(SO_SC_joined_df['SC_joined'].head(5))

#%% categorise JOURNALS WHICH PUBLISH GEOSOCIAL RESEARCH based on disciplines
# create indicator variables
# ENDED UP USING THE DICTIONARY BASED SOLUTION BELOW

#from SC_categories_function import SC_categorise_for_timeline_with_names #
#all_journals_SO_SC_cat_df =  SC_categorise_for_timeline_with_names(all_journals_SO_SC_joined_df)
#catf = 'catf_withnames'

#
#from SC_categories_function import SC_categories_4
#all_journals_SO_SC_cat_df =  SC_categories_4(all_journals_SO_SC_joined_df)
#catf = 'catf4'

from SC_categories_function import SC_categories_7
all_journals_SO_SC_cat_df=  SC_categories_7(all_journals_SO_SC_joined_df)
catf = 'catf7'

print(all_journals_SO_SC_cat_df.columns)

#Index(['CWTS_SO_NO', 'SC_joined', 'SO', 'SC_comp', 'SC_soc', 'SC_multi_inter',
#       'SC_all_geo', 'SC_phys_geo', 'SC_non_phys_geo', 'SC_non_cat', 'SC_only_soc',
#       'SC_only_non_phys_geo', 'SC_only_comp', 'SC_comp_soc',
#       'SC_comp_non_phys_geo'],
#      dtype='object')

# check non categorised SC s : double check categorisation
#noncat = all_journals_SO_SC_cat_df.loc[all_journals_SO_SC_cat_df['SC_non_cat'] == 1]
noncat = all_journals_SO_SC_cat_df.loc[all_journals_SO_SC_cat_df['non_cat'] == 1]
print(set(list(noncat.SC_joined)))
#%%
#%%
#%% GET DATA ROUND 2
#%% DATA 5: GET YEARLY GEOSOC UT COUNT FOR EACH DISCIPLINARY GROUP

# yearly

from disciplines_timeline_functions import disc_yearly_ut_counter

disc_geosoc_yearly_ut_counter_dict =  disc_yearly_ut_counter(SO_SC_cat_df, 
                                                             geosoc_journals_yearly_counter_df)

for key, item in disc_geosoc_yearly_ut_counter_dict.items():
    print(key)
    print(item)



# cumulative

disc_geosoc_yearly_ut_counter_dict_cum =  disc_yearly_ut_counter(SO_SC_cat_df, 
                                                                 geosoc_journals_yearly_counter_df_cum)

for key, item in disc_geosoc_yearly_ut_counter_dict_cum.items():
    print(key)
    print(item)

    
#%% DATA 6: YEARLY TOTAL UT COUNT FOR EACH DISCIPLINARY GROUP 
# based on subset of journals which publish geosocial papers
            

from disciplines_timeline_functions import disc_yearly_ut_counter

disc_total_yearly_ut_counter_dict_subset_journals =  disc_yearly_ut_counter(SO_SC_cat_df, 
                                                                            yearly_total_ut_all_journals_df)

for key, item in disc_total_yearly_ut_counter_dict_subset_journals.items():
    print(key)
    print(item.shape)
    print(item)

#print(yearly_total_ut_all_journals_df.columns) 
#print(yearly_total_ut_all_journals_df[['all_ut_count_2018', 'all_ut_count_2019']].head(5)) 

# cumulative -- DOES NOT WORK

disc_total_yearly_ut_counter_dict_subset_journals_cum =  disc_yearly_ut_counter(SO_SC_cat_df, 
                                                                                yearly_total_ut_all_journals_df_cum)

for key, item in disc_total_yearly_ut_counter_dict_subset_journals_cum.items():
    print(key)
    print(item)

#print(yearly_total_ut_all_journals_df_cum.columns)     
#print(yearly_total_ut_all_journals_df_cum[['all_ut_count_2018', 'all_ut_count_2019']].head(5)) 
#%% DATA 7: YEARLY TOTAL UT COUNT FOR EACH DISCIPLINARY GROUP based on all journals

from disciplines_timeline_functions import disc_yearly_ut_counter

disc_total_yearly_ut_counter_dict =  disc_yearly_ut_counter(all_journals_SO_SC_cat_df, 
                                                            yearly_total_ut_all_journals_df)


for key, item in disc_total_yearly_ut_counter_dict.items():
    print(key)
    print(item.shape)
    print(item)



# cumulative

disc_total_yearly_ut_counter_dict_cum =  disc_yearly_ut_counter(all_journals_SO_SC_cat_df,
                                                                yearly_total_ut_all_journals_df_cum)

for key, item in disc_total_yearly_ut_counter_dict_cum.items():
    print(key)
    print(item)
#%%
#%% CALCULATE NORMALISED UT COUNT
    #%% remove unwanted categories
for key, item in disc_geosoc_yearly_ut_counter_dict.items():
    print(key)
    
disc_geosoc_yearly_ut_counter_dict.pop('non_cat', None)
disc_geosoc_yearly_ut_counter_dict.pop('comp_non_phys_geo', None)
disc_geosoc_yearly_ut_counter_dict.pop('only_non_phys_geo', None)

for key, item in disc_geosoc_yearly_ut_counter_dict.items():
    print(key)
    
# cumulative
    
disc_geosoc_yearly_ut_counter_dict_cum.pop('non_cat', None)    
disc_geosoc_yearly_ut_counter_dict_cum.pop('comp_non_phys_geo', None)
disc_geosoc_yearly_ut_counter_dict_cum.pop('only_non_phys_geo', None)    
#%% NORM 1

import pandas as pd

#print(yearly_total_geosoc_df.columns)

# get a list of dfs for each disciplinary category which includes three variables:
# year
# percentage of geosoc papers (norm 1)
# disciplonary group identiifer

norm_1_data_list = []

for key, item in disc_geosoc_yearly_ut_counter_dict.items():
    #print(item.columns)
    
    merged = pd.merge(item, yearly_total_geosoc_df,
                      left_on = 'year', 
                      right_on = 'pub_year',
                      how = 'left')
    
    #print(merged[['ut_count', 'geosoc_ut_count']])
    
    merged['percentage_geosoc_papers'] = (merged['ut_count'] / merged['geosoc_ut_count']) * 100
    merged['disc_group'] = key
    
    #print(merged[['year', 'percentage_geosoc_papers', 'disc_group']])
    
    norm_1_data_list.append(merged)
    
    #print(merged.columns)
    #yearly_total_geosoc_df
    
# concatenate dataframes in norm_1_data_list to get long_df
    
norm_1_long_df = pd.concat(norm_1_data_list)
print(norm_1_long_df.columns)
#Index(['year', 'ut_count', 'pub_year', 'geosoc_ut_count',
#       'percentage_geosoc_papers', 'disc_group'],
#      dtype='object')

norm_1_long_df.drop(columns = ['ut_count', 'pub_year', 'geosoc_ut_count'], inplace = True)
print(norm_1_long_df.shape) # (144, 3)
print(norm_1_long_df.columns)
# Index(['year', 'percentage_geosoc_papers', 'disc_group'], dtype='object')

# PLOT WITH SEABRON: BETTER CONTROL OF COLORS:

import seaborn as sns

sns.set(rc={'figure.figsize':(12,8)}) # set figsize
sns.set_style(style='white') #  set background

# set color
# XKCD colors
#https://xkcd.com/color/rgb/

colors = ['black', "windows blue", 'cornflower', 
          "dusty purple", 'coral', 'hot pink', 'rose', 'light peach', 
          "greyish", 'sunshine yellow', 
          "amber", 'aqua green', 'jungle green']

current_palette = sns.xkcd_palette(colors)

#sns.palplot(current_palette)

#sns.set_palette(current_palette)

with sns.color_palette(current_palette):
    sns_plot = sns.lineplot(data=norm_1_long_df, x='year', y='percentage_geosoc_papers', hue='disc_group')
   
sns_plot.figure.savefig('P:/thesis/thesis_final_visualisations/disciplines_timeline/yearly_percentage_of_geosoc_papers_norm_1_{}.png'.format(catf))

# PLOT OTHER TYPE

#to_plot_data_df_wide_2 = norm_1_long_df.pivot(index='year', columns='disc_group', values='percentage_geosoc_papers')
#print(to_plot_data_df_wide_2)

#lines_norm_1 = to_plot_data_df_wide_2.plot.line(figsize = (12, 8), title='% of geosocial papers per disciplinary category')
#lines_norm_1.set_ylabel("% of geosocial papers")
#lines_norm_1.figure.savefig('P:/thesis/thesis_final_visualisations/yearly_percentage_of_geosoc_papers_norm_1_final.png')

#%% stacked area chart NORM 1

merged_wide_df = pd.DataFrame()

#  index is year, columns are the disciplines
#Index(['computational', 'social', 'multi_inter', 'all_geo', 'phys_geo',
#       'non_phys_geo', 'health', 'biol_env', 'arts_humanities',
#       'econ_bus_trans', 'comp_soc', 'only_social', 'only_computational'],
#      dtype='object')


norm_1_area_data_list = []

for df in norm_1_data_list:
#    print(df.head(5))
    disc = list(df.disc_group)[0]
    print(disc)
    df2 = df[['year', 'percentage_geosoc_papers']]
    df2.rename(columns = {'percentage_geosoc_papers' : disc}, inplace = True)
    print(df2)
    
    norm_1_area_data_list.append(df2)
    

merged_wide_df = norm_1_area_data_list[0]

for df in norm_1_area_data_list[1: ]:
    merged_wide_df = pd.merge(merged_wide_df,
                              df,
                              on = 'year', 
                              how = 'left')
    
print(merged_wide_df.head(5))

merged_wide_df.index = merged_wide_df.year
merged_wide_df2 = merged_wide_df.drop(columns = ['year'])

# PLOT OTHER METHOD
import matplotlib.pyplot as plt
import seaborn as sns

pal = sns.color_palette("husl", n_colors = 18)
pal = sns.color_palette("cubehelix", 18)
#pal = sns.color_palette("coolwarm", 18)

#pal = sns.cubehelix_palette(18, start=.5, rot=-.75)

#https://stackoverflow.com/questions/55214249/how-to-create-an-area-plot-in-seaborn
plt.style.use('seaborn')
merged_wide_df2.plot.area(colors=pal)


#%% CUMULATIVE NORM 1 
import pandas as pd

#print(yearly_total_geosoc_df.columns)

# get a list of dfs for each disciplinary category which includes three variables:
# year
# percentage of geosoc papers (norm 1)
# disciplonary group identiifer

norm_1_data_list = []

for key, item in disc_geosoc_yearly_ut_counter_dict_cum.items():
    #print(item.columns)
    
    merged = pd.merge(item, cum_yearly_total_geosoc_df,
                      left_on = 'year', 
                      right_on = 'pub_year',
                      how = 'left')
    
    #print(merged[['ut_count', 'geosoc_ut_count']])
    
    merged['percentage_geosoc_papers'] = (merged['ut_count'] / merged['cumulative_geosoc_ut_count']) * 100
    merged['disc_group'] = key
    
    #print(merged[['year', 'percentage_geosoc_papers', 'disc_group']])
    
    norm_1_data_list.append(merged)
    
    #print(merged.columns)
    #yearly_total_geosoc_df
    
# concatenate dataframes in norm_1_data_list to get long_df
    
norm_1_long_df = pd.concat(norm_1_data_list)
print(norm_1_long_df.columns)
#Index(['year', 'ut_count', 'pub_year', 'geosoc_ut_count',
#       'percentage_geosoc_papers', 'disc_group'],
#      dtype='object')

norm_1_long_df.drop(columns = ['ut_count', 'pub_year', 'geosoc_ut_count'], inplace = True)
print(norm_1_long_df.shape) # (144, 3)
print(norm_1_long_df.columns)
# Index(['year', 'percentage_geosoc_papers', 'disc_group'], dtype='object')

# PLOT WITH SEABRON: BETTER CONTROL OF COLORS:

import seaborn as sns

sns.set(rc={'figure.figsize':(12,8)}) # set figsize
sns.set_style(style='white') #  set background

# set color
# XKCD colors
#https://xkcd.com/color/rgb/

colors = ['black', "windows blue", 'cornflower', 
          "dusty purple", 'coral', 'hot pink', 'rose', 'light peach', 
          "greyish", 'sunshine yellow', 
          "amber", 'aqua green', 'jungle green']

current_palette = sns.xkcd_palette(colors)

#sns.palplot(current_palette)

#sns.set_palette(current_palette)

with sns.color_palette(current_palette):
    sns_plot = sns.lineplot(data=norm_1_long_df, x='year', y='percentage_geosoc_papers', hue='disc_group')
   
sns_plot.figure.savefig('P:/thesis/thesis_final_visualisations/disciplines_timeline/cumulative_yearly_percentage_of_geosoc_papers_norm_1_{}.png'.format(catf))

# PLOT OTHER TYPE

#to_plot_data_df_wide_2 = norm_1_long_df.pivot(index='year', columns='disc_group', values='percentage_geosoc_papers')
#print(to_plot_data_df_wide_2)

#lines_norm_1 = to_plot_data_df_wide_2.plot.line(figsize = (12, 8), title='% of geosocial papers per disciplinary category')
#lines_norm_1.set_ylabel("% of geosocial papers")
#lines_norm_1.figure.savefig('P:/thesis/thesis_final_visualisations/yearly_percentage_of_geosoc_papers_norm_1_final.png')

#%%
#%% NORM 2

import pandas as pd
import seaborn as sns

# get a list of dfs for each disciplinary category which includes three variables:
# year
# percentage of geosoc papers (norm 1)
# disciplonary group identiifer

norm_2_data_list = []

for key, item in disc_geosoc_yearly_ut_counter_dict.items():

    print(key)
    print(item.head(2))
    
    for key_2, item_2 in disc_total_yearly_ut_counter_dict_subset_journals.items():
        
        if key_2 == key:
            print(key_2)
            print(item_2.head(2))
    
    
            merged = pd.merge(item, item_2,
                              on = 'year', 
                              how = 'left')
    
    #print(merged[['ut_count', 'geosoc_ut_count']])
    
    merged['percentage_geosoc_papers'] = (merged['ut_count_x'] / merged['ut_count_y']) * 100
    merged['disc_group'] = key
    
    #print(merged[['year', 'percentage_geosoc_papers', 'disc_group']])
    
    norm_2_data_list.append(merged)
    
    #print(merged.columns)
    #yearly_total_geosoc_df
    
# concatenate dataframes in norm_1_data_list to get long_df
    
norm_2_long_df = pd.concat(norm_2_data_list)
print(norm_2_long_df.columns)
#Index(['year', 'ut_count', 'pub_year', 'geosoc_ut_count',
#       'percentage_geosoc_papers', 'disc_group'],
#      dtype='object')

norm_2_long_df.drop(columns = ['ut_count_x', 'ut_count_y'], inplace = True)
print(norm_2_long_df.shape) # (144, 3)
print(norm_2_long_df.columns)
# Index(['year', 'percentage_geosoc_papers', 'disc_group'], dtype='object')

# PLOT WITH SEABRON: BETTER CONTROL OF COLORS

import seaborn as sns

sns.set(rc={'figure.figsize':(12,8)}) # set figsize
sns.set_style(style='white') #  set background

# set color
# https://seaborn.pydata.org/tutorial/color_palettes.html
# https://seaborn.pydata.org/generated/seaborn.color_palette.html


#current_palette = sns.color_palette("RdBu_r", 12) # not enouh colors to help distinguish
#current_palette = sns.color_palette('dark') # too dark
#current_palette = sns.color_palette("cubehelix", 12) # interessting colors but too dark

#current_palette = sns.color_palette('bright', 12)
#current_palette = sns.color_palette("Paired")

colors = ['black', "windows blue", 'cornflower', 
          "dusty purple", 'coral', 'hot pink', 'rose', 'light peach', 
          "greyish", 'sunshine yellow', 
          "amber", 'aqua green', 'jungle green']

current_palette = sns.xkcd_palette(colors)

#sns.palplot(current_palette)

#sns.set_palette(current_palette)

#with sns.color_palette(current_palette, 12):
with sns.color_palette(current_palette):
    sns_plot = sns.lineplot(data=norm_2_long_df, x='year', y='percentage_geosoc_papers', hue='disc_group')
   
sns_plot.figure.savefig('P:/thesis/thesis_final_visualisations/disciplines_timeline/yearly_percentage_of_geosoc_papers_norm_2_{}.png'.format(catf))

# PLOT OTHER METHOD

#to_plot_data_df_wide_3 = norm_2_long_df.pivot(index='year', columns='disc_group', values='percentage_geosoc_papers')
#print(to_plot_data_df_wide_3)

#lines_norm_2 = to_plot_data_df_wide_3.plot.line(figsize = (12, 8), title='% of geosocial papers per disciplinary category')
#lines_norm_2.set_ylabel("% of geosocial papers")
#lines_norm_2.figure.savefig('P:/thesis/thesis_final_visualisations/yearly_percentage_of_geosoc_papers_norm_2_final.png')

#%% CUMULATIVE NORM 2

import pandas as pd
import seaborn as sns

# get a list of dfs for each disciplinary category which includes three variables:
# year
# percentage of geosoc papers (norm 1)
# disciplonary group identiifer

norm_2_data_list = []

for key, item in disc_geosoc_yearly_ut_counter_dict_cum.items():

    print(key)
    print(item.head(2))
    
    for key_2, item_2 in disc_total_yearly_ut_counter_dict_subset_journals_cum.items():
        
        if key_2 == key:
            print(key_2)
            print(item_2.head(2))
    
    
            merged = pd.merge(item, item_2,
                              on = 'year', 
                              how = 'left')
    
    #print(merged[['ut_count', 'geosoc_ut_count']])
    
    merged['percentage_geosoc_papers'] = (merged['ut_count_x'] / merged['ut_count_y']) * 100
    merged['disc_group'] = key
    
    #print(merged[['year', 'percentage_geosoc_papers', 'disc_group']])
    
    norm_2_data_list.append(merged)
    
    #print(merged.columns)
    #yearly_total_geosoc_df
    
# concatenate dataframes in norm_1_data_list to get long_df
    
norm_2_long_df = pd.concat(norm_2_data_list)
print(norm_2_long_df.columns)
#Index(['year', 'ut_count', 'pub_year', 'geosoc_ut_count',
#       'percentage_geosoc_papers', 'disc_group'],
#      dtype='object')

norm_2_long_df.drop(columns = ['ut_count_x', 'ut_count_y'], inplace = True)
print(norm_2_long_df.shape) # (144, 3)
print(norm_2_long_df.columns)
# Index(['year', 'percentage_geosoc_papers', 'disc_group'], dtype='object')

# PLOT WITH SEABRON: BETTER CONTROL OF COLORS

import seaborn as sns

sns.set(rc={'figure.figsize':(12,8)}) # set figsize
sns.set_style(style='white') #  set background

# set color
# https://seaborn.pydata.org/tutorial/color_palettes.html
# https://seaborn.pydata.org/generated/seaborn.color_palette.html


#current_palette = sns.color_palette("RdBu_r", 12) # not enouh colors to help distinguish
#current_palette = sns.color_palette('dark') # too dark
#current_palette = sns.color_palette("cubehelix", 12) # interessting colors but too dark

#current_palette = sns.color_palette('bright', 12)
#current_palette = sns.color_palette("Paired")

colors = ['black', "windows blue", 'cornflower', 
          "dusty purple", 'coral', 'hot pink', 'rose', 'light peach', 
          "greyish", 'sunshine yellow', 
          "amber", 'aqua green', 'jungle green']

current_palette = sns.xkcd_palette(colors)

#sns.palplot(current_palette)

#sns.set_palette(current_palette)

#with sns.color_palette(current_palette, 12):
with sns.color_palette(current_palette):
    sns_plot = sns.lineplot(data=norm_2_long_df, x='year', y='percentage_geosoc_papers', hue='disc_group')
   
sns_plot.figure.savefig('P:/thesis/thesis_final_visualisations/disciplines_timeline/cumulative_yearly_percentage_of_geosoc_papers_norm_2_{}.png'.format(catf))

# PLOT OTHER METHOD

#to_plot_data_df_wide_3 = norm_2_long_df.pivot(index='year', columns='disc_group', values='percentage_geosoc_papers')
#print(to_plot_data_df_wide_3)

#lines_norm_2 = to_plot_data_df_wide_3.plot.line(figsize = (12, 8), title='% of geosocial papers per disciplinary category')
#lines_norm_2.set_ylabel("% of geosocial papers")
#lines_no

#%% NORM 3

import pandas as pd
import seaborn as sns

# get a list of dfs for each disciplinary category which includes three variables:
# year
# percentage of geosoc papers (norm 1)
# disciplonary group identiifer

norm_3_data_list = []

for key, item in disc_geosoc_yearly_ut_counter_dict.items():

    print(key)
    print(item.head(2))
    
    for key_2, item_2 in disc_total_yearly_ut_counter_dict.items():
        
        if key_2 == key:
            print(key_2)
            print(item_2.head(2))
    
    
            merged = pd.merge(item, item_2,
                              on = 'year', 
                              how = 'left')
    
    #print(merged[['ut_count', 'geosoc_ut_count']])
    
    merged['percentage_geosoc_papers'] = (merged['ut_count_x'] / merged['ut_count_y']) * 100
    merged['disc_group'] = key
    
    #print(merged[['year', 'percentage_geosoc_papers', 'disc_group']])
    
    norm_3_data_list.append(merged)
    
    #print(merged.columns)
    #yearly_total_geosoc_df
    
# concatenate dataframes in norm_1_data_list to get long_df
    
norm_3_long_df = pd.concat(norm_3_data_list)
print(norm_3_long_df.columns)
#Index(['year', 'ut_count', 'pub_year', 'geosoc_ut_count',
#       'percentage_geosoc_papers', 'disc_group'],
#      dtype='object')

norm_3_long_df.drop(columns = ['ut_count_x', 'ut_count_y'], inplace = True)
print(norm_3_long_df.shape) # (144, 3)
print(norm_3_long_df.columns)
# Index(['year', 'percentage_geosoc_papers', 'disc_group'], dtype='object')

# PLOT WITH SEABRON: BETTER CONTROL OF COLORS

import seaborn as sns

sns.set(rc={'figure.figsize':(12,8)}) # set figsize
sns.set_style(style='white') #  set background

# set color
# https://seaborn.pydata.org/tutorial/color_palettes.html
# https://seaborn.pydata.org/generated/seaborn.color_palette.html

colors = ['black', "windows blue", 'cornflower', 
          "dusty purple", 'coral', 'hot pink', 'rose', 'light peach', 
          "greyish", 'sunshine yellow', 
          "amber", 'aqua green', 'jungle green']

#"faded green",

current_palette = sns.xkcd_palette(colors)

#sns.palplot(current_palette)

#sns.set_palette(current_palette)

#with sns.color_palette(current_palette, 12):
with sns.color_palette(current_palette):
    sns_plot = sns.lineplot(data=norm_3_long_df, x='year', y='percentage_geosoc_papers', hue='disc_group')
   
sns_plot.figure.savefig('P:/thesis/thesis_final_visualisations/disciplines_timeline/yearly_percentage_of_geosoc_papers_norm_3_{}.png'.format(catf))

#%%#%% CUMULATIVE NORM 3

import pandas as pd
import seaborn as sns

# get a list of dfs for each disciplinary category which includes three variables:
# year
# percentage of geosoc papers (norm 1)
# disciplonary group identiifer

norm_3_data_list = []

for key, item in disc_geosoc_yearly_ut_counter_dict_cum.items():

    print(key)
    print(item.head(2))
    
    for key_2, item_2 in disc_total_yearly_ut_counter_dict_cum.items():
        
        if key_2 == key:
            print(key_2)
            print(item_2.head(2))
    
    
            merged = pd.merge(item, item_2,
                              on = 'year', 
                              how = 'left')
    
    #print(merged[['ut_count', 'geosoc_ut_count']])
    
    merged['percentage_geosoc_papers'] = (merged['ut_count_x'] / merged['ut_count_y']) * 100
    merged['disc_group'] = key
    
    #print(merged[['year', 'percentage_geosoc_papers', 'disc_group']])
    
    norm_3_data_list.append(merged)
    
    #print(merged.columns)
    #yearly_total_geosoc_df
    
# concatenate dataframes in norm_1_data_list to get long_df
    
norm_3_long_df = pd.concat(norm_3_data_list)
print(norm_3_long_df.columns)
#Index(['year', 'ut_count', 'pub_year', 'geosoc_ut_count',
#       'percentage_geosoc_papers', 'disc_group'],
#      dtype='object')

norm_3_long_df.drop(columns = ['ut_count_x', 'ut_count_y'], inplace = True)
print(norm_3_long_df.shape) # (144, 3)
print(norm_3_long_df.columns)
# Index(['year', 'percentage_geosoc_papers', 'disc_group'], dtype='object')

# PLOT WITH SEABRON: BETTER CONTROL OF COLORS

import seaborn as sns

sns.set(rc={'figure.figsize':(12,8)}) # set figsize
sns.set_style(style='white') #  set background

# set color
# https://seaborn.pydata.org/tutorial/color_palettes.html
# https://seaborn.pydata.org/generated/seaborn.color_palette.html

colors = ['black', "windows blue", 'cornflower', 
          "dusty purple", 'coral', 'hot pink', 'rose', 'light peach', 
          "greyish", 'sunshine yellow', 
          "amber", 'aqua green', 'jungle green']

#"faded green",

current_palette = sns.xkcd_palette(colors)

#sns.palplot(current_palette)

#sns.set_palette(current_palette)

#with sns.color_palette(current_palette, 12):
with sns.color_palette(current_palette):
    sns_plot = sns.lineplot(data=norm_3_long_df, x='year', y='percentage_geosoc_papers', hue='disc_group')
   
sns_plot.figure.savefig('P:/thesis/thesis_final_visualisations/disciplines_timeline/cumulative_yearly_percentage_of_geosoc_papers_norm_3_{}.png'.format(catf))

#%%
# create wide dataframe for stacked area chart

merged_wide_df = pd.DataFrame()

norm_4_data_list = []

for df in norm_3_data_list:
    df2 = df.drop(columns = ['ut_count_x', 'ut_count_y'])
    disc = df2.columns[-1]
    disc2 = list(df2[disc])[0]
    df2.rename(columns = {disc: disc2}, inplace = True)
#    print(df2.columns)
    print(df2.percentage_geosoc_papers)
    df2[disc2] = list(df2.percentage_geosoc_papers)
    df3 = df2.drop(columns = ['percentage_geosoc_papers'])
    print(df3.columns)
    
    norm_4_data_list.append(df3)


merged_wide_df = norm_4_data_list[0]

for df in norm_4_data_list[1: ]:
    merged_wide_df = pd.merge(merged_wide_df,
                              df,
                              on = 'year', 
                              how = 'left')
    
print(merged_wide_df.head(5))

merged_wide_df.index = merged_wide_df.year
merged_wide_df2 = merged_wide_df.drop(columns = ['year'])

print(merged_wide_df2.columns)

#  index is year, columns are the disciplines
#Index(['computational', 'social', 'multi_inter', 'all_geo', 'phys_geo',
#       'non_phys_geo', 'health', 'biol_env', 'arts_humanities',
#       'econ_bus_trans', 'comp_soc', 'only_social', 'only_computational'],
#      dtype='object')


# PLOT OTHER METHOD
import matplotlib.pyplot as plt
import seaborn as sns

pal = sns.color_palette("husl", n_colors = 18)
pal = sns.color_palette("cubehelix", 18)
#pal = sns.color_palette("coolwarm", 18)

#pal = sns.cubehelix_palette(18, start=.5, rot=-.75)

#https://stackoverflow.com/questions/55214249/how-to-create-an-area-plot-in-seaborn
plt.style.use('seaborn')
merged_wide_df2.plot.area(colors=pal)
#%%
#%%
#%% outstanding potentially useful code
#%%
#%% TODO:  get min and max pub year of geosocial papers for each journal in my small dataset
# (earliest and latest year a geososcial paper were published in them)

pub_year_df = my_journals_yearly_df[['CWTS_SO_NO', 'pub_year']]

# get min pub year

journals_pub_year_df_min = pub_year_df.loc[pub_year_df.groupby('CWTS_SO_NO')['pub_year'].idxmin()]
journals_pub_year_df_min.rename(columns = {'pub_year' : 'min_pub_year'}, inplace = True)

print(journals_pub_year_df_min)

# for equivalent result but different code:
#journals_pub_year_df_min = pub_year_df.groupby('CWTS_SO_NO')['pub_year'].min().reset_index()
#journals_pub_year_df_min.rename(columns = {'pub_year' : 'min_pub_year'}, inplace = True)
#print(journals_pub_year_df_min)


# get max pub year

journals_pub_year_df_max = pub_year_df.loc[pub_year_df.groupby('CWTS_SO_NO')['pub_year'].idxmax()]
journals_pub_year_df_max.rename(columns = {'pub_year' : 'max_pub_year'}, inplace = True)

# create a variable that lists pub_years for journals

#SO_pub_years_listed_df = pd.DataFrame(pub_year_df.groupby('CWTS_SO_NO')['pub_year'].apply(lambda x: list(x)))
SO_pub_years_listed_df = pd.DataFrame(pub_year_df.groupby('CWTS_SO_NO')['pub_year'].apply(lambda x: list(set([int(x) for x in list(x)]))))
SO_pub_years_listed_df_2 = pd.DataFrame(pub_year_df.groupby('CWTS_SO_NO')['pub_year'].apply(lambda x: [int(x) for x in list(x)]))

# check and merge dataframes

print(journals_pub_year_df_min.head(20))

print(journals_pub_year_df_max.head(20))

print(SO_pub_years_listed_df.head(20))

print(SO_pub_years_listed_df_2.head(20))

journals_pub_years = pd.merge(journals_pub_year_df_min, journals_pub_year_df_max,
                                       left_on = 'CWTS_SO_NO',
                                       right_on = 'CWTS_SO_NO',
                                       how = 'left')


print(journals_pub_years['min_pub_year'].min())

journals_pub_years.sort_values(by = 'min_pub_year', ascending = True, inplace = True) # 1993, 1997, 1998, 2002, 2008
#journals_pub_years.sort_values(by = 'max_pub_year', ascending = False, inplace = True) # 2019

print(journals_pub_years.head(20))
#%%

