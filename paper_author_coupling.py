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

#%% read in bibliographic coupling edges files

import os
import pandas as pd

nodes_data_1_path = ('P:/thesis/thesis_final_data/collected_data/csv/' +
                     '1_all_citing_papers_data_csv/' + 
                     'geosocial_nodes_dat_1_feb_2020.csv')


all_nodes_df = pd.read_csv(nodes_data_1_path, sep = '\t')

print(all_nodes_df.shape) # (4918, 11)

# delete row added by SQL aboout the number of rows affected
all_nodes_df  = all_nodes_df [~all_nodes_df['ut'].str.contains("rows")]
print(all_nodes_df.shape) # (4917, 11)

print(all_nodes_df.columns)

#Index(['ut', 'ti', 'ab', 'de', 'id', 'pub_year', 'CWTS_SO_NO', 'CWTS_SC_NO',
#       'SC', 'WEIGHT', 'SO'],
#      dtype='object')

# plot pub_year of papers

print(min(all_nodes_df.pub_year)) # 286.0
print(max(all_nodes_df.pub_year)) # 23434.0
#all_nodes_df.sort_values(by = 'pub_year', inplace = True)
#all_nodes_df.sort_values(by = 'pub_year', ascending = False, inplace = True)
#print(all_nodes_df['pub_year'].head(5))

# there are a few odd values for pub_year, 
# I'm deleting the rows associated with them
# and changing the data type of pub_year to integer

#%% get infnormation about cited references with their authors, which are
# in 2 different csv files

#%%  cited refs csv

all_cited_edges_path = ('P:/thesis/thesis_final_data/collected_data/csv/' +
                         '2_all_cited_refs_data_csv/' + 
                         'geosocial_cited_ref_data_feb_2020.csv')


all_cited_edges_df = pd.read_csv(all_cited_edges_path, sep = '\t')

print(all_cited_edges_df .shape) # (64979, 2)

# delete row added by SQL aboout the number of rows affected
all_cited_edges_df = all_cited_edges_df [~all_cited_edges_df['ut'].str.contains("rows")]
print(all_cited_edges_df.shape) # (64978, 2)

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
                                   all_nodes_df[['ut', 'pub_year', 'SO', 'CWTS_SO_NO', 'SC']] ,
                                   left_on = 'ut',
                                   right_on = 'ut',
                                   how = 'left')

print(all_cited_edges_au_df_3.columns)

#Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'pub_year', 'SC'], dtype='object')

# check NANs

print(all_cited_edges_au_df_3.shape) # (433731, 8)

nas = all_cited_edges_au_df_3[all_cited_edges_au_df_3['pub_year'].isnull()] # (7640, 8)
print(nas.shape) 

print('\nnumber of cited refs without publication year info: ' + str(len(list(set(list(nas['ut']))))))
# number of cited refs without publication year info: 90

#%% add pub_year info to the rest of the papers

uts_missing_pub_year_path = ('P:/thesis/thesis_final_data/collected_data/csv/' +
                             '1_all_citing_papers_data_csv/' + 
                             'ut_pub_year_second_collection.csv')

uts_missing_pub_year_df = pd.read_csv(uts_missing_pub_year_path, sep = '\t')

print(uts_missing_pub_year_df.shape) # (92, 2)

# delete row added by SQL aboout the number of rows affected
uts_missing_pub_year_df  = uts_missing_pub_year_df [~uts_missing_pub_year_df['ut'].str.contains("rows")]
#uts_missing_pub_year_df.reset_index(inplace = True)
print(uts_missing_pub_year_df.shape) # (91, 2)

print(uts_missing_pub_year_df.columns)
# Index(['ut', 'pub_year'], dtype='object')
#%% merge missing data and get pub_year values

all_cited_edges_au_df_4 = pd.merge(all_cited_edges_au_df_3,
                                   uts_missing_pub_year_df,
                                   left_on = 'ut',
                                   right_on = 'ut',
                                   how = 'left')

print(all_cited_edges_au_df_4.shape) # (433731, 9)

print(all_cited_edges_au_df_4.columns)

# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'pub_year_x', 'SC',
#       'pub_year_y'],
#      dtype='object')

all_cited_edges_au_df_4['pub_year_x'].fillna(all_cited_edges_au_df_4['pub_year_y'], inplace = True)

