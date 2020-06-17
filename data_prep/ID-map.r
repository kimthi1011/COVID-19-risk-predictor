install.packages("readr")

library("readr")

library(dplyr)


setwd("C:/Users/mtkk9/Box/COVID hackathon/Symptom prediction project/N3C demo data 2020-06-05-v1/Data_filtering/parsed_data/")
cond <- read.csv("unmap1.csv")
View(cond)
head(cond)



?read.fwf
icd = read_fwf('icd10cm_codes_2020.txt', fwf_empty('icd10cm_codes_2020.txt', col_names = c("ID", "description")))
head(icd)
icd = as.data.frame(icd)
head(icd)

#merge = merge(cond,icd, by.x = 'CONDITION_SOURCE_VALUE', by.y = 'description', all.x = T )
write.csv(merge, file = "r_filter_merge_condition.csv")

idx2 <- sapply(cond$CONDITION_SOURCE_VALUE, grep, icd$description, fixed=TRUE)
idx1 <- sapply(seq_along(idx2), function(i) rep(i, length(idx2[[i]])))
merge1 = cbind(cond[unlist(idx1),,drop=F], icd[unlist(idx2),,drop=F])
head(merge1)

merge = merge(cond,merge1,by= 'CONDITION_SOURCE_VALUE', all.x=T)
write.csv(merge, file = "r_filter_merge_condition.csv")

