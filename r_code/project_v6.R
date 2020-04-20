## install appropriate var package and load to library
#install.packages('vars')
library(vars)
library(lubridate)

#Define Code Version and Subfolder to save results
# Version = 'V6'

## Read Data from CSV
data <- read.csv("../data/change_percent.csv")

## Define a threshold p_value1 and p_value2 to be included in the visualization
p_value1 = 0.05
p_value2 = 0.10

## Create table without date and of sample length trade_days_per_slice
num_slices = 20
k1 = num_slices-1
day_start = 2
num_trade_days = 1
this_year = 0


for (slice in 0:k1){
## Create a valiable to iterate on each time slice starting with 0
  this_quarter = slice-(4*this_year)+1
  for (d in (day_start):(day_start+75)){
    if (!is.na(quarter(as.Date(data['DATE'][d,1])))){
      if (quarter(as.Date(data['DATE'][d,1])) == this_quarter){
        num_trade_days = num_trade_days + 1
      }  
    }
  }
  dataframe = data[(day_start):(num_trade_days+day_start-2),c(1:length(data))]
  day_0 = as.Date(dataframe['DATE'][1,1])
  day_last = as.Date(dataframe['DATE'][num_trade_days-1,1])
  stocks = data[(day_start):(num_trade_days+day_start-1),c(2:length(data))]

  num_stocks = length(stocks)
  
  stocks.train <- stocks[0:num_trade_days,]
  
  ##  Q3 2017 was being difficult so added epsilon to all values and now it works?
  num_trade_days1 = num_trade_days - 1
  if (day_0 == "2017-07-03"){

    stocks.train <- stocks[0:num_trade_days,]+0.00000001
  }
  
  ## Create a Vector Autoregressive model on the training data 
  ## with a max lag lookback of lag.max and AIC used to determine model 


  
  mod <- VAR(stocks.train[,], lag.max=1, ic = 'AIC')
  
  ## Option to create an impulse model to measure interactions
  # irf(mod, impulse = NULL, response = NULL, n.ahead = 1,
  #     ortho = TRUE, cumulative = FALSE, boot = TRUE, ci = 0.9,
  #     runs = 100, seed = NULL)
  
  ## Define an empty matrix for data input
  Results = matrix((0), ncol = num_stocks, nrow = num_stocks)
  
  ## Set column and row names to stock names
  colnames(Results) <- colnames(stocks)
  rownames(Results) <- colnames(stocks)
  
  #Create loop to populate matrix for p1
  for (p in 1:num_stocks){ #Access each source stock
    for (j in 0:num_stocks-1){ #Access each target stock
      if (j != -1){
          if (abs(coef(mod)[[p]][[(3*(num_stocks))+1+j]])<p_value1 && p != j+1){ #if the p value is < the given p_value1 and not identity 
        Results[j+1,p] = round((coef(mod)[[p]][[1+j]]),2) # then write the coefficient to the matrix
  
          }
      }
    }
  }
  ## Calculate Stock Performance in given time period
  for (p in 1:num_stocks){
    Results[p,p] = 1
    for (j in 1:num_trade_days1){
      Results[p,p]  = Results[p,p]*(1+stocks[j,p])
    }
    Results[p,p] = round((Results[p,p]-1)*100,2)#subtract one from each to show the gain or loss
  }  
  
  ## Write the results matrix to csv titled whatever is in filename
  year = year(day_0)
  my_quarter = (quarter(day_0))
  filename = sprintf("%s_Q%s_pval%s", year, my_quarter , p_value1*100)
  write.csv(Results, sprintf("../r_data/%s.csv", filename), row.names = TRUE)
  
  ##  Create loop to populate matrix for p2
  for (p in 1:num_stocks){ #Access each source stock
    for (j in 0:num_stocks-1){ #Access each target stock
      if (j != -1){
        if (abs(coef(mod)[[p]][[(3*(num_stocks))+1+j]])<p_value2 && p != j+1){ #if the p value is < the given p_value2 and not identity 
          Results[j+1,p] = round((coef(mod)[[p]][[1+j]]),2) # then write the coefficient to the matrix
          
        }
      }
    }
  }
  ## Calculate Stock Performance in given time period
  # for (p in 1:num_stocks){
  #   Results[p,p] = 1
  #   for (j in 1:num_trade_days1){
  #     Results[p,p]  = Results[p,p]*(1+stocks[j,p])
  #   }
  #   Results[p,p] = round((Results[p,p]-1)*100,2) #subtract one from each to show the gain or loss
  # }  
  
  ## Write the results matrix to csv titled whatever is in filename
  year = year(day_0) #Current year defined by current year of data entry 
  my_quarter = (quarter(day_0)) #Current Quarter defined by current quarter of data
  filename = sprintf("%s_Q%s_pval%s", year, my_quarter, p_value2*100) #Outputs example '2015_Q1_pval10'
  write.csv(Results, sprintf("../r_data/%s.csv", filename), row.names = TRUE)
  
   ## Reset number of Trade Days
  
  day_start = num_trade_days+day_start-1
  num_trade_days = 1
  if ((slice+1)%% 4 == 0){
    this_year = this_year+1
  }

}
    
    
