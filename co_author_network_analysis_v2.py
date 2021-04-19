# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:23:43 2020

@author: vargajv
"""

#%%

'''

this script:
    
1. prepare data that can serve basis for temporal co-author networks

2. create temporal co-author network files

in R: 

3. calculate modularity of co-author networks and compare this to modularity of random graph null models

4. plot

steps 3 and 4 done in R because there is a community detection algorithm which can take weight into account


'''

#%%
#%%  1. prepare data that can serve basis for temporal co-author networks
#%%  read in nodes (citing papers) with info, pub_year already filtered
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

#%% check papers with no authorname  info, delete NAs

nas = all_nodes_df.AU.isnull().sum() # check number of nas in AU column
print(nas) # 1

all_nodes_df['AU'].fillna('0', inplace = True)
#print(all_nodes_df[all_nodes_df['AU'] == '0'])

# drop the 1 paper with no author info
print(all_nodes_df.shape)  # (17701, 14)
all_nodes_df = all_nodes_df.loc[all_nodes_df['AU'] != '0']
print(all_nodes_df.shape) # (17700, 14)

#%% select columns for co-author network

temp_nodes_authors_df = all_nodes_df.loc[:, ['UT', 'AU_NO', 'pub_year']]
temp_nodes_authors_df.rename(columns = {'UT': 'ut'}, inplace = True)
    
print(temp_nodes_authors_df.columns) # Index(['ut', 'AU_NO', 'pub_year'], dtype='object')
print(temp_nodes_authors_df.shape) # (17700, 3)

#%% assign numeric ids to auhtors so they can be ordered as part of the co-author function

author_ids = pd.DataFrame()
author_ids['AU_NO'] = list(set(list(temp_nodes_authors_df['AU_NO'])))
author_ids.reset_index(inplace = True)
author_ids.rename(columns = {'index': 'ran_id'}, inplace = True)

print(author_ids.columns)
# Index(['ran_id', 'AU'], dtype='object')

print(author_ids.shape) # (7797, 2)
print(author_ids.head(5))

temp_nodes_authors_df_2 = pd.merge(temp_nodes_authors_df,
                                   author_ids,
                                   on = 'AU_NO',
                                   how = 'left')

print(temp_nodes_authors_df_2.columns)
# Index(['ut', 'AU_NO', 'pub_year', 'ran_id'], dtype='object')
print(temp_nodes_authors_df_2.shape)
# (17700, 4)

# drop duplicates
temp_nodes_authors_df_2.drop_duplicates(subset = ['ut', 'AU_NO', 'pub_year', 'ran_id'], inplace = True)
print(temp_nodes_authors_df_2.shape) # (9635, 4)

#%% SPLIT DATA TO 3 TIME PERIODS, BECAUSE I'LL HAVE TO 
# CALCULATE THE NETWORK SEPARATELY FOR THEM

# I decided to split the data to periods so that 
# the volume of papers included in periods is incremental
# tried these bins:
# [2019, 2018, 2017], [2016, 2015, 2014], [<= 2013]
# or
# [2019, 2018], [2017, 2016], [2015, 2014], [<= 2013] - I decided with this

folder_temp_authors_nodes = ('P:/thesis/thesis_final_data/produced_data/' + 
                             'co_authors_graph_data/1_temporal_co_authors_nodes/')

import os
if not os.path.exists(folder_temp_authors_nodes):
    os.makedirs(folder_temp_authors_nodes)

# also filter for papers after 2007, beccause there are a few very early papers in the dataset for some reason
ut_au_t1 = temp_nodes_authors_df_2.loc[temp_nodes_authors_df_2['pub_year'] < 2014]
print(ut_au_t1.shape) # (849, 4)
#print(citing_papers_words_t1.columns) #Index(['ut', 'pub_year', 'de'], dtype='object')
ut_au_t1.to_csv(folder_temp_authors_nodes + 'co_author_nodes_t_1.csv', index = False)
#print(citing_papers_words_t1.pub_year.head(5))
#print(max(citing_papers_words_t1.pub_year))
#print(min(citing_papers_words_t1.pub_year))

ut_au_t2 = temp_nodes_authors_df_2.loc[temp_nodes_authors_df_2['pub_year'] < 2016]
print(ut_au_t2.shape) # (2535, 4)
#print(citing_papers_words_t1.columns) #Index(['ut', 'pub_year', 'de'], dtype='object')
ut_au_t2.to_csv(folder_temp_authors_nodes + 'co_author_nodes_t_2.csv', index = False)

ut_au_t3 = temp_nodes_authors_df_2.loc[temp_nodes_authors_df_2['pub_year'] < 2018]
print(ut_au_t3.shape) # (5432, 4)
#print(citing_papers_words_t1.columns) #Index(['ut', 'pub_year', 'de'], dtype='object')
ut_au_t3.to_csv(folder_temp_authors_nodes + 'co_author_nodes_t_3.csv', index = False)


#citing_papers_words_t3 = citing_papers_words.loc[citing_papers_words['pub_year'] > 2017]
ut_au_t4 = temp_nodes_authors_df_2
print(ut_au_t4.shape) # (9635, 4)
ut_au_t4.to_csv(folder_temp_authors_nodes + 'co_author_nodes_t_4.csv', index = False)

#%% 
#%% 2. create co-author network files
#%% call coword cos sim fuction on temporal author ut files

# set cosine similarity cutoff value

my_cos_sim = 0.1
cos_sim_subfolder = 'cos_sim_filt_' + str(my_cos_sim).replace('.', '_') + '/' # for dir names

# create directory to save word cos sim files

folder_temp_authors_cos_sim = ('P:/thesis/thesis_final_data/produced_data/' + 
                               'co_authors_graph_data/2_temporal_co_authors_cos_sim/' 
                               + cos_sim_subfolder)

import os
if not os.path.exists(folder_temp_authors_cos_sim):
    os.makedirs(folder_temp_authors_cos_sim)

# create word cos sim files
directory = folder_temp_authors_nodes

# NEEDS MANUAL INPUT: COS_SIM cutoff value

for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
         coword_edges_filedir = os.path.join(directory, filename)
         coword_edges = pd.read_csv(coword_edges_filedir)
         # print(coword_edges.columns)
         time_period = filename[-8:-4]
         print(time_period)
         print(coword_edges.columns)
         
         # file to use in function call
         coword_edges_2 = coword_edges[['ut', 'ran_id']]
         
         # change working directory
         os.chdir("P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts")
         #print("Current Working Directory " , os.getcwd())


         from co_word_edges import coword_similarity_df

         cos_sim = my_cos_sim
         cos_sim_for_filename = str(cos_sim).replace('.', '_')

         coword_cos_sim_df = coword_similarity_df(coword_edges_2, cos_sim)
         
         # rename 'word_1' and 'word_2' to 'author_1_ran_id' and 'author_2_ran_id'
         coword_cos_sim_df.rename(columns = {'word_1' : 'author_1_ran_id',
                                             'word_2' : 'author_2_ran_id'}, inplace = True)
    
         coword_cos_sim_df.to_csv(folder_temp_authors_cos_sim + 'co_authors_edges_cos_sim{}.csv'.format(time_period), index = False)
    else:
        continue
    
#%% check authors cos sim files
        
directory = folder_temp_authors_cos_sim

for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
         coword_edges_filedir = os.path.join(directory, filename)
         coword_edges = pd.read_csv(coword_edges_filedir)
         print(coword_edges.columns)
#         print(coword_edges[['author_1_ran_id', 'author_2_ran_id']].head(5))
         print(coword_edges.head(5))
         print(coword_edges.shape)
         # t_1 (1499, 3)
         # t_2 (4453, 3)
         # t-3 (10853, 3)
         # t_4 (19864, 3)
         my_histogram = coword_edges.hist(column= 'cosine_similarity', bins = 12, grid = False)
    else:
        continue
    
#%%  
#%% unused scripts - simulation done in R because 
#%% create weight counter df for simulation
        
folder_temp_authors_cos_sim_counter = ('P:/thesis/thesis_final_data/produced_data/' + 
                                       'co_authors_graph_data/3_co_authors_cos_sim_weight_counter/' 
                                       + cos_sim_subfolder)

import os
if not os.path.exists(folder_temp_authors_cos_sim_counter):
    os.makedirs(folder_temp_authors_cos_sim_counter)
        
directory = folder_temp_authors_cos_sim

for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
         coword_edges_filedir = os.path.join(directory, filename)
         coword_edges = pd.read_csv(coword_edges_filedir)
         print(coword_edges.columns)
         # Index(['cosine_similarity', 'author_1_ran_id', 'author_2_ran_id'],
         time_period = filename[-8:-4]
         #counter
         weight_counter_df = coword_edges[['cosine_similarity', 'author_1_ran_id']].groupby('cosine_similarity').count().reset_index()
         weight_counter_df.rename(columns = {'author_1_ran_id' : 'number_of_edges'}, inplace = True)
         print(weight_counter_df.head(5))
         
#         my_barchart = weight_counter_df.plot.bar(y= 'number_of_edges',  \
#                                                  x= 'cosine_similarity', \
#                                                  rot=90, \
#                                                  color= 'yellow',\
#                                                  grid = False)
         
         print(weight_counter_df.shape)
         
         weight_counter_df.to_csv(folder_temp_authors_cos_sim_counter + 'co_authors_cos_sim_weight_counter{}.csv'.format(time_period))
    else:
        continue


#%%compare modularity of temporal co-author graphs to simulated ones and plot
        
def sim_null_models(all_edges_df, directory, time_stamp):
    
    '''
    Arguments: 
        all_edges_df = df with edges of an undirected network, at least 3 columns:
            i. 'cosine_similarity'  = cos simularity between nodes = edge weight
            ii. 'author_1_ran_id' = node 1
            iii. 'author_2_ran_id' = node 2
    '''
    
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # import packages
    import pandas as pd
    from random import shuffle
    import networkx as nx
    from networkx.algorithms.community import greedy_modularity_communities
    from networkx.algorithms.community.centrality import girvan_newman
    import numpy as np
    
    all_edges_df.columns = ['weight', 'node_1', 'node_2']
    
    # number of edges and nodes for simlation
    
    n_nodes = len(list(set(list (list(all_edges_df['node_1']) + list(all_edges_df['node_2'])))))
    print('number of nodes: ' + str(n_nodes))
    n_edges =  all_edges_df.shape[0]
    print('number of edges: ' + str(n_edges))
    cos_sim_list = all_edges_df['weight']
    
    # round edges df
    all_edges_df_ord_round = all_edges_df.round({'weight': 3})
    
    # calculate modularity of original graph
    G = nx.from_pandas_edgelist(all_edges_df_ord_round, 'node_1', 'node_2', ['weight'])
    
    #comm = list(greedy_modularity_communities(G))
    comm = list(girvan_newman(G))
    
    mod_G = nx.algorithms.community.modularity(G, comm)  # to go with greedy mod max
    
    print('mod original graph: ')
    print(mod_G)

    # create list to save subgraph modularities in
    all_simulated_graph_modularities = []
    
    print('original mod detected, simulating graphs')
    
    # simulate 100 networks
    for num in list(range(0, 5)):
        
        GRAN = nx.gnm_random_graph(n_nodes, n_edges)
        print('graph {} simulated'.format(num))
        
        # add edge weights to simulated graph
        df = nx.to_pandas_edgelist(GRAN)
        # df['weight'] = shuffle(cos_sim_list) # shuffle takes way too long, works in place and returns None
        df['weight'] = np.random.permutation(cos_sim_list)
        
        # detect communitoes om GRAN
        #communities = list(greedy_modularity_communities(GRAN))
        communities = list(girvan_newman(GRAN))
    
    
        # calculate modularity of the subgraph
        sim_graph_modularity = nx.algorithms.community.modularity(GRAN, communities) # to go with greedy modmax algorithm
        all_simulated_graph_modularities.append(sim_graph_modularity)
        print('mod calculated for network ' + str(num))
        
        
    # plot
    
    from matplotlib import pyplot as plt
    

    # calculate 'conf int 1'
    rangess_sorted_2 = sorted(all_simulated_graph_modularities)
    confint_no_weights = rangess_sorted_2[25:-25]
    confint_no_weights_min = min(confint_no_weights)
    confint_no_weights_max = max(confint_no_weights)

    #plot
    fig, ax = plt.subplots()
    ax = plt.axes(frameon=False)
    ax.hist(rangess_sorted_2, color = 'green', bins=100, alpha=0.5)
#    ax.set_xlim(0.025, 0.038)

    plt.axhline(linewidth=2, color = 'black')

    plt.axvline(linewidth=1, x= mod_G, color = 'red')
    plt.axvline(linewidth=1, x= 0.025, color = 'black')

    # conf interval lines
    plt.axvline(linewidth=1, x= confint_no_weights_min, color = 'green')
    plt.axvline(linewidth=1, x= confint_no_weights_max, color = 'green')


    fig.savefig(directory + 'hist_sim_co_author_mod_with_weight_{}.png'.format(time_stamp), transparent=False, dpi=80, bbox_inches="tight")
        
    return('all done')
    
    
    #%%