library("writexl")

# my_data <- read.csv("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/init_sol_pyomo/pyomo_instance_22.csv", header = FALSE)
# nod <- my_data[grepl("The SC has", my_data$V1),]
# number_nodes <- as.numeric(nod$V2)
# ed <- my_data[grepl("edges", my_data$V1),]
# number_edges <- as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", ed$V1))


folders <- c("hint_start_1min","hint_start_4min", "hint_start_10min","hint_start_35min")
for(j in 1:length(folders)){
  table_obj = data.frame()
  to_folder = paste("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/",folders[j],sep = "")
  instances <- sprintf("%02d",seq("01","38",1))
  for(i in seq(1,38)){
    ins = instances[i]
    file_path_G <- paste(to_folder,paste(paste("/sol_gurobi/gurobi_instance_",ins,sep=""),".csv",sep=""),sep="")
    file_path_P <- paste(to_folder,paste(paste("/init_sol_pyomo/pyomo_instance_",ins,sep=""),".csv",sep=""),sep="")
    my_data <- read.csv(file_path_G, header = FALSE)
    violates_text <- my_data[grepl("violates", my_data$V1),]
    pyo_sol <- read.csv(file_path_P, header = FALSE)
    pyo_text_obj <- pyo_sol[grepl("using Pyomo is", pyo_sol$V1),]
    #pyo_objective <- format(round(as.numeric(pyo_text_obj$V2), 1), nsmall=2, big.mark=",")
    pyo_objective <- as.numeric(pyo_text_obj$V2)
    pyo_text_time <- pyo_sol[grepl("Time to run", pyo_sol$V1),]
    #pyo_time <- format(round(as.numeric(pyo_text_time$V2), 1), nsmall=2, big.mark=",")
    pyo_time <- as.numeric(pyo_text_time$V2)
    nod <- pyo_sol[grepl("The SC has", pyo_sol$V1),]
    number_nodes <- as.numeric(nod$V2)
    ed <- pyo_sol[grepl("edges", pyo_sol$V1),]
    number_edges <- as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", ed$V1))
    if( nrow(violates_text) == 0){
      init_sol <- "T"
    }else{
      init_sol <- "F"
    }
    gurobi_text <- my_data[grepl("Best objective", my_data$V1),]
    best_obj <- as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", gurobi_text$V1))
    #best_obj <- format(round(as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", gurobi_text$V1)), 2), nsmall=1, big.mark=",")
    best_bound <- as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", gurobi_text$V2))
    #best_bound <- format(round(as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", gurobi_text$V2)), 2), nsmall=1, big.mark=",")
    gap <- as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", gurobi_text$V3))
    #gap <- format(round(as.numeric(sub("^.*?(?:([-+]?\\d*\\.?\\d+(?:[eE][-+]?\\d+)?).*|$)","\\1", gurobi_text$V3)), 2), nsmall=1, big.mark=",")
    
    gurobi_text_time <- my_data[grepl("Time to run", my_data$V1),]
    gurobi_time <- as.numeric(gurobi_text_time$V2)
    #gurobi_time <- format(round(as.numeric(gurobi_text_time$V2), 2), nsmall=1, big.mark=",")
    output <- c(i,number_nodes,number_edges,pyo_objective,pyo_time, init_sol, best_obj, best_bound, gap, gurobi_time)
    table_obj = rbind(table_obj, output)
  }
  result_name <- paste(paste("res_", folders[j],sep = ""),".xlsx", sep="")
  colnames(table_obj)<-c("ins","stages","edges","IPOpt_z","IPOpt_t","Init_Sol","Best_Obj","Best_Bound","Gap","Gurobi_t")
  write_xlsx(table_obj,result_name,col_names = TRUE,format_headers = TRUE)
}
