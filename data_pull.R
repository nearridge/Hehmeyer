library(tidyverse)
library(httr)
library(curl)

# Data this approach only goes to May 2016
# https://www.reddit.com/r/BitMEX/comments/6v2ns4/does_bitmex_provide_a_way_to_download_historical/


# while date <= current date, pull again. Original date is static 2016-05-14 12:00:00
# start_count <- 0, incriment by 500 
# bind_rows into blank df 
curl("https://www.bitmex.com/api/v1/funding?_format=csv&count=500&start=0&symbol=XBT&reverse=false") %>%
  read_csv()
