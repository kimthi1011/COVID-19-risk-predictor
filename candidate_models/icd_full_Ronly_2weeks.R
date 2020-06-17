# Trying just R

#install.packages("scorecard")
#install.packages("plyr)

# Traditional Credit Scoring Using Logistic Regression
library(scorecard)
library(plyr)

# data preparing ------
# load data
positive_data = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/2week-filter/positive_full_group_categorical.csv')
negative_data = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/2week-filter/negative_full_group_categorical.csv')

positive_data_df = as.data.frame(positive_data)
negative_data_df = as.data.frame(negative_data)

positive_data_df$target=1
negative_data_df$target=0

all_condition_data = rbind.fill(positive_data_df,negative_data_df)
all_condition_data[is.na(all_condition_data)]=0

# get just R
all_condition_data = all_condition_data[c(grep(pattern="CONCEPT_CODE_R", names(all_condition_data))
                                          ,grep(pattern="PERSON_ID", names(all_condition_data)) 
                                          ,grep(pattern="target", names(all_condition_data)))]

demographic_data_positive = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/person_positive.csv')
demographic_data_negative = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/person_negative.csv')

all_demographic_data = rbind(demographic_data_positive,demographic_data_negative)
head(all_demographic_data)
all_demographic_data = all_demographic_data[ 
  , !(names(all_demographic_data) %in% c("YEAR_OF_BIRTH", "DEATH_DATE"))]
# Replace bklank race with "U"
levels(all_demographic_data$RACE_SOURCE_VALUE)[1] = "U"
all_demographic_data$ETHNICITY_SOURCE_VALUE[all_demographic_data$ETHNICITY_SOURCE_VALUE==""]="Unknown"




observation_data_positive = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/positive_observation_categorical.csv')
observation_data_negative = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/negative_observation_categorical.csv')
all_observation_data = rbind.fill(observation_data_positive, observation_data_negative)
all_observation_data[is.na(all_observation_data)]=0

condition_demographic = merge(all_condition_data, all_demographic_data, by.x = "PERSON_ID", by.y="PERSON_ID" )
all_data = merge(condition_demographic, all_observation_data, by.x="PERSON_ID", by.y="PERSON_ID" )
head(all_data)
all_data = all_data[ , !(names(all_data) %in% c("person_id"))]

# look at iv
information_values = iv(all_data, y="target")
write.csv(information_values, file ="/data/project/ubrite/covid19-hackathon/Team4_staging_area/intermediate_results/icd10_full_2weeks/icd10_full_2week_iv.csv")

# filter variable via missing rate, iv, identical value rate
all_data_f = var_filter(all_data, y="target", positive=0, identical_limit = 0.95, iv_limit = 0.005)
# breaking dt into train and test
dt_list = split_df(all_data_f, y="target", ratio = 0.8, seed = 30)
label_list = lapply(dt_list, function(x) x$target)

# woe binning ------
bins = woebin(all_data_f, y="target")
# woebin_plot(bins)

# binning adjustment
## adjust breaks interactively
# breaks_adj = woebin_adj(all_data_f, "target", bins) 
## or specify breaks manually
breaks_adj = list(
  RACE_SOURCE_VALUE=c("Decline/Refuse%,%U"
                      , "Asian"
                      , "Multiple%,%Other%,%American Indian or Alaska Native"
                      , "White"
                      , "Black or African American" 
                      , "Native Hawaiian/Other Pacific Islander"
                      , "Hispanic or Latino"),
  approx_age=c("10", "20", "40", "55")
)
bins_adj = woebin(all_data_f, y="target", breaks_list=breaks_adj)

# converting train and test into woe values
dt_woe_list = lapply(dt_list, function(x) woebin_ply(x, bins_adj))

# glm / selecting variables ------
m1 = glm( target ~ ., family = binomial(), data = dt_woe_list$train)
# vif(m1, merge_coef = TRUE) # summary(m1)
# Select a formula-based model by AIC (or by LASSO for large dataset)
m_step = step(m1, direction="both", trace = FALSE)
m2 = eval(m_step$call)
# vif(m2, merge_coef = TRUE) # summary(m2)

# performance ks & roc ------
## predicted proability
pred_list = lapply(dt_woe_list, function(x) predict(m2, x, type='response'))
## Adjusting for oversampling (support.sas.com/kb/22/601.html)
# card_prob_adj = scorecard2(bins_adj, dt=dt_list$train, y='creditability', 
#                x=sub('_woe$','',names(coef(m2))[-1]), badprob_pop=0.03, return_prob=TRUE)


## performance
perf_train = perf_eva(pred = pred_list$train, label = label_list$train)
perf_test = perf_eva(pred = pred_list$test, label = label_list$test)
# perf_adj = perf_eva(pred = card_prob_adj$prob, label = label_list$train)

# score ------
## scorecard
card = scorecard(bins_adj, m2, points0 = 600, odds=1/50, pdo=50)

## credit score
score_list = lapply(dt_list, function(x) scorecard_ply(x, card))
## psi
perf_psi(score = score_list, label = label_list)

