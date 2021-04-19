# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:46:39 2020

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

ALGORITHM AND GOAL

1. find patterns based on term co-occurrence: TERM MAP of geosocial papers

    1.1. (probably only social + technical, not health based on my SC based classification)

2. find patterns based on citation relations: conduct community detection on author bibliographic coupling network 
    (of social and technical papers ?) (potentially: play with different granularities)
    
    for cosine similarity network AND for waltmann et al based similarity network:
        
        AND for whole network vs network filtered based on SC cat (only soc + only comp)
    
        2.1. characterise communities based on SC categories see if social and technical end 
        up in the same or similar clusters then
    
        2.2. and characterise communities by tf-idf 
            (this requires saving titles & abstracts manually, loading them into VOSviewer)
    

'''

#%%

''' 1. LOAD DATA ABOUT CITING PAPERS '''

#%% load in citing papers' data

import os
import pandas as pd

nodes_data_1_path = ('P:/thesis/thesis_final_data/collected_data/csv/' +
                     '1_all_citing_papers_data_csv/' + 
                     'ut_source_sc_finaldat.csv')

all_nodes_df = pd.read_csv(nodes_data_1_path, sep = '\t')

print(all_nodes_df.shape) # (5187, 7)

# delete row added by SQL aboout the number of rows affected
all_nodes_df  = all_nodes_df [~all_nodes_df['ut'].str.contains("rows")]
all_nodes_df  = all_nodes_df [~all_nodes_df['ut'].str.contains("Comple")]
#all_nodes_df  = all_nodes_df [~all_nodes_df['UT'].str.contains("rows")]
#all_nodes_df  = all_nodes_df [~all_nodes_df['UT'].str.contains("Comple")]
print(all_nodes_df.shape) # (5185, 7)

print(all_nodes_df.columns)

#Index(['ut', 'pub_year', 'source', 'source_id', 'doc_type',
#       'subject_category_id', 'subject_category_weight'],
#      dtype='object')

print(len(set(all_nodes_df.ut))) # 2756 -- good, same as in SSMS

print(min(all_nodes_df.pub_year)) # 2008
print(max(all_nodes_df.pub_year)) # 2019

#%% get papers' abstratcs - good file - 

# THIS IS NOT FILTERED BASED ON PUBLICATION YEAR

import pandas as pd

#abstracts = pd.read_csv("P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/ut_ab_v2.csv", sep = '\t')
abstracts = pd.read_csv("P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/ut_abstract_v3.txt", sep = '\t')

print(abstracts.shape) # (2791, 2)
abstracts.drop_duplicates(inplace = True)
print(abstracts.shape) # (2791, 2)

print(abstracts.columns) # Index(['ut', 'ab'], dtype='object')

#print(list(abstracts.ab))[:10] # Index(['ut', 'ab'], dtype='object')

# delete uts without abstract
abstracts.fillna('0', inplace = True)
abstracts_no_na = abstracts.loc[abstracts['ab'] != '0']
print(abstracts_no_na.shape) # (2763, 3)

# check max word count of abstracts
abstracts_no_na['word_count'] = abstracts_no_na['ab'].apply(lambda x: len(x.split(' ')))
print(max(abstracts_no_na['word_count'])) # 10088 - this feels too long, so I'll manually edit

# check manually

abstracts_no_na = abstracts_no_na.to_excel("P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/ut_abstract_v5.xlsx")

# editing notes - 2 ppapers' abstract was unreasonably long, I manually edited them
# 1. this paper's abstract got messsed up, was 10088 character, I manually changed it https://onlinelibrary.wiley.com/doi/abs/10.1111/bioe.12474
# 2. this paper's abstract got messed up, was 8035 characters, I manually changed it https://pubmed.ncbi.nlm.nih.gov/30194688/

#%% load manually edited file abstracts file

abstracts = pd.read_excel("P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/ut_abstract_v5_manually_edited.xlsx")

print(abstracts.shape) # (2763, 4)
abstracts.drop_duplicates(inplace = True)
print(abstracts.shape) # (2763, 4)

print(abstracts.columns) # Index(['Unnamed: 0', 'ut', 'ab', 'word_count'], dtype='object')
abstracts.drop(columns = ['Unnamed: 0'], inplace = True)
print(abstracts.columns) # Index(['ut', 'ab', 'word_count'], dtype='object')

# delete uts without abstract
abstracts.fillna('0', inplace = True)
abstracts_no_na = abstracts.loc[abstracts['ab'] != '0']
print(abstracts_no_na.shape) # (2763, 3)

# check max word count of abstracts
abstracts_no_na['word_count'] = abstracts_no_na['ab'].apply(lambda x: len(x.split(' ')))
print(max(abstracts_no_na['word_count'])) # 864

#%% get titles' files : this is manuallly edited file, with all uts and teir titles
# ALREADY DID MANUAL CLEANING ON THESE FILES - THERE WAS 1 LINE THAT GOT MESSED UP WHEN I EXPORTED DATA FROM SSMS
#I should have made more detailed notes about how I manually edited it

# THIS IS NOT FILTERED BASED ON PUBLICATION YEAR

titles = pd.read_excel("P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/ut_title_v3_manual_edit_no_duplicates.xlsx")
#print(titles.loc[titles['it']])

print(titles.shape) # (2789, 2)
titles.drop_duplicates(inplace = True)
print(titles.shape) # (2789, 2)

print(titles.shape) # (2789, 2)

print(len(list(titles.ti))) # 2789

# delete uts without abstract
titles.fillna('0', inplace = True)
titles_no_na = titles.loc[titles['ti'] != '0']
print(titles_no_na.shape) # (2789, 2)

# check max word count of abstracts
titles_no_na['word_count'] = titles_no_na['ti'].apply(lambda x: len(x.split(' ')))
print(max(titles_no_na['word_count'])) # 34 - sounds reasonable

#%% join titles and abstract files

ut_text_df = pd.merge(titles, abstracts, on = 'ut', how = 'left')

print(ut_text_df.shape) # (2789, 3)

ut_text_df.drop_duplicates(inplace = True)

print(ut_text_df.shape) # (2789, 3)
print(ut_text_df.columns) # Index(['ut', 'ti', 'ab', 'word_count'], dtype='object')

# filer based  on pub_year

# load pub_year data

pub_year_data = pd.read_csv("P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/ut_pub_year.csv", sep = '\t')
print(pub_year_data.shape) # (2791, 2)
pub_year_data  = pub_year_data [~pub_year_data['ut'].str.contains("rows")]
pub_year_data  = pub_year_data [~pub_year_data['ut'].str.contains("Comple")]
print(pub_year_data.shape) # (2791, 2)


ut_year_filt = pub_year_data.loc[(pub_year_data['pub_year'] > 2007) & (pub_year_data['pub_year'] < 2020)]
print(ut_year_filt.shape) # (2781, 2)
print(max(ut_year_filt.pub_year)) # 2019.0
print(min(ut_year_filt.pub_year)) # 2008.0

# add pub_year data to text data

ut_text_df_2 = pd.merge(ut_text_df, ut_year_filt, how = 'inner', on = 'ut')
print(ut_text_df_2.shape) # (2779, 5) 2779 PAPERS WITH ABSTRACTS, TITLES BETWEEN 2008 AND 2019
print(len(set(ut_text_df_2.ut))) # 2779 PAPERS WITH ABSTRACTS, TITLES BETWEEN 2008 AND 2019
print(ut_text_df_2.columns) # (2789, 3)
# Index(['ut', 'ti', 'ab', 'word_count', 'pub_year'], dtype='object')
print(min(ut_text_df_2.pub_year)) # 2008.0
print(max(ut_text_df_2.pub_year)) # 2019.0

# save text data to make VOSviewer term map
#ut_text_df_2[['ti', 'ab', 'pub_year']].to_csv("P:/thesis/thesis_final_data/produced_data/term_maps_data_ch7/1_all_SC_cat_VIS_DONE/terms_data/abstract_titles_all_SC_cat_ch7_v3.txt", sep = '\t', index = False)
 

#%% get papers with machine learning with abstract or title

searchterm_for_file_new = 'machine_learning'
#searchterm_for_file_new = 'social_network_analysis'

stuff3 = pd.read_excel('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/{}/ut_{}.xlsx'.format(searchterm_for_file_new, searchterm_for_file_new))
print(stuff3['ut'])
stuff3['ut_txt'] = stuff3['ut_txt'].apply(lambda x: str(x)[2:])
print(stuff3['ut_txt'])

ut_text_df_3 = ut_text_df.copy()
ut_text_df_3['ut'] = ut_text_df_3['ut'].apply(lambda x: str(x))

print(ut_text_df_3.ut[:10])
print(ut_text_df_3.columns)

stuff4 = pd.merge(stuff3[['ut_txt']], ut_text_df_3, how = 'left', left_on = 'ut_txt', right_on = 'ut')
print(stuff4.columns)

stuff4.rename(columns = {'ab' : 'AB', 'ti' : 'TI'}, inplace = True)

stuff4[['TI', 'AB']].to_csv('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/{}/ti_ab_{}.txt'.format(searchterm_for_file_new, searchterm_for_file_new), sep = '\t', index = False)
stuff4[['TI', 'AB']].to_excel('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/{}/ti_ab_{}.xlsx'.format(searchterm_for_file_new, searchterm_for_file_new), index = False)

#%% create file with all info about citing papers

all_nodes_df_alldat = pd.merge(all_nodes_df, ut_text_df_2[['ut', 'ti', 'ab',]], on = 'ut', how = 'left')

print(len(list(set(list(all_nodes_df_alldat['ut']))))) # 2756 unique uts, between 2008 and 2019 with sourcce, sc info

all_nodes_df = all_nodes_df_alldat

print(all_nodes_df.columns)
#Index(['ut', 'pub_year', 'source', 'source_id', 'doc_type',
#       'subject_category_id', 'subject_category_weight', 'subject_category',
#       'ti', 'ab'],
#      dtype='object')
print(all_nodes_df.shape) # (5185, 9)

all_nodes_df.rename(columns = {'subject_category' : 'SC',
                               'source' : 'SO',
                               'source_id' : 'CWTS_SO_NO'}, inplace = True)
    
print(all_nodes_df.columns)

#Index(['ut', 'pub_year', 'SO', 'CWTS_SO_NO', 'doc_type', 'subject_category_id',
#       'subject_category_weight', 'SC', 'ti', 'ab'],
#      dtype='object')

#%%
#%% 
#%% 

''' 2. CATEGORISE SUBJECT CATEGORIES OF CITING PAPERS'''

#%% join SC s for SC_categories function

SC_joined_df = pd.DataFrame(all_nodes_df[['SO', 'SC']].groupby('SO')['SC'].apply(lambda x: '; '.join(x))).reset_index()

print(SC_joined_df.head(5))
print(SC_joined_df.shape) # (1062, 1)

SC_joined_df.rename(columns = {'SC' : 'SC_joined'}, inplace = True)

uts_df = all_nodes_df.drop_duplicates(subset = 'ut')
uts_df.drop(columns = ['SC'], inplace = True)

all_nodes_joined_SC_df = pd.merge(uts_df,
                                  SC_joined_df,
                                  left_on = 'SO',
                                  right_on = 'SO',
                                  how = 'left')

print(all_nodes_joined_SC_df.columns)
#Index(['ut', 'pub_year', 'SO', 'CWTS_SO_NO', 'doc_type', 'subject_category_id',
#       'subject_category_weight', 'ti', 'ab', 'SC_joined'],
#      dtype='object')
print(all_nodes_joined_SC_df.shape) # (2756, 10)

print(len(list(all_nodes_joined_SC_df['SC_joined']))) # 2756

#print(set(list(all_nodes_joined_SC_df['SC_joined']))) # 2756

# change to upper case so it works with SC categories function

all_nodes_joined_SC_df['SC_joined'] = all_nodes_joined_SC_df['SC_joined'].apply(lambda x: x.upper())

#print(set(list(all_nodes_joined_SC_df['SC_joined']))) # 2756

#%% categorise subject categories of citing papers

# function description

#    Argument: a dataframe which has at least 1 column called 'SC_joined', which is a string
#              and contains information about the WOSKB subject category associated with papers 
              
#    Output: a dataframe with additional columns which signal subject category categories

import os

print("Current Working Directory " , os.getcwd()) # C:\Users\vargajv

# change working directory
os.chdir("P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/")
print("Current Working Directory " , os.getcwd())

#from SC_categories_function import SC_categories
#SC_cat_cited_edges = SC_categories(all_cited_edges_au_df_7)

from SC_categories_function import SC_categories_7

SC_cat_citing_nodes = SC_categories_7(all_nodes_joined_SC_df)
print(SC_cat_citing_nodes.columns)

#Index(['ut', 'pub_year', 'SO', 'CWTS_SO_NO', 'doc_type', 'subject_category_id',
#       'subject_category_weight', 'ti', 'ab', 'SC_joined', 'computational',
#       'social', 'multi_inter', 'all_geo', 'phys_geo', 'non_phys_geo',
#       'health', 'biol_env', 'arts_humanities', 'econ_bus_trans', 'comp_soc',
#       'comp_non_phys_geo', 'non_cat', 'only_social', 'only_non_phys_geo',
#       'only_computational'],
#      dtype='object')

#%% print SC categories

# change working directory
os.chdir("P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/")
print("Current Working Directory " , os.getcwd())

#from SC_categories_function import print_subject_categories

#print_edges = print_subject_categories(SC_cat_cited_edges)

from SC_categories_function import print_subject_categories_2

print_edges = print_subject_categories_2(SC_cat_citing_nodes)

#%% print non categorised

non_cat_df = SC_cat_citing_nodes.loc[SC_cat_citing_nodes['non_cat'] == 1]
print(non_cat_df.SC_joined) #3 papers, all art

#%% 
#%% 
#%% 

''' 3. CREATE TXT FILES FOR TERMP MAPS '''

#%% SELECCT SUBSETS OF THE DATA FOR TERM MAPS

print(SC_cat_citing_nodes.columns)
print(SC_cat_citing_nodes.shape)

#selected_df = SC_cat_citing_nodes.loc[(SC_cat_citing_nodes['computational'] == 1) | (SC_cat_citing_nodes['social'] == 1) | (SC_cat_citing_nodes['all_geo'] == 1) | (SC_cat_citing_nodes['phys_geo'] == 1) | (SC_cat_citing_nodes['non_phys_geo'] == 1)]

# select EVERYTHING THAT'S SOCIAL, COMP, GEO, OR INTERDISCIPLINARY
#selection = 'all_comp_soc_geo_inter' # 2241
#selected_df = SC_cat_citing_nodes.loc[(SC_cat_citing_nodes['computational'] == 1) | (SC_cat_citing_nodes['social'] == 1) | (SC_cat_citing_nodes['multi_inter'] == 1) | (SC_cat_citing_nodes['all_geo'] == 1) | (SC_cat_citing_nodes['arts_humanities'] == 1) | (SC_cat_citing_nodes['econ_bus_trans'] == 1)]

# select EVERYTHING
selection = 'all_SC_cat' # 
selected_df = SC_cat_citing_nodes.copy()

# select only comp + only social (to align wih simulation analysis)
#selection = 'comp_plus_soc' # 1278
#selected_df = SC_cat_citing_nodes.loc[(SC_cat_citing_nodes['only_computational'] == 1) | (SC_cat_citing_nodes['only_social'] == 1)]


# select only comp
#selection = 'only_comp' # 533
#selected_df = SC_cat_citing_nodes.loc[SC_cat_citing_nodes['only_computational'] == 1]


# select only soc
#selection = 'only_soc' # 746
#selected_df = SC_cat_citing_nodes.loc[SC_cat_citing_nodes['only_social'] == 1]


#relevant_abstracts_df = SC_cat_cited_edges.shape)

print(selected_df.shape)

selected_df.rename(columns = {'ab_full' : 'ab'}, inplace = True)
print(selected_df.columns)
# | (SC_cat_citing_nodes['multi_inter'] == 1)
print(selected_df.shape) # (2054, 28)

print(len(set(list(selected_df.ti)))) # 752
#print(set(list(selected_df.ti))) # 2053
print(len(set(list(selected_df.ab)))) # 746

selected_df.dropna(subset = ['ab', 'ti'], inplace = True)
print(len(set(list(selected_df.ti)))) # 745
print(len(set(list(selected_df.ab)))) # 745

# create directory

mypath = "P:/thesis/thesis_final_data/produced_data/term_maps_data_ch7/{}/terms_data/".format(selection)

import os
if not os.path.exists(mypath):
    os.makedirs(mypath)

selected_df[['ti', 'ab']].to_excel(mypath + "abstracts_titles_{}_ch7.xlsx".format(selection), index = False)
selected_df[['ti', 'ab']].to_csv(mypath + "abstract_titles_{}_ch7_v2.txt".format(selection), sep="\t", index = False)

selected_df[['ab']].to_excel(mypath + "abstracts_{}_ch7.xlsx".format(selection), index = False)
selected_df[['ab']].to_csv(mypath + "abstracts_{}_ch7.txt".format(selection), sep="\t", index = False)

#%%
#%%
#%%

''' 4. GET DATA ABOUT PAPERS' CITATTIONS SO I CAN CREATE AUTHOR BIBLIOGRAPHIC COUPLING NETWORK '''

