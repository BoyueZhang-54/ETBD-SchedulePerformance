library(readxl)
library(ggplot2)
library(reshape2)
library(scatterplot3d)

path <- rstudioapi::getActiveDocumentContext()$path
path
dirname(path)
setwd(dirname(path))
getwd()

files <- list.files(
  path = "E:\\work\\research\\ETBD\\schedule\\ETBDprogram\\data\\CrfToFI\\original data",
  pattern = "\\.xlsx$",
  full.names = TRUE
)


#IC=[(n-1)(Rn-R0)-2sum_i=1^n-1(Ri-R0)]/n(Rn-R0)
#Ri list have to be from Ri to Rn-1(NOT Rn)
IC = function(n, Ri_list, R0, Rn){
  SumItem =c()
  
  for(Ri in Ri_list){
    SumItem = c(SumItem, Ri - R0)
  }
  
  SumItem = sum(SumItem)
  
  return(((n-1)*(Rn - R0) - 2*SumItem)/(n*(Rn-R0)))
  
}

#main---------------------------------


ResList = list()

#matrix for IC means
MeansIC = matrix(nrow = 6,ncol = 6)
rownames(MeansIC) <- c("0.01", "0.05", "0.1", "0.15","0.2","0.3")
colnames(MeansIC) <- c("FI 5", "FI 10", "FI 20", "FI40", "FI80", "FI200")

#matrix for IC medians
MediansIC = matrix(nrow = 6,ncol = 6)
rownames(MediansIC) <- c("0.01", "0.05", "0.1", "0.15","0.2","0.3")
colnames(MediansIC) <- c("FI 5", "FI 10", "FI 20", "FI40", "FI80", "FI200")


#process each file
for(file in files){
  
  dat <- read_excel(file)
  
  dat <- dat[-1, ]
  
  ReinforcedTicks = dat[dat$reinforcement == 1,]$ticks#pick up Reinforced ticks
  
  #Endpoints of each Interval
  EndPoints = matrix(ncol = 2, nrow = 0) 
  for( i in 1:(length(ReinforcedTicks)-1)){
    
    Pair = c(ReinforcedTicks[i],ReinforcedTicks[i+1])
    EndPoints <- rbind(EndPoints, Pair)
  }
  
  #cut data into several intervals,and calculate IC
  ICList = c()
  for(i in seq_len(nrow(EndPoints))){
    
    EPPair <- EndPoints[i, ]
    DatSlice = dat[dat$ticks>=EPPair[1] &dat$ticks<=EPPair[2], ]

    n = nrow(DatSlice)-1
    Ri_list = DatSlice$CumRes[-length(DatSlice$CumRes)]
    R0 = DatSlice$CumRes[1]
    Rn = tail(DatSlice$CumRes,1)
    
    ICValue = IC(n, Ri_list, R0, Rn)
    
    ICList = c(ICList,ICValue)
  }
  
  MeansIC[ as.character(dat$MutRate[1]), as.character(dat$Schedule[1]) ] = mean(ICList)
  MediansIC[ as.character(dat$MutRate[1]), as.character(dat$Schedule[1]) ] = median(ICList)
  
  name = paste(dat$Schedule[1], dat$MutRate[1], sep = "_")
  
  ResList[[name]] <- ICList
  
  
}

#fill by NA
MaxLen <- max(sapply(ResList, length))
ResListNA = lapply(ResList, function(x){
  length(x) <- MaxLen
  x
})

#save
df <- as.data.frame(ResListNA)
write.csv(df, "ICs.csv", row.names = FALSE)



#Figure:IC about Interval
for(name in names(ResList)){
  
  i <- ResList[[name]]
  
  i <- data.frame(
    x = seq_along(i),
    y = i
  )
  
  IntervalFigure = ggplot2::ggplot(data = i, aes(x = x, y = y))+
    geom_line()
  
  ggsave(
    filename = paste0(name, ".png"),
    plot = IntervalFigure,
    width = 8,
    height = 6,
    dpi = 300
  )
}


#plot of Mean ICs
#rownames(MeansIC) = c("0.01", "0.05", "0.10", "0.15","0.20","0.30")
{
colnames(MeansIC) = c(5,10,20,40,80,200)
dfMeans <- melt(MeansIC)
names(dfMeans) <- c("Mutation Rate", "FI Value", "Index of Curvature")
dfplot = dfMeans[dfMeans$`FI Value` != 200 | dfMeans$`Mutation Rate` != "0.01",]
dfplot$`Mutation Rate` = sprintf("%.2f", dfplot$`Mutation Rate`)


ggplot(
  dfplot,
  aes(
    x = `FI Value`,
    y = `Index of Curvature`,
    group= as.character(`Mutation Rate`),
    shape = as.character(`Mutation Rate`),
  )
) +
  geom_line(size = 1) +
  geom_point(size = 4)+
  theme_classic()+
  labs(shape = "Mutation Rate")+
  theme(text = element_text(family = "serif",
                            size = 14))+
  scale_y_continuous(labels = function(x) sprintf("%.2f", x))
  
}


#plot of Median ICs
{
colnames(MediansIC) = c(5,10,20,40,80,200)
dfMedians <- melt(MediansIC)
names(dfMedians) <- c("Mutation Rate", "FI Value", "Index of Curvature")
dfplot = dfMedians[dfMedians$`FI Value` != 200 | dfMedians$`Mutation Rate` != "0.01",]
dfplot$`Mutation Rate` = sprintf("%.2f", dfplot$`Mutation Rate`)


ggplot(
  dfplot,
  aes(
    x = `FI Value`,
    y = `Index of Curvature`,
    group= as.character(`Mutation Rate`),
    shape = as.character(`Mutation Rate`),
  )
) +
  geom_line(size = 1) +
  geom_point(size = 4)+
  theme_classic()+
  labs(shape = "Mutation Rate")+
  theme(text = element_text(family = "serif",
                            size = 14))+
  scale_y_continuous(labels = function(x) sprintf("%.2f", x))
}