print(all_cited_edges_au_df_4.loc[all_cited_edges_au_df_4['pub_year_x'].isna()]) # eempty df

all_cited_edges_au_df_4.rename(columns = {'pub_year_x' : 'pub_year'}, inplace = True)

print(all_cited_edges_au_df_4.columns)
# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'pub_year', 'SC',
#       'pub_year_y'],
#      dtype='object')
#%% select data about citing papers published after 2007

all_cited_edges_au_df_4['pub_year'] = all_cited_edges_au_df_4['pub_year'].astype(int)

# select papers published between 2008 and 2020
all_cited_edges_au_df_5 = all_cited_edges_au_df_4.loc[(all_cited_edges_au_df_4['pub_year'] > 2007) \
                                                      & (all_cited_edges_au_df_4['pub_year'] < 2020)]

#my_histogram = all_nodes_df.hist(column= 'pub_year', bins = 12, grid = False)

# get yearly publication count so I can do barchart as opposed to histogram

yearly_pub_count = pd.DataFrame(all_cited_edges_au_df_5[['ut', 'pub_year']].\
                                groupby('pub_year').count()).\
                                reset_index()
                                
yearly_pub_count.rename(columns = {'ut' : 'pub_count'}, inplace = True)
                                
#print(yearly_pub_count.head(5))
                                
my_barchart = yearly_pub_count.plot.bar(y= 'pub_count',  \
                                        x= 'pub_year', \
                                        rot=20, \
                                        color= 'yellow',\
                                        grid = False)

# TODO: probably should normalise it by some sort of growth factor

print('\nnumber of unique citing papers: ' + str(len(list(set(list(all_cited_edges_au_df_5['ut']))))))
# number of unique citing papers: 2781

print('number of cited refs: ' + str(len(list(set(list(all_cited_edges_au_df_5['S_UT']))))))
#number of cited refs: 43982, instead of 44171 before getting papers publisedh after 2007

#%% join SC s for SC_categories function

SC_joined_df = pd.DataFrame(all_nodes_df.groupby('SO')['SC'].apply(lambda x: '; '.join(x)))

print(SC_joined_df.head(5))
print(SC_joined_df.shape) # (1062, 1)

SC_joined_df.rename(columns = {'SC' : 'SC_joined'}, inplace = True)

all_cited_edges_au_df_6 = pd.merge(all_cited_edges_au_df_5,
                                   SC_joined_df,
                                   left_on = 'SO',
                                   right_on = 'SO',
                                   how = 'left')

print(all_cited_edges_au_df_6.columns)
# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'pub_year', 'SO', 'SC',
#       'pub_year_y', 'SC_joined'],
#      dtype='object')


# remove duplicate nodes resulting from multiple SCs categorised to any one journal
all_cited_edges_au_df_7 = all_cited_edges_au_df_6.drop_duplicates() 
all_cited_edges_au_df_7.drop(columns = ['SC'], inplace = True)

print(all_cited_edges_au_df_7.columns)

# Index(['ut', 'pub_year', 'CWTS_SO_NO', 'SO', 'CWTS_SC_NO', 'WEIGHT',
#      'SC_joined'],
#       dtype='object')

print(all_cited_edges_au_df_7.shape) # (2255, 8)

print('\nnumber of unique citing papers: ' + str(len(list(set(list(all_cited_edges_au_df_7['ut']))))))
# number of unique citing papers: 2781
# number of unique citing papers: 2781

print('number of cited refs: ' + str(len(list(set(list(all_cited_edges_au_df_7['S_UT']))))))
#number of cited refs: 43982, instead of 44171 before getting papers publisedh after 2007
# number of cited refs: 43982

#%% categorise subject categories of citing papers

# function description

#    Argument: a dataframe which has at least 1 column called 'SC_joined', which is a string
#              and contains information about the WOSKB subject category associated with papers 
              
#    Output: a dataframe with additional columns which signal subject category categories

import os

print("Current Working Directory " , os.getcwd()) # C:\Users\vargajv

# change working directory
os.chdir("P:/thesis_final_scripts/2_python_final_data_analysis_scripts/")
print("Current Working Directory " , os.getcwd())

from SC_categories_function import SC_categories

SC_cat_cited_edges = SC_categories(all_cited_edges_au_df_7)

#%% print SC categories