#%% get infnormation about cited references with their authors, which are
# in 2 different csv files

#%%  cited refs csv

all_cited_edges_path = ('P:/thesis/thesis_final_data/collected_data/csv/' +
                         '2_all_cited_refs_data_csv/' + 
                         'geosocial_cited_ref_data_feb_2020.csv')


all_cited_edges_df = pd.read_csv(all_cited_edges_path, sep = '\t')

print(all_cited_edges_df.shape) # (64979, 2)
print(all_cited_edges_df.columns) # Index(['ut', 's_ut'], dtype='object')

# delete row added by SQL aboout the number of rows affected
all_cited_edges_df = all_cited_edges_df [~all_cited_edges_df['ut'].str.contains("rows")]
print(all_cited_edges_df.shape) # (64978, 2)

all_cited_edges_df  = all_cited_edges_df [~all_cited_edges_df['ut'].str.contains("rows")]
all_cited_edges_df  = all_cited_edges_df [~all_cited_edges_df['ut'].str.contains("Comple")]

print('number of cited refs: ' + str(len(list(set(list(all_cited_edges_df['s_ut']))))))
#number of cited refs: 44171

print('\nnumber of citing papers: ' + str(len(list(set(list(all_cited_edges_df['ut']))))))
#number of citing papers: 2791

#%% cited refs authors csv

all_cited_edges_path_2 = ('P:/thesis/thesis_final_data/collected_data/csv/' +
                          '3_all_cited_refs_data_csv/' + 
                          'cited_ref_authors_data_feb_2020.csv')


all_cited_edges_au_df = pd.read_csv(all_cited_edges_path_2, sep = '\t')

print(all_cited_edges_au_df.shape) # (163456, 4)
print(all_cited_edges_au_df.columns) # Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU'], dtype='object')

# delete row added by SQL aboout the number of rows affected
#all_cited_edges_au_df = all_cited_edges_au_df [~all_cited_edges_au_df['S_UT'].str.contains("rows")]
all_cited_edges_au_df.drop(all_cited_edges_au_df.tail(1).index,inplace=True) # drop last n rows
print(all_cited_edges_au_df.shape) # (163455, 4)

print('number of cited refs: ' + str(len(list(set(list(all_cited_edges_au_df['S_UT']))))))
# number of cited refs: 44171

#%% merge cited refs and cited authors

all_cited_edges_au_df_2 = pd.merge(all_cited_edges_au_df,
                                   all_cited_edges_df,
                                   left_on = 'S_UT',
                                   right_on = 's_ut',
                                   how = 'left')

print(all_cited_edges_au_df_2.columns)
# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut'], dtype='object')

print('number of cited refs: ' + str(len(list(set(list(all_cited_edges_au_df_2['s_ut']))))))
#number of cited refs: 44171

print('number of cited refs: ' + str(len(list(set(list(all_cited_edges_au_df_2['S_UT']))))))
#number of cited refs: 44171

print('\nnumber of citing papers: ' + str(len(list(set(list(all_cited_edges_au_df_2['ut']))))))
#number of citing papers: 2791


#%% select papers published after 2007

#%%  merge pub_year, SO and SC info to citing papers

print(all_cited_edges_au_df_2.columns)
# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut'], dtype='object')

all_cited_edges_au_df_3 = pd.merge(all_cited_edges_au_df_2,
                                   all_nodes_joined_SC_df,
                                   left_on = 'ut',
                                   right_on = 'ut',
                                   how = 'inner') # inner join to get only papers published between 2008 - 2019,
                                                  # because all_nodes_joined_SC_df is filtered based on pub_year

print(all_cited_edges_au_df_3.columns)

#Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'pub_year', 'SO',
#       'CWTS_SO_NO', 'doc_type', 'subject_category_id',
#       'subject_category_weight', 'ti', 'ab', 'SC_joined', 'computational',
#       'social', 'multi_inter', 'all_geo', 'phys_geo', 'non_phys_geo',
#       'health', 'biol_env', 'arts_humanities', 'econ_bus_trans', 'comp_soc',
#       'comp_non_phys_geo', 'non_cat', 'only_social', 'only_non_phys_geo',
#       'only_computational'],
#      dtype='object')

# check NANs

print(all_cited_edges_au_df_3.shape) # (233874, 31)
print(min(all_cited_edges_au_df_3.pub_year)) # 2008.0
print(max(all_cited_edges_au_df_3.pub_year)) # 2019.0

nas = all_cited_edges_au_df_3[all_cited_edges_au_df_3['pub_year'].isnull()] # (0, 31)
print(nas.shape) 

print('\nnumber of cited refs without publication year info: ' + str(len(list(set(list(nas['ut']))))))
# number of cited refs without publication year info: 0


#%% 
#%% 

'''
    5. CREATE AUTHOR BIBLIOGRAPHIC COUPLING NETWORK
    
    NEED TO MANUALLY REPEAT FROM HERE FOR EACH NETWORK BASED ON SC FILTER AND MATRIX NORM TILL LINE 1535
    
        SC_filters:    
            all_SC_Filt: no filter based on SC categories
            comp_SOC: network where only nodes whcih are only computational and only social included
        
        Matrix norm: 
            cosine similarity
            waltmann et al.
'''

#%% OPTIONAL: FILTER BASED SC CAT THE PAPERS TO DO COMMUNITY DETECTION ON

'''
    MANUAL INPUT REQUIRED: FILTER BASED SC CAT THE PAPERS TO DO COMMUNITY DETECTION ON
'''

print(SC_cat_citing_nodes.columns)

#Index(['ut', 'pub_year', 'SO', 'CWTS_SO_NO', 'doc_type', 'subject_category_id',
#       'subject_category_weight', 'ti', 'ab', 'SC_joined', 'computational',
#       'social', 'multi_inter', 'all_geo', 'phys_geo', 'non_phys_geo',
#       'health', 'biol_env', 'arts_humanities', 'econ_bus_trans', 'comp_soc',
#       'comp_non_phys_geo', 'non_cat', 'only_social', 'only_non_phys_geo',
#       'only_computational'],
#      dtype='object')

# OPTION 1: no filter based on SC CAT
#SC_filter = 'all_SC_cat' # 
#selected_df = SC_cat_citing_nodes.copy()
#print(selected_df.shape) # (2756, 26)


# OPTION 2: select only comp + only social (to align wih simulation analysis)
SC_filter = 'comp_plus_soc' # 1278
selected_df = SC_cat_citing_nodes.loc[(SC_cat_citing_nodes['only_computational'] == 1) | (SC_cat_citing_nodes['only_social'] == 1)]
print(selected_df.shape) # (1319, 26)

# old version:
#'''MANUAL EDIT REQUIRED: FILTER NETWORK BASED ON SC_CAT'''
#
## OPTION 1: only comp + only soc
##citing_cited_edges = all_cited_edges_au_df_3
##SC_filter = 'comp_soc_SC_cat'
#
## OPTION 2: all SC cat
#citing_cited_edges = all_cited_edges_au_df_2
#SC_filter = 'all_SC_cat'


#%% add cited author info to selected df

print(all_cited_edges_au_df_2.columns) # Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut'], dtype='object')
print(all_cited_edges_au_df_2.shape)


all_cited_edges_au_df_3 = pd.merge(selected_df['ut'], all_cited_edges_au_df_2, on = 'ut', how = 'inner')
print(all_cited_edges_au_df_3.shape)
print(len(list(set(list(all_cited_edges_au_df_3['ut']))))) # 2756

citing_cited_edges = all_cited_edges_au_df_3.copy()

#%% create numeric id for ut s

ut_num_id_df = pd.DataFrame()

ut_num_id_df['ut'] = list(set(list(citing_cited_edges['ut'])))
ut_num_id_df['ut_ran_id'] = ut_num_id_df.index

print(ut_num_id_df.head(5))

#%% merge citing papers and radnom numeric ids

SC_cat_cited_edges_2 = pd.merge(citing_cited_edges,
                                ut_num_id_df,
                                left_on = 'ut',
                                right_on = 'ut',
                                how = 'left')

print(SC_cat_cited_edges_2.columns)
# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'ut_ran_id'], dtype='object')


print('number of cited refs: ' + str(len(list(set(list(SC_cat_cited_edges_2['s_ut']))))))
#number of cited refs: 43586

print('number of cited refs: ' + str(len(list(set(list(SC_cat_cited_edges_2['S_UT']))))))
#number of cited refs: 43586

print('\nnumber of citing papers: ' + str(len(list(set(list(SC_cat_cited_edges_2['ut']))))))
#number of citing papers: 2756 or 1319

print('\nnumber of citing papers: ' + str(len(list(set(list(SC_cat_cited_edges_2['ut_ran_id']))))))
#number of citing papers: 2756 or 1319


#%% check nas

nan_rows = SC_cat_cited_edges_2[SC_cat_cited_edges_2['AU'].isnull()]
print(nan_rows.shape) # (110, 7)

print('\nnumber of cited refs without author info: ' + str(len(list(set(list(nan_rows['s_ut']))))))
# number of cited refs without author info: 26

print('\nnumber of citing papers which have cited ref without author info: ' + str(len(list(set(list(nan_rows['ut']))))))
# number of cited refs without author info: 109

#%% drop na
print(SC_cat_cited_edges_2.shape) # (233874, 7) or for comp soc (71171, 7)

SC_cat_cited_edges_3 = SC_cat_cited_edges_2[['ut', 'AU', 'ut_ran_id']]
SC_cat_cited_edges_3.dropna(inplace = True)
print(SC_cat_cited_edges_3.shape) # (233765, 3) or for comp soc (71171, 7)

print(min(SC_cat_cited_edges_3['ut_ran_id'])) # 0
print(max(SC_cat_cited_edges_3['ut_ran_id'])) # 2755 or 1318 for comp soc

