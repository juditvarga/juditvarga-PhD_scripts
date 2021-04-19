# juditvarga-PhD_scripts

This repository contains Python and R scripts I wrote for my PhD thesis.

My PhD thesis, submitted in April 2021 at the School of Sociology of the University of Nottingham (UK) uses scientometrics, interviews and participant observation to explore how scholars from diverse disciplines use geotagged social media data (e.g. geolocated tweets, Instagram posts etc.). This folder contains Python and R scripts I wrote to analyse the scientometric data.

The description are files in this repository are intended to complement the thesis' methods chapter, which describes each method in detail.

I collected scientometric data from Web of Science. My scientometric field delineation matched a total of 2762 papers, broadly related to academic research that uses geotagged social media data between 2008-2019 (for short, geosocial papers).

The project was sponsored by the Horizon Digital Economy Centre for Doctoral Training at the University of Nottingham - Engineering and Physical Sciences Research Council and Ordnance Survey.

Contributors: Judit Varga 

Contact: j.varga@cwts.leidenuniv.nl

Below I briefly outline the methos in my thesis and related scripts.


1.	Co-authorship analysis

Prepare temporal co-authorship network data: (updated 7th of July 2020) 
co_author_network_analysis_v2.py

Calculate and plot modularity of co-authorship network and of simulate graphs: (updated 7th of July 2020) 
coauthorship_modularity_v3.R


2.	Line graphs that depict the proportion of geosocial papers over time with respect to three paper sets.

Description of algorithm and execution: 
journals_timeline_geosocial_ut_count_datavis_v3.py

Functions: 
disciplines_timeline_functions.py


3.	An analysis which compares the modularity of the author-bibliographic coupling network of geosocial papers published in social scientific and technical papers (G1, number of edges = k) which omits network edges between geosocial papers published in social scientific and technical journals (number of 'inter-edges' = m) (SG1, number of edges = k - m = n) to the modularities of 1000 randomly generated networks whose edge count equals the edge count of SG1 ( = n ) but which omit random edges.

3.1. Author-bibliographic coupling normalised with cosine similarity

Temporal data prep (updated 09 June 2020) 
journals_coauthor_coupling_temporal_v2.py

Functions (updated 27 Aug 2020) 
simulate_sub_graphs_functions_igraph.py

3.2. Author-bibliographic coupling normalised using different method

Data prep (updated 14 Nov 2020) 
journals_coauthor_coupling_temporal_v3.py

Functions (updated 14 Nov 2020) 
simulate_sub_graphs_functions_igraph_v7.py

Call Functions for both 2.1 and 2.2. (updated 14 Nov 2020) 
simulate_sub_graph_of_the_same_graph_v7_temporal_igraph.py


4.	Network clustering bar charts & term frequency - inverse document frequency (TF-IDF) analyses

Updated: 02 Dec 2020
Bibliographic coupling netvis & barcharts with WoS subject categories in clusters
paper_author_coupling_v5.py papers_communities_graph_vis_3.R


5.	Heterogeneous network analyses to explore how machine learning and social network analyses are used in geosocial research

5.1 Visualisation using author and author-keyword information using R (Updated: 17 Oct 2020)
Data preparation 
machine_learning_datavis_v3.py

Select author keywords and authors associated with papers with a specific searchterm (e.g. ‘machine learning’ or ‘social network analysis’) in their abstracts or author keywords
Calculate co-occurrence cosine similarity between actants (author keywords and authors) Saves edges = cosine similarity between keywords / authors Saves nodes = numeric id, name of keywords or authors, etc. other data

Data visualisation (R) 
heterogeneous_graph_vis_v2.R

5.2. Visualisation using VOSviewer term map Data preparation (Updated 19 Dec 2020)

machine_learning_datavis_v3.py LINES 0 – 218
paper_author_coupling.py LINES 207 – 229