# change working directory
os.chdir("P:/thesis_final_scripts/2_python_final_data_analysis_scripts/")
print("Current Working Directory " , os.getcwd())

from SC_categories_function import print_subject_categories

print_edges = print_subject_categories(SC_cat_cited_edges)

#%%
#%% create numeric id for ut s

ut_num_id_df = pd.DataFrame()

ut_num_id_df['ut'] = list(set(list(all_cited_edges_au_df_2['ut'])))
ut_num_id_df['ut_ran_id'] = ut_num_id_df.index

print(ut_num_id_df.head(5))

#%% merge citing papers and radnom numeric ids

SC_cat_cited_edges_2 = pd.merge(all_cited_edges_au_df_2,
                                ut_num_id_df,
                                left_on = 'ut',
                                right_on = 'ut',
                                how = 'left')

print(SC_cat_cited_edges_2.columns)
# Index(['S_UT', 'AU_COUNT', 'AU_NO', 'AU', 'ut', 's_ut', 'ut_ran_id'], dtype='object')


print('number of cited refs: ' + str(len(list(set(list(SC_cat_cited_edges_2['s_ut']))))))
#number of cited refs: 44171

print('number of cited refs: ' + str(len(list(set(list(SC_cat_cited_edges_2['S_UT']))))))
#number of cited refs: 44171

print('\nnumber of citing papers: ' + str(len(list(set(list(SC_cat_cited_edges_2['ut']))))))
#number of citing papers: 2791

print('\nnumber of citing papers: ' + str(len(list(set(list(SC_cat_cited_edges_2['ut_ran_id']))))))
#number of citing papers: 2791


#%% check nas

nan_rows = SC_cat_cited_edges_2[SC_cat_cited_edges_2['AU'].isnull()]
print(nan_rows.shape) # (110, 7)

print('\nnumber of cited refs without author info: ' + str(len(list(set(list(nan_rows['s_ut']))))))
# number of cited refs without author info: 26

print('\nnumber of citing papers which have cited ref without author info: ' + str(len(list(set(list(nan_rows['ut']))))))
# number of cited refs without author info: 109

#%% drop na
print(SC_cat_cited_edges_2.shape) # (236794, 7)

SC_cat_cited_edges_3 = SC_cat_cited_edges_2[['ut', 'AU', 'ut_ran_id']]
SC_cat_cited_edges_3.dropna(inplace = True)
print(SC_cat_cited_edges_3.shape) # (236684, 3)

#%% delete duplicate edges
# one paper can cite the same authro multiple times but that's not important for me
SC_cat_cited_edges_3.drop_duplicates(inplace = True) 
print(SC_cat_cited_edges_3.shape) # shape (207019, 3)


#%%

print(SC_cat_cited_edges_3.columns)
# Index(['ut', 'AU', 'ut_ran_id'], dtype='object')
#%% PAPERS - AUTHOR -COUPLING NETWORK

# CALCULATE COSINE SIMILARITY among citing 'journals' - for journals' co-author coupling

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

cos_sim = 0.1
cos_sim_for_filename = str(cos_sim).replace('.', '_')

papers_auth_coupling_cos_sim_df = bib_couple_cosine_similarity.bib_couple_cos_similarity_df(SC_cat_cited_edges_3, cos_sim)


#%% PAPERS - AUTHOR COUPLING NETWORK
# check bib coupling df

print(papers_auth_coupling_cos_sim_df.shape)
# for cos sim > 0.2, shape (1183, 3)
# for cos sim > 0.25, shape (502, 3)
# for cos sim > 0.35, shape (122,3)
# for cos sim > 0.36, shape (108,3)
# for cos sim > 0.4, shape (74,3)

papers_auth_coupling_cos_sim_df.columns = ['paper_auth_cosine_similarity', 'paper_1', 'paper_2']

print(papers_auth_coupling_cos_sim_df.head(5))

#%% 

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

paper_co_author_for_gephi_path = ('P:/thesis_final_data/produced_data/' +
                                  'papers_author_coupling/' + cos_sim_for_folder +
                                  '/for_gephi/')

import os
if not os.path.exists(paper_co_author_for_gephi_path):
    os.makedirs(paper_co_author_for_gephi_path)
  
gephi_edges.to_csv( paper_co_author_for_gephi_path + 'papers_author_coupling_for_gephi.csv', index=False)

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