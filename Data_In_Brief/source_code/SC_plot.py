#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:57:47 2024

@author: luismoncayo
"""
import pandas as pd
pd.set_option('display.max_columns', None)
from pyvis.network import Network

file_name = "MSOM-06-038-R2 Data Set in Excel.xls"  

list_instances = ['01','02','03','04','05','06','07','08','09','10',
                  '11','12','13','14','15','16','17','18','19','20',
                  '21','22','23','24','25','26','27','28','29','30',
                  '31','32','33','34','35','36','37']#,'38']

for ins in list_instances:
    instace = ins #two digit format 01,02,...,09,10,11,..., 15,16,...,36,37,38. 
    nodes_info = instace+"_SD"
    edges_info = instace+"_LL"
        
    nodes_data = pd.read_excel(r'/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/'+file_name,sheet_name=nodes_info,dtype=object)
    nodes_data = nodes_data.fillna(0)
    nodes_dic = nodes_data.to_dict()
    edges_data = pd.read_excel (r'/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/'+file_name,sheet_name=edges_info)
    edges_data.rename(columns = {'sourceStage' : 'source', 'destinationStage' : 'target'}, inplace = True)


    nt = Network('1500px', '1500px', notebook=True, cdn_resources="remote", directed =True)
    nt.repulsion()
    # populates the nodes and edges data structures
    for node in nodes_data["Stage Name"]:
        if 'Dist' in node:
            nt.add_node(node, color='#ef476f', size=20)
        elif 'Manuf' in node:
            nt.add_node(node, color='#ffd166',size=20)
        elif 'Part' in node:
            nt.add_node(node, color='#06d6a0',size=20)
        elif 'Retail' in node:
            nt.add_node(node, color='#118ab2',size=20)
        else:
            nt.add_node(node, color='#073b4c',size=20)#Trans

    list_edges = zip(edges_data['source'],edges_data['target'])
    nt.add_edges(list_edges)
    nt.toggle_physics(True)
    nt.save_graph('html_SC_structure/instance'+instace+".html")
    
    nt = Network('1500px', '1500px', notebook=True, cdn_resources="remote", directed =True)
    #nt.repulsion()
    # populates the nodes and edges data structures
    for i in range(len(nodes_data.index)):
        if 'Dist' in nodes_data.iloc[i,0]:
            nt.add_node(nodes_data.iloc[i,0],color='#ef476f',size=20,x=int(nodes_data.iloc[i,22]),y=int(nodes_data.iloc[i,23]))
        elif 'Manuf' in nodes_data.iloc[i,0]:
            nt.add_node(nodes_data.iloc[i,0],color='#ffd166',size=20,x=int(nodes_data.iloc[i,22]),y=int(nodes_data.iloc[i,23]))
        elif 'Part' in nodes_data.iloc[i,0]:
            nt.add_node(nodes_data.iloc[i,0],color='#06d6a0',size=20,x=int(nodes_data.iloc[i,22]),y=int(nodes_data.iloc[i,23]))
        elif 'Retail' in nodes_data.iloc[i,0]:
            nt.add_node(nodes_data.iloc[i,0],color='#118ab2',size=20,x=int(nodes_data.iloc[i,22]),y=int(nodes_data.iloc[i,23]))
        else:
            nt.add_node(nodes_data.iloc[i,0],color='#073b4c',size=20,x=int(nodes_data.iloc[i,22]),y=int(nodes_data.iloc[i,23]))#Trans
    
    list_edges = zip(edges_data['source'],edges_data['target'])
    nt.add_edges(list_edges)
    nt.toggle_physics(False)
    nt.save_graph('html_SC_structure/depth'+instace+".html")
    
    
    