#%% delete duplicate edges
# one paper can cite the same authro multiple times but that's not important for me
SC_cat_cited_edges_3.drop_duplicates(inplace = True) 
print(SC_cat_cited_edges_3.shape) # for comp soc (63502, 3)


#%%

print(SC_cat_cited_edges_3.columns)
# Index(['ut', 'AU', 'ut_ran_id'], dtype='object')
print(SC_cat_cited_edges_3.shape) # (204507, 3)
#%% 
#%%CHOOSE METHOD TO CALCULATE AUTHOR BIBLIOGRAPHIC COUPLING NETWORK EDGE WEIGHTS

''' 
    
    6. CREATE AUTHOR BIB COUPLE NETWORK

        CHOOSE METHOD TO CALCULATE AUTHOR BIBLIOGRAPHIC COUPLING NETWORK EDGE WEIGHTS    
        MANUAL INPUT REQUIRED: CHOOSE MATRIX NORMALISATION METHOD
            IF OPTION 1: 'cosine_similarity_norm': author bibliograohic coupling edges are calculated based on cosine similarity
            IF OPTION 2: 'waltmann_etal' : author bibliograohic coupling edges are calculated based on Waltmann et al. 2020
        
'''
#%%
#%% OPTION 1
# CALCULATE COSINE SIMILARITY among citing 'journals' - for journals' co-author coupling

matrixnorm = 'norm_cosine_similarity'

print("Current Working Directory " , os.getcwd())

#files = [f for f in os.listdir('.') if os.path.isfile(f)] # lists files in working directory
#for f in files:
#    print(f)
    
# change working directory
os.chdir("P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts")
print("Current Working Directory " , os.getcwd())

import bib_couple_cosine_similarity

#    Arguments:
#        1. edges_df: dataframe with info about citing papers' cited references. 
#        The df needs to have at least 2 columns (the ones capitaled below)
#        but this code is written for a dataframe with the following 3 columns:
#            i.  first column (to the left): id of the citing papers
#            ii. SECOND COLUMN (to the right): id of the cited papers
#            iii. THIRD COLUMN: NUMERIC ID OF CITING PAPERS. 

# columns of the journal co-author dataframe to be used: Index(['SO', 'AU_NO', 'SO_ran_id'], dtype='object')

cos_sim = 0
cos_sim_for_filename = str(cos_sim).replace('.', '_')

papers_auth_coupling_cos_sim_df = bib_couple_cosine_similarity.bib_couple_cos_similarity_df(SC_cat_cited_edges_3, cos_sim)


# check bib coupling df

print(papers_auth_coupling_cos_sim_df.shape)


papers_auth_coupling_cos_sim_df.columns = ['weight', 'paper_1', 'paper_2']

print(papers_auth_coupling_cos_sim_df.head(5))

papers_auth_coupling_cos_sim_df_2 = papers_auth_coupling_cos_sim_df[['paper_1', 'paper_2', 'weight']]

print(papers_auth_coupling_cos_sim_df_2.head(5))

#%% sampel code

a = ['p1', 'p1','p2','p2','p2','p3','p3','p3']
b = ['a1', 'a2','a1','a3','a4','a3','a2','a5']
c = ['1', '1','2','2','2','3','3','3']
df = pd.DataFrame()
df['p'] = a
df['au'] = b
df['ran_id'] = c
df2 = df.copy()
df2.rename(columns = {'p': 'p2', 'ran_id' : 'ran_id2'}, inplace = True)
r_edges = pd.merge(df, df2, on = 'au', how = 'left')  # this returns all combinations of the citing papers
r_edges_2 = r_edges.loc[r_edges['ran_id'] != r_edges['ran_id2']]
print(r_edges_2) # this does return all combinations of edges
#%% OPTION 2: PAPERS - AUTHOR BIBLIOGAPHIC COUPLING NETWORK

matrixnorm = 'norm_waltmann_etal'

print(SC_cat_cited_edges_3.shape) # (207019, 3) # for comp soc (63502, 3)
print(SC_cat_cited_edges_3.columns) # Index(['ut', 'AU', 'ut_ran_id'], dtype='object')


# calcualte number of shared authors between papers (raw author bibliographic coupling count)

SC_cat_cited_edges_4 = SC_cat_cited_edges_3.copy()
SC_cat_cited_edges_4.rename(columns = {'ut' : 'ut_2',
                                       'ut_ran_id' : 'ut_ran_id_2'}, inplace = True)

raw_edges = pd.merge(SC_cat_cited_edges_3, SC_cat_cited_edges_4, on = 'AU', how = 'left')
print(raw_edges.shape) # for comp soc (531612, 5)

# delete edges between the same paper (loops)
raw_edges_2 = raw_edges.loc[raw_edges['ut_ran_id_2'] != raw_edges['ut_ran_id']]
print(raw_edges_2.shape) # (2246296, 5) # for comp soc (468110, 5)
print(raw_edges_2.columns) # (2246296, 5)

# group by edges 

raw_edges_3 = pd.DataFrame(raw_edges_2[['ut_ran_id', 'ut_ran_id_2', 'AU']].groupby(['ut_ran_id', 'ut_ran_id_2']).count()).reset_index()
raw_edges_3.rename(columns = {'AU' : 'raw_shared_cited_au',
                              'ut_ran_id' : 'p1',
                              'ut_ran_id_2' : 'p2'}, inplace = True)
print(raw_edges_3.shape) # (802412, 2) for comp soc  (169260, 3)
print(raw_edges_3.head(20)) # (802412, 3)
print(raw_edges_3.columns) # (802412, 3)

# TODO ADDED NOV 23, TO RERUN

#raw_edges_4 = pd.DataFrame(raw_edges_2[['ut_ran_id', 'ut_ran_id_2', 'AU']].groupby(['ut_ran_id_2', 'ut_ran_id']).count()).reset_index()
#raw_edges_4.rename(columns = {'AU' : 'raw_shared_cited_au',
#                              'ut_ran_id_2' : 'p1',
#                              'ut_ran_id' : 'p2'}, inplace = True)
#print(raw_edges_4.shape) # (802412, 2)
#print(raw_edges_4.head(20)) # (802412, 3)
#print(raw_edges_4.columns) # (802412, 3)
#
#raw_edges_5 = pd.concat([raw_edges_3, raw_edges_4])
#print(raw_edges_5.shape) # (802412, 2)
#print(raw_edges_5.head(20)) # (802412, 3)
#print(raw_edges_5.columns) # (802412, 3)

#%% normalise raw au bib coupling

all_connections_ut_ran_id = pd.DataFrame(raw_edges_3[['p1','raw_shared_cited_au']].groupby('p1').sum()).reset_index()
all_connections_ut_ran_id.rename(columns = {'raw_shared_cited_au' : 'all_connections_p1'}, inplace = True)
print(all_connections_ut_ran_id.shape) # for comp soc  (1229, 2), realistic since I had 1319 papers and some have no citation  info
print(all_connections_ut_ran_id.head(20))

raw_edges_6 = pd.merge(raw_edges_3, all_connections_ut_ran_id, on = 'p1', how = 'left')
print(raw_edges_6.columns)
#Index(['ut_ran_id', 'ut_ran_id_2', 'raw_shared_cited_au',
#       'all_connections_ut_ran_id'],
#      dtype='object')
print(raw_edges_6.shape) # (338520, 4) for comp soc  (169260, 3)

#%%

normalised_edge_1 = raw_edges_6.copy()
normalised_edge_1['norm_AU_bibcouple'] = normalised_edge_1['raw_shared_cited_au'] / normalised_edge_1['all_connections_p1']
print(normalised_edge_1.columns)

# delete duplicate edges

# create tule from nodes in edges
normalised_edge_1['edge_tuple'] = list(zip(normalised_edge_1.p1, normalised_edge_1.p2))

# sort tule from nodes in edges
normalised_edge_1['edge_tuple'] = normalised_edge_1['edge_tuple'].apply(lambda x : tuple(sorted(x)))

print(normalised_edge_1['edge_tuple'].head(5))
print(normalised_edge_1.shape) # (338520, 6) for comp asn soc (169260, 6)
print(normalised_edge_1.columns)

#Index(['p1', 'p2', 'raw_shared_cited_au', 'all_connections_p1',
#       'norm_AU_bibcouple', 'edge_tuple'],
#      dtype='object')


normalised_edge_2 = pd.DataFrame(normalised_edge_1[['edge_tuple', 'norm_AU_bibcouple']].groupby('edge_tuple').mean()).reset_index()

normalised_edge_2['paper_1'] = [i[0] for i in list(normalised_edge_2['edge_tuple'])]
normalised_edge_2['paper_2'] = [i[1] for i in list(normalised_edge_2['edge_tuple'])]
normalised_edge_2['weight'] = normalised_edge_2['norm_AU_bibcouple']
normalised_edge_2.drop(columns = ['edge_tuple', 'norm_AU_bibcouple'], inplace = True)

print(normalised_edge_2.shape) # for comp as soc (84630, 3)
print(normalised_edge_2.columns)
# Index(['paper_1', 'paper_2', 'weight'], dtype='object')

#print(normalised_edge_2.head(5))
#print(normalised_edge_1.head(5))

papers_auth_coupling_cos_sim_df = normalised_edge_2.copy()

# check
print(papers_auth_coupling_cos_sim_df.columns) # Index(['paper_1', 'paper_2', 'weight'], dtype='object')
#%%
print(normalised_edge_1.shape) # (338520, 6)
print(normalised_edge_2.shape) # (84630, 3)

# 338520 / 84630 = 4
#%%

'''
    PREPARE NETWORK EDGE DATA FOR COMMUNITY DETECTION
'''
#%% add new node ids for leiden alg, i think it's messed up for not having nodes 1-incremental

# add uts 

papers_auth_coupling_cos_sim_df_2 = pd.merge(papers_auth_coupling_cos_sim_df,
                                             ut_num_id_df,
                                             left_on = 'paper_1', right_on = 'ut_ran_id', how = 'left')

papers_auth_coupling_cos_sim_df_2.rename(columns = {'ut' : 'paper_1_ut'}, inplace = True)
papers_auth_coupling_cos_sim_df_2.drop(columns = ['ut_ran_id'], inplace = True)

print(papers_auth_coupling_cos_sim_df_2.columns)

#Index(['weight', 'paper_1', 'paper_2', 'paper_1_ut'], dtype='object')

print(papers_auth_coupling_cos_sim_df_2.head(5))

#

papers_auth_coupling_cos_sim_df_3 = pd.merge(papers_auth_coupling_cos_sim_df_2,
                                             ut_num_id_df,
                                             left_on = 'paper_2', right_on = 'ut_ran_id', how = 'left')

papers_auth_coupling_cos_sim_df_3.rename(columns = {'ut' : 'paper_2_ut'}, inplace = True)
papers_auth_coupling_cos_sim_df_3.drop(columns = ['ut_ran_id'], inplace = True)

print(papers_auth_coupling_cos_sim_df_3.columns)

#Index(['weight', 'paper_1', 'paper_2', 'paper_1_ut', 'paper_2_ut'], dtype='object')

#%%
# create new random id

ut_num_id_df_2 = pd.DataFrame()

ut_num_id_df_2['ut'] = list(set(list(papers_auth_coupling_cos_sim_df_3['paper_1_ut']) + list(papers_auth_coupling_cos_sim_df_3['paper_2_ut'])))
ut_num_id_df_2['ut_ran_id'] = ut_num_id_df_2.index

print(ut_num_id_df_2.head(5))

print(min(ut_num_id_df_2.ut_ran_id))
print(max(ut_num_id_df_2.ut_ran_id))

#%% add new random id

# node 1

papers_auth_coupling_cos_sim_df_4 = pd.merge(papers_auth_coupling_cos_sim_df_3,
                                             ut_num_id_df_2,
                                             left_on = 'paper_1_ut', right_on = 'ut', how = 'left')

papers_auth_coupling_cos_sim_df_4.rename(columns = {'ut_ran_id' : 'paper_1_new_ran_id'}, inplace = True)
papers_auth_coupling_cos_sim_df_4.drop(columns = ['ut'], inplace = True)

print(papers_auth_coupling_cos_sim_df_4.columns)

# node 2

papers_auth_coupling_cos_sim_df_5 = pd.merge(papers_auth_coupling_cos_sim_df_4,
                                             ut_num_id_df_2,
                                             left_on = 'paper_2_ut', right_on = 'ut', how = 'left')

papers_auth_coupling_cos_sim_df_5.rename(columns = {'ut_ran_id' : 'paper_2_new_ran_id'}, inplace = True)
papers_auth_coupling_cos_sim_df_5.drop(columns = ['ut'], inplace = True)

print(papers_auth_coupling_cos_sim_df_5.columns)

print(papers_auth_coupling_cos_sim_df_5.head(5))

print(papers_auth_coupling_cos_sim_df_5[['paper_1', 'paper_2', 'paper_1_new_ran_id', 'paper_2_new_ran_id']].head(5))

#%%

papers_auth_coupling_cos_sim_df_6 = papers_auth_coupling_cos_sim_df_5[['paper_1_new_ran_id', 'paper_2_new_ran_id', 'weight']]

print(papers_auth_coupling_cos_sim_df_6.head(5))

print(min(papers_auth_coupling_cos_sim_df_6.paper_1_new_ran_id)) # 0
print(max(papers_auth_coupling_cos_sim_df_6.paper_1_new_ran_id)) # 2662
#%% 

