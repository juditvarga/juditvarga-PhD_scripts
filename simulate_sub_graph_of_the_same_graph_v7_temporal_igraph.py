# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 00:05:26 2020

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

#%% 

import os
import re
import pandas as pd

# folders with networks normalised according to cosine similarity based on vectors

#mydir = 'P:/thesis/thesis_final_data/produced_data/journals_bib_coupling/temporal/cos001_catf4/' # DONE
#mydir = 'P:/thesis/thesis_final_data/produced_data/journals_bib_coupling/temporal/cos001_catf5/' # DONE
#mydir = 'P:/thesis/thesis_final_data/produced_data/journals_bib_coupling/temporal/cos001_catf6/' # DONE
#mydir = 'P:/thesis/thesis_final_data/produced_data/journals_bib_coupling/temporal/cos001_catf7/' # DONE

# folders with networks normalised according to waltmann et al.

#mydir = 'P:/thesis/thesis_final_data/produced_data/NEESnorm_journals_bib_coupling/temporal/catf4/' # DONE
mydir = 'P:/thesis/thesis_final_data/produced_data/NEESnorm_journals_bib_coupling/temporal/catf5/' # todo for round decimal 1, done for round decimal 2
#mydir = 'P:/thesis/thesis_final_data/produced_data/NEESnorm_journals_bib_coupling/temporal/catf6/' # todo
#mydir = 'P:/thesis/thesis_final_data/produced_data/NEESnorm_journals_bib_coupling/temporal/catf7/' # DONE

years_list = list(range(2010, 2020))
inter_edges_dfs_dict = {}
edges_dfs_dict = {}

file_list = []
#print(file_list)


for file in os.listdir(mydir):
    
#    print(file)
    file_list.append(file)
    
    
for file in file_list:
    
    # laod inter edges
    if file.startswith('inter'):
    
        # get variables for file names
        year = file.split('.')[0].split('_')[-1]
        print(year)
        catf = file.split('.')[0].split('_')[-2]
        print(catf)
    
        # read inter edges as csv
        regex_string = 'interedges.*{}'.format(year)
        inter_edges_file = [x for x in file_list if re.findall(regex_string, x)][0]
#        print(inter_edges_file)
        
        inter_soc_tech_graph_edges = pd.read_csv(mydir + inter_edges_file)
#        print(inter_soc_tech_graph_edges.shape)
        #get number of inter_edges
        number_of_inter_edges = inter_soc_tech_graph_edges.shape[0]
        
        # save inter edges df and number of inter edges into yearly dictionary
        inter_edges_dfs_dict[year] = [inter_soc_tech_graph_edges, number_of_inter_edges, catf]
        
     # laod all edges   
    elif file.startswith('edges'):
        
        year = file.split('.')[0].split('_')[-1]
#        print(year)
#        cos_sim_for_filename = file.split('.')[0].split('_')[-3]
#        print(cos_sim_for_filename)
        catf = file.split('.')[0].split('_')[-2]
#        print(catf)
        
        # laod all edges
        regex_string = 'edges.*{}'.format(year)
        edges_file = [x for x in file_list if re.findall(regex_string, x)][0]
#        print(edges_file)
        all_edges = pd.read_csv(mydir + edges_file)
        print(edges_file)
        print(all_edges.shape)
        number_of_all_edges = all_edges.shape[0]
        
        edges_dfs_dict[year] = [all_edges, number_of_all_edges, catf]


# merge edges dfs
all_edges_dict = {}

for key, value in inter_edges_dfs_dict.items():
    for key2, value2 in edges_dfs_dict.items():
        
        if key == key2:
            
            all_edges_dict[key] = value + value2

# check
for key, value in all_edges_dict.items():
#    print(len(value)) # 6
#    print(type(value[0])) # <class 'pandas.core.frame.DataFrame'>, inter_edges_df
#    print(type(value[1])) # <class 'int'>, number_of_inter_edges
#    print(value[1]) 
#    print(type(value[2])) # <class 'str'> catf inter_edges
#    print(value[2])
#    print(type(value[3])) # <class 'pandas.core.frame.DataFrame'>, all_edges_df
#    print(type(value[4])) # <class 'int'>,  number_of_all_edges
#    print(value[4])
#    print(type(value[5])) # <class 'str'> catf all_edges

# check that only 1 type of cattf is in the folder    
    if value[2] != value[5]:
        raise(ValueError)
#        

            
#%% CONTINUE FROM HERE
#%%

