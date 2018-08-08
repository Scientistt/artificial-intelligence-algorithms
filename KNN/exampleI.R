# Created by Fabio Vitor at 22-05-2017
# K-nearest neighbor Algorithm

getDistance <- function(a, b) {
  return(2 * ifelse(a[1] == b[1], 0, 1) +
         2 * ifelse(a[2] == b[2], 0, 1) + 
         ifelse(a[3] > b[3], a[3] - b[3], b[3] - a[3]))
}

classifyKNN <- function(dataset, element, answers, k){
  for(i in c(1:length(dataset[,1]))) {
    if(i == 1) {
      distances <- getDistance(element[1:length(element) - 1], dataset[i,][1:length(dataset[i,]) - 1])
    } else {
      distances <- cbind(distances, getDistance(element[1:length(element) - 1], dataset[i,][1:length(dataset[i,]) - 1]))
    }
  }
  result1c = 0
  result2c = 0
  for(i in c(1:k)) {
    pos = which.min(distances)
    distances[pos] = NA
    ifelse(dataset[,length(dataset[1,])][pos] == answers[1], result1c <- result1c + 1, result2c <- result2c + 1)
  }
  return(ifelse(result1c > result2c, answers[1], answers[2]))
}

yes = 1
no  = 0
java   = 1127523
python = 1127524
cpp    = 1127525
dataset <- c(java, no, 3.1, yes)
dataset <- rbind(dataset, c(java, no, 2.0, no))
dataset <- rbind(dataset, c(cpp, yes, 3.5, yes))
dataset <- rbind(dataset, c(python, yes, 2.5, yes))
dataset <- rbind(dataset, c(java, yes, 3.9, no))
dataset <- rbind(dataset, c(cpp, no, 2.9, no))
dataset <- rbind(dataset, c(java, no, 1.9, no))
dataset <- rbind(dataset, c(python, yes, 3.2, yes))
element <- c(cpp, yes, 3.0, NA)

classifyKNN(dataset, element, c(yes,no), 3)

