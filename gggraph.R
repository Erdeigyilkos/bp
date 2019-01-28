setwd("/home/tom/Plocha/export/Full")
library(ggplot2) 

files = list.files(pattern="fullexport.*.csv")

myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd("/home/tom/Plocha/export")

pdf("graph-full.pdf",width=40,height=40,paper='special') 
ggplot(myfiles, aes(x = Date, y = signal, colour = mac)) +  geom_point() +  facet_wrap( ~ mac)

dev.off()
