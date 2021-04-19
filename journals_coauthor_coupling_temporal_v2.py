# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:35:13 2020

@author: vargajv
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 00:04:45 2020

@author: vargajv
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 20:46:49 2019

@author: vargajv
"""

# TO COMMENT LINE OUT: CTR:L + 1

#%%

'''
*GOALS*

I.
Create journal author bibliographic coupling data for simulate_sub_graph task
Create network edges data, where nodes are journals and edges are weighted
author bibliographic coupling betwen journals, 
and journals are classified according to disciplines

Procude 2 files: one for edges between social and technical journals, and
one for edges between all journals.

II.
Create csv file to visualise the journal author-bibliographic coupling
network in Gephi. I chose Gephi over R because Gephi seems to be better at
visualising large graphs


*ALGORITHM*

I. 

*CREATE FILE TO CALCULATE BIBLIOGRAPHIC COUPLING WITH*
Index(['SO', 'AU_NO_cited', 'SO_ran_id'], dtype='object')


LOAD CITED- CITING EDGES DATA

1. load geosocial citing - cited papers edge data
    'citing_cited_edges_df'
    #Index(['ut', 's_ut'], dtype='object')
    
2. load authors of cited papers data (and check number of cited papers) and rename columns
    'cited_authors_df'
    # Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited'], dtype='object')
    
3. merge dataframes (1) and (2)
    'cited_authors_citing_ut_df'
    # Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited', 'ut',
             's_ut'], dtype='object')


LOAD CITING UTs and SOs data
    
4. load geosocial citing papers data (and check the number of geosocial citing papers in the edge data)
    'citing_papers_df'    
    # Index(['UT', 'pub_year', 'CWTS_SO_NO', 'SC', 'SO'], dtype='object')


CREATE EDGES BETWEEN 'CWTS_SO_NO' and 'AU_NO_cited'

5. to create edges between SO and cited_AU: merge dataframes (3) and (4)
    'citing_cited_alldat_df_nona'
    #Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited', 'ut', 's_ut',
    #       'UT', 'pub_year', 'CWTS_SO_NO', 'SC', 'SO'],
    #      dtype='object')
    

ADD 'SO_RAN_ID' : PREPARE DATA FOR THE COS SIMILARITY FUNCTION

6. create random numeric id for SO so that cosine similarity function works
    'all_SO_df'
    # Index(['SO', 'SO_ran_id'], dtype='object')
    
    'citing_cited_alldat_2_df'
    #Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited', 'ut', 's_ut',
    #       'UT', 'pub_year', 'CWTS_SO_NO', 'SC', 'SO', 'SO_ran_id'],
    #      dtype='object')

7. create dataframe to be used with cosine similarity function
    'journals_cited_authors_df'
    # Index(['SO', 'AU_NO_cited', 'SO_ran_id'], dtype='object')
 
    
    
    
    
*CALCULATE AUTHOR BIBLIOGRAPHIC COUPLING COSINE SIMILARITY BETWEEN JOURNALS BASED ON AUTHORS CITED*
    
8.'journal_auth_coupling_cos_sim_df'

    


*CLASSIFY EDGES ACCORDING TO DISCIPLINES*

9. create citing papers df with SC s joined
    'citing_papers_SC_joined_df'
    #Index(['ut', 'pub_year', 'CWTS_SO_NO', 'SO', 'SC_joined'], dtype='object')
           dtype='object')

10. classify SC_joined SO s according to disciplines
    'citing_SOs_SC_categories_df'

    #Index(['CWTS_SO_NO', 'SO', 'SC_joined', 'SC_cat_1', 'SC_cat_2', 'SC_cat_3',
    #       'SC_cat_4', 'SC_cat_5', 'SC_cat_6', 'SC_cat_7', 'SC_cat_8', 'SC_cat_9',
    #       'SC_cat_10', 'SC_cat_11', 'SO_ran_id'],
    #      dtype='object')

11. get SO, SC categories for journal_1 SO_ran_id and journal_2 SO_ran_id
    join 'citing_cited_alldat__2_df' on journal_1 and journal_2
    
    'edges_classified_df'
    #Index(['journal_auth_cosine_similarity', 'journal_1', 'journal_2',
    #       'SO_ran_id_j1', 'SC_cat_10_j1', 'SC_cat_11_j1', 'SO_ran_id_j2',
    #       'SC_cat_10_j2', 'SC_cat_11_j2'],
    #      dtype='object')
    
12. create 2 files: inter edges and all edges


II.
Create csv file to visualise the journal author-bibliographic coupling
network in Gephi.

Gephi nodes variables: 
    ['id', 'title', 'size', 'size_norm', 'SC_cat']

Gephi edges variables:
   ['Source', 'Target', 'Weight']

'''

#%%
#%% *CREATE FILE TO CALCULATE BIBLIOGRAPHIC COUPLING WITH*
#Index(['SO', 'AU_NO_cited', 'SO_ran_id'], dtype='object')
#%% LOAD CITED- CITING EDGES DATA
#%% 1. load geosocial citing - cited edges file

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')

from load_csv_data import load_cited_edges

citing_cited_edges_df = load_cited_edges()

# get number of cited and citing papers for checks later on
number_citing_papers_edge = len(list(set(list(citing_cited_edges_df['ut']))))
print(number_citing_papers_edge) # 2791
number_cited_papers = len(list(set(list(citing_cited_edges_df['s_ut']))))
#print(number_cited_papers) # 44171

print(citing_cited_edges_df.columns) #Index(['ut', 's_ut'], dtype='object')
print(citing_cited_edges_df.shape) # (64978, 2)

# drop duplicates
citing_cited_edges_df.drop_duplicates(inplace = True)
print(citing_cited_edges_df.shape) # (64978, 2)

# check nas
nas = citing_cited_edges_df[citing_cited_edges_df.isna().any(axis = 1)]
print(nas.shape) # (81, 2)

#print(nas)

print(citing_cited_edges_df.isna().sum())

print('number of citing papers with NA cited ref: {}'.format(str(len(list(set(list(nas.ut)))))))
# number of citing papers with NA cited ref: 81
#ut       0
#s_ut    81
#dtype: int64

# 81 papers don't have cited references - delete these
citing_cited_edges_df.dropna(inplace = True)
print(citing_cited_edges_df.shape) # (64897, 2)
number_citing_papers_edge_nona = len(list(set(list(citing_cited_edges_df['ut']))))
#%%
#%% 2. load authors of cited papers data

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')

from load_csv_data import load_cited_authors

cited_authors_df = load_cited_authors()

# rename columns to help later joins

cited_authors_df.columns = [word + '_cited' for word in cited_authors_df.columns]

print(cited_authors_df.columns) 
# Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited'], dtype='object')

print(cited_authors_df.shape) # (163455, 4)
# check number of cited papers in edges data and cited_authors data
number_cited_papers_2 = len(list(set(list(cited_authors_df.S_UT_cited))))
print(number_cited_papers_2) # 44171

number_cited_papers == number_cited_papers_2 # True

# check na
print(cited_authors_df.isna().sum())
#S_UT_cited         1
#AU_COUNT_cited     1
#AU_NO_cited        1
#AU_cited          26

cited_authors_df.dropna(inplace = True)
#%%
#%% 3. merge dataframes (1) and (2)

import pandas as pd

cited_authors_citing_ut_df = pd.merge(cited_authors_df, 
                                      citing_cited_edges_df,
                                      left_on = 'S_UT_cited', 
                                      right_on ='s_ut' ,
                                      how = 'right')

print(cited_authors_citing_ut_df.columns)
# Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited', 'ut',
#       's_ut'],
#      dtype='object')
print(cited_authors_citing_ut_df.shape) # (236713, 6)

print(len(list(set(list(cited_authors_citing_ut_df.ut))))) # 2710

# check na
print(cited_authors_citing_ut_df.isna().sum())

#S_UT_cited        29
#AU_COUNT_cited    29
#AU_NO_cited       29
#AU_cited          29
#ut                 0
#s_ut               0
#dtype: int64

#%% 
#%% LOAD CITING UTs and SOs data
#%%
#%% 4.1. load geosocial citing papers 

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')

#from load_csv_data import load_ut_nodes_data_2
#from load_csv_data import load_ut_nodes
from load_csv_data import load_ut_nodes_3

#citing_papers_df = load_ut_nodes() # 2732 distinct uts after pub_year filtering
#citing_papers_df = load_ut_nodes_data_2() # 2701 distinct uts after pub_year filtering
citing_papers_df = load_ut_nodes_3() # # 2763 distinct uts before pub_ear filtering, 2749 after pub_year filtering

# columns 
#Index(['UT', 'ti', 'ab', 'de', 'id', 'pub_year', 'CWTS_SO_NO', 'CWTS_SC_NO',
#       'SC', 'WEIGHT', 'SO', 'AU_COUNT', 'AU_NO', 'AU'],
#      dtype='object')

# get number of citing papers
citing_papers_nodupl = citing_papers_df.drop_duplicates(subset = 'UT')
#citing_papers_nodupl = citing_papers_df.drop_duplicates(subset = 'ut')
print('number of uts:')
number_citing_papers = citing_papers_nodupl.shape[0]
print(number_citing_papers) 

# check na
#print(citing_papers_df.isna().sum())

#UT               0
#ti               0
#ab             124
#de            2584
#id            2961
#pub_year         0
#CWTS_SO_NO       0
#CWTS_SC_NO       0
#SC               0
#WEIGHT           0
#SO               0
#AU_COUNT         0
#AU_NO            0
#AU               1

#ut              0
#ti              0
#ab             37
#de            655
#id            984
#pub_year        0
#CWTS_SO_NO      0
#CWTS_SC_NO      0
#SC              0
#WEIGHT          0
#SO              0

# drop columns that I don't need

citing_papers_df.drop(columns = ['ti', 'ab', 'de', 'id',  'CWTS_SC_NO', 
                                 'WEIGHT', 'AU_COUNT', 'AU_NO', 'AU'], inplace = True)

print(citing_papers_df.isna().sum())

#UT            0
#pub_year      0
#CWTS_SO_NO    0
#SC            0
#SO            0

print(citing_papers_df.columns)
# Index(['UT', 'pub_year', 'CWTS_SO_NO', 'SC', 'SO'], dtype='object')
# * THIS GETS USED* 

#%% 4.2. compare number of citing papers in edges and nodes data

import pandas as pd

print(number_citing_papers_edge == number_citing_papers)  # False
print(number_citing_papers_edge_nona == number_citing_papers ) #False

print(number_citing_papers_edge) # 2791 out of which 81 uts have NAN s_ut
print(number_citing_papers_edge_nona) # 2710  uts have s_ut associated with them
print(number_citing_papers) # 2732

check_common_ut_df = pd.merge(citing_cited_edges_df,
                              citing_papers_df,
                              left_on = 'ut',
                              right_on = 'UT',
                              how = 'inner')

print(check_common_ut_df.isna().sum())

#ut            0
#s_ut          0
#UT            0
#pub_year      0
#CWTS_SO_NO    0
#SC            0
#SO            0

print(len(list(set(list(check_common_ut_df.ut))))) #  2668 uts are shared between the edges and nodes datasets

#TODO: check document type of uts which are not shared between the two datasets

check_ut_df = pd.merge(citing_cited_edges_df,
                       citing_papers_df,
                       left_on = 'ut',
                       right_on = 'UT',
                       how = 'outer')

print(check_ut_df.isna().sum())

#ut             271
#s_ut           271
#UT            1180
#pub_year      1180
#CWTS_SO_NO    1180
#SC            1180
#SO            1180

print(len(list(set(list(check_ut_df.ut))))) #  2711
#print(len(list(set(list(check_ut_df.UT))))) #  2733
#%% 
#%% load document types

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')

#from load_csv_data import load_ut_nodes_data_2
#from load_csv_data import load_ut_nodes
from load_csv_data import load_cwts_document_types

doc_types_df = load_cwts_document_types()

print(doc_types_df)
#%%
#%% CREATE EDGES BETWEEN 'CWTS_SO_NO' and 'AU_NO_cited'
#%%
#%% 5. create edges between SO and cited_AU: merge dataframes (3) and (4)
    # 'citing_cited_alldat_df'
    #Index(['AU_NO_cited', 'ut', 's_ut', SO, CWTS_SO_NO)

import pandas as pd

citing_cited_alldat_df = pd.merge(cited_authors_citing_ut_df, 
                                  citing_papers_df,
                                  left_on = 'ut',
                                  right_on = 'UT',
                                  how = 'left')

print(type(list(cited_authors_citing_ut_df)[0])) # <class 'str'>

print(citing_cited_alldat_df.columns)
#Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited', 'ut', 's_ut',
#       'UT', 'pub_year', 'CWTS_SO_NO', 'SC', 'SO'],
#      dtype='object')

# shape check
print(citing_cited_alldat_df.shape[0]) # 236794
print(cited_authors_citing_ut_df.shape[0]) # 236794

# check na
print(citing_cited_alldat_df.isna().sum())

#S_UT_cited         208
#AU_COUNT_cited     208
#AU_NO_cited        208
#AU_cited           208
#ut                   0
#s_ut                 0
#UT                3650
#pub_year          3650
#CWTS_SO_NO        3650
#SC                3650
#SO                3650

nas = citing_cited_alldat_df[citing_cited_alldat_df['SO'].isna()]
print(nas.shape) # (4600, 19)

print(len(list(set(list(nas.ut))))) # 58 papers for which there is no SO, pub_date info
# drop these... I don't know why this happens...

# delete NA

citing_cited_alldat_df_nona = citing_cited_alldat_df.dropna()

# check na
print(citing_cited_alldat_df_nona.isna().sum())

#S_UT_cited        0
#AU_COUNT_cited    0
#AU_NO_cited       0
#AU_cited          0
#ut                0
#s_ut              0
#UT                0
#pub_year          0
#CWTS_SO_NO        0
#SC                0
#SO                0

print(citing_cited_alldat_df_nona.shape) # (182279, 19)
print(citing_cited_alldat_df_nona.columns) 

#Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited', 'ut', 's_ut',
#       'UT', 'pub_year', 'CWTS_SO_NO', 'SC', 'SO'],
#      dtype='object')

#%%
#%% ADD 'SO_RAN_ID' : PREPARE DATA FOR THE COS SIMILARITY FUNCTION
#%%
#%% 6. create random numeric id for SO so that cosine similarity function works

# create random id for SOs
#all_SO_df = pd.DataFrame(citing_cited_alldat_df['SO'].drop_duplicates())
all_SO_df = pd.DataFrame(citing_cited_alldat_df_nona['SO'].drop_duplicates())

# create 'SO_ran_id' column
all_SO_df.reset_index(inplace = True)
all_SO_df['SO_ran_id'] = all_SO_df.index
all_SO_df.drop(columns = ['index'], inplace = True)

# check shape
print(all_SO_df.shape) # (1069, 2)
print(all_SO_df.columns) # Index(['SO', 'SO_ran_id'], dtype='object')

print(max(all_SO_df['SO_ran_id'])) # 1068

# add SO_ran_id column to 'citing_cited_alldat_df'
citing_cited_alldat_2_df = pd.merge(citing_cited_alldat_df_nona,
                                    all_SO_df,
                                    on = 'SO',
                                    how = 'left')

# shape check
print(citing_cited_alldat_2_df.shape[0]) # 182279
print(citing_cited_alldat_df.shape[0]) # 236794

print(citing_cited_alldat_2_df.columns)

#Index(['S_UT_cited', 'AU_COUNT_cited', 'AU_NO_cited', 'AU_cited', 'ut', 's_ut',
#       'UT', 'pub_year', 'CWTS_SO_NO', 'SC', 'SO', 'SO_ran_id'],
#      dtype='object')
#%%
#%% create temporal files

years_list = list(range(2008,2020))

#year = years_list[0] # no author bibcouple edges at all
#year = years_list[1] # no author bibcouple edges at all
year = years_list[2] # done for all catf
#year = years_list[3] # done for all catf
#year = years_list[4] # done for all catf
#year = years_list[5] # done for all catf
#year = years_list[6] # done for all catf
#year = years_list[7] # done for all catf
#year = years_list[8] # done for all catf
#year = years_list[9] # done for all catf
#year = years_list[10] # done for all catf
#year = years_list[11] # done for all catf

print(year)

#print(citing_cited_alldat_2_df.shape)

citing_cited_alldat_temp_df = citing_cited_alldat_2_df.loc[citing_cited_alldat_2_df.pub_year <= year]
print(citing_cited_alldat_temp_df.shape)
#%% 7. create dataframe to be used with cosine similarity function

journals_cited_authors_df = citing_cited_alldat_temp_df[['SO', 'AU_NO_cited', 'SO_ran_id']]
print(journals_cited_authors_df.shape) # (182279, 3) # 236794 good
print(journals_cited_authors_df.columns)
# Index(['SO', 'AU_NO_cited', 'SO_ran_id'], dtype='object')
#%%
#%% check NAs
print(journals_cited_authors_df.shape) # (1891840, 3)
nas = journals_cited_authors_df[journals_cited_authors_df.isna().any(axis = 1)] # (0, 3)
print(nas.shape) # (0, 3)

journals_cited_authors_df_nona = journals_cited_authors_df.dropna()
print(journals_cited_authors_df_nona.shape)

nas = journals_cited_authors_df_nona[journals_cited_authors_df_nona.isna().any(axis = 1)]
print(nas.shape) # (0, 3)  
#%%

#%%
#%% 8. CALCULATE AUTHOR BIBLIOGRAPHIC COUPLING COSINE SIMILARITY BETWEEN JOURNALS 
# BASED ON AUTHORS OF CITED PAPERS
#%% 8. JOURNALS - AUTHOR -BIBLIOGRAPHIC COUPLING NETWORK
# CALCULATE COSINE SIMILARITY among citing 'journals

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')
    
from bib_couple_cosine_similarity import bib_couple_cos_similarity_df

# columns of the journal co-author dataframe to be used: Index(['SO', 'AU_NO', 'SO_ran_id'], dtype='object')

cos_sim = 0.01
cos_sim_for_filename = 'cos' + str(cos_sim).replace('.', '')

journal_auth_coupling_cos_sim_df = bib_couple_cos_similarity_df(journals_cited_authors_df, cos_sim)

#print(journal_auth_coupling_cos_sim_df.head(5))
# JOURNALS - AUTHOR COUPLING NETWORK
# check bib coupling df

print(journal_auth_coupling_cos_sim_df.shape)
# for cos sim > 0.2, shape (1183, 3)
# for cos sim > 0.25, shape (502, 3)
# for cos sim > 0.35, shape (122,3)
# for cos sim > 0.36, shape (108,3)
# for cos sim > 0.4, shape (74,3)

# rename columns
journal_auth_coupling_cos_sim_df.columns = ['journal_auth_cosine_similarity', 'journal_1', 'journal_2']

print(journal_auth_coupling_cos_sim_df.head(5))
print(journal_auth_coupling_cos_sim_df.shape) # (25958, 3)

print(pd.DataFrame(journal_auth_coupling_cos_sim_df.info()))
#<class 'pandas.core.frame.DataFrame'>
#Int64Index: 41491 entries, 757264 to 456893
#Data columns (total 3 columns):
#journal_auth_cosine_similarity    41491 non-null float64
#journal_1                         41491 non-null int64
#journal_2                         41491 non-null int64
#dtypes: float64(1), int64(2)
#memory usage: 1.3 MB
#Empty DataFrame
#Columns: []
#Index: []
print(journal_auth_coupling_cos_sim_df.memory_usage())

#Index                             331928
#journal_auth_cosine_similarity    331928
#journal_1                         331928
#journal_2                         331928

print(journal_auth_coupling_cos_sim_df.memory_usage(index=True).sum())
#1242368
print(journal_auth_coupling_cos_sim_df.shape) # (38824, 3)


#print(journal_auth_coupling_cos_sim_df)
#%%
#%% *CLASSIFY EDGES ACCORDING TO DISCIPLINES*
#%%
#%% 9. create citing papers df with SC s joined

# rename UT column for join SC function
citing_papers_df.rename(columns = {'UT' : 'ut'}, inplace = True)

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')

from join_SC import join_SC

citing_papers_SC_joined_df = join_SC(citing_papers_df)

# check for duplicates
print(citing_papers_SC_joined_df.shape) # (2732, 14)
citing_papers_SC_joined_df.drop_duplicates(inplace = True)
print(citing_papers_SC_joined_df.shape) # (2732, 14)

# check number of citing papers
number_citing_papers_2 = len(list(set(list(citing_papers_SC_joined_df.ut))))
print(number_citing_papers_2 == number_citing_papers) # True

print(citing_papers_SC_joined_df.columns)
#Index(['ut', 'pub_year', 'CWTS_SO_NO', 'SO', 'SC_joined'], dtype='object')

# check na
print(citing_papers_SC_joined_df.isna().sum())

#ut            0
#pub_year      0
#CWTS_SO_NO    0
#SO            0
#SC_joined     0

print(type(list(citing_papers_SC_joined_df.ut)[0])) # <class 'str'>

print(len(list(set(list(citing_papers_SC_joined_df.ut))))) # 2732
#%%
#%% 10. classify SO s according to disciplines based on SC_joined

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')

#from SC_categories_function import SC_categories
#citing_papers_SC_categories_df = SC_categories(citing_papers_SC_joined_df)

#from SC_categories_function import SC_categories_2
#citing_papers_SC_categories_df = SC_categories_2(citing_papers_SC_joined_df)

#from SC_categories_function import SC_categories_3
## SC_cat_10 (onyl social science) is the same as with disciplines timeline
#citing_papers_SC_categories_df = SC_categories_3(citing_papers_SC_joined_df)
#catf = 'catf3'

# NEW CATEOGORISATION FUNCTIONS

#from SC_categories_function import SC_categories_4 
## SC_cat_10 (onyl social science) has social science categories
#citing_papers_SC_categories_df = SC_categories_4(citing_papers_SC_joined_df)
#catf = 'catf4'

from SC_categories_function import SC_categories_5
# compared to 'SC_categories_4' function, 'social' category includes keywords for 
#    'social' AND 'arts_humanities'
citing_papers_SC_categories_df = SC_categories_5(citing_papers_SC_joined_df)
catf = 'catf5'
##
#
#from SC_categories_function import SC_categories_6
## compared to 'SC_categories_4' function, 'social' category includes keywords for 
##    'social' AND 'econ_bus_trans' 
#citing_papers_SC_categories_df = SC_categories_6(citing_papers_SC_joined_df)
#catf = 'catf6'

#from SC_categories_function import SC_categories_7
## SC_cat_10 (onyl social science) has social science and humanities AND travel/econ/business papers
#citing_papers_SC_categories_df = SC_categories_7(citing_papers_SC_joined_df)
#catf = 'catf7'

# create folder to save data
directory = 'P:/thesis/thesis_final_data/produced_data/journals_bib_coupling/temporal/{}_{}/'.format(cos_sim_for_filename, catf)

import os
if not os.path.exists(directory):
    os.makedirs(directory)

print(citing_papers_SC_joined_df.shape) # (2732, 14)
print(citing_papers_SC_categories_df.shape)   # (2732, 25)
print(citing_papers_SC_categories_df.columns)

#Index(['ut', 'pub_year', 'CWTS_SO_NO', 'SO', 'SC_joined', 'SC_cat_1',
#       'SC_cat_2', 'SC_cat_3', 'SC_cat_4', 'SC_cat_5', 'SC_cat_6', 'SC_cat_7',
#       'SC_cat_8', 'SC_cat_9', 'SC_cat_10', 'SC_cat_11'],
#      dtype='object')

#print(citing_papers_SC_categories_df.isna().sum())

# get SC categorised SO s dataframe
citing_SOs_SC_categories_df = citing_papers_SC_categories_df.drop(columns = ['ut', 'pub_year'])
citing_SOs_SC_categories_df.drop_duplicates(subset = 'SO', inplace = True)

print(citing_SOs_SC_categories_df.shape) # (1075, 14)
print(citing_SOs_SC_categories_df.columns)
#Index(['CWTS_SO_NO', 'SO', 'SC_joined', 'SC_cat_1', 'SC_cat_2', 'SC_cat_3',
#       'SC_cat_4', 'SC_cat_5', 'SC_cat_6', 'SC_cat_7', 'SC_cat_8', 'SC_cat_9',
#       'SC_cat_10', 'SC_cat_11'],
#      dtype='object')

# add SO_ran_id column

citing_SOs_SC_categories_df = pd.merge(citing_SOs_SC_categories_df,
                                       all_SO_df,
                                       on = 'SO', 
                                       how = 'left')

print(citing_SOs_SC_categories_df.shape) # (1075, 15)
print(citing_SOs_SC_categories_df.columns)

#Index(['CWTS_SO_NO', 'SO', 'SC_joined', 'SC_cat_1', 'SC_cat_2', 'SC_cat_3',
#       'SC_cat_4', 'SC_cat_5', 'SC_cat_6', 'SC_cat_7', 'SC_cat_8', 'SC_cat_9',
#       'SC_cat_10', 'SC_cat_11', 'SO_ran_id'],
#      dtype='object')
#%% FROM HERE REWRITE CATEGORY NAMES
#%% 11.1. get SO, SC categories for journal_1 SO_ran_id
# join 'citing_cited_alldat__2_df' on journal_1 and journal_2

import pandas as pd

#SO_cat_smaller_data = citing_SOs_SC_categories_df[['SO', 'CWTS_SO_NO', 'SO_ran_id', 'SC_cat_10', 'SC_cat_11']]
SO_cat_smaller_data = citing_SOs_SC_categories_df[['SO', 'CWTS_SO_NO', 'SO_ran_id', 'only_social', 'only_computational']]


SO_cat_smaller_data_j1 = SO_cat_smaller_data.copy()
SO_cat_smaller_data_j1.columns = [word + '_j1' for word in SO_cat_smaller_data.columns]

print(SO_cat_smaller_data_j1.shape) # (233034, 3)

# IMPORTANT: drop duplicates to reduce size of dataframe
SO_cat_smaller_data_j1.drop_duplicates(inplace = True)

print(pd.DataFrame(SO_cat_smaller_data_j1.info()))

print(SO_cat_smaller_data_j1.isna().sum())

#<class 'pandas.core.frame.DataFrame'>
#Int64Index: 38824 entries, 0 to 38823
#Data columns (total 7 columns):
#journal_auth_cosine_similarity    38824 non-null float64
#journal_1                         38824 non-null int64
#journal_2                         38824 non-null int64
#SO_j1                             38824 non-null object
#SO_ran_id_j1                      38824 non-null float64
#SC_cat_10_j1                      38824 non-null int32
#SC_cat_11_j1                      38824 non-null int32
#dtypes: float64(2), int32(2), int64(2), object(1)
#memory usage: 2.1+ MB

merged_1 = pd.merge(journal_auth_coupling_cos_sim_df, 
                    SO_cat_smaller_data_j1,
                    left_on = 'journal_1',
                    right_on = 'SO_ran_id_j1',
                    how = 'left')


print(merged_1.columns)
print(merged_1.shape) # (34027681, 6)

print(merged_1.isna().sum())

#Index(['journal_auth_cosine_similarity', 'journal_1', 'journal_2',
#       'SO_ran_id_j1', 'SC_cat_10_j1', 'SC_cat_11_j1'],
#      dtype='object')


print(pd.DataFrame(merged_1.info()))

#<class 'pandas.core.frame.DataFrame'>
#Int64Index: 38824 entries, 0 to 38823
#Data columns (total 7 columns):
#journal_auth_cosine_similarity    38824 non-null float64
#journal_1                         38824 non-null int64
#journal_2                         38824 non-null int64
#SO_j1                             38824 non-null object
#SO_ran_id_j1                      38824 non-null float64
#SC_cat_10_j1                      38824 non-null int32
#SC_cat_11_j1                      38824 non-null int32
#dtypes: float64(2), int32(2), int64(2), object(1)
#memory usage: 2.1+ MB

print(merged_1.memory_usage())

#Index                             310592
#journal_auth_cosine_similarity    310592
#journal_1                         310592
#journal_2                         310592
#SO_j1                             310592
#SO_ran_id_j1                      310592
#SC_cat_10_j1                      155296
#SC_cat_11_j1                      155296

print(merged_1.memory_usage(index=True).sum())
#2174144
#%%
#%% 11.2. get SO, SC categories for journal_2 SO_ran_id

#SO_cat_smaller_data_j2 = citing_SOs_SC_categories_df[['SO', 'CWTS_SO_NO', 'SO_ran_id', 'SC_cat_10', 'SC_cat_11']]
SO_cat_smaller_data_j2 = citing_SOs_SC_categories_df[['SO', 'CWTS_SO_NO', 'SO_ran_id', 'only_social', 'only_computational']]

SO_cat_smaller_data_j2.columns = [word + '_j2' for word in SO_cat_smaller_data.columns]

edges_classified_df = pd.merge(merged_1, 
                               SO_cat_smaller_data_j2,
                               left_on = 'journal_2',
                               right_on = 'SO_ran_id_j2',
                               how = 'left')

print(edges_classified_df.columns)

print(edges_classified_df.shape)
#
#Index(['journal_auth_cosine_similarity', 'journal_1', 'journal_2',
#       'SO_ran_id_j1', 'SC_cat_10_j1', 'SC_cat_11_j1', 'SO_ran_id_j2',
#       'SC_cat_10_j2', 'SC_cat_11_j2'],
#      dtype='object')

print(edges_classified_df.memory_usage(index=True).sum()) # 2484736

print(edges_classified_df.memory_usage())

edges_classified_df.to_csv(directory + 'edges_journals_aubibcouple_{}_{}_{}.csv'.format(cos_sim_for_filename, catf, year), index = False)


#Index                             310592
#journal_auth_cosine_similarity    310592
#journal_1                         310592
#journal_2                         310592
#SO_j1                             310592
#SO_ran_id_j1                      310592
#SC_cat_10_j1                      155296
#SC_cat_11_j1                      155296
#SO_j2                             310592
#SO_ran_id_j2                      310592
#SC_cat_10_j2                      155296
#SC_cat_11_j2                      155296

#%%
#%% 12. CREATE INTERDISCIPLINARY EDGES

print(edges_classified_df.shape) # (38824, 11)

#inter_edges_1 = edges_classified_df.loc[(edges_classified_df['SC_cat_10_j1'] == 1) & (edges_classified_df['SC_cat_11_j2'] == 1)]
inter_edges_1 = edges_classified_df.loc[(edges_classified_df['only_social_j1'] == 1) & (edges_classified_df['only_computational_j2'] == 1)]
print(inter_edges_1.shape) # catf4 (1357, 13) catf5(1386, 13) catf 6 (1641, 13) catf7 (1670, 13)

#inter_edges_2 = edges_classified_df.loc[(edges_classified_df['SC_cat_11_j1'] == 1) & (edges_classified_df['SC_cat_10_j2'] == 1)]
inter_edges_2 = edges_classified_df.loc[(edges_classified_df['only_computational_j1'] == 1) & (edges_classified_df['only_social_j2'] == 1)]
print(inter_edges_2.shape) # catf4 (1084, 13) catf5 (1141, 13) catf 6 (1393, 13) catf7  (1450, 13)

inter_edges = pd.concat([inter_edges_1, inter_edges_2])

inter_edges.to_csv(directory + 'interedges_journals_aubibcouple_{}_{}_{}.csv'.format(cos_sim_for_filename, catf, year), 
                   index = False)



#%%