'''
    DO COMMUNITY DETECTION
'''

#%% create igrah graph object

import igraph as ig
import leidenalg as la

SG = ig.Graph.TupleList(papers_auth_coupling_cos_sim_df_6.values, 
                        weights=True, directed=False)

#from igraph import Graph
#
#tuples = [tuple(x) for x in papers_auth_coupling_cos_sim_df_6.values]
#SG2 = ig.Graph.TupleList(tuples, directed = True, edge_attrs = ['weight'])

#{v['name']: v.index for v in list(SG2.vs)}

print(SG.vs[0:10]["name"])
#print(SG2.vs[0:10]["name"])

print(papers_auth_coupling_cos_sim_df_6.head(5))

print(type(SG))
print(SG.is_weighted())
print(SG.ecount())
print(SG.get_edgelist()[0:10])

#print(type(SG2))
#print(SG2.is_weighted())
#print(SG2.ecount())
#print(SG2.get_edgelist()[0:10])

#%% this only does modularity schore, or somehting, what I need is partition
#communities = SG.community_leiden(objective_function= "modularity", weights = 'weight')
##print(communities[0])
##print(type(communities))
##print(communities)
#
##print(len(communities.membership)) # I think this is the membership of each node
#
#cluster_list = list(communities)
##print(cluster_list[0])

#%%

'''

    OK so here's the story:
        the partition = la.find_partition(SG, la.ModularityVertexPartition) returns the nodes partitioned
        into communities
        
        BUT
        
        when I transform this into a dataframe, instead of the nodes' names, their ids are displayed 
        that igraph assigns them in the order they appear in the edge list
        
        to get the nodes back: first save the partition into a dataframe, transpose this
        so that each column corresponds to node ids in a cluster
        
        then get vertex_names and vertex_ids (see code below)
        
        and finally do multiple join: join each column which corresponds to a cluster
        on node ids
'''

#%% detect communities

partition = la.find_partition(SG, la.ModularityVertexPartition)
print(type(partition))
print(len(partition))
df1 = pd.DataFrame(partition)
print(partition)
#print(partition[0])

df_nodepartition_transposed = df1.T

#print(df1_transposed.shape)

print(df_nodepartition_transposed.head(10))

vertex_names = pd.DataFrame()
vertex_names['names'] = SG.vs[:]["name"]
vertex_names['id'] = vertex_names.index
print(vertex_names.shape)

print(SG.vs[0:10]["name"])

print(vertex_names.columns)
#Index(['names', 'id'], dtype='object')

#%% check data

#print(vertex_names[vertex_names['id'] == 377]) # 793
#print(vertex_names[vertex_names['id'] == 378]) # 1112
#print(vertex_names[vertex_names['id'] == 838]) # 452
#print(vertex_names[vertex_names['id'] == 839]) # 1707

#cluster_list = list(communities)
#print(cluster_list[0])
#ig.plot(communities)
#NG = ig.cluster_graph(communities, combine_vertices=None, combine_edges=None)

#%% add node random ids (node names) to df with node ids partitioned
#%% to create a dataframe with nodes' communities


df_nodepartition_transposed.columns = ['cluster_' + str(column) for column in df_nodepartition_transposed.columns]

columns_list = df_nodepartition_transposed.columns

df_list = []

for column in columns_list:
    print(column)
    df_nodepartition_transposed_merged = pd.merge(df_nodepartition_transposed[[str(column)]],
                                                  vertex_names,
                                                  left_on = str(column), right_on = 'id', how = 'left')
    
    df_nodepartition_transposed_merged['cluster'] = column
    df_nodepartition_transposed_merged.rename(columns = {'names' : 'node_names',
                                                         'id' : 'igraph_node_id'}, inplace = True)
    df_nodepartition_transposed_merged.drop(columns = [column], inplace = True)
    
    #df_nodepartition_transposed_merged.rename(columns = {'names' : 'node_names_' + str(column)}, inplace = True)
    #df_nodepartition_transposed_merged.drop(columns = ['id'], inplace = True)
    
    df_nodepartition_transposed_merged.dropna(inplace = True)
    
    print(df_nodepartition_transposed_merged.columns)
    print(df_nodepartition_transposed_merged.head(5))
    
    df_list.append(df_nodepartition_transposed_merged)

#%%  create 1 dataframe with nodes and their communities
    
communities_nodes_df = pd.concat(df_list, axis = 0)
print(communities_nodes_df.columns) # Index(['node_names', 'igraph_node_id', 'cluster'], dtype='object')
print(communities_nodes_df.shape)

# delete 'cluster_' from cluster name

communities_nodes_df['cluster'] = communities_nodes_df['cluster'].apply(lambda x: x[8:])

#Index(['node_names', 'igraph_node_id', 'cluster'], dtype='object')
#(2636, 3)

#%% ADD UT TO NODES

print(ut_num_id_df_2.columns) #Index(['ut', 'ut_ran_id'], dtype='object')
print(ut_num_id_df_2.shape) #(2636, 2)

print(communities_nodes_df.shape) # (2636, 3)

communities_nodes_df_ut = pd.merge(communities_nodes_df, ut_num_id_df_2,
                                   left_on = 'node_names', right_on = 'ut_ran_id', how = 'left')

communities_nodes_df_ut.drop(columns = ['ut_ran_id'], inplace = True)

print(communities_nodes_df_ut.columns) #Index(['node_names', 'igraph_node_id', 'cluster', 'ut'], dtype='object')
print(communities_nodes_df_ut.shape) #(2636, 4)

#%% 

#%%
'''
    CREATE NETWORK WHERE NODES ARE CLUSTERS
    
    CALCULATE EDGES BETWEEN COMMUNITIES
'''

#%% merge nodes' community with cos_sim edges

cos_sim_edges_and_comm = pd.merge(papers_auth_coupling_cos_sim_df_5,
                                  communities_nodes_df,
                                  left_on = 'paper_1_new_ran_id',
                                  right_on = 'node_names',
                                  how = 'left')

cos_sim_edges_and_comm.rename(columns = {'cluster' : 'paper_1_community'}, inplace = True)
cos_sim_edges_and_comm.drop(columns = ['node_names'], inplace = True)

print(cos_sim_edges_and_comm.head(10))

#%%

cos_sim_edges_and_comm_2 = pd.merge(cos_sim_edges_and_comm,
                                    communities_nodes_df,
                                    left_on = 'paper_2_new_ran_id',
                                    right_on = 'node_names',
                                    how = 'left')

cos_sim_edges_and_comm_2.rename(columns = {'cluster' : 'paper_2_community'}, inplace = True)
cos_sim_edges_and_comm_2.drop(columns = ['node_names'], inplace = True)

print(cos_sim_edges_and_comm_2.columns)

#Index(['paper_1', 'paper_2', 'weight', 'paper_1_community',
#       'paper_2_community'],
#      dtype='object')

print(cos_sim_edges_and_comm_2[['paper_1', 'paper_2']].head(10))
print(cos_sim_edges_and_comm_2[['paper_1_community', 'paper_2_community']].head(10))
print(cos_sim_edges_and_comm_2.shape)
#%% calculate edges between communities
#%% calculate edges between communities and reorder tuples so there's no duplicate edges

cos_sim_edges_and_comm_2['edges_between_comm'] = list(zip(cos_sim_edges_and_comm_2.paper_1_community, cos_sim_edges_and_comm_2.paper_2_community))
cos_sim_edges_and_comm_2['weighted_edges_between_comm'] = list(zip(cos_sim_edges_and_comm_2.paper_1_community, cos_sim_edges_and_comm_2.paper_2_community))

cos_sim_edges_and_comm_2['edges_between_comm'] = cos_sim_edges_and_comm_2['edges_between_comm'].apply(lambda x : tuple(sorted(x)))
cos_sim_edges_and_comm_2['weighted_edges_between_comm'] = cos_sim_edges_and_comm_2['weighted_edges_between_comm'].apply(lambda x : tuple(sorted(x)))

print(cos_sim_edges_and_comm_2['edges_between_comm'].head(5))
print(cos_sim_edges_and_comm_2['weighted_edges_between_comm'].head(5))

#%%

inter_comm_edges = cos_sim_edges_and_comm_2[['edges_between_comm', 'paper_1']].groupby('edges_between_comm').count().reset_index()
inter_comm_edges.rename(columns = {'paper_1' : 'edge_count'}, inplace = True)

inter_comm_edges_weight = cos_sim_edges_and_comm_2[['edges_between_comm', 'weight']].groupby('edges_between_comm').mean().reset_index()

print(inter_comm_edges.head(15))
print(inter_comm_edges_weight.head(15))

#%% create 1 dataframe with edges between comm, their count and weight

inter_comm_edges_2 = pd.merge(inter_comm_edges,
                              inter_comm_edges_weight,
                              on = 'edges_between_comm',
                              how = 'left')

print(inter_comm_edges_2.columns)
# Index(['edges_between_comm', 'edge_count', 'Weight'], dtype='object')
print(inter_comm_edges_2.head(10))

#%%

#%% count percentegae of links between communities

# calculate edges related to each cluster (keep in mind, some edges are counted twice, e.g. 0 -> 1 and 1 -> 0)

number_of_communities = list(set(list(communities_nodes_df['cluster'])))

print(number_of_communities)

all_edges_of_all_communities = {}


for i in number_of_communities:
    print(i)
    all_edges_of_all_communities[i] = []
    
    for index, row in inter_comm_edges.iterrows():

        if row['edges_between_comm'][0] == str(i):
            all_edges_of_all_communities[i].append(row['edge_count'])

for key, item in all_edges_of_all_communities.items():
    print(key)
    print(item)
   
# add up number od edges associated with each community
all_edges_of_all_communities_2 = all_edges_of_all_communities

for key, item in all_edges_of_all_communities_2.items():
    all_edges_of_all_communities_2[key] = sum(item)
    
#for key, item in all_edges_of_all_communities_2.items():
    #print(key)
    #print(item)

all_edges_of_all_communities_df = pd.DataFrame.from_dict(all_edges_of_all_communities_2, orient='index').reset_index()
all_edges_of_all_communities_df.rename(columns = {'index' : 'community',
                                                  0 : 'number_of_edges'}, inplace = True)

print(all_edges_of_all_communities_df)
#%% calculate percentage of edges between communities

# split communities tuple into 2 columns
    
inter_comm_edges_2['comm_1'] = list(i[0] for i in list(inter_comm_edges_2['edges_between_comm']))
inter_comm_edges_2['comm_2'] = list(i[1] for i in list(inter_comm_edges_2['edges_between_comm']))

print(inter_comm_edges_2)

#%%
print(all_edges_of_all_communities_df)
#%%

inter_comm_edges_3 = pd.merge(inter_comm_edges_2,
                              all_edges_of_all_communities_df,
                              left_on = 'comm_1',
                              right_on = 'community',
                              how = 'left')

inter_comm_edges_3.rename(columns = {'number_of_edges' : 'n_edges_comm_1'}, inplace = True)
inter_comm_edges_3.drop(columns = ['community'], inplace = True)

inter_comm_edges_4 = pd.merge(inter_comm_edges_3 ,
                              all_edges_of_all_communities_df,
                              left_on = 'comm_2',
                              right_on = 'community',
                              how = 'left')

inter_comm_edges_4.rename(columns = {'number_of_edges' : 'n_edges_comm_2'}, inplace = True)
inter_comm_edges_4.drop(columns = ['community'], inplace = True)

print(inter_comm_edges_4.columns)
# Index(['edges_between_comm', 'edge_count', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2'],
#      dtype='object')

#Index(['edges_between_comm', 'edge_count', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_1', 'n_edges_comm_2'],
#      dtype='object')

print(inter_comm_edges_4.head(5))


#%% add up umber of edges

inter_comm_edges_4['all_edges'] = 0

for index_label, row_series in inter_comm_edges_4.iterrows():
    #print(index_label)
    #print(row_series)
    
    if row_series['comm_1'] == row_series['comm_2']:
        inter_comm_edges_4.at[index_label, 'all_edges'] = row_series['n_edges_comm_1']

    else:
        inter_comm_edges_4.at[index_label, 'all_edges'] = row_series['n_edges_comm_1'] + row_series['n_edges_comm_2']

print(inter_comm_edges_4[['comm_1', 'comm_2', 'all_edges']].head(20))
print(inter_comm_edges_4.columns)
#Index(['edges_between_comm', 'edge_count', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2', 'all_edges'],
#      dtype='object')


#%% calculate percentage of edges between communites

inter_comm_edges_4['percentage_inter_edges'] = inter_comm_edges_4['edge_count'] / inter_comm_edges_4['all_edges'] 
#print(inter_comm_edges_3['percentage_inter_edges'])

inter_comm_edges_4['weighted_percentage_inter_edges'] = inter_comm_edges_4['percentage_inter_edges']  *  inter_comm_edges_4['weight']

print(inter_comm_edges_4.columns)

#Index(['edges_between_comm', 'edge_count', 'Weight', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2', 'all_edges',
#       'percentage_inter_edges', 'weighted_percentage_inter_edges'],
#      dtype='object')
#%% drop edges between same nodes

print(inter_comm_edges_4.shape) # (38, 10)
print(inter_comm_edges_4.columns)

#Index(['edges_between_comm', 'edge_count', 'Weight', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2', 'all_edges',
#       'percentage_inter_edges', 'weighted_percentage_inter_edges'],
#      dtype='object')

inter_comm_edges_5 = inter_comm_edges_4[inter_comm_edges_3['comm_1'] != inter_comm_edges_4['comm_2']]

