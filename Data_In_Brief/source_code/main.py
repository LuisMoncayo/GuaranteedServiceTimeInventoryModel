#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:04:47 2022

@author: luismoncayo
"""
import pandas as pd
pd.set_option('display.max_columns', None)
import networkx as nx
import math
from scipy.stats import norm
import sys
import pyomo.environ as pyo
import gurobipy as gp
from gurobipy import GRB
import time

#list_instances = ['34','35','36','37','38']

list_instances = ['01','02','03','04','05','06','07','08','09','10',
                  '11','12','13','14','15','16','17','18','19','20',
                  '21','22','23','24','25','26','27','28','29','30',
                  '31','32','33','34','35','36','37','38']

for ins in list_instances:
    # -----------------------------------------------------------------------------
    # IMPORT THE DATA -------------------------------------------------------------
    # -----------------------------------------------------------------------------
    file_name = "MSOM-06-038-R2 Data Set in Excel.xls"
    
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
        
    stage_no_predecessor = []
    stage_no_successor = []
    stages_with_succ_pred = []
    for j in list(G.nodes):
        #print(j)
        predecessors = list(G.predecessors(j))
        successors = list(G.successors(j))
        if not predecessors:
            stage_no_predecessor.append(j)
        elif not successors:
            stage_no_successor.append(j)
        else:
            stages_with_succ_pred.append(j)
    
    lst_dep = sorted(nodes_dic['relDepth'].items(), key=lambda x:x[1])
    for i in lst_dep:
        number_node = i[0]
        actual_node = nodes_dic['Stage Name'][number_node]
        #print(actual_node)
        predecessors = list(G.predecessors(actual_node))
        if predecessors:
            for v in predecessors:
                G.nodes[v]["cum_demand"] += G.nodes[actual_node]["cum_demand"]
                variance = G.nodes[v]["cum_std_dev"]**2 + G.nodes[actual_node]["cum_std_dev"]**2
                G.nodes[v]["cum_std_dev"] = math.sqrt(variance)
    
    lst_depths = sorted(nodes_dic['relDepth'].items(), key=lambda x:x[1], reverse=True)
    for i in lst_depths:
        number_node = i[0]
        actual_node = nodes_dic['Stage Name'][number_node]
        succ_nodes = list(G.successors(actual_node))
        if succ_nodes:
            for s in succ_nodes:
                G.nodes[s]["cum_cost"] += G.nodes[actual_node]["cum_cost"]
                
    for i in stage_no_predecessor:
        G.nodes[i]["max_time"] = G.nodes[i]["time"]
    
    lst_st = stages_with_succ_pred+stage_no_successor 
    while len(lst_st) != 0:
        k = lst_st[0]
        prede = list(G.predecessors(k))
        max_times = []
        for p in prede:
            max_times.append(G.nodes[p]["max_time"])
        if min(max_times) != -1:
           G.nodes[k]["max_time"] = G.nodes[k]["time"] + max(max_times)
           lst_st.remove(k)
        else:
            lst_st.append(lst_st.pop(lst_st.index(k)))
    
    # SERVICE LEVEL - ALPHA -------------------------------------------------------
    lst_service_levels = []
    lst_max_ser_time = []
    ser_level = 0
    max_service_time = 0
    for j in stage_no_successor:
        lst_service_levels.append(G.nodes[j]["ser_level"])
        lst_max_ser_time.append(G.nodes[j]["max_time"])
    ser_level = norm.ppf(max(lst_service_levels))
    max_service_time = max(lst_max_ser_time)
    
    holding_cost = 0.2
    # -----------------------------------------------------------------------------
    # for i in list(G.nodes(data=True)):
    #    print(i)
    # -----------------------------------------------------------------------------
    
    # -----------------------------------------------------------------------------
    # GENERATE THE INITIAL SOLUTION -----------------------------------------------
    # -----------------------------------------------------------------------------
    pyomo_init_time = time.time()
    model = pyo.ConcreteModel(name="(GSIM_Pyomo)")
    
    model.Su_Pr = pyo.Set(initialize =  stages_with_succ_pred)
    model.No_Pr = pyo.Set(initialize = stage_no_predecessor)
    model.No_Suc = pyo.Set(initialize = stage_no_successor)
    
    # define the variables SI and S and bound them.
    def set_bounds_S(model, i):
        return(0.00,G.nodes[i]["max_time"])
    
    def set_bounds_SI(model, i):
        return (0.00 , G.nodes[i]["max_time"]-G.nodes[i]["time"])
    
    model.S = pyo.Var((model.Su_Pr | model.No_Pr) | model.No_Suc, bounds=set_bounds_S, domain=pyo.PositiveReals)
    model.SI = pyo.Var(model.Su_Pr | model.No_Suc, bounds=set_bounds_SI, domain=pyo.PositiveReals)
    model.aux = pyo.Var((model.Su_Pr | model.No_Pr) | model.No_Suc, bounds=(0.01,max_service_time), domain=pyo.PositiveReals)
    
    
    # define the objective function 
    def obj_function(model,i):
        return holding_cost*ser_level*sum(G.nodes[i]["cum_cost"]*G.nodes[i]["cum_std_dev"]*pyo.sqrt(model.aux[i])  for i in (model.Su_Pr | model.No_Pr) | model.No_Suc)
    model.obj_fun = pyo.Objective(rule=obj_function, sense=pyo.minimize)
    
    # constraint SI + t - S >= 0 for all nodes
    def no_negative_time(model, i):
        if i in model.No_Pr:
            return(G.nodes[i]["time"] - model.S[i] >= 0)
        else:
            return (model.SI[i] + G.nodes[i]["time"] - model.S[i] >= 0)
    model.no_neg_time = pyo.Constraint((model.Su_Pr | model.No_Pr) | model.No_Suc, rule=no_negative_time)  
    
    # S_i <= SI_j for all (i,j) 
    def relationship_out_in(mdl, i, j):
        return (model.SI[j]- model.S[i] >= 0)
    model.rel_in_out = pyo.Constraint(list(G.edges), rule=relationship_out_in)
    
    # S_i = service_time for all i in D
    def service_time_no_succ_stage(mdl, j):
        return (model.S[j] <= G.nodes[j]["ser_time"])
    model.ser_times = pyo.Constraint(model.No_Suc, rule=service_time_no_succ_stage)
    
    # auxiliar constraint
    def aux_constraint(model, i):
        if i in model.No_Pr:
            return(G.nodes[i]["time"] - model.S[i] == model.aux[i])
        else:
            return (model.SI[i] + G.nodes[i]["time"] - model.S[i] == model.aux[i])
    model.aux_const = pyo.Constraint((model.Su_Pr | model.No_Pr) | model.No_Suc, rule=aux_constraint) 
    
    
    #model.pprint()
    
    solver  = pyo.SolverFactory('ipopt')
    status = solver.solve(model, tee=False)
    #solver.options['max_iter'] = 33
    status = solver.solve(model,tee=False,logfile='init_sol_pyomo/'+instace+'.log')
    
    pyomo_fin_time = time.time()
    
    # --- Store the values of variables in the network ----------------------------
    for i in list(G.nodes):
        if i in stage_no_predecessor:
            G.nodes[i]["SI"] = 0.00
            G.nodes[i]["S"] = round(pyo.value(model.S[i]),2)
            #G.nodes[i]["aux_val"]=G.nodes[i]["time"]-pyo.value(model.S[i])
        else:
            G.nodes[i]["SI"] = round(pyo.value(model.SI[i]),2)
            G.nodes[i]["S"] = round(pyo.value(model.S[i]),2)
            #G.nodes[i]["aux_val"]=G.nodes[i]["time"]-pyo.value(model.S[i])
    # -----------------------------------------------------------------------------
    orig_stdout = sys.stdout
    sys.stdout = open('init_sol_pyomo/pyomo_instance_'+instace+'.csv','wt')
    
    # test solution to optimality +++++++++++++++++++++++++++++++++++++++++++++++++
    print("Optimality test +++++++++++++++++++++++++++++")
    print("The following constraints are not satisfied: ")
    for i in list(G.nodes):
        if i in stage_no_predecessor:
            if G.nodes[i]["time"] - G.nodes[i]["S"] < 0:
                print(i,", The constraint is not satisfied.")
        else:
            if G.nodes[i]["SI"]+G.nodes[i]["time"]-G.nodes[i]["S"] < 0:
                print(i," The constraint is not satisfied.")
            
    
    for i in list(G.edges):
        from_node = i[0]
        to_node = i[1]
        if G.nodes[to_node]["SI"]-G.nodes[from_node]["S"]<0:
            print(i,", The constraint is not satisfied.")
    print("+++++++++++++++++++++++++++")
    print("Time to run:, %s ,seconds" % (pyomo_fin_time - pyomo_init_time))
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    print("------")
    print("The SC has,", G.number_of_nodes(),", nodes and, ",G.number_of_edges(),"edges.")
    print("------")
    print("The value of the objective using Pyomo is, %5.2f " % pyo.value(model.obj_fun) )
    print("stage, SI, time, S" )
    for i in list(G.nodes):
        if i in stage_no_predecessor:
            print(i,',',0.00,',',G.nodes[i]["time"],',',G.nodes[i]["S"])
        else:
            print(i,',',G.nodes[i]["SI"],',',G.nodes[i]["time"],',',G.nodes[i]["S"])
    
    sys.stdout.close()
    sys.stdout=orig_stdout
    
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # FINDING THE OPTIMUM SOLUTION ------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    gurobi_init_time = time.time()
    m = gp.Model("GSTInvModel")
    def cb(model, where):
        if where == GRB.Callback.MIPNODE:
            # Get model objective
            obj = model.cbGet(GRB.Callback.MIPNODE_OBJBST)
    
            # Has objective changed?
            if abs(obj - model._cur_obj) > 1e-2:
                # If so, update incumbent and time
                model._cur_obj = obj
                model._time = time.time()
    
        # Terminate if objective has not improved in 20s
        if time.time() - model._time > 60*10:
            model.terminate()
    #---------------------------- Terminate the model -----------------------------
    # auxiliar variables
    aux = m.addVars(list(G.nodes),lb=0,vtype=GRB.CONTINUOUS , name="a")
    aux1 = m.addVars(list(G.nodes),lb=0,vtype=GRB.CONTINUOUS , name="a1")
    #---------
    
    out_var = m.addVars(list(G.nodes),lb=0,vtype=GRB.INTEGER , name="y")
    for i in list(G.nodes):
        out_var[i].ub = G.nodes[i]["max_time"]
        aux[i].ub = G.nodes[i]["max_time"]
        #aux1[i].ub = G.nodes[i]["max_time"]
    
    in_var = m.addVars(stage_no_successor+stages_with_succ_pred, vtype=GRB.INTEGER, name="x")
    for i in (stage_no_successor+stages_with_succ_pred):
        in_var[i].ub = G.nodes[i]["max_time"]-G.nodes[i]["time"]
        aux[i].ub = G.nodes[i]["max_time"]-G.nodes[i]["time"]
        #aux1[i].ub = G.nodes[i]["max_time"]-G.nodes[i]["time"]
        
    #
    # Set initial values to variables 
    #
    '''
    for i in list(G.nodes):
        if i in stage_no_predecessor:
            out_var[i].Start = round(G.nodes[i]["S"],2)
            aux[i].Start = round(G.nodes[i]["time"]-G.nodes[i]["S"],2)
        else:
            in_var[i].Start  = round(G.nodes[i]["SI"],2)
            out_var[i].Start  = round(G.nodes[i]["S"],2)
            aux[i].Start = round(G.nodes[i]["SI"]+G.nodes[i]["time"]-G.nodes[i]["S"],2)
    '''       
    for i in list(G.nodes):
        if i in stage_no_predecessor:
            #out_var[i].VarHintVal = round(G.nodes[i]["S"],2)
            out_var[i].Start = round(G.nodes[i]["S"],2)
            aux[i].VarHintVal = round(G.nodes[i]["time"]-G.nodes[i]["S"],2)
            
        else:
            in_var[i].Start = round(G.nodes[i]["SI"],2)
            out_var[i].Start = round(G.nodes[i]["S"],2)
            aux[i].VarHintVal = round(G.nodes[i]["SI"]+G.nodes[i]["time"]-G.nodes[i]["S"],2)
    
    '''
    m.update()
    for j in list(G.nodes):
        if j in stage_no_predecessor:
            left = G.nodes[j]["time"]-out_var[j].Start
            if round(left,2)==aux[j].VarHintVal:
                print(j,"TRUE")
            else:
                print(j,"FALSE")
            print(j,0,G.nodes[j]["time"],out_var[j].Start,aux[j].Start)
        else:
            left = in_var[j].Start+G.nodes[j]["time"]-out_var[j].Start
            if round(left,2)==aux[j].VarHintVal:
                print(j,"TRUE")
            else:
                print(j,"FALSE")
            print(j,in_var[j].Start,G.nodes[j]["time"],out_var[j].Start,aux[j].Start)
    '''
    
    # Set the objective funcion
    m.setObjective( sum(ser_level*holding_cost*G.nodes[j]["cum_cost"]*G.nodes[j]["cum_std_dev"]*aux1[j] for j in  list(G.nodes)), GRB.MINIMIZE )
    
    #--- AUXLIAR ---------------------
    for stage in stage_no_predecessor:
        m.addConstr(-out_var[stage]-aux[stage],GRB.EQUAL,-G.nodes[stage]["time"], name='a1'+stage)
        m.addGenConstrPow(aux[stage], aux1[stage], 0.5, name='cf_'+stage)#, options="FuncPieces=200000"
        
    for stage in stage_no_successor+stages_with_succ_pred:
        m.addConstr(in_var[stage]-out_var[stage]-aux[stage],GRB.EQUAL,-G.nodes[stage]["time"], name='a1'+stage)
        m.addGenConstrPow(aux[stage], aux1[stage], 0.5, name='cf_'+stage)
    #--------------------------------
    
    for stage in stage_no_predecessor:
        m.addConstr(G.nodes[stage]["time"] - out_var[stage], GRB.GREATER_EQUAL, 0, name=stage)
    
    for stage in stage_no_successor+stages_with_succ_pred:
        m.addConstr(in_var[stage] + G.nodes[stage]["time"] - out_var[stage], GRB.GREATER_EQUAL, 0, name=stage)
        
    for edge in G.edges:
        from_stage = edge[0]
        to_stage = edge[1]
        m.addConstr(out_var[from_stage], GRB.LESS_EQUAL, in_var[to_stage], name=from_stage+to_stage)
    
    for stage in stage_no_successor:
        m.addConstr(out_var[stage], GRB.LESS_EQUAL, G.nodes[stage]["ser_time"],name=stage+'_demand')
    
    #m.write("myLP.lp")
    
    second_stdout = sys.stdout
    sys.stdout = open('sol_gurobi/gurobi_instance_'+instace+'.csv','wt')
    
    
    m._cur_obj = float('inf')
    m._time = time.time()
    m.update()
    m.optimize(callback=cb)
    
    gurobi_fin_time = time.time()
    
    print(" ----------------------------------------")
    print("Time to run:, %s ,seconds" % (gurobi_fin_time - gurobi_init_time))
    print("The value of the objective using Gurobi is, %5.2f " % m.getObjective().getValue() )
    for i in list(G.nodes):
        if i in stage_no_predecessor:
            print(i , ',', 0,',',G.nodes[i]["time"],",",out_var[i].X)
        else:
            print(i ,',',in_var[i].X,',',G.nodes[i]["time"],",",out_var[i].X)
    sys.stdout.close()
    sys.stdout=second_stdout


















