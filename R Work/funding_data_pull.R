library(tidyverse)
library(httr)
library(curl)
library(lubridate)
library(magrittr)
library(glue)
 
# Get most recent funding period
current <- now() %>% 
  # Adjust times to be in Eastern time because that is easiest cuz funding periods start at 00:00:00.
  with_tz("US/Eastern") 
last_funding <- current %>% 
  floor_date("8 hour")

hold_date <- ymd_hms("2016-05-14 08:00:00", tz = "US/Eastern")

df <- tibble()

counter <- 0
while (hold_date <= last_funding) {
  url <- glue("https://www.bitmex.com/api/v1/funding?_format=csv&count=500&start={counter}&symbol=XBT&reverse=false")
  # print(url)
  recent_pull <- curl(url) %>%
    read_csv() #%>%
 #   mutate(timestamp = with_tz(timestamp, "US/Eastern"))
  df <- bind_rows(df, recent_pull)
   counter <- counter + 500
  hold_date <- recent_pull %>%
    extract2(1,1)
}

# Uncomment to get updated data. Last updated at 11-04-2020 at 11:00 PM CST
write_csv(df, "funding_data.csv")