print(inter_comm_edges_5.shape) # (6, 10)
print(inter_comm_edges_5) # (6, 10)

#%% OLD CODE get size of each community

#community_size = communities_nodes_df[['cluster', 'node_names']].groupby('cluster').count().reset_index()
#community_size.rename(columns = {'node_names' : 'cluster_size'}, inplace = True)
#print(community_size)


#%%
'''
    prepare NODES AND EDGES cluster network for R netvis
'''
#%% prepare NODES cluster network for R netvis

cluster_size = pd.DataFrame(communities_nodes_df_ut[['ut', 'cluster']].groupby('cluster').count()).reset_index()
cluster_size.rename(columns = {'ut' : 'size',
                               'cluster' : 'id'}, inplace = True)
print(cluster_size.columns) # Index(['id', 'size'], dtype='object')
print(cluster_size.shape) # (6, 2)

print(cluster_size) # (6, 2)

mypath = "P:/thesis/thesis_final_data/produced_data/clusters_network_nodes_edges_ch7/{}_{}_v2/".format(SC_filter, matrixnorm)

import os
if not os.path.exists(mypath):
    os.makedirs(mypath)

cluster_size.to_csv(mypath + "clusters_nodes_{}_{}_v2.csv".format(SC_filter, matrixnorm), index = False)

#%% prepare EDGES cluster network for R netvis

edges_df = inter_comm_edges_5[[ 'comm_1', 'comm_2', 'weighted_percentage_inter_edges']]

edges_df.rename(columns = {'comm_1' : 'from',
                           'comm_2' : 'to', 
                           'weighted_percentage_inter_edges' : 'weight'}, inplace = True)
print(edges_df.columns)
print(edges_df.shape)

edges_df['weight'] = edges_df['weight']

print(edges_df)

mypath = "P:/thesis/thesis_final_data/produced_data/clusters_network_nodes_edges_ch7/{}_{}/".format(SC_filter, matrixnorm)

import os
if not os.path.exists(mypath):
    os.makedirs(mypath)

edges_df.to_csv(mypath + "clusters_edges_{}_{}_v2.csv".format(SC_filter, matrixnorm), index = False)
#%%



#%%
'''
    OLD CODE
'''

#%% OLD CODE:  create a dataframe with nodes' communities - this code is not good because it
# concatenates the node ids to node names

#communities_df_dict = []
#
#for i in range(0, len(communities)):
#    print(communities[i])
#    
#    df = pd.DataFrame()
#    df['nodes'] = communities[i]
#    df['community'] = i
#    communities_df_dict.append(df)
#
#communities_nodes_df = pd.concat(communities_df_dict)
#
#print(communities_nodes_df.shape)
##optimiser = la.Optimiser()
#
##profile = optimiser.resolution_profile(SG, la.CPMVertexPartition, resolution_range=(0,1))
##%%
#print(communities_nodes_df.head(50))
#
#print(min(communities_nodes_df.nodes)) # 0
#print(max(communities_nodes_df.nodes)) # 2666


#%%
#%%
'''
    PREPARE DATA FOR SC BARCHARTS FOR EACH CLUSTER
'''

#%%

'''
    GET JOINED SC FOR EACH UT
'''

#%%  get SC cat for each node

print(SC_cat_citing_nodes.shape)
print(SC_cat_citing_nodes.columns)

#Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'pub_year', 'SO',
#       'CWTS_SO_NO', 'ab_full', 'ti', 'pub_year_y', 'SC_joined',
#       'computational', 'social', 'multi_inter', 'all_geo', 'phys_geo',
#       'non_phys_geo', 'health', 'biol_env', 'arts_humanities',
#       'econ_bus_trans', 'comp_soc', 'comp_non_phys_geo', 'non_cat',
#       'only_social', 'only_non_phys_geo', 'only_computational'],
#      dtype='object')

#SC_cat_citing_nodes.drop(columns = ['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 's_ut','SO',
#                                     'CWTS_SO_NO', 'ab_full', 'ti', 'pub_year_y'], inplace = True)

SC_cat_uts = SC_cat_citing_nodes.drop_duplicates(subset = 'ut')
print(SC_cat_citing_nodes.shape) # (2756, 26)

# add SC joined info to nodes communities df

community_nodes_SC = pd.merge(communities_nodes_df_ut, SC_cat_uts,
                             on = 'ut', how = 'left')

print(community_nodes_SC.columns)

#Index(['node_names', 'igraph_node_id', 'cluster', 'ut', 'pub_year',
#       'SC_joined', 'computational', 'social', 'multi_inter', 'all_geo',
#       'phys_geo', 'non_phys_geo', 'health', 'biol_env', 'arts_humanities',
#       'econ_bus_trans', 'comp_soc', 'comp_non_phys_geo', 'non_cat',
#       'only_social', 'only_non_phys_geo', 'only_computational'],
#      dtype='object')

print(community_nodes_SC.shape) # (2636, 29)
community_nodes_SC.drop_duplicates(inplace = True)
print(community_nodes_SC.shape) # (2636, 29)
print(community_nodes_SC.columns)

#%% get SC for each cluster

clusters_SC = pd.DataFrame(community_nodes_SC[['cluster', 'computational', 'social', 'multi_inter', 'all_geo',
                                               'phys_geo', 'non_phys_geo', 'health', 'biol_env', 'arts_humanities',
                                               'econ_bus_trans', 'comp_soc', 'comp_non_phys_geo', 'non_cat',
                                               'only_social', 
                                               'only_non_phys_geo', 'only_computational']].groupby('cluster').sum()).reset_index()

    
print(clusters_SC.columns)
print(clusters_SC.shape)

#Index(['cluster', 'computational', 'social', 'multi_inter', 'all_geo',
#       'phys_geo', 'non_phys_geo', 'health', 'biol_env', 'arts_humanities',
#       'econ_bus_trans', 'comp_soc', 'comp_non_phys_geo', 'non_cat',
#       'only_social', 'only_non_phys_geo', 'only_computational'],
#      dtype='object')

print(clusters_SC.head(5))

#%% create long df

clusters_SC_long = pd.melt(clusters_SC, id_vars=['cluster'], value_vars=['computational', 'social',
                           'multi_inter', 'all_geo', 'phys_geo', 'non_phys_geo', 'health', 'biol_env', 
                           'arts_humanities', 'econ_bus_trans', 'comp_soc', 'comp_non_phys_geo', 'non_cat',
                           'only_social', 'only_non_phys_geo', 'only_computational'])
    
clusters_SC_long = pd.melt(clusters_SC, id_vars=['cluster'], value_vars=['multi_inter', 'phys_geo', 'non_phys_geo',
                           'only_social', 'only_computational'])
    
#clusters_SC_long['color'] = clusters_SC_long['variable']
    
clusters_SC_long.rename(columns = {'variable' : 'discipline',
                                   'value': 'pub_count'}, inplace = True)
    
print(clusters_SC_long.columns) # Index(['cluster', 'discipline', 'pub_count'], dtype='object')
print(clusters_SC_long.head(6))
print(clusters_SC_long)
#%%

import seaborn as sns

#g = sns.FacetGrid(clusters_SC_long, row = 'cluster')
#g.map(sns.barplot,'variable', 'value')

#g = sns.FacetGrid(clusters_SC_long, row="cluster")
#g.map(sns.barplot, 'variable', 'value')

#sns.catplot(x="cluster", y="value", hue="variable", kind="bar", data=clusters_SC_long)

g = sns.catplot(x="discipline", y="pub_count", col="cluster",
                data=clusters_SC_long, saturation=.5,
                kind="bar", ci=None, aspect=0.2)

# rotate label
# https://stackoverflow.com/questions/26540035/rotate-label-text-in-seaborn-factorplot

g.set_xticklabels(rotation=90)

mypath = 'P:/thesis/thesis_final_visualisations/papers_clusters_ch7_SC_barchart/{}_{}/'.format(SC_filter, matrixnorm)

import os
if not os.path.exists(mypath):
    os.makedirs(mypath)

g.savefig(mypath + 'cluster_sc_categories_{}_{}_v2.png'.format(SC_filter, matrixnorm))
g.savefig(mypath + 'cluster_sc_categories_{}_{}_v2.pdf'.format(SC_filter, matrixnorm))


#sns.barplot(x = 'cluster', y = 'value', data = clusters_SC_long) 
  
# Show the plot 
#plt.show() 

#%%

#%%

'''
    term map & tf - idf for each cluster
'''

#%% OLD CODE: NOT NECESSARY ANYMORE 
# get ut set for each community so I can extract terms

#print(community_nodes_SC.columns)
#
##Index(['node_names', 'igraph_node_id', 'cluster', 'ut', 'pub_year',
##       'SC_joined', 'computational', 'social', 'multi_inter', 'all_geo',
##       'phys_geo', 'non_phys_geo', 'health', 'biol_env', 'arts_humanities',
##       'econ_bus_trans', 'comp_soc', 'comp_non_phys_geo', 'non_cat',
##       'only_social', 'only_non_phys_geo', 'only_computational'],
##      dtype='object')
#
#print(all_nodes_df_fullab.columns)
#
##Index(['ut', 'ti', 'ab_full', 'de', 'id', 'pub_year', 'cwts_so_no',
##       'cwts_sc_no', 'sc', 'weight', 'so', 'au_count', 'au_no', 'au'],
##      dtype='object')
#
#print(all_nodes_df_fullab.shape) # (17976, 14)
#
##
#
#all_nodes_df_fullab_2 = all_nodes_df_fullab.drop_duplicates(subset = ['ut'])
#
#print(all_nodes_df_fullab_2.shape) # (2759, 14)
#
## get ut, abstract, title and communities in 1 df
#
#communities_ut_dat = pd.merge(all_nodes_df_fullab, community_nodes_SC, on = 'ut', how = 'left')
#print(communities_ut_dat.shape) # (2759, 35)
#print(communities_ut_dat.columns) # (2759, 35)

#%%

communities_ut_dat = community_nodes_SC.copy()

# get rid of nodes that are not in the clustered author bib coupling network
communities_ut_dat.dropna(subset = ['cluster'], inplace = True)
print(communities_ut_dat.shape) # (2636, 35)
print(communities_ut_dat.columns) # 
print(len(set(communities_ut_dat.ut))) # 2655
print(len(set(communities_ut_dat.ab))) # 2655
print(len(set(communities_ut_dat.ti))) # 2655

communities_ut_dat2 = communities_ut_dat.drop(columns = ['ab', 'ti'])
print(communities_ut_dat2.columns) # 

communities_ut_dat3 = pd.merge(communities_ut_dat2[['cluster', 'ut']], all_nodes_df, on = 'ut', how = 'left')
communities_ut_dat3.drop_duplicates(subset = 'ut', inplace = True)
print(len(set(communities_ut_dat3.ut))) # 2655
print(len(set(communities_ut_dat3.ab))) # 2655
print(len(set(communities_ut_dat3.ti))) # 2655
#%% save dat for each community separately

communities = list(set(communities_ut_dat.cluster))

# create directory

mypath = "P:/thesis/thesis_final_data/produced_data/clusters_ch7_terms/1_clusters_abstract_title_files/{}_{}/".format(SC_filter, matrixnorm)

import os
if not os.path.exists(mypath):
    os.makedirs(mypath)

for cl in communities:
    print(cl)
    dat = communities_ut_dat.loc[communities_ut_dat['cluster'] == cl]
    dat.drop_duplicates(inplace = True)
    print(dat.shape)
    dat.dropna(subset = ['ti'], inplace = True) # drop rows with no title
    print(dat.shape)
#    print(dat.columns)
#    dat.rename(columns = {'ab_full' : 'ab'}, inplace = True)
    # save dat so I can make term map
#    print(dat.columns)
    dat[['ti', 'ab']].to_excel(mypath + "cluster_{}_{}_{}_v2.xlsx".format(cl, SC_filter, matrixnorm), index = False)
    dat[['ti', 'ab']].to_csv(mypath + "cluster_{}_{}_{}_v2.txt".format(cl, SC_filter, matrixnorm), sep="\t", index = False)


#%% 
#%% 
    
    ''' CALCULATE TF - IDF '''
    
#%% get extracted terms

'''
    MANUAL INPUT REQUIRED: extract terms with VOSviewer
    
    extracted terms with_VOSviewer based on txt files with 'manual edit' in their filenames: a few papers' (cc 3)
    titles and abstracts were messed up
    
    minimum occurence = 2
    relevance score = keep all

'''

#%% 
#%% get extracted terms
    
      
'''
    used VOSviewer, minimum number of occurrence was 2, and no filtering based on relevance score

'''

# 1. read in 'VOSviewer map' file names into a dictionary, these files contain the noun phrases and their occurrence (among other info)

'''
    MANUAL INPUT REQUIRED : manually repeae for each combination of SC cat filtering & matrixnorm

'''

import os
import pandas as pd

# SC filter options options
SC_filter = 'all_SC_cat'
#SC_filter = 'comp_plus_soc'

# matrixnorm options
#matrixnorm = 'norm_cosine_similarity'
matrixnorm = 'norm_waltmann_etal'

#mypath = "P:/thesis/thesis_final_data/produced_data/term_map_data/au_bibcouple_network_clusters/all_SC_cat/terms_extracted/"
#mypath = "P:/thesis/thesis_final_data/produced_data/term_map_data/au_bibcouple_network_clusters/{}/terms_extracted_with_VOSviewer/{}/".format(SC_filter, matrixnorm)
mypath = "P:/thesis/thesis_final_data/produced_data/clusters_ch7_terms/2_clusters_noun_phrases_extracted/{}_{}/".format(SC_filter, matrixnorm)


