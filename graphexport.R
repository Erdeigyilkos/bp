
args<-commandArgs(TRUE)
q = args[1]

print("Graph export started.")

setwd(paste(q,"Full", sep="/"))
files = list.files(pattern="fullexport.*.csv")
myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))
print("Full data loaded.")

setwd(paste(q,"Device", sep="/"))
files = list.files(pattern="numberDevice.*.csv")
myfiles2 = do.call(rbind, lapply(files, function(x) read.csv(x)))
print("Device data loaded.")

setwd(paste(q,"Vendor", sep="/"))
files = list.files(pattern="vendor.*.csv")
myfiles3 = do.call(rbind, lapply(files, function(x) read.csv(x,stringsAsFactors = FALSE)))
print("Vendor data loaded.")

setwd(paste(q,"StackBar", sep="/"))
files = list.files(pattern="stackBar.*.csv")
myfiles4 = do.call(rbind, lapply(files, function(x) read.csv(x)))
print("StackBar data loaded.")

print("Data loaded.")

library(anytime)
library(RColorBrewer)
library(anytime)

setwd(args[1])

png("stackbar.png", width = 960, height = 540)
n <- 60
qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
colors =  sample(col_vector, n)
par(xpd=T, mar=par()$mar+c(5,20,0,0))
data = myfiles4
data$Date<-NULL
barplot(t(data), main="Počet rozeznaných zařízení dle výrobců", xlab="Čas",ylab="Počet rozeznaných zařízení (ks)", col=colors, space=0.1, cex.axis=0.8, las=1,
   names.arg=c(anytime(myfiles4$Date)), cex=0.8) 
legend("left", inset=-.590, names(data), cex=0.8, fill=colors);
dev.off()

png("piechart.png", width = 960, height = 540)

orderpie <- myfiles3[order(-myfiles3$Count),]
if(nrow(orderpie) > 5){
orderpie <- myfiles3[order(-myfiles3$Count),]
others <- orderpie[6:nrow(orderpie),]
toppie <- orderpie[1:5,]
toppie[nrow(toppie) + 1,] = list("225","Ostatní",sum(others$Count))
par(mar=c(10,10,10,10)+0.1)

slices <- c(toppie$Count)
lbls <- c(toppie$Vendor)
pie(toppie$Count,labels=paste(toppie$Vendor, toppie$Count),  main="Počet rozeznaných zařízení dle výrobců - top 5")
}else{
par(mar=c(10,10,10,10)+0.1)
slices <- c(myfiles3$Count)
lbls <- c(myfiles3$Vendor)
pie(myfiles3$Count,labels=paste(myfiles3$Vendor, myfiles3$Count),  main="Počet rozeznaných zařízení dle výrobců")
}

dev.off()

png("numberofdevice.png", width = 960, height = 540)


if(nrow(myfiles2)>10){
plot(smooth.spline(myfiles2$number),ylim=c(0,max(myfiles2$number)), type="l",xaxt="n",main="Počet nalezených zařízení",xlab="Čas",ylab="Počet nalezených zařízení (ks)")
axis(1, at=1:nrow(myfiles2),labels=anytime(myfiles2$Date))
}else{
plot(myfiles2$number,type="l",ylim=c(0,max(myfiles2$number)), xaxt="n",main="Počet nalezených zařízení",xlab="Čas",ylab="Počet nalezených zařízení (ks)")
axis(1, at=1:nrow(myfiles2),labels=anytime(myfiles2$Date))

}

dev.off()

png("bargraph.png", width = 960, height = 540)

counts <- table(myfiles$mac)
if(nrow(counts)>60){
par(mar=c(11,11,5,0)+0.1)
counts <- table(myfiles$mac)
dataframebar = data.frame(counts)
orderbar <- dataframebar[order(-dataframebar$Freq),]
topbar <- orderbar[1:60,]
topbar = topbar[-1,]
barplot(topbar$Freq,main="Pocet odchycených Wi-Fi rámců jednotlivých zařízení - top 60",names.arg = topbar$Var1,las=2)
title(ylab="Počet odchycených Wi-Fi rámců (ks)", line=-1.5)
}else{
par(mar=c(11,11,11,11)+0.1)
counts <- table(myfiles$mac)
barplot(counts, main="Pocet odchycených Wi-Fi rámců jednotlivých zařízení", las=2)
title(ylab="Počet odchycených Wi-Fi rámců (ks)", line=-1.5)
}

dev.off()



















pdf("graphs.pdf",width=15,height=10,paper='special') 

library(RColorBrewer)
n <- 60
qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
colors =  sample(col_vector, n)
par(xpd=T, mar=par()$mar+c(5,20,0,0))
data = myfiles4
data$Date<-NULL
barplot(t(data), main="Počet rozeznaných zařízení dle výrobců", xlab="Čas",ylab="Počet rozeznaných zařízení (ks)", col=colors, space=0.1, cex.axis=0.8, las=1,
   names.arg=c(anytime(myfiles4$Date)), cex=0.8) 
legend("left", inset=-.5, names(data), cex=0.8, fill=colors);


#numberofdevice
orderpie <- myfiles3[order(-myfiles3$Count),]
if(nrow(orderpie) > 5){
orderpie <- myfiles3[order(-myfiles3$Count),]
others <- orderpie[6:nrow(orderpie),]
toppie <- orderpie[1:5,]
toppie[nrow(toppie) + 1,] = list("225","Ostatní",sum(others$Count))
par(mar=c(10,10,10,10)+0.1)

slices <- c(toppie$Count)
lbls <- c(toppie$Vendor)
pie(toppie$Count,labels=paste(toppie$Vendor, toppie$Count),  main="Počet rozeznaných zařízení dle výrobců - top 5")
}



if(nrow(myfiles2)>10){
plot(smooth.spline(myfiles2$number),ylim=c(0,max(myfiles2$number)),type="l",xaxt="n",main="Počet nalezených zařízení",xlab="Čas",ylab="Počet nalezených zařízení (ks)")
axis(1, at=1:nrow(myfiles2),labels=anytime(myfiles2$Date))
}else{
plot(myfiles2$number,ylim=c(0,max(myfiles2$number)),type="l",xaxt="n",main="Počet nalezených zařízení",xlab="Čas",ylab="Počet nalezených zařízení (ks)")
axis(1, at=1:nrow(myfiles2),labels=anytime(myfiles2$Date))
}

print("75%")


counts <- table(myfiles$mac)
if(nrow(counts)>60){
par(mar=c(11,11,5,0)+0.1)
counts <- table(myfiles$mac)
dataframebar = data.frame(counts)
orderbar <- dataframebar[order(-dataframebar$Freq),]
topbar <- orderbar[1:60,]
topbar = topbar[-1,]

barplot(topbar$Freq,main="Pocet odchycených Wi-Fi rámců jednotlivých zařízení - top 60",names.arg = topbar$Var1,las=2)
title(ylab="Počet odchycených Wi-Fi rámců (ks)", line=-1.5)
}else{
par(mar=c(11,11,11,11)+0.1)
counts <- table(myfiles$mac)
barplot(counts, main="Pocet odchycených Wi-Fi rámců jednotlivých zařízení", las=2)
title(ylab="Počet odchycených Wi-Fi rámců (ks)", line=-1.5)
}


print("100%")
print("Done")



dev.off()