# TODO: MANUAL CHOICE REQUIRED
# choice community detectin=on algorithm
        # if True : community detection algorithm is passed a weight variable,
        # if False: community detection algorithm is NOT passed a weight variable.
 
'''choose  how many decimal points to do we round up edge weights (cosine similarity fr weighted simulation) '''
       
round_number = 2 # how many decimal points to do we round up edge weights (cosine similarity fr weighted simulation)
#round_number = 1        
weigthed_detection_choice = True
#weigthed_detection_choice = False

# load and run scripts


import pandas as pd

import os
os.chdir('P:/thesis/thesis_final_scripts/2_python_final_data_analysis_scripts/')

from simulate_sub_graphs_functions_igraph_v7 import round_group_edges
from simulate_sub_graphs_functions_igraph_v7 import subgraph_simulator_with_edge_weight
from simulate_sub_graphs_functions_igraph_v7 import subgraph_simulator_no_edge_weight
from simulate_sub_graphs_functions_igraph_v7 import get_mod_non_sim
from simulate_sub_graphs_functions_igraph_v7 import confint_and_plot_sim_modularities

# create dictionary to save data in
all_temp_sim_dat = {}

# for each year, create simulated graphs, create plots and get data
for key, value in all_edges_dict.items():
    
    # get dfs for simulation functions
    compare_weight_groups_no_na = round_group_edges(value[0], value[3], round_number)
    #print(compare_weight_groups_no_na[['percentage']])
    all_edges_classified = value[3]
    
    # get number of inter edges and all edges
    number_of_inter_edges = value[1]
    number_of_all_edges = value[4]
    
    # get catf data
    catf_name = value[2]
    
    # get modularity of network with inter edges deleted (NOT SIMULATED)
    mod_non_sim = get_mod_non_sim(all_edges_classified)
    
    # simulate graphs
    sim_mods_with_weight = subgraph_simulator_with_edge_weight(compare_weight_groups_no_na, 
                                                               all_edges_classified,
                                                               round_number)
    
    sim_mods_no_weight = subgraph_simulator_no_edge_weight(all_edges_classified, 
                                                           number_of_inter_edges)
    
    # calculate mod and 95% interval infos
    confint_no_weight = confint_and_plot_sim_modularities(simulated_modularities_list = sim_mods_no_weight,
                                                          nonsim_mod = mod_non_sim,
                                                          color_graph = 'green',
                                                          color_95_lines = 'blue',
                                                          weighted = 'no',
                                                          year = str(key),
                                                          catf = catf_name,
                                                          weigthed_detection = weigthed_detection_choice,
                                                          round_number = round_number)
    
    confint_with_weight = confint_and_plot_sim_modularities(simulated_modularities_list = sim_mods_with_weight,
                                                            nonsim_mod = mod_non_sim,
                                                            color_graph = 'blue',
                                                            color_95_lines = 'green',
                                                            weighted = 'with',
                                                            year = str(key),
                                                            catf = catf_name,
                                                            weigthed_detection = weigthed_detection_choice,
                                                            round_number = round_number)
    
    
    # save data
    
#    alldat_df = pd.DataFrame()
#    alldat_df['year'] = key
#    alldat_df['number_of_inter_edges'] = number_of_inter_edges
#    alldat_df['number_of_all_edges'] = number_of_all_edges
#    alldat_df['perc_deleted_edges'] = alldat_df['number_of_inter_edges'] / alldat_df['number_of_all_edges']
#    alldat_df['mod_deleted'] = mod_non_sim
#    alldat_df['mod_95_lower_no_weight'] = confint_no_weight[0]
#    alldat_df['mod_95_upper_no_weight'] = confint_no_weight[1]
#    alldat_df['mod_95_lower_with_weight'] = confint_with_weight[0]
#    alldat_df['mod_95_upper_with_weight'] = confint_with_weight[1]
#    
#    print(alldat_df)
    
    alldat_list = [key, number_of_inter_edges, number_of_all_edges, mod_non_sim, 
                   confint_no_weight[0], confint_no_weight[1], 
                   confint_with_weight[0], confint_with_weight[1]]

    
    # save all data in dictionary
    # convert list into dataframe
    # https://stackoverflow.com/questions/42202872/how-to-convert-list-to-row-dataframe-with-pandas
    all_temp_sim_dat[key] = pd.DataFrame([alldat_list])
    
#%% create long and wide df to plot

# create data
import pandas as pd

#cos_sim_for_filename = all_edges_dict['2010'][2]
catf = all_edges_dict['2010'][2]

alldat_df_list = []

