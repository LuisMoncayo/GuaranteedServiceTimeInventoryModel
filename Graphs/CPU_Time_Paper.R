library(ggplot2)
library(tidyverse)

set_types <- function(DataFrame){
  DataFrame$ins <- as.numeric(as.character(DataFrame$ins))
  DataFrame$IPOpt_z <- as.numeric(as.character(DataFrame$IPOpt_z))
  DataFrame$IPOpt_t <- as.numeric(as.character(DataFrame$IPOpt_t))
  DataFrame$Init_Sol <- as.character(DataFrame$Init_Sol)
  DataFrame$Best_Obj <- as.numeric(as.character(DataFrame$Best_Obj))
  DataFrame$Best_Bound <- as.numeric(as.character(DataFrame$Best_Bound))
  DataFrame$Gap <- as.numeric(as.character(DataFrame$Gap))
  DataFrame$Gurobi_t <- as.numeric(as.character(DataFrame$Gurobi_t))
  DataFrame$Total_Time <- DataFrame$IPOpt_t+DataFrame$Gurobi_t
  #print(sapply(DataFrame, class))
  return(DataFrame)
}

one_min <- set_types(data.frame(read_excel("res_hint_start_1min.xlsx")))
four_min <- set_types(data.frame(read_excel("res_hint_start_4min.xlsx")))
ten_min <- set_types(data.frame(read_excel("res_hint_start_10min.xlsx")))
thirty_five_min <- set_types(data.frame(read_excel("res_hint_start_35min.xlsx")))

i=33
by_ins = data.frame()
by_ins = rbind(by_ins, one_min[i,])
by_ins = rbind(by_ins, four_min[i,])
by_ins = rbind(by_ins, ten_min[i,])
by_ins = rbind(by_ins, thirty_five_min[i,])
by_ins
#objective data
min_by_ins_obj <- min(by_ins$Best_Obj)
objective_rows <- subset(by_ins, subset=((by_ins$Best_Obj > min_by_ins_obj-0.1 & by_ins$Best_Obj < min_by_ins_obj+0.1)))
#time data
min_by_ins_time <- min(objective_rows$Total_Time)
selected_row <- subset(by_ins, subset=((by_ins$Total_Time > min_by_ins_time-0.001 & by_ins$Total_Time < min_by_ins_time+0.001)))
selected_row

minimum_obj <- data.frame()
for(i in 1:38){
  by_ins = data.frame()
  by_ins = rbind(by_ins, one_min[i,])
  by_ins = rbind(by_ins, four_min[i,])
  by_ins = rbind(by_ins, ten_min[i,])
  by_ins = rbind(by_ins, thirty_five_min[i,])
  by_ins
  #objective data
  min_by_ins_obj <- min(by_ins$Best_Obj)
  objective_rows <- subset(by_ins, subset=((by_ins$Best_Obj > min_by_ins_obj-0.1 & by_ins$Best_Obj < min_by_ins_obj+0.1)))
  #time data
  min_by_ins_time <- min(objective_rows$Total_Time)
  selected_row <- subset(by_ins, subset=((by_ins$Total_Time > min_by_ins_time-0.001 & by_ins$Total_Time < min_by_ins_time+0.001)))
  minimum_obj <- rbind(minimum_obj, selected_row)
}

