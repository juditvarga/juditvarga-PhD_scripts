# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 14:11:10 2020

@author: vargajv
"""

#%%

'''

Goal: create heterogeneous ego network of methods (searchterm) where nodes are keywords OR authors, 
    and edges are their cosine similarity values
    based on co-occurrence in same ut, which also show if keywords first occur in the year when searchterm or before,
    to be visualsed in R

ALGORITHM

1. get earliest occurrence of all KEYWORDs in the data

2. get earliest occurrence of all AUTHORs in the data

3. identify all uts which have searchterm in their abstract or title AMONG PAPERS THAT HAVE AUTHOR KEYWORDS
    becuase only these will end up in my analysis

4. create edges df: 
    4.1. get author keywords (de), ut info for all uts with searchterm
    4.2. get author, ut info for all uts with searchterm
    4.3. merge these

5. create nodes df 
    5.1. calculate novelty of authors and keywords in light of searchterm
    5.2. create nodes_df
    5.3. create numeric node id

6. add numeric id to edges df

7. calculate cosine similarity between nodes

8. prepare variables for plotting (add node attributes)

'''

#%%

''' 1. get earliest occurrence of all KEYWORDs in the data'''

#%% 1.1. get data with ut, authors and pub_year (all_nodes_df)
import pandas as pd
#all_nodes_df = pd.read_csv('P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/geosocial_nodes_all_third_collection.csv', sep = '\t')
all_nodes_df = pd.read_csv('P:/thesis/thesis_final_data/collected_data/csv/1_all_citing_papers_data_csv/geosocial_nodes_all_third_collection_fullabstract.csv', sep = '\t')

print(all_nodes_df.columns)

#Index(['UT', 'ti', 'ab', 'de', 'id', 'pub_year', 'CWTS_SO_NO', 'CWTS_SC_NO',
#       'SC', 'WEIGHT', 'SO', 'AU_COUNT', 'AU_NO', 'AU'],
#      dtype='object')

# lower case all column names
all_nodes_df.columns = map(str.lower, all_nodes_df.columns)
print(all_nodes_df.columns)

#Index(['ut', 'ti', 'ab', 'de', 'id', 'pub_year', 'cwts_so_no', 'cwts_sc_no',
#       'sc', 'weight', 'so', 'au_count', 'au_no', 'au'],
#      dtype='object')

# delete all papers published before 2008

all_nodes_df = all_nodes_df[all_nodes_df['pub_year'] > 2007]

print(len(list(set(list(all_nodes_df['ut']))))) # 2759 unique uts

#print(set(stuff2['ab']))

#print(stuff.columns)
#print(set(list(stuff.de)))

#all_nodes_df.to_excel('P:/thesis/thesis_final_data/produced_data/geosocial_uts_alldat.xlsx', index = False)

#%% 1.2. create edges between words and UT s (required for the coword cos sim function) 
# and assign numeric ids to words

def word_edges_fun(coword_nodes):
    '''
    Function: creates edges between individual authors keywords and UT s  and assigns numeric ids to words
    (required for the coword cos sim function)
    Argument: coword_nodes df
    Output: dataframe with 4 columns: author keyword, UT, pub_year, random  numeric id for author keyword 
    '''
    
    import pandas as pd
    
    coword_nodes.dropna(inplace = True)
    coword_nodes['DE_split'] = coword_nodes['de'].apply(lambda x: [x.strip() for x in x.split(';')])
    coword_nodes['DE_split'] = coword_nodes['DE_split'].apply(lambda x: [w.lower() for w in x])

    coword_edges_df = pd.DataFrame()
    
    words = []
    ut_list = []
    pub_yrs = []

    for ind, row in coword_nodes.iterrows():
        for i in row['DE_split']:
     #        cowords_with_dates.append((i, int(row['pub_year'])))
            words.append(i.lower())
            ut_list.append(row['ut'])
            pub_yrs.append(int(row['pub_year']))
    #    print(type(row['DE_split']))
    #    print(row['DE_split'])
    #    print(len(row['DE_split']))

    coword_edges_df['word'] = words
    coword_edges_df['ut'] = ut_list
    coword_edges_df['pub_year'] = pub_yrs     
#    print(coword_edges_df.head(5))
#    print(coword_edges_df.shape) # (17382, 3)

    coword_edges_df.drop_duplicates(inplace = True)
    #print(coword_edges_df.shape) # (17382, 3)
    
    # create ids for words
    words_ids = pd.DataFrame()

    words_ids['keyword'] = list(set(list(list(coword_edges_df['word']))))
    words_ids['id_keyword'] = words_ids.index
    
    # merge ids with edges df
    coword_edges_df_id = pd.merge(coword_edges_df,
                                  words_ids,
                                  left_on = 'word',
                                  right_on = 'keyword',
                                  how = 'left')

    coword_edges_df_id.rename(columns = {'id_keyword' : 'id_keyword'}, inplace = True)
    coword_edges_df_id.drop(columns = ['keyword'], inplace = True)
#    print(coword_edges_df_id.columns)
#    print(coword_edges_df_id.head(5))

#    print(coword_edges_df_id.shape) # (12482, 4)
    coword_edges_df_id.drop_duplicates(inplace = True)
#    print(coword_edges_df_id.shape) # (12482, 4)
    
    return(coword_edges_df_id)

#%% get edges between keywords and uts
    
allkeywords_df = word_edges_fun(all_nodes_df)
print(allkeywords_df.shape)
print(allkeywords_df.columns)
#Index(['word', 'ut', 'pub_year', 'id_keyword'], dtype='object')
#%% get earliest occurrence of each keyword

min_py_keywords_df = pd.DataFrame(allkeywords_df[['pub_year', 'word']].groupby('word').min()).reset_index()
min_py_keywords_df.rename(columns = {'pub_year' : 'min_pub_year'}, inplace = True)
print(min_py_keywords_df.head(5))
print(min_py_keywords_df.shape)


#%%

'''2. get earliest occurrence of all AUTHORs in the data'''

#%%

min_py_authors_df = pd.DataFrame(all_nodes_df[['pub_year', 'au']].groupby('au').min()).reset_index()
min_py_authors_df.rename(columns = {'pub_year' : 'min_pub_year'}, inplace = True)
print(min_py_authors_df.head(5))
print(min_py_authors_df.shape)

#%%
#%%

'''3. identify all uts which have searchterm in their abstract or title AMONG PAPERS THAT HAVE AUTHOR KEYWORDS
    becuase only these will end up in my analysis'''

#%% 3. get all uts with searchterm (ego term)

#my_searchterm = 'bayesian'  
#my_searchterm = 'deep learning'
    
my_searchterm = 'machine learning'
#my_searchterm = 'social network analysis'

searchterm_for_file_new = my_searchterm.replace(' ', '_')

#stuff = print_info_searchterms(all_nodes_df, my_searchterm)


#stuff = get_ego_net_df_npdat(all_nodes_df, my_searchterm)

print(all_nodes_df.shape)
all_nodes_df2 = all_nodes_df.dropna(subset = ['de'])

print(all_nodes_df2.shape)
all_nodes_df2['ab'] = all_nodes_df2['ab'].str.lower()
stuff2 = all_nodes_df2[all_nodes_df2['ab'].str.contains(my_searchterm, regex = True) | all_nodes_df2['de'].str.contains(my_searchterm, regex = True)]

print('searching for abstracts')
print(len(list(set(list(stuff2['ut'])))))
print(min(stuff2['pub_year']))

a = min(stuff2['pub_year'])

ut_list = list(set(list(stuff2['ut'])))
print(ut_list)
print(len(ut_list))
#print(set(stuff2['ti']))

#print(set(stuff2['ab']))

print(stuff2.columns)

stuff3 = stuff2[['ut', 'ab']]
stuff3['ut_txt'] = stuff3['ut'].apply(lambda x: 'a_' + str(x))
stuff3.drop_duplicates(inplace = True)
stuff3.to_excel('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/{}/ut_{}.xlsx'.format(searchterm_for_file_new, searchterm_for_file_new))
stuff3.to_csv('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/{}/ut_{}.csv'.format(searchterm_for_file_new, searchterm_for_file_new))

#%%

'''
4. create edges df: 
    4.1. author keywords (de), UT for all uts with searchterm
'''

#%% 3.5. select rows with certain searchterm

def get_ego_net_df_npdat(nodes_df):
    
    '''
    Function: subsets nodes_df to only include uts (papers) with searchterm in their ABSTRACT / TITLES
    '''
    
#    ego_net_df = nodes_df[nodes_df['de'].str.contains(searchterm)]
    ego_net_df_indices = nodes_df[nodes_df['ut'].isin(ut_list)].index
    
    #print(ego_net_df_indices)
    #print(len(list(ego_net_df_indices)))

    
    ego_net_df = nodes_df.loc[ego_net_df_indices]
    print('number of uts before deleting uts with no author keywords')
    print(len(list(set(list(ego_net_df['ut'])))))
    print('\n')
    
    # delete rows (uts) without author keywords
    ego_net_df.dropna(subset=['word'], inplace = True)
    print('number of uts after deleting uts with no author keywords')
    print(len(list(set(list(ego_net_df['ut'])))))
    print('\n')
#    print(ego_net_df.shape)
    
    return(ego_net_df) 
    
#%%
ego_keywords = get_ego_net_df_npdat(allkeywords_df)
ego_keywords.rename(columns = {'word' : 'actant'}, inplace = True)
ego_keywords.drop(columns = ['pub_year', 'id_keyword'], inplace = True)
ego_keywords['actant_type'] = 'keyword'

print(ego_keywords.columns)
print(ego_keywords.shape)

#%%

'''
4. create edges df: 
    4.2. AUTHOR, UT for all uts with searchterm
'''

ego_authors = stuff2[['ut', 'au']]
ego_authors.rename(columns = {'au' : 'actant'}, inplace = True)
ego_authors['actant_type'] = 'author'
print(ego_authors.columns)
print(ego_authors.columns)

print(len(list(set(list(ego_authors.ut)))))


#%%
'''
4. create edges df: 
    4.3. get all edges
'''

# KEYWORDS and AUTHORS
all_edges_df = pd.concat([ego_authors, ego_keywords], sort = True)
print(all_edges_df.shape)
print(all_edges_df.columns) # Index(['actant', 'actant_type', 'ut'], dtype='object')

#%%
'''
5. create nodes df 
    5.1. calculate novelty of authors and keywords in light of searchterm
'''

# diff in pub year of authors

print(min_py_authors_df.columns)
min_py_authors_df.rename(columns = {'au' : 'actant'}, inplace = True)
min_py_authors_df['actant_type'] = 'author'
print(min_py_authors_df.columns)
min_py_authors_df['searchterm_min_py'] = a
min_py_authors_df['diff'] = min_py_authors_df['searchterm_min_py'] - min_py_authors_df['min_pub_year']

year_diff = pd.DataFrame(min_py_authors_df[['diff', 'actant']].groupby('diff').count()).reset_index()
year_diff.rename(columns = {'actant' : 'count'}, inplace = True)
                                
my_barchart = year_diff.plot.bar(y= 'count',  \
                                 x= 'diff', \
                                 rot=20, \
                                 color= 'orange',\
                                 grid = False)

import numpy as np
min_py_authors_df['diff_binary'] = np.where(min_py_authors_df['diff'] > 0, 'previously_used', 'first_time_with_keyword')

year_diff_bin = pd.DataFrame(min_py_authors_df[['diff_binary', 'actant']].groupby('diff_binary').count()).reset_index()
year_diff_bin.rename(columns = {'actant' : 'count'}, inplace = True)

my_barchart = year_diff_bin.plot.bar(y= 'count',  \
                                     x= 'diff_binary', \
                                     rot=0, \
                                     color= 'green',\
                                     grid = False)

print(min_py_authors_df.shape)
#%% diff in pub year of keywords

print(min_py_keywords_df.columns)
min_py_keywords_df.rename(columns = {'word' : 'actant'}, inplace = True)
min_py_keywords_df['actant_type'] = 'keyword'
print(min_py_keywords_df.columns)
min_py_keywords_df['searchterm_min_py'] = a
min_py_keywords_df['diff'] = min_py_keywords_df['searchterm_min_py'] - min_py_keywords_df['min_pub_year']
min_py_keywords_df['diff_binary'] = np.where(min_py_keywords_df['diff'] > 0, 'previously_used', 'first_time_with_keyword')



print(min_py_keywords_df.shape)
print(min_py_keywords_df.head(5))
#%% diff in pub year all actants

min_py_df = pd.concat([min_py_authors_df, min_py_keywords_df], sort = True)
print(min_py_df.shape)
print(min_py_df.columns) # Index(['actant', 'actant_type', 'min_pub_year'], dtype='object')
min_py_df.drop_duplicates(inplace = True)
print(min_py_df.shape)
print(min_py_df.columns) 

# Index(['actant', 'actant_type', 'diff', 'diff_binary', 'min_pub_year',
#       'searchterm_min_py'],      dtype='object')

#%%
'''
5. create nodes df 
    5.2. create nodes_df
'''

nodes_df_1 = all_edges_df[['actant']].drop_duplicates()
print(nodes_df_1.shape)
print(nodes_df_1.columns)

nodes_df_2 = pd.merge(nodes_df_1, min_py_df, how = 'left', on = 'actant')

# remove searchterm from nodes

nodes_df_3 = nodes_df_2[nodes_df_2['actant'] != my_searchterm]

print(nodes_df_3.shape)
print(nodes_df_3.columns)
#%%
'''
5. create nodes df 
    5.3. create numeric node id
'''
nodes_df_3.reset_index(inplace = True)
nodes_df_3['num_id'] = nodes_df_3.index + 1
print(nodes_df_3['num_id'])

print(nodes_df_3.columns)

#Index(['actant', 'actant_type', 'diff', 'diff_binary', 'min_pub_year',
#       'searchterm_min_py', 'Id', 'num_id'],
#      dtype='object')

print(nodes_df_3['num_id'])

#%% plot newness of nodes

nodes_df_subset = nodes_df_3[nodes_df_3['actant_type'] == 'author'] 
my_color = 'green' 

nodes_df_subset = nodes_df_3[nodes_df_3['actant_type'] == 'keyword']
my_color = 'blue' 

year_diff = pd.DataFrame(nodes_df_subset[['diff', 'actant']].groupby('diff').count()).reset_index()
year_diff.rename(columns = {'actant' : 'count'}, inplace = True)
                                
my_barchart = year_diff.plot.bar(y= 'count',  \
                                 x= 'diff', \
                                 rot=20, \
                                 color= 'orange',\
                                 grid = False)

import numpy as np

year_diff_bin = pd.DataFrame(nodes_df_subset[['diff_binary', 'actant']].groupby('diff_binary').count()).reset_index()
year_diff_bin.rename(columns = {'actant' : 'count'}, inplace = True)

my_barchart = year_diff_bin.plot.bar(y= 'count',  \
                                     x= 'diff_binary', \
                                     rot=0, \
                                     color= my_color,\
                                     grid = False)


#%%

'''6. add numeric id to edges df'''

print(all_edges_df.shape)

# remove edges to machine learning

all_edges_df_2 = all_edges_df[all_edges_df['actant'] != my_searchterm]
print(all_edges_df_2.shape)
print(all_edges_df_2.columns)

# get numeric id
all_edges_df_3 = pd.merge(all_edges_df_2, nodes_df_3, how = 'left', on = 'actant')
print(all_edges_df_3.shape)
print(all_edges_df_3.columns)

#
all_edges_df_4 = all_edges_df_3[['actant', 'ut', 'num_id']]
print(all_edges_df_4.shape)


#%%

'''7. calculate cosine similarity between nodes'''

import os

# change working directory
os.chdir("P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/")
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

cos_sim = 0.0
cos_sim_for_filename = str(cos_sim).replace('.', '_')
cos_sim_for_folder = 'cos_sim_' + cos_sim_for_filename 

cos_sim_het_network = bib_couple_cosine_similarity.bib_couple_cos_similarity_df(all_edges_df_4, cos_sim)

#%% get original names of nodes

print(cos_sim_het_network.head(5))
print(cos_sim_het_network.columns)

cos_sim_het_network.rename(columns = {'citing_paper_1' : 'Source',
                                      'citing_paper_2' : 'Target'}, inplace = True)
    
    
print(cos_sim_het_network.head(5))
print(cos_sim_het_network.columns)
#%%

''' 8. prepare variables for plotting (add node attributes) '''

#%% save nodes and edges csv

my_searchterm_for_folder = my_searchterm.replace(' ', '_')
print(my_searchterm_for_folder)

nodes_folder = ('P:/thesis/thesis_final_data/produced_data/' +
                'heterogeneous_networks/' + my_searchterm_for_folder + '/' + 
                cos_sim_for_folder)

import os
if not os.path.exists(nodes_folder):
    os.makedirs(nodes_folder)

# save nodes
print(nodes_df_3.columns)
nodes_df_3.rename(columns = {'num_id' : 'Id'}, inplace = True)

print(nodes_df_3.columns)
# Index(['index', 'word_or_AU', 'diff_binary', 'type', 'Id', 'shape'], dtype='object')

print('number of nodes in nodes: ' + str(len(list(set(list(nodes_df_3.Id))))))
# number of nodes in nodes: 191

# add vertex shape attribute for R

import numpy as np
nodes_df_3['shape'] = np.where(nodes_df_3['actant_type'] == 'author', 'circle', 'square')

print(nodes_df_3['shape'].head(5))

print('\nshapes: ')
print(set(list(nodes_df_3['shape'])))

print('\nsdiff: ')
print(set(list(nodes_df_3['diff_binary'])))

print(len(set(list(nodes_df_3['actant']))))

print(max(nodes_df_3['Id']))

print(min(nodes_df_3['Id']))


#%%


nodes_df_3.drop_duplicates(inplace = True)
nodes_df_3.to_csv(nodes_folder + '/{}_nodes.csv'.format(my_searchterm_for_folder), index = False)
nodes_df_3.to_excel(nodes_folder + '/{}_nodes.xlsx'.format(my_searchterm_for_folder), index = False)


# save edges

print('number of nodes in edges: ' + str(len(list(set(list(list(cos_sim_het_network.Source) + list(cos_sim_het_network.Target)))))))
#number of nodes in edges: 191
cos_sim_het_network.rename(columns = {'cosine_similarity' : 'Weight'}, inplace = True)
cos_sim_het_network_2 = cos_sim_het_network[['Source', 'Target', 'Weight']]

print(len(set(list(cos_sim_het_network_2['Source']) + list(cos_sim_het_network_2['Target']))))

#%%

print(max(nodes_df_3['Id']))


my_histogram = cos_sim_het_network_2.hist(column= 'Weight', bins = 60, grid = False)

print(cos_sim_het_network_2.shape)

cos_sim_het_network_2.to_csv(nodes_folder + '/{}_edges.csv'.format(my_searchterm_for_folder), index = False)
cos_sim_het_network_2.to_excel(nodes_folder + '/{}_edges.xlsx'.format(my_searchterm_for_folder), index = False)

#%% check relationship between the two

social_media_nodes = pd.read_csv('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/social_network_analysis/cos_sim_0_0/social_network_analysis_nodes.csv')

ml_nodes = pd.read_csv('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/machine_learning/cos_sim_0_0/machine_learning_nodes.csv')

inner = pd.merge(social_media_nodes, ml_nodes, how = 'inner', on = 'actant')

print(inner)

#%%

social_media_nodes = pd.read_excel('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/social_network_analysis/cos_sim_0_0/social_network_analysis_nodes_manual_classified.xlsx')

ml_nodes = pd.read_excel('P:/thesis/thesis_final_data/produced_data/heterogeneous_networks/machine_learning/cos_sim_0_0/machine_learning_nodes_manual_classified.xlsx')




