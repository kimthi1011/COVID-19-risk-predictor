#install.packages("scorecard")
#install.packages("plyr)

# Traditional Credit Scoring Using Logistic Regression
library(scorecard)
library(plyr)

# data preparing ------
# load condition/symptom data
positive_data = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/2week-filter/positive_period_group_categorical.csv')
negative_data = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/2week-filter/negative_period_group_categorical.csv')

positive_data_df = as.data.frame(positive_data)
negative_data_df = as.data.frame(negative_data)

positive_data_df$target=1
negative_data_df$target=0

all_condition_data = rbind.fill(positive_data_df,negative_data_df)
all_condition_data[is.na(all_condition_data)]=0

# load demographic data
demographic_data_positive = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/person_positive.csv')
demographic_data_negative = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/person_negative.csv')

all_demographic_data = rbind(demographic_data_positive,demographic_data_negative)
head(all_demographic_data)
all_demographic_data = all_demographic_data[ 
  , !(names(all_demographic_data) %in% c("YEAR_OF_BIRTH", "DEATH_DATE"))]
# Replace blank race with "U"
levels(all_demographic_data$RACE_SOURCE_VALUE)[1] = "U"
# Replae blank ethnicity with "unknown"
all_demographic_data$ETHNICITY_SOURCE_VALUE[all_demographic_data$ETHNICITY_SOURCE_VALUE==""]="Unknown"



# Load observation (substance use) data
observation_data_positive = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/positive_observation_categorical.csv')
observation_data_negative = read.csv(file = '/data/project/ubrite/covid19-hackathon/Team4_staging_area/parsed_data/negative_observation_categorical.csv')
all_observation_data = rbind.fill(observation_data_positive, observation_data_negative)
# Negative table has more conditions, so fill those columns in positive part of table with 0.
all_observation_data[is.na(all_observation_data)]=0
names(all_observation_data)

condition_demographic = merge(all_condition_data, all_demographic_data, by.x = "PERSON_ID", by.y="PERSON_ID" )
all_data = merge(condition_demographic, all_observation_data, by.x="PERSON_ID", by.y="PERSON_ID" )
head(all_data)
all_data = all_data[ , !(names(all_data) %in% c("person_id"))]

# look at iv for feature selection
information_values = iv(all_data, y="target")
# Record IVs
write.csv(information_values, file ="/data/project/ubrite/covid19-hackathon/Team4_staging_area/intermediate_results/final_model.csv")

# filter variable via missing rate, iv, identical value rate
all_data_f = var_filter(all_data
                        , y="target"
                        , positive=0
                        , identical_limit = 0.95
                        , var_kp=c('icd_R06'
                                   , 'icd_R05'
                                   , 'icd_R50'
                                   , 'icd_R53'
                                   , 'icd_M79'
                                   , 'icd_R09'
                                   , 'icd_R51'
                                   , 'icd_J44'
                                   , 'icd_E11'
                                   , 'icd_I25'
                                   , 'icd_I10'
                                   ))

# breaking dt into train and test
dt_list = split_df(all_data_f, y="target", ratio = 0.8, seed = 30)
label_list = lapply(dt_list, function(x) x$target)

# woe binning ------
bins = woebin(all_data_f, y="target")
# woebin_plot(bins)

# binning adjustment
## specify breaks manually for some features
breaks_adj = list(
  RACE_SOURCE_VALUE=c("Decline/Refuse%,%U"
                      , "Asian"
                      , "Multiple%,%Other%,%American Indian or Alaska Native"
                      , "White"
                      , "Black or African American" 
                      , "Native Hawaiian/Other Pacific Islander"
                      , "Hispanic or Latino"),
  approx_age=c("10", "20", "40", "55")
  , icd_R50=c("1")
  , icd_R53=c("1")
  , icd_R51=c("1")
  , icd_R09=c("1")
  , icd_J44=c("1")
)
bins_adj = woebin(all_data_f, y="target", breaks_list=breaks_adj)

# converting train and test into woe values
dt_woe_list = lapply(dt_list, function(x) woebin_ply(x, bins_adj))

# glm / selecting variables ------
# biggest possible model includes everything
upper = glm( target ~ ., family = binomial(), data = dt_woe_list$train)
# smallest possible model includes features from literature (with unintuitive results removed from final model)
lower = glm( target ~  icd_R05_woe +icd_R50_woe + icd_R53_woe + icd_M79_woe + icd_R09_woe + icd_R51_woe + icd_E11_woe, family = binomial(), data = dt_woe_list$train)


# Select a formula-based model by AIC (or by LASSO for large dataset)
m_step = step(lower, scope=list(
  upper=formula(upper)
  , lower=formula(lower)
), direction="both", trace = FALSE)
m2 = eval(m_step$call)

# performance ks & roc ------
## predicted proability
pred_list = lapply(dt_woe_list, function(x) predict(m2, x, type='response'))
## Consider adjusting for oversampling (support.sas.com/kb/22/601.html)
# card_prob_adj = scorecard2(bins_adj, dt=dt_list$train, y='creditability', 
#                x=sub('_woe$','',names(coef(m2))[-1]), badprob_pop=0.03, return_prob=TRUE)


## performance
perf_train = perf_eva(pred = pred_list$train, label = label_list$train)
perf_test = perf_eva(pred = pred_list$test, label = label_list$test)
# perf_adj = perf_eva(pred = card_prob_adj$prob, label = label_list$train)

# score ------
## scorecard
card = scorecard(bins_adj, m2, points0 = 600, odds=1/50, pdo=50)

## "credit" score for all patients
score_list = lapply(dt_list, function(x) scorecard_ply(x, card))
## psi -- performance plot and stability index
perf_psi(score = score_list, label = label_list)

