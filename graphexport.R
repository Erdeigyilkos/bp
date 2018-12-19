setwd("/home/tom/Plocha/export/Full")
files = list.files(pattern="fullexport.*.csv")
myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd("~/Plocha/export/Device")
files = list.files(pattern="numberDevice.*.csv")
myfiles2 = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd("~/Plocha/export/Vendor")
files = list.files(pattern="vendor.*.csv")
myfiles3 = do.call(rbind, lapply(files, function(x) read.csv(x)))



setwd("/home/tom/Plocha/export")


pdf("graphs-device.pdf",width=20,height=20,paper='special') 
#numberofdevice
plot(myfiles2$Date, myfiles2$number,type="l")


plot(myfiles3$Date, myfiles3$Count,type="p",pch=20, cex=2, col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")[myfiles3$Vendor])
par(mar=c(0,0,0,0), xpd=TRUE)
legend(x="topleft",inset=c(0,0),legend=levels(myfiles3$Vendor),col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow"),pch=1 )






pdf("graphs.pdf",width=40,height=40,paper='special') 

#kolecka
plot(myfiles$Date, myfiles$signal,type="p",pch=20, cex=2, col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")[myfiles$mac])
par(mar=c(0,0,0,0), xpd=TRUE)
legend(x="topleft",inset=c(0,0),legend=levels(myfiles$mac),col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow"),pch=1 )

#kolecka - MAC device
plot(myfiles$Date, myfiles$signal,type="p",pch=20, cex=2, col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")[myfiles$mac])
par(mar=c(0,0,0,0), xpd=TRUE)
legend(x="topleft",inset=c(0,0),legend=levels(myfiles$mac),col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow"),pch=1 )

#graphforeverymac
library(ggplot2) 
ggplot(myfiles, aes(x = Date, y = signal, colour = mac)) +  geom_point() +  facet_wrap( ~ mac)

#histogram
X <- barplot(table(myfiles$mac),col=colors(),xaxt='n', ann=FALSE)
legend(x="topleft",inset=c(0,0),legend=levels(myfiles$mac),col=colors(),pch=1 )




dev.off()




