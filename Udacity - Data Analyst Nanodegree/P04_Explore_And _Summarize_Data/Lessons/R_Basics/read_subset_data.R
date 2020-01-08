getwd()
setwd('~/GitHub/Online_Courses/Udacity-ND/P04_/Lessons')

stateInfo <- read.csv('stateData.csv') # load file into df

View(stateInfo)

# subset data
stateSubSet <- subset(stateInfo, state.region == 1)
head(stateSubSet, 2)
dim(stateSubSet)

# another way to subset :
stateSubSet_2 <- stateInfo[stateInfo$state.region == 1 , ]
head(stateSubSet_2, 2)
dim(stateSubSet_2)