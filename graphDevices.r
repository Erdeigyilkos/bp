data <- read.csv("~/Plocha/exportNumberOfDevice.csv")

pdf("numberOfDevice.pdf",width=6,height=4,paper='special') 
plot(data$Date, data$number,type="l")
dev.off()