for key, value in all_temp_sim_dat.items():
#    print(key)
#    print(value.shape)
#    print(value)
    
    alldat_df_list.append(value)
#
# create wide df
alldat_wide_df = pd.concat(alldat_df_list)
#print(alldat_wide_df.columns)
#print(alldat_wide_df.shape)
#print(alldat_wide_df.head(5))

alldat_wide_df.rename(columns = {0: 'year',
                                 1: 'number_of_inter_edges',
                                 2: 'number_of_all_edges',
                                 3: 'mod_non_sim',
                                 4: 'min_confint_no_weight',
                                 5: 'max_confint_no_weight',
                                 6: 'min_confint_with_weight',
                                 7: 'max_confint_with_weight'}, inplace = True)
    
print(alldat_wide_df.columns)
print(alldat_wide_df.shape)
print(alldat_wide_df.head(5))

# create percentage of deleted edges

alldat_wide_df['perc_deleted'] = alldat_wide_df['number_of_inter_edges'] / alldat_wide_df['number_of_all_edges']


# SELECT WHICH FOLDER TO SAVE DTA VIS DEPENDING ON THE COMMUNITY DETECTION
# ALGORITHM CHOSEN

if weigthed_detection_choice == False:
    # directory for data vis with community detection algorithm which DOES NOT take edge weight into account
#    dir2 = 'P:/thesis/thesis_final_data/produced_data/journals_bib_coupling/temporal/alldat_{}_{}_edgedecimal{}/'.format(cos_sim_for_filename, catf, round_number)
    dir2 = 'P:/thesis/thesis_final_data/produced_data/NEESnorm_journals_bib_coupling/temporal/alldat_{}_edgedecimal{}/'.format(catf, round_number)

elif weigthed_detection_choice == True:
    # directory for data vis with community detection algorithm which DOES take edge weight into account
#    dir2 = 'P:/thesis/thesis_final_data/produced_data/journals_bib_coupling/temporal/weighted_comm_detection_alldat_{}_{}_edgedecimal{}/'.format(cos_sim_for_filename, catf, round_number)
    dir2 = 'P:/thesis/thesis_final_data/produced_data/NEESnorm_journals_bib_coupling/temporal/weighted_comm_detection_alldat_{}_edgedecimal{}/'.format(catf, round_number)


import os
if not os.path.exists(dir2):
    os.makedirs(dir2)

#alldat_wide_df.to_csv(dir2 + 'wide_alldat_mod_{}_{}.csv'.format(cos_sim_for_filename, catf))
alldat_wide_df.to_csv(dir2 + 'wide_alldat_mod_{}.csv'.format(catf))

alldat_wide_df2 = alldat_wide_df.drop(columns = ['number_of_inter_edges', 'number_of_all_edges'])


print(alldat_wide_df2.columns)
# create long df
alldat_long_df = pd.melt(alldat_wide_df2,id_vars=['year'],var_name='metrics', value_name='values')
print(alldat_long_df.head(15))
print(alldat_long_df.columns)
print(alldat_long_df.shape) # (60, 3)

# save long df
#alldat_long_df.to_csv(dir2 + 'long_alldat_mod_{}_{}.csv'.format(cos_sim_for_filename, catf))
alldat_long_df.to_csv(dir2 + 'long_alldat_mod_{}.csv'.format(catf))

#%% plot wide df NO WEIGHT

#fmri = sns.load_dataset("fmri")
#
#print(fmri.columns)
#print(fmri.head(5))

import matplotlib.pyplot as plt

# The lines to plot
x = list(alldat_wide_df2['year'])
y1 = list(alldat_wide_df2['mod_non_sim'])
y2 =  list(alldat_wide_df2['max_confint_no_weight'])                          
y3 = list(alldat_wide_df2['min_confint_no_weight'])
y4 = list(alldat_wide_df2['perc_deleted'])

# Plotting of lines
#plt.plot(x, y1,
#         x, y2,
#         x, y3)

''' MANUAL INPUT REQUIRED: CHOOSE WIDTH OF RED LINE '''
line_width = 0.5
#line_width = 1
line_width_for_file = str(line_width).replace('.', '')

# plot
plt.plot(x,y1, lw=line_width, color = 'red')
plt.plot(x,y2,lw=0.5, color = 'green')
plt.plot(x,y3,lw=0.5, color = 'green')
plt.plot(x,y4, '--', lw=1, color = 'black')

# Filling between line y3 and line y4
plt.fill_between(x, y2, y3, color='green', alpha='0.3')

fig = plt.figure()