terms_filenames = {} # dictionary of 'VOSviewer map' filenames

for file in os.listdir(mypath):
    if 'map' in file:
        cluster = file[9:18]
        print(cluster)
        terms_filenames[cluster] = mypath + file

# 2. load noun phrase data for each cluster into a dataframe and add these to a dictionary
   
terms_dfs = {} # create dictionary with terms dfs for each cluster
     
for cluster, file in terms_filenames.items():
    df = pd.read_csv(file, sep = '\t')
#    print(df.columns)
#    print(df.shape)
    terms_dfs[cluster] = df
    print(min(df['weight<Occurrences>']))
    
# 3. check data
    
#for cluster, terms_df in terms_dfs.items():
#    print(terms_df.columns)
#    print(terms_df.shape)

#%% filter based on minimum occurrence value
    
#min_occ = 2
min_occ = 10
    
terms_dfs_filt = {}

for cluster, terms_df in terms_dfs.items():
#    print(terms_df.columns)
    print(terms_df.shape)
    print(terms_df.columns)
    terms_df = terms_df.loc[terms_df['weight<Occurrences>'] >= min_occ]
    print(terms_df.shape)
    if terms_df.shape[0] > 0: # do not save empty databases, for small clusters whcih consist of 1-2 papers, none of the terms occur at least 10 times
        terms_dfs_filt[cluster] = terms_df


#%% calculate tf-idf

#%% calculate term frequency for each term per cluster

# tf(t,d) = count of t in d / number of words in d
    
# count of term = the 'weight<Occurrences>' variable calculated by VOSviewer
    
for cluster, terms_df in terms_dfs_filt.items():
    terms_df['term_frequency'] = terms_df['weight<Occurrences>'] / terms_df.shape[0]
    print(min(list(terms_df['weight<Occurrences>'])))
#    print(list(terms_df['weight<Occurrences>']))
    print(min(list(terms_df['term_frequency'])))
    print(max(list(terms_df['term_frequency'])))

#%% calculate inverse document frequency of each noun phrase = their total number of occurrence across all clusters

# get number of documents (clusters)
    
clusters_list = []
    
for cluster, terms_df in terms_dfs_filt.items():
    clusters_list.append(cluster)
    
n_cluster = len(clusters_list)
print(n_cluster) # 5

# create a dataframe with all noun phrases
   
df_list = []
    
for cluster, terms_df in terms_dfs_filt.items():
    df_list.append(terms_df)
    print(max(terms_df['weight<Occurrences>'])) # 810, 546, 415, 400, 388

all_clusters_all_terms = pd.concat(df_list)

print(all_clusters_all_terms.shape)  # (16943, 8)

# calculate document frequency = ocurrence of terms across cluters

doc_freq = pd.DataFrame(all_clusters_all_terms[['label', 'weight<Occurrences>']].groupby('label').sum()).reset_index()
print(doc_freq.shape) #(11346, 2)
print(max(doc_freq['weight<Occurrences>'])) # 2046
print(min(doc_freq['weight<Occurrences>'])) # 2

# calculate inverse document frequency
# idf(t) = log(N/(df + 1))

import numpy as np

doc_freq['idf'] = np.log(n_cluster / ((doc_freq['weight<Occurrences>'] + 1)))
print(max(doc_freq['idf'])) # 0.5108256237659907
print(min(doc_freq['idf'])) # -6.014692673227189
print(doc_freq.columns) # Index(['label', 'weight<Occurrences>', 'idf'], dtype='object')
#%% get tf-idf

# tf-idf(t, d) = tf(t, d) * log(N/(df + 1))

''' 

MANUAL INPUT REQUIRED: PATH DEPENDS ON SC CAT FILTER

'''

mypath = 'P:/thesis/thesis_final_data/produced_data/clusters_ch7_terms/3_clusters_tf_idf/{}_{}/'.format(SC_filter, matrixnorm)

import os
if not os.path.exists(mypath):
    os.makedirs(mypath)

for cluster, terms_df in terms_dfs_filt.items():
    terms_df_2 = pd.merge(terms_df, doc_freq, on = 'label', how = 'left')
#    print(terms_df_2.columns)
    terms_df_2['tf_idf'] = terms_df_2['term_frequency'] * terms_df_2['idf']
    print(terms_df_2.shape)
    terms_df_3 =  terms_df_2.sort_values(by = ['tf_idf'], ascending = False)
    print(terms_df_3.columns)
    terms_df_3['tf_idf'] = terms_df_3['tf_idf'].apply(lambda x: str(x).replace(',', '.')) # to ensure excel reads it as numeric
    terms_df_3[['label', 'tf_idf', 'term_frequency', 'weight<Occurrences>_x']].to_excel(mypath + '{}_occ{}_terms_tf_idf.xlsx'.format(cluster, min_occ), index = False)

#    terms_df_3[['label', 'tf_idf']].to_excel('P:/thesis/thesis_final_data/produced_data/clusters_ch7/all_SC/{}_occ{}_terms_tf_idf.xlsx'.format(cluster, min_occ), index = False)


#%%
    
    
    '''
    
    get overlap of noun phrases between clusters
    
    '''

#%% get overlap of noun phrases between clusters


import os
import pandas as pd

# SC filter options options
#SC_filter = 'all_SC_cat'
SC_filter = 'comp_plus_soc'

# matrixnorm options
#matrixnorm = 'norm_cosine_similarity'
matrixnorm = 'norm_waltmann_etal'


# min -ccurrence filter
#min_occ = 'occ2'
min_occ = 'occ10'

mypath = 'P:/thesis/thesis_final_data/produced_data/clusters_ch7_terms/3_clusters_tf_idf/{}_{}/'.format(SC_filter, matrixnorm)


terms_filenames = {} # dictionary of 'VOSviewer map' filenames

for file in os.listdir(mypath): #
    if 'tf_idf' in file:
        cluster = file[:9]
#        print(cluster)
        if min_occ in file:
            print(cluster)
            terms_filenames[cluster] = mypath + file

#%% 2. load noun phrase data for each cluster into a dataframe and add these to a dictionary

# TODO: manual input required, 
#filt = 10
#filt = 5
#filt = 2
   
    
terms_dfs = {} # create dictionary with terms dfs for each cluster
     
for cluster, file in terms_filenames.items():
    df = pd.read_excel(file)
    print(df.columns)
#    print(df.shape)
    terms_dfs[cluster] = df
#    print(min(df['term_frequency']))

mypath2 = 'P:/thesis/thesis_final_data/produced_data/clusters_ch7_terms/3_clusters_tf_idf/{}_{}/intersection_between_terms_clusters/'.format(SC_filter, matrixnorm)
    

#%% get noun phrases present both in clusters 0 and 1

# 1. load cluster 0 data

cluster_0_df = terms_dfs['cluster_0']
print(cluster_0_df.shape)

# change numeric columns to numeric

cluster_0_df['tf_idf'] = cluster_0_df['tf_idf'].apply(lambda x: str(x).replace(',', '.'))
cluster_0_df['tf_idf'] = pd.to_numeric(cluster_0_df['tf_idf'])

cluster_0_df['term_frequency'] = cluster_0_df['term_frequency'].apply(lambda x: str(x).replace(',', '.'))
cluster_0_df['term_frequency'] = pd.to_numeric(cluster_0_df['term_frequency'])

# rename columns before merge

cluster_0_df.rename(columns = {'tf_idf' : 'tf_idf_cl_0',
                               'term_frequency' : 'term_frequency_cl_0'}, inplace = True)
print(cluster_0_df.columns)



# 2. load cluster 1 data

cluster_1_df = terms_dfs['cluster_1']
print(cluster_1_df.shape)

# change numeric columns to numeric

cluster_1_df['tf_idf'] = cluster_1_df['tf_idf'].apply(lambda x: str(x).replace(',', '.'))
cluster_1_df['tf_idf'] = pd.to_numeric(cluster_1_df['tf_idf'])

cluster_1_df['term_frequency'] = cluster_1_df['term_frequency'].apply(lambda x: str(x).replace(',', '.'))
cluster_1_df['term_frequency'] = pd.to_numeric(cluster_1_df['term_frequency'])

# rename columns before merge

cluster_1_df.rename(columns = {'tf_idf' : 'tf_idf_cl_1',
                               'term_frequency' : 'term_frequency_cl_1'}, inplace = True)

    
    
# 3. get intersection
inner_0_1_df = pd.merge(cluster_0_df, cluster_1_df, how = 'inner', on = 'label')
print(inner_0_1_df.columns)
#Index(['label', 'tf_idf_cl_0', 'term_frequency_cl_0', 'tf_idf_cl_1',
#       'term_frequency_cl_1'],
#      dtype='object')
print(inner_0_1_df.shape) # (837, 5)



# 4. save data

inner_0_1_df.to_excel(mypath2 + 'intersection_cluster_0_cluster_1_min_occ_{}.xlsx'.format(min_occ), index = False)

# if filt = 10, intersection (278, 7)

# save intersection of top 30% from both to
#%% get noun phrases present both in clusters 0 and 2

# get ccluster 2 data

cluster_2_df = terms_dfs['cluster_2']
print(cluster_2_df.shape)  


# change numeric columns to numeric

cluster_2_df['tf_idf'] = cluster_2_df['tf_idf'].apply(lambda x: str(x).replace(',', '.'))
cluster_2_df['tf_idf'] = pd.to_numeric(cluster_2_df['tf_idf'])

cluster_2_df['term_frequency'] = cluster_2_df['term_frequency'].apply(lambda x: str(x).replace(',', '.'))
cluster_2_df['term_frequency'] = pd.to_numeric(cluster_2_df['term_frequency'])

# rename columns before merge

cluster_2_df.rename(columns = {'tf_idf' : 'tf_idf_cl_2',
                               'term_frequency' : 'term_frequency_cl_2'}, inplace = True)
    
# get intersection
inner_0_2_df = pd.merge(cluster_0_df, cluster_2_df, how = 'inner', on = 'label')
print(inner_0_2_df.columns)
#Index(['label', 'tf_idf_cl_0', 'term_frequency_cl_0', 'tf_idf_cl_2',
#       'term_frequency_cl_2'],
#      dtype='object')
print(inner_0_2_df.shape) # (755, 5)

# save file

inner_0_2_df.to_excel(mypath2 + 'intersection_cluster_0_cluster_2_min_occ_{}.xlsx'.format(min_occ), index = False)

# if filt = 10, intersection is (196, 7)

#%% get noun phrases present both in clusters 1 and 2
    
# get intersection
inner_1_2_df = pd.merge(cluster_1_df, cluster_2_df, how = 'inner', on = 'label')
print(inner_1_2_df.columns)
#Index(['label', 'tf_idf_cl_1', 'term_frequency_cl_1', 'tf_idf_cl_2',
#       'term_frequency_cl_2'],
#      dtype='object')
print(inner_1_2_df.shape) # (726, 5)

inner_1_2_df.to_excel(mypath2 + 'intersection_cluster_1_cluster_2_min_occ_{}.xlsx'.format(min_occ), index = False)

# if filt = 10, intersection is (201, 7)

#%%

#%% 


''' GET EGO NETWORK OF A FEW NOUN PHRASES IN THE INTERSECTION:
    
    country
    city
    network
    
    citizen
    
    case study
    
    disaster
    change
    

'''



#%% get VOSviewer map and network files

import os
import pandas as pd

# path to folder with VOSviewer term map files for clusters 0 & 1 (soc and comp), min occurrence 10, but not filtered based on relevance score 

mypath2 = 'P:/thesis/thesis_final_data/produced_data/clusters_ch7_terms/2_clusters_noun_phrases_extracted/comp_plus_soc_norm_waltmann_etal/o10_r1_for_ego_network/'
  
terms_filenames = {} # dictionary of 'VOSviewer map' filenames

map_dfs = {}
network_dfs = {}

for file in os.listdir(mypath2):#
    if 'map' in file:
        cluster = file[-20:-11]
        print(cluster)
        map_df = pd.read_csv(mypath2 + file, sep = '\t')
        map_dfs[cluster] = map_df
    if 'network' in file:
        cluster = file[-20:-11]
        print(cluster)
        network_df = pd.read_csv(mypath2 + file, sep = '\t')
        network_dfs[cluster] = network_df

#%%
        
#myterm = 'country'
#myterm = 'city'
#myterm = 'network'
#myterm = 'citizen' # DONE
#myterm = 'case study'
#myterm = 'disaster'
#myterm = 'space'
#myterm = 'place'
#myterm = 'pattern'
myterm = 'real time'
#myterm = 'resident'
#myterm = 'privacy'

# get the id of terms I am looking for
labels_ids = {}
dfs = []
        
for key, df in map_dfs.items():
    print(key)
    print(df.columns)
#    Index(['id', 'label', 'x', 'y', 'cluster', 'weight<Links>',
#       'weight<Total link strength>', 'weight<Occurrences>'],
#      dtype='object')
    label_df_row = df.loc[df['label'] == myterm]
    labels_ids[key] = label_df_row[['id', 'label']]
    
    dfs.append(df)

#inner = pd.merge(dfs[0], dfs[1], how = 'inner', on = 'label')
#inner.to_excel('P:/thesis/thesis_final_data/produced_data/intersection_comp_soc_waltmann_etal_cl0_cl1_good_version.xlsx')
#%% subset the network to only include id

ego_dfs_edges = {}