##########################################
## Figure 3: Total CPU time to compute. ##
##########################################
plot_time <- ggplot(minimum_obj) + 
  geom_line(aes(x = ins, y = Total_Time/60), size=0.3, linetype = "longdash") +
  #geom_point(aes(x = instance, y = total_tim_min, shape = start_sol), shape=5, size = 2, stroke = 0.7) +
  geom_point(aes(x = ins, y = Total_Time/60, shape = Init_Sol), size = 2.3) +
  scale_shape_manual(values = c(0,1),name  ="Total CPU TIme",labels=c("Solution found without initial IPOpt solution", "Solution found with initial IPOpt solution")) +
  geom_point(aes(x = ins, y = IPOpt_t/60),shape=3, size = 1.5, stroke = 0.7) +
  annotate("point", 2.3, 80, shape = 3, size = 1.7, stroke = 0.7) +
  annotate("text", x = 5.3, y = 80, label = "IPOpt Solution", size = 2.85)  + 
  geom_point(aes(x = ins, y = Gurobi_t/60),shape=4, size = 1.5, stroke = 0.7) +
  annotate("point", 2.3, 68, shape = 4, size = 1.7, stroke = 0.7) +
  annotate("text", x = 5.3, y = 68, label = "Gurobi Solution", size = 2.85)  + 
  labs(x = "Instance") + labs(y = "Total CPU Time to Compute the Min z (min)") +
  scale_x_continuous(breaks=seq(1,38), minor_breaks=NULL) +
  scale_y_continuous(breaks=seq(0,150,10), minor_breaks=NULL, limits=c(0,150)) +
  theme_bw() +
  theme( legend.position = c(0.2, 0.8),
         axis.text.x = element_text(size = 8),
         axis.text = element_text(size = 8),
         legend.text = element_text(size = 8),
         legend.title = element_text(size = 8),
         axis.title.x = element_text(size = 8),
         axis.title.y = element_text(size = 8),
         legend.background = element_rect(fill='transparent'),
         legend.key = element_rect(fill = "transparent", colour = "transparent")
  )
plot_time
ggsave("plot_all_time.pdf", width = 20, height = 8, units = "cm", dpi = 320)
###############################################################
## Figure 4: Relation among CPU time, the 𝑣𝐺, and the 𝑢𝐺 ##
###############################################################
var_cosntrainst <- data.frame(read_excel("instance_description.xlsx", sheet = "instances_structure"))
minimum_obj$vari_G <- var_cosntrainst$variables_g
minimum_obj$cons_G <- var_cosntrainst$constraints_g

ggplot(minimum_obj, aes(x=as.numeric(vari_G), y=as.numeric(cons_G), size = Total_Time/60, label=ins)) +
  geom_point(alpha=0.2) + geom_text(size=2.5,vjust=-1.2) + coord_trans(x="log2", y="log2") +
  scale_size_area(breaks = c(0,30,60,90,120,150)) +
  scale_x_continuous(breaks=seq(0,7500,500)) + 
  scale_y_continuous(breaks=seq(0,25000,2500)) +
  labs(x = "Number of Variables in Gurobi Implentation") + labs(y = "Constraint in Gurobi Implentation", size="Minutes to Compute Min z") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,size = 7),
        axis.text = element_text(size = 6),
        legend.text = element_text(size = 8),
        legend.title = element_text(size = 8),
        axis.title.x = element_text(size = 8),
        axis.title.y = element_text(size = 8),
        legend.position = c(0.12, 0.4),
        legend.background = element_rect(fill='transparent'),
        legend.key = element_rect(fill = "transparent", colour = "transparent")
  )
ggsave("var_cont.pdf", width = 18, height = 11.5, units = "cm", dpi = 320)

###############################################################
## Table 2.  ##################################################
###############################################################
library(writexl)
library(dplyr)
table_latex_ouput <- data.frame(instance=one_min$ins,P_1=one_min$IPOpt_z,G_BO1=one_min$Best_Obj,G_BB1=one_min$Best_Bound,G_Gap1=one_min$Gap,
                                          P_4=four_min$IPOpt_z,G_BO1=four_min$Best_Obj,G_BB1=four_min$Best_Bound,G_Gap1=four_min$Gap,
                                          P_10=ten_min$IPOpt_z,G_BO10=ten_min$Best_Obj,G_BB10=ten_min$Best_Bound,G_Gap10=ten_min$Gap,
                                          P_35=thirty_five_min$IPOpt_z,G_BO35=thirty_five_min$Best_Obj,G_BB35=thirty_five_min$Best_Bound,G_Gap35=thirty_five_min$Gap)
write_xlsx(table_latex_ouput,"table_latex_ouput.xlsx",col_names = TRUE,format_headers = TRUE)


df_temp <- table_latex_ouput %>%
  select('P_1','P_4','P_10','P_35') %>%
  rowwise %>%
  mutate(match = n_distinct(unlist(cur_data())) == 1) %>%
  ungroup()

#add new column to existing data frame
table_latex_ouput$match <- df_temp$match





