# save plot to png file - plotting by creating sub plots
#https://stackoverflow.com/questions/34162443/why-do-many-examples-use-fig-ax-plt-subplots-in-matplotlib-pyplot-python
#https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.05-Multi-Line-Plots/

fig, ax = plt.subplots()

ax.plot(x,y1, lw=line_width, color = 'red')
ax.plot(x,y2,lw=0.5, color = 'green')
ax.plot(x,y3,lw=0.5, color = 'green')
ax.plot(x,y4, '--', lw=1, color = 'black')


# Filling between line y3 and line y4
ax.fill_between(x, y2, y3, color='green', alpha='0.3')


#directory = 'P:/thesis/thesis_final_visualisations/weighted_comm_simulated_journal_authorbibcouple/temporal/{}_{}_edgedecimal{}/'.format(cos_sim_for_filename, catf, round_number)
directory = 'P:/thesis/thesis_final_visualisations/NEESnorm_weighted_comm_simulated_journal_authorbibcouple/temporal/{}_edgedecimal{}/'.format(catf, round_number)


# save figure
#fig.savefig(directory + 'alldat_no_weight_mod_{}_{}.png'.format(cos_sim_for_filename, catf))
fig.savefig(directory + 'alldat_no_weight_mod_{}_linewidth{}.png'.format(catf, line_width_for_file))
fig.savefig(directory + 'alldat_no_weight_mod_{}_linewidth{}.pdf'.format(catf, line_width_for_file))


#%% plot wide df WITH  WEIGHT

import matplotlib.pyplot as plt

# The lines to plot
x = list(alldat_wide_df2['year'])
y1 = list(alldat_wide_df2['mod_non_sim'])
y2 =  list(alldat_wide_df2['max_confint_with_weight'])                          
y3 = list(alldat_wide_df2['min_confint_with_weight'])
y4 = list(alldat_wide_df2['perc_deleted'])

# Plotting of lines
#plt.plot(x, y1,
#         x, y2,
#         x, y3)

''' MANUAL INPUT REQUIRED: CHOOSE WIDTH OF RED LINE '''
line_width = 0.5
#line_width = 1
line_width_for_file = str(line_width).replace('.', '')

# plot

plt.plot(x,y1, lw=line_width, color = 'red')
plt.plot(x,y2,lw=0.5, color = 'blue')
plt.plot(x,y3,lw=0.5, color = 'blue')
plt.plot(x,y4, '--', lw=1, color = 'black')

# Filling between line y3 and line y4
plt.fill_between(x, y2, y3, color='blue', alpha='0.3')

fig = plt.figure()


# save plot to png file - plotting by creating sub plots
#https://stackoverflow.com/questions/34162443/why-do-many-examples-use-fig-ax-plt-subplots-in-matplotlib-pyplot-python

fig, ax = plt.subplots()

ax.plot(x,y1, lw=line_width, color = 'red')
ax.plot(x,y2,lw=0.5, color = 'blue')
ax.plot(x,y3,lw=0.5, color = 'blue')
ax.plot(x,y4, '--', lw=1, color = 'black')


# Filling between line y3 and line y4
ax.fill_between(x, y2, y3, color='blue', alpha='0.3')



# TODO: MANUALLY SELECT WHICH FOLDER TO SAVE DTA VIS DEPENDING ON THE COMMUNITY DETECTION
# ALGORITHM CHOSEN

# directory for data vis with community detection algorithm which DOES take edge weight into account
#directory = 'P:/thesis/thesis_final_visualisations/weighted_comm_simulated_journal_authorbibcouple/temporal/{}_{}_edgedecimal{}/'.format(cos_sim_for_filename, catf, round_number)
directory = 'P:/thesis/thesis_final_visualisations/NEESnorm_weighted_comm_simulated_journal_authorbibcouple/temporal/{}_edgedecimal{}/'.format(catf, round_number, line_width_for_file)


# directory for data vis with community detection algorithm which DOES NOT take edge weight into account
#directory = 'P:/thesis/thesis_final_visualisations/simulated_journal_authorbibcouple/temporal/{}_{}/'.format(cos_sim_for_filename, catf)


# save figure

#fig.savefig(directory + 'alldat_with_weight_mod_{}_{}.png'.format(cos_sim_for_filename, catf))
fig.savefig(directory + 'alldat_with_weight_mod_{}_linewidth{}.png'.format(catf, line_width_for_file))
fig.savefig(directory + 'alldat_with_weight_mod_{}_linewidth{}.pdf'.format(catf, line_width_for_file))

#%%