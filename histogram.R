setwd("/home/tom/Plocha/export/Full")
files = list.files(pattern="fullexport.*.csv")
myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))
setwd("/home/tom/Plocha/export")

pdf("graph-histogram.pdf",width=40,height=40,paper='special') 
X <- barplot(table(myfiles$mac),col=colors(),xaxt='n', ann=FALSE)
legend(x="topleft",inset=c(0,0),legend=levels(myfiles$mac),col=colors(),pch=1 )


dev.off()
