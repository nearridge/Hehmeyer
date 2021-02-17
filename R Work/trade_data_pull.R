library(tidyverse)
library(glue)
library(data.table)
library(magrittr)
library(lubridate)
library(stringr)


## BEGINNING FROM START
startDate <- ymd("20180604")
endDate <- today() %>% ymd()
op <- options(digits.secs = 10)

data <- tibble()

while (startDate <= endDate - 1) {
  string <- as.character(startDate) %>% str_remove_all("-")
  read <- fread(glue("https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/trade/{string}.csv.gz")) %>%
    as_tibble() %>%
    filter(symbol == "XBTUSD") %>%
    mutate(timestamp = ymd_hms(timestamp)) %>%
    group_by(hour(timestamp)) %>%
    filter(row_number() == 1,
           hour(timestamp) == 4 | hour(timestamp) == 12 | hour(timestamp) == 20)
  data <- bind_rows(data, read)
  startDate <- startDate + 1
  print(startDate)
}

write_csv(data, "price_data.csv")

## UPDATING EXISTING DATA SHEET
