#install.packages("scorecard")

# Traditional Credit Scoring Using Logistic Regression
library(scorecard)

# data preparing ------
# load data
israeliData <- read.csv(file = 'corona_tested_individuals_ver_0017.csv')
israeliData_df = as.data.frame(israeliData)
head(israeliData_df)
israeliData_df = israeliData_df[-1]
israeliData_df = subset(israeliData_df, corona_result %in% c("Negative", "Positive"))
# filter variable via missing rate, iv, identical value rate
israeliData_df_f = var_filter(israeliData_df, y="corona_result", positive="Positive")
# breaking dt into train and test
dt_list = split_df(israeliData_df_f, y="corona_result", ratio = 0.8, seed = 30)
label_list = lapply(dt_list, function(x) x$corona_result)

# woe binning ------
bins = woebin(israeliData_df_f, y="corona_result")
# woebin_plot(bins)

# binning adjustment
## adjust breaks interactively
# breaks_adj = woebin_adj(dt_f, "creditability", bins) 
## or specify breaks manually
#breaks_adj = list(
#  age.in.years=c(26, 35, 40),
#  other.debtors.or.guarantors=c("none", "co-applicant%,%guarantor"))
#bins_adj = woebin(dt_f, y="creditability", breaks_list=breaks_adj)

# converting train and test into woe values
dt_woe_list = lapply(dt_list, function(x) woebin_ply(x, bins))

# glm / selecting variables ------
m1 = glm( corona_result ~ ., family = binomial(), data = dt_woe_list$train)
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
card = scorecard(bins, m2, points0 = 600, odds=1/50, pdo=50)

## credit score
score_list = lapply(dt_list, function(x) scorecard_ply(x, card))
## psi
perf_psi(score = score_list, label = label_list)

