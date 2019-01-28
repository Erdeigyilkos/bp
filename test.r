setwd("~/Plocha/export/Full")
files = list.files(pattern="fullexport.*.csv")

myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd("~/Plocha/export")

pdf("graph.pdf",width=20,height=20,paper='special') 
plot(myfiles$Date, myfiles$signal,type="p",pch=20, cex=2, col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")[myfiles$mac])
par(mar=c(0,0,0,0), xpd=TRUE)
legend(x="topleft",inset=c(0,0),legend=levels(myfiles$mac),col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow"),pch=1 )
dev.off()


