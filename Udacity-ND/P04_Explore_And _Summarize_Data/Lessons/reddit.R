getwd()
reddit <- read.csv('reddit.csv')
str(reddit)

table(reddit$employment.status)

summary(reddit)


############
str(reddit)
levels(reddit$age.range)

#install.packages('ggplot2', dependencies = T) 
#library(ggplot2) 

qplot(data = reddit, x = age.range)

# ordered factors
reddit$age.range <- ordered(reddit$age.range, levels = c('Under 18', '18-24', '25-34', '35-44', '45-54', '55-65', '65 or above'))
qplot(data = reddit, x = age.range)

## alternative solution
reddit$age.range <- factor(reddit$age.range, levels = c('Under 18', '18-24', '25-34', '35-44', '45-54', '55-65', '65 or above'), ordered = T)
qplot(data = reddit, x = age.range)