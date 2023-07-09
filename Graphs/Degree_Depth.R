library(data.table)
library(ggplot2)
library(gridExtra)
#library(tidyr)
#library(dplyr)
#https://statisticsglobe.com/draw-multiple-ggplot-plots-side-by-side


# data <- fread("graph_structure/graph_01.csv")
# degree_depth <-data.frame(Degree = c(data$Degree), Depth = c(data$Depth))
# max_degree <- max(degree_depth$Degree)
# max_depth <- max(degree_depth$Depth)
# hist_degree <- ggplot(degree_depth, aes(x=Degree)) + 
#   geom_histogram(color="black", fill="black", bins = max_degree, binwidth = 0.3) +
#   labs(y = "No Stages (Frequency)") +
#   theme_bw()+
#   theme(axis.text=element_text(size=8),
#         axis.title=element_text(size=8),
#         panel.grid.minor.x = element_blank()
#         )
# hist_depth <- ggplot(degree_depth, aes(x=Depth)) + 
#   geom_histogram(color="black", fill="black", bins = max_depth, binwidth = 0.1) +
#   labs(y = NULL) +
#   theme_bw()+
#   theme(axis.text=element_text(size=8),
#         axis.title=element_text(size=8),
#         panel.grid.minor.x = element_blank()
#         )
# grid.arrange(hist_degree, hist_depth, ncol = 2)
# g <- arrangeGrob(hist_degree, hist_depth, nrow=1) #generates g
# ggsave("my_newPlot.pdf", g, width = 12, height = 6, units = "cm", dpi = 320)


### for all instances
instances <- sprintf("%02d",seq("01","38",1))
for(i in seq(1,38)){
  ins = instances[i]
  file_route <- paste("graph_structure/",paste(paste("graph_",ins,sep=""),".csv",sep=""),sep="")
  data <- fread(file_route)
  degree_depth <-data.frame(Degree = c(data$Degree), Depth = c(data$Depth))
  max_degree <- max(degree_depth$Degree)
  max_depth <- max(degree_depth$Depth)
  
  degree_name <- paste(paste("deg_dep_his/deg_dep",ins,sep = ""),".pdf",sep="")
  hist_degree <- ggplot(degree_depth, aes(x=Degree)) + 
    geom_histogram(color="black", fill="black", bins = max_degree, binwidth = 0.3) +
    labs(y = "No Stages (Frequency)") +
    theme_bw()+
    theme(axis.text=element_text(size=8),
          axis.title=element_text(size=8),
          panel.grid.minor.x = element_blank()
    )
  hist_depth <- ggplot(degree_depth, aes(x=Depth)) + 
    geom_histogram(color="black", fill="black", bins = max_depth, binwidth = 0.1) +
    labs(y = NULL) +
    theme_bw()+
    theme(axis.text=element_text(size=8),
          axis.title=element_text(size=8),
          panel.grid.minor.x = element_blank()
    )
  grid.arrange(hist_degree, hist_depth, ncol = 2)
  g <- arrangeGrob(hist_degree, hist_depth, nrow=1) #generates g
  ggsave(degree_name, g, width = 12, height = 6, units = "cm", dpi = 320)
}



