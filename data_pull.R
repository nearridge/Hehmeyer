library(tidyverse)
library(httr)
library(curl)

# Data this approach only goes to 2017
# https://www.reddit.com/r/BitMEX/comments/6v2ns4/does_bitmex_provide_a_way_to_download_historical/
curl("https://www.bitmex.com/api/v1/funding?_format=csv&count=100&symbol=XBT&reverse=true&startTime=2017") %>%
  read_csv()