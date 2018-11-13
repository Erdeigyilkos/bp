data <- read.csv("~/Plocha/export.csv")

#c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")
plot(data$Date, data$signal,type="p",pch=20, cex=1, col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow")[data$mac])
par(mar=c(0,0,0,0), xpd=TRUE)
legend(x="topleft",inset=c(-0.15,0),legend=levels(data$mac),col=c("black","cyan","brown","darkgreen","darkorange","darkorchid","tan","navy","red","blue","green","yellow"),pch=1 )
#text(data$Date,data$signal, labels=data$mac, cex= 0.4)


