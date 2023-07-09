library(igraph)
library(readxl)
#https://kelseyandersen.github.io/DataVizR/Networks.html

instances <- sprintf("%02d",seq("01","38",1))

for(i in 1:38){
  vertices_ins = paste0(instances[i], '_SD', collapse = NULL)
  edges_ins = paste0(instances[i], '_LL', collapse = NULL)
  path_save = paste0("networks_structure/structure_",instances[i],".pdf", collapse = NULL)
  
  read_1 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = vertices_ins)
  read_2 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = edges_ins)
  
  vertices <- data.frame(nodes = c(read_1$`Stage Name`), x = read_1$xPosition, y = read_1$yPosition)
  links <- data.frame(source = c(read_2$sourceStage), destination = c(read_2$destinationStage ))
  
  pdf(file = path_save, width=7, height=7)
  g <- graph_from_data_frame(links, directed=TRUE, vertices=vertices)
  plot(g, layout=as.matrix(vertices[,c("x","y")]),
       vertex.color = "black",
       vertex.frame.color="black",
       vertex.size=3.5,
       vertex.label.cex = 0.5,
       vertex.label.dist = 1,
       edge.arrow.size = .2,
       edge.color = "gray",
       rescale=TRUE)
  dev.off()
}

# #################
# # INSTANCE 01 
# #################
# read_1 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "01_SD")
# read_2 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "01_LL")
# 
# vertices <- data.frame(nodes = c(read_1$`Stage Name`), x = read_1$xPosition, y = read_1$yPosition)
# links <- data.frame(source = c(read_2$sourceStage), destination = c(read_2$destinationStage ))
# 
# pdf(file = "ins_01.pdf", width=7, height=7)
# g <- graph_from_data_frame(links, directed=TRUE, vertices=vertices)
# plot(g, layout=as.matrix(vertices[,c("x","y")]),
#      vertex.color = "black",
#      vertex.frame.color="black",
#      vertex.size=7,
#      vertex.label.cex = 0.9,
#      vertex.label.dist = 1.3,
#      edge.arrow.size = .8,
#      edge.color = "gray",
#      rescale=TRUE)
# dev.off()
# ###############################
# #################
# # INSTANCE 11 
# #################
# read_1 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "11_SD")
# read_2 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "11_LL")
# 
# vertices <- data.frame(nodes = c(read_1$`Stage Name`), x = read_1$xPosition, y = read_1$yPosition)
# links <- data.frame(source = c(read_2$sourceStage), destination = c(read_2$destinationStage ))
# 
# pdf(file = "ins_11.pdf", width=7, height=7)
# g <- graph_from_data_frame(links, directed=TRUE, vertices=vertices)
# plot(g, layout=as.matrix(vertices[,c("x","y")]),
#      vertex.color = "black",
#      vertex.frame.color="black",
#      vertex.size=3.5,
#      vertex.label.cex = 0.6,
#      vertex.label.dist = 1,
#      edge.arrow.size = .4,
#      edge.color = "gray",
#      rescale=TRUE)
# dev.off()
# #graphics.off() 
# ###############################
# #################
# # INSTANCE 19 
# #################
# read_1 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "19_SD")
# read_2 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "19_LL")
# 
# vertices <- data.frame(nodes = c(read_1$`Stage Name`), x = read_1$xPosition, y = read_1$yPosition)
# links <- data.frame(source = c(read_2$sourceStage), destination = c(read_2$destinationStage ))
# 
# pdf(file = "ins_19.pdf", width=7, height=7)
# g <- graph_from_data_frame(links, directed=TRUE, vertices=vertices)
# plot(g, layout=as.matrix(vertices[,c("x","y")]),
#      vertex.color = "black",
#      vertex.frame.color="black",
#      vertex.size=3,
#      vertex.label.cex = 0.5,
#      vertex.label.dist = 1,
#      edge.arrow.size = .4,
#      edge.color = "gray",
#      rescale=TRUE)
# dev.off()
# #graphics.off() 
# ###############################
# #################
# # INSTANCE 30 
# #################
# read_1 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "30_SD")
# read_2 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "30_LL")
# 
# vertices <- data.frame(nodes = c(read_1$`Stage Name`), x = read_1$xPosition, y = read_1$yPosition)
# links <- data.frame(source = c(read_2$sourceStage), destination = c(read_2$destinationStage ))
# 
# pdf(file = "ins_30.pdf", width=7, height=7)
# g <- graph_from_data_frame(links, directed=TRUE, vertices=vertices)
# plot(g, layout=as.matrix(vertices[,c("x","y")]),
#      vertex.color = "black",
#      vertex.frame.color="black",
#      vertex.size=2.8,
#      vertex.label.cex = 0.5,
#      vertex.label.dist = 0.3,
#      edge.arrow.size = .4,
#      edge.color = "gray",
#      rescale=TRUE)
# dev.off()
# #graphics.off() 
# ###############################
# #################
# # INSTANCE 32 
# #################
# read_1 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "32_SD")
# read_2 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "32_LL")
# 
# vertices <- data.frame(nodes = c(read_1$`Stage Name`), x = read_1$xPosition, y = read_1$yPosition)
# links <- data.frame(source = c(read_2$sourceStage), destination = c(read_2$destinationStage ))
# 
# pdf(file = "ins_32.pdf", width=7, height=7)
# g <- graph_from_data_frame(links, directed=TRUE, vertices=vertices)
# plot(g, layout=as.matrix(vertices[,c("x","y")]),
#      vertex.color = "black",
#      vertex.frame.color="black",
#      vertex.size=2.8,
#      vertex.label.cex = 0.5,
#      vertex.label.dist = 0.7,
#      edge.arrow.size = .4,
#      edge.color = "gray",
#      rescale=TRUE)
# dev.off()
# #graphics.off() 
# ###############################
# #################
# # INSTANCE 38 
# #################
# read_1 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "38_SD")
# read_2 <- read_excel("/Users/luismoncayo/Library/CloudStorage/Dropbox/Python/GST_inventory/supply_chains_data/MSOM-06-038-R2 Data Set in Excel.xls", sheet = "38_LL")
# 
# vertices <- data.frame(nodes = c(read_1$`Stage Name`), x = read_1$xPosition, y = read_1$yPosition)
# links <- data.frame(source = c(read_2$sourceStage), destination = c(read_2$destinationStage ))
# 
# pdf(file = "ins_38.pdf", width=7, height=7)
# g <- graph_from_data_frame(links, directed=TRUE, vertices=vertices)
# plot(g, layout=as.matrix(vertices[,c("x","y")]),
#      vertex.color = "black",
#      vertex.frame.color="black",
#      vertex.size=2.8,
#      vertex.label.cex = 0.5,
#      vertex.label.dist = 0.7,
#      edge.arrow.size = .4,
#      edge.color = "gray",
#      rescale=TRUE)
# dev.off()
# #graphics.off() 
# ###############################