for key, df in network_dfs.items():
    print(key)
#    print(df.columns)
    df.columns = ['from', 'to', 'weight']
    
    for key2, termid_df in labels_ids.items():
        if key == key2:
            print(termid_df)
            termid = int(termid_df['id'])
            term = str(termid_df['label'])
            print(termid)
            
            ego_df_edges = pd.concat([ df.loc[df['from'] == termid], df.loc[df['to'] == termid] ])
            print(ego_df_edges.shape)
            nodes_list = list(set(list(ego_df_edges['from']) + list(ego_df_edges['to'])))
            ego_dfs_edges[key] = [term, ego_df_edges, nodes_list]
#    df2 = df.loc[df['']]    
#%% get subset of map file

ego_dfs_nodes = {}


for key, value in ego_dfs_edges.items():
    print(key)
    print(value[0]) # searchterm whose ego net we are getting
    print(value[1].head(5)) # ego net df EDGES
#    print(value[2]) # ego net nodes list
    
    term = value[0]
    
    nodes_list = value[2]
    print(len(nodes_list))
    
    for key2, map_df in map_dfs.items():
        if key == key2:
            map_df_filt = map_df.loc[map_df['id'].isin(nodes_list)]
            print(map_df_filt.shape)
            
            ego_dfs_nodes[key] = [term, map_df_filt]

#%% save txt files
            
            
mypath2 = 'P:/thesis/thesis_final_visualisations/term_maps_ch7/ego_nets_clusters_comp_soc_norm_waltmann_etal/'
  

for key, item in ego_dfs_nodes.items():
    print(key)
    print(item[0])
    print(item[1].head(5))
    item[1].to_csv(mypath2 + 'map_ego_{}_{}.txt'.format(myterm, key), sep = '\t', index = False)
    
for key, item in ego_dfs_edges.items():
    print(key)
    print(item[0])
    print(item[1].head(5))
    item[1].to_csv(mypath2 + 'network_ego_{}_{}.txt'.format(myterm, key), sep = '\t', header = False, index = False)
#%%
#%%
#%%
#%%

'''
    OLD and UNUSED CODE
'''
#%% get SC cat for each community

# ('cat 3: multi and interdisc')
#('cat 4: all geography')
#('cat 5: physical geography')
#('cat 6: not physical geography')
#('cat 7: mixed computation and social')
#('cat 9: (not categorised)')#
#('cat 10: (social sciemce & humanities, NOT technical and NOT inter/multi disciplinary)')
#('cat 11: (technical (incl. physical geography) and NOT inter/multi disciplinary or soc sci)')

df_list = []

