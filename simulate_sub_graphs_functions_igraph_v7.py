# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:11:54 2020

@author: vargajv
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:42:07 2020

@author: vargajv
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 22:30:09 2020

@author: vargajv
"""

#%%

'''
GOAL

Study the role of edges between 'only social' and 'only technical' journals
by comparing the modularity of the journal author-bibliographic coupling network
without the edges between 'only technical' and 'only social' journals AND 
1000 simulated sub-graphs of the whole journal author-bibliographic coupling network
A) NOT controlling for the edge weights of edges between  'only technical' and 'only social' journals
B) controlling for the edge weights of edges between  'only technical' and 'only social' journals


ALGORITHM (main steps, there is a bit of extra code)

1. Load disciplinry classified journal author-bibliographic coupling edges data, 
produced with journals_coauthor_coupling_v2.py

2. simulate sub-graphs with and without controlling for weight

3. calculate the modularity of simulated graphs, and graph without soc-technical edges

3. plot and save plots

'''


#%% def round and grpup edges for simulation with edge weight

def round_group_edges(inter_edges_df, all_edges_df, round_number):
    '''
    round_number: how many decimal points to do we round up edge weights (cosine similarity fr weighted simulation
    '''
    
    import pandas as pd
    
    # inter edges
    # round up edges of the small inter edges graph
    rounded_inter_edges = inter_edges_df.round({'journal_auth_cosine_similarity': round_number})
    #print(rounded_inter.journal_auth_cosine_similarity)
    # group
    grouped_inter_edges = rounded_inter_edges[['journal_auth_cosine_similarity', 'journal_1']].groupby('journal_auth_cosine_similarity').count()
#    print(grouped_inter_edges)
    
    
    # all edges
    # round up and group edges of the large graph
    rounded_all = all_edges_df.round({'journal_auth_cosine_similarity': round_number})
    grouped_all_edges = rounded_all[['journal_auth_cosine_similarity', 'journal_2']].groupby('journal_auth_cosine_similarity').count()
#    print(grouped_all_edges)
    
    
    # compare percentage of inter edges within all edges per weight categories
    compare_weight_groups = pd.concat([grouped_inter_edges, grouped_all_edges], axis=1)
#    print(compare_weight_groups)
    
    compare_weight_groups.rename(columns = {'journal_1' : 'small_inter_graph',
                                            'journal_2' : 'large_graph'}, inplace = True)

    compare_weight_groups['percentage'] = (compare_weight_groups['small_inter_graph'] /  compare_weight_groups['large_graph'] ) * 100

    #print(compare_weight_groups)

    compare_weight_groups_no_na = compare_weight_groups.dropna()

    compare_weight_groups_no_na['journal_auth_cosine_similarity'] = compare_weight_groups_no_na.index

    
    return(compare_weight_groups_no_na)
    
#%%
#%% simulate sub-graphs


def subgraph_simulator_with_edge_weight(geosoc_edges_counter, all_edges_df, round_number):
    '''
    Use: apply tthis funciton to data from different time periods
    Input:
        1. geosoc_edges_counter = df with at least 2 columns:
            i.  weight rounded to 2 decimals of author coupling
            ii. number of edges with the specific weight in the geosoc small graph
            in the given time period
            
        2. all_edges_df = edges of all the papers pertaining to the 
        given time period
        
        DELETED weigthed_detection = True or False. Boolean variable, which determines 
            whether the community detection algorithm 'greedy_modularity_communities'
            is ran with specifying an edge weight variable (True) 
            or without specifying an edge weight variable (False)
            
            # note 27 Aug 2020: this argument got removed, only weighted community detection is performed
            with leidenalgorithm function within python - igraph.
        
        3. round_number = how many decimal points to do we round up edge weights (cosine similarity for weighted simulation)
        
    Output:
        1. all_subgraph_modularities = a list which contains the modularity
        of 101 counterfactual networks, whose node size equals
        number of nodes(all_nodes_df) - number of nodes(geosoc_nodes_df)
    '''
    
    # import packages
    import pandas as pd
    import random 
    import igraph as ig
    
    # reorder edges so that they are indexed in the dataframe in ascending order
    all_edges_df_ord = all_edges_df.sort_values(by = 'journal_auth_cosine_similarity')
    all_edges_df_ord.reset_index(inplace = True)
    
    # round edges df
    all_edges_df_ord_round = all_edges_df_ord.round({'journal_auth_cosine_similarity': round_number})
    all_edges_df_ord_round.sort_values(by = 'journal_auth_cosine_similarity', inplace = True)
    all_edges_df_ord_round.reset_index(inplace = True)

    # create list to save subgraph modularities in
    all_subgraph_modularities = []
    
    # drop these nodes from big network 101 times - create 101 sub-graphs
    # and calculate their modularity scores
    
    sim_ranges = {}
    
    for w in list(set(list(geosoc_edges_counter.journal_auth_cosine_similarity))):
    
        df = all_edges_df_ord_round.loc[all_edges_df_ord_round.journal_auth_cosine_similarity == w]
        idx = df.index
        # get ranges of indices in the large edges dataframe for each journal_auth_cosine_similarity
        i_min = idx.min()
        i_max = idx.max()
        print(i_min)
        print(i_max)
        
        
        # get number of edges to delete in simulated networks for each for each journal_auth_cosine_similarity
        n_edges_to_del = geosoc_edges_counter.loc[geosoc_edges_counter['journal_auth_cosine_similarity'] == w, 'small_inter_graph'].iloc[0]
        print(n_edges_to_del)
        
        # save the above 2 info in a dictionary
        sim_ranges[w] = [i_min, i_max, int(n_edges_to_del)]
        
        

    
    
    # simulate 100 networks
    for num in list(range(0, 1001)):
        
        # 1. get list of random edges to drop
        list_of_edges_to_drop = []
        
        
        for key, value in sim_ranges.items():
            
#            print(key)
#            print(type(value[2]))
#            print(value[2])
#            print(value[2])
            
            ids_to_del = random.sample(range(value[0], value[1]+1), k = value[2])
            list_of_edges_to_drop.append(ids_to_del)
            
        # flatten the list of edges to drop
        flat_list_of_edges_to_drop = [y for x in list_of_edges_to_drop for y in x] 
        # print(len(flat_list_of_edges_to_drop)) # 2306 a 100 times which is good, same as number of inter edges
        
        
        # 2. create simulated subgraph edges df
        
        sim_subgraph_edges = all_edges_df_ord.drop(all_edges_df_ord.index[flat_list_of_edges_to_drop])
        # print(sim_subgraph_edges.shape) # (28936, 35) 100 times which is good because 28936 + 2306 = 31242
        
        # create new df with just the edges I need
        sim_subgraph_edges_2 = sim_subgraph_edges[['journal_1', 'journal_2', 'journal_auth_cosine_similarity']]
        sim_subgraph_edges_2.columns = ['node_1', 'node_2', 'weight']
        
        # 3. create subgraphs objects
        
        SG = ig.Graph.TupleList(sim_subgraph_edges_2.values, 
                                weights=True, directed=False)
        
        communities = SG.community_leiden(objective_function= "modularity", weights = 'weight')
        
        #print(communities)
        
        # calculate modularity of the subgraph
        subgraph_modularity = communities.modularity
        all_subgraph_modularities.append(subgraph_modularity)
        print('mod calculated for network ' + str(num))
        
    return(all_subgraph_modularities)
            
#%% 
#%% simulate sub-graphs


def subgraph_simulator_no_edge_weight(all_edges_df, number_of_inter_edges):
    '''
    Use: apply tthis funciton to data from different time periods
    TODO; automate k in radnom num simulator
    Input:
            
        1. all_edges_df = edges of all the papers pertaining to the 
        given time period
        
        2. number of interdisciplinary edges
        
        3. weigthed_detection = True or False. Boolean variable, which determines 
            whether the community detection algorithm 'greedy_modularity_communities'
            is ran with specifying an edge weight variable (True) 
            or without specifying an edge weight variable (False)
            
            # note 27 Aug 2020: this argument got removed, only weighted community detection is performed
            with leidenalgorithm function within python - igraph.
        
    Output:
        1. all_subgraph_modularities = a list which contains the modularity
        of 101 counterfactual networks, whose node size equals
        number of nodes(all_nodes_df) - number of nodes(geosoc_nodes_df)
    '''
    
    # import packages
    import pandas as pd
    import random
    import igraph as ig
    
    # reorder edges so that they are indexed in the dataframe in ascending order
    all_edges_df_ord = all_edges_df.sort_values(by = 'journal_auth_cosine_similarity')
    all_edges_df_ord.reset_index(inplace = True)
    
    idx = all_edges_df_ord.index
    min_idx = min(idx)
    max_idx = max(idx)

    # create list to save subgraph modularities in
    all_subgraph_modularities = []
    
    for num in list(range(0, 1001)):

        # 1. get list of random edges to drop
        list_of_edges_to_drop = random.sample(range(min_idx, max_idx+1), k = number_of_inter_edges)
    
        # 2. create simulated subgraph edges df
        
        sim_subgraph_edges = all_edges_df_ord.drop(all_edges_df_ord.index[list_of_edges_to_drop])
        # print(sim_subgraph_edges.shape) # (28936, 35) 100 times which is good because 28936 + 2306 = 31242
        
        # create mew df with just the edges I need
        sim_subgraph_edges_2 = sim_subgraph_edges[['journal_1', 'journal_2', 'journal_auth_cosine_similarity']]
        sim_subgraph_edges_2.columns = ['node_1', 'node_2', 'weight']
        
        # 3. create subgraphs objects
        
        SG = ig.Graph.TupleList(sim_subgraph_edges_2.values, 
                                weights=True, directed=False)
        
        # detect communities
        communities = SG.community_leiden(objective_function= "modularity", weights = 'weight')
        
        #print(communities)
        
        # calculate modularity of the subgraph
        subgraph_modularity = communities.modularity
        all_subgraph_modularities.append(subgraph_modularity)
        print('mod calculated for network ' + str(num))
        
    return(all_subgraph_modularities)
#%%  
#%% get non sim modularity

def get_mod_non_sim(journals_coupling_SC_2):
    
    '''
    Arguments: 
        
        1. journals_coupling_SC_2 is the df with classified ALL edges
        
        2. weigthed_detection = True or False. Boolean variable, which determines 
            whether the community detection algorithm 'greedy_modularity_communities'
            is ran with specifying an edge weight variable (True) 
            or without specifying an edge weight variable (False)
            
            # note 27 Aug 2020: this argument got removed, only weighted community detection is performed
            with leidenalgorithm function within python - igraph.
        
        
    '''
    
    import igraph as ig
    
    inter_edges_1_ind = journals_coupling_SC_2.loc[(journals_coupling_SC_2['only_social_j1'] == 1) & (journals_coupling_SC_2['only_computational_j2'] == 1)].index
    inter_edges_2_ind = journals_coupling_SC_2.loc[(journals_coupling_SC_2['only_computational_j1'] == 1) & (journals_coupling_SC_2['only_social_j2'] == 1)].index


    sub_journals_coupling_SC_2 = journals_coupling_SC_2.drop(inter_edges_1_ind)
    sub_2_journals_coupling_SC_2 = sub_journals_coupling_SC_2.drop(inter_edges_2_ind)
 
#    print(sub_2_journals_coupling_SC_2.shape) # (28936, 34) / (35944, 11) which is good
    
    
    sub_2_journals_coupling_SC_2_2 = sub_2_journals_coupling_SC_2[['journal_1', 'journal_2', 'journal_auth_cosine_similarity']]
    sub_2_journals_coupling_SC_2_2.columns = ['node_1', 'node_2', 'weight']
        
    # 3. create subgraphs objects   
    SG_o = ig.Graph.TupleList(sub_2_journals_coupling_SC_2_2.values, 
                              weights=True, directed=False)
        
    # detect communitoes on SG_o
    
    communities = SG_o.community_leiden(objective_function= "modularity", weights = 'weight')
        
    # calculate modularity of the subgraph
    subgraph_o_modularity = communities.modularity
#    print(subgraph_o_modularity) # 0.03480828304315487
    
    return(subgraph_o_modularity)

#%% 
#%% plot function

def confint_and_plot_sim_modularities(simulated_modularities_list, 
                                      nonsim_mod,
                                      color_graph, 
                                      color_95_lines,
                                      weighted, 
                                      year, 
                                      catf,
                                      weigthed_detection,
                                      round_number):
    
    '''
    ARGUMENTS
    
        simulated_modularities_list: list of simulated modularities
    
        color_graph: color of the graph (e.g. green or blue)
    
        color_95_lines: color oft he 95% lines (so that it's different from 'color_graph')
    
        weighted: string which can take value 'with' OR 'no' to signal 
                  if the simualtion takes weights into account or not
              
                year: year
    
        cos_sim_for_filename: cos sim used for journal bibliographic coupling
    
        catf: categorisation function used for datavis
        
        weigthed_detection = True or False. changes the directory that output is saved to .
            Boolean variable, which determines 
            whether the community detection algorithm 'greedy_modularity_communities'
            is ran with specifying an edge weight variable (True) 
            or without specifying an edge weight variable (False)
            
            # note 27 Aug 2020: this got changed, only weighted community detection is performed
            with leidenalgorithm function within python - igraph.
        
        round_number = changes directory to save to, number of decimals edge weight is rounded to
    
    OUTPUT:
    
        datavis
    
    
    
    '''
    
    #  import packages
    from matplotlib import pyplot as plt
    import statistics
    import os
    
    # create directory to save datavis in
    
    if weigthed_detection == False:
        directory = 'P:/thesis/thesis_final_visualisations/NEESnorm_simulated_journal_authorbibcouple/temporal/{}_edgedecimal{}/'.format(catf, round_number)

    elif weigthed_detection == True:
        directory = 'P:/thesis/thesis_final_visualisations/NEESnorm_weighted_comm_simulated_journal_authorbibcouple/temporal/{}_edgedecimal{}/'.format(catf, round_number)

    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # sort simulated modularities
    simulated_modularities_sorted = sorted(simulated_modularities_list)
    min_mod = min(simulated_modularities_sorted)
    max_mod = max(simulated_modularities_sorted)
    sd_1 = statistics.stdev(simulated_modularities_sorted)
    plot_x_min_lim = min([min_mod - sd_1, nonsim_mod - sd_1])
    plot_x_max_lim = max([max_mod + sd_1, nonsim_mod + sd_1])
    
    # calculate 95% bounds
    confint = simulated_modularities_sorted[25:-25]
    confint_min = min(confint)
    confint_max = max(confint)
    
    # plot
    fig, ax = plt.subplots()
    ax = plt.axes(frameon=False)
    ax.hist(simulated_modularities_sorted, color = color_graph, bins=100, alpha=0.5)
    ax.set_xlim(plot_x_min_lim, plot_x_max_lim)
    
    # plot y axis black line
    plt.axhline(linewidth=2, color = 'black')
    plt.axvline(linewidth=1, x= plot_x_min_lim, color = 'black')

    # conf interval lines
    plt.axvline(linewidth=1, x= confint_min, color = color_95_lines)
    plt.axvline(linewidth=1, x= confint_max, color = color_95_lines)
    
    # modularity without simulation (plot it after the 95% lines to be sure that this is visible if they coincide)
    plt.axvline(linewidth=1, x= nonsim_mod, color = 'red')
    
    # save figure
#    fig.savefig(directory + 'hist_sim_journals_{}_weight_cos{}_{}_{}.png'.format(weighted, cos_sim_for_filename, catf, year), transparent=False, dpi=80, bbox_inches="tight")

    fig.savefig(directory + 'hist_sim_journals_{}_weight_{}_{}.png'.format(weighted, catf, year), transparent=False, dpi=80, bbox_inches="tight")

    # save 95% interval data
    
    intervals_data = [confint_min, confint_max]
    
    return(intervals_data)
     

#%% 