#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 20:08:40 2023

@author: luismoncayo
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:04:47 2022

@author: luismoncayo
"""
#http://www.sthda.com/english/articles/33-social-network-analysis/135-network-visualization-essentials-in-r/

import pandas as pd
pd.set_option('display.max_columns', None)
import networkx as nx
import sys

list_instances = ['01','02','03','04','05','06','07','08','09','10',
                  '11','12','13','14','15','16','17','18','19','20',
                  '21','22','23','24','25','26','27','28','29','30',
                  '31','32','33','34','35','36','37','38']

for ins in list_instances:
# -----------------------------------------------------------------------------
# IMPORT THE DATA -------------------------------------------------------------
# -----------------------------------------------------------------------------
    file_name = "MSOM-06-038-R2 Data Set in Excel.xls"  
    #file_name = "instances.xlsx"
    
    instace = ins #two digit format 01,02,...,09,10,11,..., 15,16,...,36,37,38. 
    nodes_info = instace+"_SD"
    edges_info = instace+"_LL"
    
    nodes_data = pd.read_excel (r'/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/'+file_name, sheet_name=nodes_info,dtype=object)
    nodes_data = nodes_data.fillna(0)
    nodes_dic = nodes_data.to_dict()
    edges_data = pd.read_excel (r'/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/'+file_name, sheet_name=edges_info)
    edges_data.rename(columns = {'sourceStage' : 'source', 'destinationStage' : 'target'}, inplace = True)
    
    G = nx.from_pandas_edgelist(edges_data, create_using=nx.DiGraph() )
    
    # Plot the graph
    #nx.draw_networkx(G)
    
    # -----------------------------------------------------------------------------
    # GENERATE THE SUPPLY CHAIN DATA ----------------------------------------------
    # -----------------------------------------------------------------------------
    for i in range(G.number_of_nodes()):
        vertex = nodes_dic['Stage Name'][i]
        G.nodes[vertex]["time"] = nodes_dic['stageTime'][i]
        G.nodes[vertex]["cost"] = nodes_dic['stageCost'][i]
        G.nodes[vertex]["demand"] = nodes_dic['avgDemand'][i]
        G.nodes[vertex]["ser_time"] = nodes_dic['maxServiceTime'][i]
        G.nodes[vertex]["std_dev"] = nodes_dic['stdDevDemand'][i]
        G.nodes[vertex]["ser_level"] = nodes_dic['serviceLevel'][i]
        G.nodes[vertex]["depth"] = nodes_dic['relDepth'][i]
        G.nodes[vertex]["cum_cost"] = nodes_dic['stageCost'][i]
        G.nodes[vertex]["cum_demand"] = nodes_dic['avgDemand'][i]
        G.nodes[vertex]["max_time"] = -1
        G.nodes[vertex]["cum_std_dev"] = nodes_dic['stdDevDemand'][i]
        G.nodes[vertex]["SI"] = -100
        G.nodes[vertex]["S"] = 100
        G.nodes[vertex]["aux_val"] = 0.00
        
            
    second_stdout = sys.stdout
    sys.stdout = open('Graphs/graph_structure/graph_'+instace+'.csv','wt')
    
    print("Stage",",","Degree",",","In_Edges",",","Out_Edges",",","Depth")
    for i in G.nodes():
        print(i,",",G.degree(i),",",len(G.in_edges(i)),",",len(G.out_edges(i)),",",G.nodes[i]["depth"])
    
    #dframe = pd.DataFrame(columns=['Stage','Degree','In_Edges','Out_Edges','Depth'],index=range(len(list(G))))  
    #for i in range(len(list(G))):
    #    node_name = list(G)[i]
    #    dframe.loc[i].Stage = node_name
    #    dframe.loc[i].Degree = G.degree(node_name)
    #    dframe.loc[i].In_Edges = len(G.in_edges(node_name))
    #    dframe.loc[i].Out_Edges = len(G.out_edges(node_name))
    #    dframe.loc[i].Depth = G.nodes[node_name]["depth"]
        
    sys.stdout.close()
    sys.stdout=second_stdout