# get count of geography papers for each community
communities_all_multi = community_nodes_SC[['SC_cat_3', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_all_multi.rename(columns = {'SC_cat_3' : 'multi_inter_papers_count'}, inplace = True)
df_list.append(communities_all_multi)

# get count of geography papers for each community
communities_all_geo = community_nodes_SC[['SC_cat_4', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_all_geo.rename(columns = {'SC_cat_4' : 'all_geo_papers_count'}, inplace = True)
df_list.append(communities_all_geo)

# get count of physical geography papers for each community
communities_phys_geo = community_nodes_SC[['SC_cat_5', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_phys_geo.rename(columns = {'SC_cat_5' : 'physical_geo_papers_count'}, inplace = True)
df_list.append(communities_phys_geo)

# get count of  human geography papers for each community
communities_hum_geo = community_nodes_SC[['SC_cat_6', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_hum_geo.rename(columns = {'SC_cat_6' : 'human_geo_papers_count'}, inplace = True)
df_list.append(communities_hum_geo)

# get count of mixed social AND computational papers for each community
communities_socio_tech = community_nodes_SC[['SC_cat_7', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_socio_tech.rename(columns = {'SC_cat_7' : 'mixed_soc_comp_papers_count'}, inplace = True)
df_list.append(communities_socio_tech)

# get count of  not categorised papers for each community
communities_not_cat = community_nodes_SC[['SC_cat_9', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_not_cat.rename(columns = {'SC_cat_9' : 'not_cat_papers_count'}, inplace = True)
df_list.append(communities_not_cat)

# get count of only social science papers for each community
communities_only_social = community_nodes_SC[['SC_cat_10', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_only_social.rename(columns = {'SC_cat_10' : 'soc_papers_count'}, inplace = True)
df_list.append(communities_only_social )

# get count of only techncial papers for each community
communities_only_tech = community_nodes_SC[['SC_cat_11', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_only_tech.rename(columns = {'SC_cat_11' : 'tech_papers_count'}, inplace = True)
df_list.append(communities_only_tech)

#%% merge SC  dfs

print(communities_all_multi.head(5))
print(communities_all_geo.head(5))

#%%

from functools import reduce

comm_SC_counts = reduce(lambda x, y: pd.merge(x, y, on = 'modularity_class'), df_list)

#%% check SC  dfs

print(comm_SC_counts.columns)
# Index(['modularity_class', 'multi_inter_papers_count', 'all_geo_papers_count',
#       'physical_geo_papers_count', 'human_geo_papers_count',
#       'mixed_soc_comp_papers_count', 'not_cat_papers_count',
#       'soc_papers_count', 'tech_papers_count'],
#      dtype='object')

print(comm_SC_counts.shape) # (45, 9)

#%% link size too

comm_SC_counts_size = pd.merge(comm_SC_counts, community_size[['modularity_class', 'community_size']],
                               on = 'modularity_class', how = 'left')

comm_SC_counts_size.rename(columns = {'modularity_class' : 'Id'}, inplace = True)

print(comm_SC_counts_size.shape) # (45, 10)

print(comm_SC_counts_size.columns)

nodes_comm_folder_2 = ('P:/thesis_final_data/produced_data/' +
                       'papers_author_coupling/' + cos_sim_for_folder +
                       '/communities_graph/')

import os
if not os.path.exists(nodes_comm_folder_2):
    os.makedirs(nodes_comm_folder_2)

comm_SC_counts_size.to_csv(nodes_comm_folder_2 + 'nodes_communities_graph.csv')

#%%

'''
OLD CODE
'''

#%% EDGES TO GEPHI

gephi_edges = papers_auth_coupling_cos_sim_df.copy()

gephi_edges.rename(columns = {'paper_1' : 'Source',
                              'paper_2' : 'Target',
                              'paper_auth_cosine_similarity' : 'Weight'}, inplace = True)

gephi_edges.reset_index(drop = True, inplace = True) 
   
print(gephi_edges.head(20))

print(gephi_edges.shape) # (31242, 3)
#%% save edges_gephi file

cos_sim_for_folder = 'cos_sim_' + cos_sim_for_filename

paper_co_author_for_gephi_path = ('P:/thesis/thesis_final_data/produced_data/' +
                                  'papers_author_coupling/' + cos_sim_for_folder +
                                  '/for_gephi/')

import os
if not os.path.exists(paper_co_author_for_gephi_path):
    os.makedirs(paper_co_author_for_gephi_path)
  
gephi_edges.to_csv( paper_co_author_for_gephi_path + 'papers_author_coupling_for_gephi.csv', index=False)

#%% 
#%% EDGES TO R IGRAPH

# get uts, and make new  ran_id for them
# get uts

ut_ran_id = SC_cat_cited_edges_3.drop(columns = 'ut_cited_ref').drop_duplicates()
print(ut_ran_id.shape) # (2710, 2)

igraph_edges = papers_auth_coupling_cos_sim_df.copy()

igraph_edges2 = pd.merge(igraph_edges,
                         ut_ran_id,
                         left_on = 'paper_1',
                         right_on = 'citing_ran_id',
                         how = 'left')

igraph_edges2.drop(columns = ['citing_ran_id', ], inplace = True)
igraph_edges2.rename(columns = {'ut_citing_paper' : 'ut_citing_paper1'}, inplace = True)


igraph_edges3 = pd.merge(igraph_edges2,
                         ut_ran_id,
                         left_on = 'paper_2',
                         right_on = 'citing_ran_id',
                         how = 'left')

igraph_edges3.drop(columns = ['citing_ran_id'], inplace = True)
igraph_edges3.rename(columns = {'ut_citing_paper' : 'ut_citing_paper2'}, inplace = True)

print(igraph_edges3.columns)
print(igraph_edges3.ut_citing_paper1[:10])

# new random id for uts, nodes

uts_ran_ids_new = pd.DataFrame()
uts_ran_ids_new['ut'] = list(list(set(list(igraph_edges3.ut_citing_paper1) + (list(set(list(igraph_edges3.ut_citing_paper2)))))))
uts_ran_ids_new['ran_id'] = uts_ran_ids_new.index + 1
print(uts_ran_ids_new.head(5))

# add new random ids

igraph_edges4 = pd.merge(igraph_edges3,
                         uts_ran_ids_new,
                         left_on = 'ut_citing_paper1',
                         right_on = 'ut',
                         how = 'left')

igraph_edges4.drop(columns = ['ut', ], inplace = True)
igraph_edges4.rename(columns = {'ran_id' : 'ut1_ran_id'}, inplace = True)


igraph_edges5 = pd.merge(igraph_edges4,
                         uts_ran_ids_new,
                         left_on = 'ut_citing_paper2',
                         right_on = 'ut',
                         how = 'left')

igraph_edges5.drop(columns = ['ut', ], inplace = True)
igraph_edges5.rename(columns = {'ran_id' : 'ut2_ran_id'}, inplace = True)

print(igraph_edges5.columns)
#Index(['paper_auth_cosine_similarity', 'paper_1', 'paper_2',
#       'ut_citing_paper1', 'ut_citing_paper2', 'ut1_ran_id', 'ut2_ran_id'],
#      dtype='object')

igraph_edges6 = igraph_edges5[['ut1_ran_id', 'ut2_ran_id', 'paper_auth_cosine_similarity']]
print(igraph_edges6.columns)
#%%

igraph_edges6.rename(columns = {'ut1_ran_id' : 'from',
                                'ut2_ran_id' : 'to',
                                 'paper_auth_cosine_similarity' : 'weight'}, inplace = True)

igraph_edges6.reset_index(drop = True, inplace = True) 
   
print(igraph_edges6.head(20))

print(igraph_edges6.shape) # (31242, 3)

#%% save igraph_edges file

cos_sim_for_folder = 'cos_sim_' + cos_sim_for_filename

paper_co_author_for_igraph_path = ('P:/thesis/thesis_final_data/produced_data/' +
                                  'papers_author_coupling/' + cos_sim_for_folder +
                                  '/for_igraph/')

import os
if not os.path.exists(paper_co_author_for_igraph_path):
    os.makedirs(paper_co_author_for_igraph_path)
  
igraph_edges6.to_csv( paper_co_author_for_igraph_path + 'papers_author_coupling_for_igraph.csv', index=False)

#%%

#%% save ut & ran id data
#%% save ut and ut_ran_id data

uts_ran_ids_new.to_csv(paper_co_author_for_igraph_path + 'ut_ran_id_author_coupling.csv', index=False)

#%%

# MANUALLY  IMPORT DATA TO GEPHI, GET NODES'S COMMUNITIES

#%% get nodes'communities from gephi

cos_sim_for_folder = 'cos_sim_' + cos_sim_for_filename


import pandas as pd

nodes_comm_folder = ('P:/thesis_final_data/produced_data/' +
                     'papers_author_coupling/' + cos_sim_for_folder +
                     '/csv_from_gephi/')

nodes_comm = pd.read_csv(nodes_comm_folder + 'papers_author_coupling_nodes_comm.csv')

print(nodes_comm.head(5))

nodes_comm.drop(columns = ['Label', 'timeset'], inplace = True)
nodes_comm.rename(columns = {'Id' : 'ut_ran_id'}, inplace = True)

# get real ut of citing papers

nodes_comm_2 = pd.merge(nodes_comm, ut_num_id_df, on = 'ut_ran_id', how = 'left')

print(nodes_comm_2.columns)

# Index(['ut_ran_id', 'modularity_class', 'Eccentricity', 'closnesscentrality',
#       'harmonicclosnesscentrality', 'betweenesscentrality', 'componentnumber',
#       'ut'],
#      dtype='object')

#%% get size of each community

community_size = nodes_comm.groupby('modularity_class').count().reset_index()
community_size.rename(columns = {'ut_ran_id' : 'community_size'}, inplace = True)
#print(community_size)

#%%  get SC cat for each node

print(SC_cat_cited_edges.shape) # (432717, 22)
SC_cat_uts = SC_cat_cited_edges.drop_duplicates(subset = 'ut')
print(SC_cat_uts.shape) # (2781, 22)
print(SC_cat_uts.columns)

# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'pub_year', 'SO',
#       'CWTS_SO_NO', 'pub_year_y', 'SC_joined', 'SC_cat_1', 'SC_cat_2',
#       'SC_cat_3', 'SC_cat_4', 'SC_cat_5', 'SC_cat_6', 'SC_cat_7', 'SC_cat_8',
#       'SC_cat_9', 'SC_cat_10', 'SC_cat_11'],
#      dtype='object')

print(nodes_comm_2.shape) # (2266, 7)
print(nodes_comm_2.columns) 
# Index(['ut_ran_id', 'modularity_class', 'Eccentricity', 'closnesscentrality',
#       'harmonicclosnesscentrality', 'betweenesscentrality',
#       'componentnumber'],
 #     dtype='object')

community_nodes_SC = pd.merge(nodes_comm_2, SC_cat_uts,
                             on = 'ut', how = 'left')

print(community_nodes_SC.columns)

# Index(['ut_ran_id', 'modularity_class', 'Eccentricity', 'closnesscentrality',
#       'harmonicclosnesscentrality', 'betweenesscentrality', 'componentnumber',
#       'ut', 'S_UT', 'AU_COUNT', 'AU_NO', 'AU', 's_ut', 'pub_year', 'SO',
#       'CWTS_SO_NO', 'pub_year_y', 'SC_joined', 'SC_cat_1', 'SC_cat_2',
#       'SC_cat_3', 'SC_cat_4', 'SC_cat_5', 'SC_cat_6', 'SC_cat_7', 'SC_cat_8',
#       'SC_cat_9', 'SC_cat_10', 'SC_cat_11'],      dtype='object')

print(community_nodes_SC.shape) # (2266, 29)
community_nodes_SC.drop_duplicates(inplace = True)
print(community_nodes_SC.shape) # (2266, 29)
print(community_nodes_SC.columns)

#%% get SC cat for each community

# ('cat 3: multi and interdisc')
#('cat 4: all geography')
#('cat 5: physical geography')
#('cat 6: not physical geography')
#('cat 7: mixed computation and social')
#('cat 9: (not categorised)')#
#('cat 10: (social sciemce & humanities, NOT technical and NOT inter/multi disciplinary)')
#('cat 11: (technical (incl. physical geography) and NOT inter/multi disciplinary or soc sci)')

df_list = []

# get count of geography papers for each community
communities_all_multi = community_nodes_SC[['SC_cat_3', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_all_multi.rename(columns = {'SC_cat_3' : 'multi_inter_papers_count'}, inplace = True)
df_list.append(communities_all_multi)

# get count of geography papers for each community
communities_all_geo = community_nodes_SC[['SC_cat_4', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_all_geo.rename(columns = {'SC_cat_4' : 'all_geo_papers_count'}, inplace = True)
df_list.append(communities_all_geo)

# get count of physical geography papers for each community
communities_phys_geo = community_nodes_SC[['SC_cat_5', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_phys_geo.rename(columns = {'SC_cat_5' : 'physical_geo_papers_count'}, inplace = True)
df_list.append(communities_phys_geo)

# get count of  human geography papers for each community
communities_hum_geo = community_nodes_SC[['SC_cat_6', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_hum_geo.rename(columns = {'SC_cat_6' : 'human_geo_papers_count'}, inplace = True)
df_list.append(communities_hum_geo)

# get count of mixed social AND computational papers for each community
communities_socio_tech = community_nodes_SC[['SC_cat_7', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_socio_tech.rename(columns = {'SC_cat_7' : 'mixed_soc_comp_papers_count'}, inplace = True)
df_list.append(communities_socio_tech)

# get count of  not categorised papers for each community
communities_not_cat = community_nodes_SC[['SC_cat_9', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_not_cat.rename(columns = {'SC_cat_9' : 'not_cat_papers_count'}, inplace = True)
df_list.append(communities_not_cat)

# get count of only social science papers for each community
communities_only_social = community_nodes_SC[['SC_cat_10', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_only_social.rename(columns = {'SC_cat_10' : 'soc_papers_count'}, inplace = True)
df_list.append(communities_only_social )

# get count of only techncial papers for each community
communities_only_tech = community_nodes_SC[['SC_cat_11', 'modularity_class']].groupby('modularity_class').sum().reset_index()
communities_only_tech.rename(columns = {'SC_cat_11' : 'tech_papers_count'}, inplace = True)
df_list.append(communities_only_tech)

#%% merge SC  dfs

print(communities_all_multi.head(5))
print(communities_all_geo.head(5))

#%%

from functools import reduce

comm_SC_counts = reduce(lambda x, y: pd.merge(x, y, on = 'modularity_class'), df_list)

#%% check SC  dfs

print(comm_SC_counts.columns)
# Index(['modularity_class', 'multi_inter_papers_count', 'all_geo_papers_count',
#       'physical_geo_papers_count', 'human_geo_papers_count',
#       'mixed_soc_comp_papers_count', 'not_cat_papers_count',
#       'soc_papers_count', 'tech_papers_count'],
#      dtype='object')

print(comm_SC_counts.shape) # (45, 9)

#%% link size too

comm_SC_counts_size = pd.merge(comm_SC_counts, community_size[['modularity_class', 'community_size']],
                               on = 'modularity_class', how = 'left')

comm_SC_counts_size.rename(columns = {'modularity_class' : 'Id'}, inplace = True)

print(comm_SC_counts_size.shape) # (45, 10)

print(comm_SC_counts_size.columns)

nodes_comm_folder_2 = ('P:/thesis_final_data/produced_data/' +
                       'papers_author_coupling/' + cos_sim_for_folder +
                       '/communities_graph/')

import os
if not os.path.exists(nodes_comm_folder_2):
    os.makedirs(nodes_comm_folder_2)

comm_SC_counts_size.to_csv(nodes_comm_folder_2 + 'nodes_communities_graph.csv')

#%%
#%% merge nodes' community with cos_sim edges

cos_sim_edges_and_comm = pd.merge(gephi_edges,
                                  nodes_comm,
                                  left_on = 'Source',
                                  right_on = 'ut_ran_id',
                                  how = 'left')

cos_sim_edges_and_comm.rename(columns = {'modularity_class' : 'source_mod_class'}, inplace = True)
cos_sim_edges_and_comm.drop(columns = ['ut_ran_id'], inplace = True)

print(cos_sim_edges_and_comm.head(10))

#%%

cos_sim_edges_and_comm_2 = pd.merge(cos_sim_edges_and_comm,
                                    nodes_comm,
                                    left_on = 'Target',
                                    right_on = 'ut_ran_id',
                                    how = 'left')

cos_sim_edges_and_comm_2.rename(columns = {'modularity_class' : 'target_mod_class'}, inplace = True)
cos_sim_edges_and_comm_2.drop(columns = ['ut_ran_id'], inplace = True)

print(cos_sim_edges_and_comm_2.columns)

#Index(['index', 'Weight', 'Source', 'Target', 'source_mod_class',
#       'target_mod_class'],
#      dtype='object')

print(cos_sim_edges_and_comm_2.head(15))
#%% calculate edges between communities and reorder tuples so there's no duplicate edges

cos_sim_edges_and_comm_2['edges_between_comm'] = list(zip(cos_sim_edges_and_comm_2.source_mod_class, cos_sim_edges_and_comm_2.target_mod_class))
cos_sim_edges_and_comm_2['weighted_edges_between_comm'] = list(zip(cos_sim_edges_and_comm_2.source_mod_class, cos_sim_edges_and_comm_2.target_mod_class))

cos_sim_edges_and_comm_2['edges_between_comm'] = cos_sim_edges_and_comm_2['edges_between_comm'].apply(lambda x : tuple(sorted(x)))
cos_sim_edges_and_comm_2['weighted_edges_between_comm'] = cos_sim_edges_and_comm_2['weighted_edges_between_comm'].apply(lambda x : tuple(sorted(x)))

print(cos_sim_edges_and_comm_2['edges_between_comm'].head(5))
print(cos_sim_edges_and_comm_2['weighted_edges_between_comm'].head(5))

#%%

inter_comm_edges = cos_sim_edges_and_comm_2[['edges_between_comm', 'Source']].groupby('edges_between_comm').count().reset_index()
inter_comm_edges.rename(columns = {'Source' : 'edge_count'}, inplace = True)

inter_comm_edges_weight = cos_sim_edges_and_comm_2[['edges_between_comm', 'Weight']].groupby('edges_between_comm').mean().reset_index()

print(inter_comm_edges.head(5))
print(inter_comm_edges_weight.head(5))

#%%

inter_comm_edges_2 = pd.merge(inter_comm_edges,
                              inter_comm_edges_weight,
                              on = 'edges_between_comm',
                              how = 'left')

print(inter_comm_edges_2.columns)
# Index(['edges_between_comm', 'edge_count', 'Weight'], dtype='object')
print(inter_comm_edges_2.head(10))
#%% count percentegae of links between communities

number_of_communities = list(set(list(nodes_comm.modularity_class)))

print(number_of_communities)

all_edges_of_all_communities = {}


for i in number_of_communities:
    print(i)
    all_edges_of_all_communities[i] = []
    
    for index, row in inter_comm_edges.iterrows():

        if row['edges_between_comm'][0] == int(i):
            all_edges_of_all_communities[i].append(row['edge_count'])

for key, item in all_edges_of_all_communities.items():
    print(key)
    print(item)
   
    # add up number od edges associated with each community
all_edges_of_all_communities_2 = all_edges_of_all_communities

for key, item in all_edges_of_all_communities_2.items():
    all_edges_of_all_communities_2[key] = sum(item)
    
#for key, item in all_edges_of_all_communities_2.items():
    #print(key)
    #print(item)

all_edges_of_all_communities_df = pd.DataFrame.from_dict(all_edges_of_all_communities_2, orient='index').reset_index()
all_edges_of_all_communities_df.rename(columns = {'index' : 'community',
                                                  0 : 'number_of_edges'}, inplace = True)

print(all_edges_of_all_communities_df)
#%% calculate percentage of edges between communities
    
inter_comm_edges_2['comm_1'] = list(i[0] for i in list(inter_comm_edges_2['edges_between_comm']))
inter_comm_edges_2['comm_2'] = list(i[1] for i in list(inter_comm_edges_2['edges_between_comm']))

print(inter_comm_edges_2)

#%%
print(all_edges_of_all_communities_df)
#%%

inter_comm_edges_3 = pd.merge(inter_comm_edges_2,
                              all_edges_of_all_communities_df,
                              left_on = 'comm_1',
                              right_on = 'community',
                              how = 'left')

inter_comm_edges_3.rename(columns = {'number_of_edges' : 'n_edges_comm_1'}, inplace = True)
inter_comm_edges_3.drop(columns = ['community'], inplace = True)

inter_comm_edges_4 = pd.merge(inter_comm_edges_3 ,
                              all_edges_of_all_communities_df,
                              left_on = 'comm_2',
                              right_on = 'community',
                              how = 'left')

inter_comm_edges_4.rename(columns = {'number_of_edges' : 'n_edges_comm_2'}, inplace = True)
inter_comm_edges_4.drop(columns = ['community'], inplace = True)

print(inter_comm_edges_4.columns)
# Index(['edges_between_comm', 'edge_count', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2'],
#      dtype='object')

#Index(['edges_between_comm', 'edge_count', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_1', 'n_edges_comm_2'],
#      dtype='object')

print(inter_comm_edges_4.head(5))


#%% add up umber of edges

inter_comm_edges_4['all_edges'] = 0

for index_label, row_series in inter_comm_edges_4.iterrows():
    #print(index_label)
    #print(row_series)
    
    if row_series['comm_1'] == row_series['comm_2']:
        inter_comm_edges_4.at[index_label, 'all_edges'] = row_series['n_edges_comm_1']

    else:
        inter_comm_edges_4.at[index_label, 'all_edges'] = row_series['n_edges_comm_1'] + row_series['n_edges_comm_2']

print(inter_comm_edges_4[['comm_1', 'comm_2', 'all_edges']].head(20))
print(inter_comm_edges_4.columns)
#Index(['edges_between_comm', 'edge_count', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2', 'all_edges'],
#      dtype='object')


#%% calculate percentage of edges between communites

inter_comm_edges_4['percentage_inter_edges'] = inter_comm_edges_4['edge_count'] / inter_comm_edges_4['all_edges'] 
#print(inter_comm_edges_3['percentage_inter_edges'])

inter_comm_edges_4['weighted_percentage_inter_edges'] = inter_comm_edges_4['percentage_inter_edges']  *  inter_comm_edges_4['Weight']

print(inter_comm_edges_4.columns)

#Index(['edges_between_comm', 'edge_count', 'Weight', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2', 'all_edges',
#       'percentage_inter_edges', 'weighted_percentage_inter_edges'],
#      dtype='object')
#%% drop edges between same nodes

print(inter_comm_edges_4.shape) # (38, 10)
print(inter_comm_edges_4.columns)

#Index(['edges_between_comm', 'edge_count', 'Weight', 'comm_1', 'comm_2',
#       'n_edges_comm_1', 'n_edges_comm_2', 'all_edges',
#       'percentage_inter_edges', 'weighted_percentage_inter_edges'],
#      dtype='object')

inter_comm_edges_5 = inter_comm_edges_4[inter_comm_edges_3['comm_1'] != inter_comm_edges_4['comm_2']]

print(inter_comm_edges_5.shape) # (30, 10)

#%% prep edges for gephi

gephi_edges_2 = inter_comm_edges_5[['comm_1', 'comm_2', 'weighted_percentage_inter_edges']]

gephi_edges_2.rename(columns = {'comm_1' : 'Source',
                                'comm_2' : 'Target',
                                'weighted_percentage_inter_edges' : 'Weight'}, inplace = True)

gephi_edges_2['Weight'] = gephi_edges_2['Weight'] * 100

gephi_edges_2.reset_index(inplace = True) 
   

nodes_comm_folder_2 = ('P:/thesis_final_data/produced_data/' +
                       'papers_author_coupling/' + cos_sim_for_folder +
                       '/communities_graph/')

import os
if not os.path.exists(nodes_comm_folder_2):
    os.makedirs(nodes_comm_folder_2)

gephi_edges_2.to_csv(nodes_comm_folder_2 + 'edges_communities_graph.csv', index = False)

#%%

import networkx as nx

G = nx.from_pandas_edgelist(gephi_edges_2, 'Source', 'Target', ['Weight'])

nx.draw(G)