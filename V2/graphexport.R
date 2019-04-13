
args<-commandArgs(TRUE)
q = args[1]

print("Graph export started.")

setwd(paste(q,"Full", sep="/"))
files = list.files(pattern="fullexport.*.csv")
myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd(paste(q,"Device", sep="/"))
files = list.files(pattern="numberDevice.*.csv")
myfiles2 = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd(paste(q,"Vendor", sep="/"))
files = list.files(pattern="vendor.*.csv")
myfiles3 = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd(paste(q,"StackBar", sep="/"))
files = list.files(pattern="stackBar.*.csv")
myfiles4 = do.call(rbind, lapply(files, function(x) read.csv(x)))


library(anytime)

setwd(args[1])


pdf("graphs-device.pdf",width=20,height=15,paper='special') 

library(RColorBrewer)
n <- 60
qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
#pie(rep(1,n), col=sample(col_vector, n))


colors =  sample(col_vector, n)

par(xpd=T, mar=par()$mar+c(5,20,0,0))

data = myfiles4
data$Date<-NULL

barplot(t(data), main="Počet rozeznaných zařízení dle výrobců", xlab="Čas",ylab="Počet rozeznaných zařízení (ks)", col=colors, space=0.1, cex.axis=0.8, las=1,
   names.arg=c(anytime(myfiles4$Date)), cex=0.8) 
   
legend("left", inset=-.325, names(data), cex=0.8, fill=colors);


#numberofdevice
par(mar=c(10,10,10,10)+0.1)
slices <- c(myfiles3$Count)
lbls <- c(myfiles3$Vendor)
pie(myfiles3$Count,labels=paste(myfiles3$Vendor, myfiles3$Count),  main="Počet rozeznaných zařízení dle výrobců")



orderpie <- myfiles3[order(-myfiles3$Count),]
if(nrow(orderpie) > 10){
orderpie <- myfiles3[order(-myfiles3$Count),]
toppie <- orderpie[1:10,]
par(mar=c(10,10,10,10)+0.1)
slices <- c(toppie$Count)
lbls <- c(toppie$Vendor)
pie(toppie$Count,labels=paste(toppie$Vendor, toppie$Count),  main="Počet rozeznaných zařízení dle výrobců - top 10")

}




library(anytime)
plot(myfiles2$number,type="l",xaxt="n",main="Počet nalezených zařízení",xlab="Čas",ylab="Počet nalezených zařízení (ks)")
axis(1, at=1:nrow(myfiles2),labels=anytime(myfiles2$Date))

library(anytime)
plot(smooth.spline(myfiles2$number),type="l",xaxt="n",main="Počet nalezených zařízení",xlab="Čas",ylab="Počet nalezených zařízení (ks)")
axis(1, at=1:nrow(myfiles2),labels=anytime(myfiles2$Date))




print("50%")


















pdf("graphs.pdf",width=20,height=20,paper='special') 
#mac - pocet paketu
par(mar=c(10,10,10,10)+0.1)
counts <- table(myfiles$mac)
barplot(counts, main="Pocet odchycených Wi-Fi rámců jednotlivých zařízení",ylab="Počet odchycených Wi-Fi rámců (ks)",xlab="Odchycené MAC adresy", las=2)




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
ggplot(myfiles, aes(x = Date, y = signal, colour = mac)) +  geom_point() +  facet_wrap( ~ mac)+theme(legend.position="none")



#ggplot(r, aes(x = GroupDate, y = Signal, colour = GroupMac)) +  geom_point() +  facet_wrap( ~ GroupMac)
print("100%")
print("Done")



dev.off()




