setwd("/home/tom/Plocha/V2/export/Full")
files = list.files(pattern="fullexport.*.csv")
myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd("~/Plocha/V2/export/Device")
files = list.files(pattern="numberDevice.*.csv")
myfiles2 = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd("~/Plocha/V2/export/Vendor")
files = list.files(pattern="vendor.*.csv")
myfiles3 = do.call(rbind, lapply(files, function(x) read.csv(x)))



setwd("/home/tom/Plocha/V2/export")


pdf("graphs-device.pdf",width=20,height=20,paper='special') 

#numberofdevice
par(mar=c(10,10,10,10)+0.1)
slices <- c(myfiles3$Count)
lbls <- c(myfiles3$Vendor)
pie(myfiles3$Count,labels=paste(myfiles3$Vendor, myfiles3$Count),  main="Pie Chart of Devices")


plot(myfiles2$Date, myfiles2$number,type="l")







pdf("graphs.pdf",width=40,height=40,paper='special') 

#mac - pocet paketu
par(mar=c(10,10,10,10)+0.1)
counts <- table(myfiles$mac)
barplot(counts, main="XXX", las=2)




#kolecka
plot(myfiles$Date, myfiles$signal,type="p",pch=20, cex=2, col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")[myfiles$mac])
par(mar=c(0,0,0,0), xpd=TRUE)
legend(x="topleft",inset=c(0,0),legend=levels(myfiles$mac),col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow"),pch=1 )




r <- aggregate(. ~myfiles$Date+myfiles$mac, data=myfiles, mean, na.rm=TRUE)
colnames(r) <- c("GroupDate", "GroupMac","Date","Mac","Signal","Vendor")

plot(r$GroupDate, r$Signal,type="p",pch=20, cex=2, col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")[r$GroupMac])
par(mar=c(0,0,0,0), xpd=TRUE)
legend(x="topleft",inset=c(0,0),legend=levels(r$GroupMac),col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow"),pch=1 )


x <- r$GroupDate
y <- c(r$Signal)
smoothingSpline = smooth.spline(x, y, spar=0.35)
lines(smoothingSpline)





#graphforeverymac
library(ggplot2) 
ggplot(myfiles, aes(x = Date, y = signal, colour = mac)) +  geom_point() +  facet_wrap( ~ mac)



ggplot(r, aes(x = GroupDate, y = Signal, colour = GroupMac)) +  geom_point() +  facet_wrap( ~ GroupMac)


dev.off()




