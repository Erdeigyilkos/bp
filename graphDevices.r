setwd("~/Plocha/export/Device")
files = list.files(pattern="numberDevice.*.csv")

myfiles = do.call(rbind, lapply(files, function(x) read.csv(x)))

setwd("~/Plocha/export")

pdf("numberOfDeviceGraph.pdf",width=6,height=4,paper='special') 
plot(myfiles$Date, myfiles$number,type="l")
dev.off()