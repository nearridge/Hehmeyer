EDA
================
Neeraj Sharma
10/1/2020

``` r
running_size <- data
```

``` r
data %>%
  mutate(above = if_else(fundingRate > 0.0001, 1, 
                        if_else(fundingRate < -0.0001, -1, 0))) %>%
  ggplot(aes(x = timestamp, y = fundingRate)) + 
  geom_line() + 
  geom_hline(yintercept = -0.0001) + 
  geom_hline(yintercept = 0.0001) + 
  labs(title = "Lifetime Funding Rate Data Plotted") 
```

![](EDA_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

``` r
ytd2019 <- running_size %>%
  filter(timestamp < ymd_hms("2020-01-01 00:00:00", tz = "US/Eastern"),
         timestamp >= ymd_hms("2019-01-01 00:00:00", tz = "US/Eastern"))

ar <- arima(ytd2019$fundingRate, order = c(3, 0, 15))
resids <- residuals(ar)

fit <- ytd2019$fundingRate - resids

fitted <- tibble(timestamp = ytd2019$timestamp, values = fit)

ggplot() + 
  geom_line(ytd2019, mapping = aes(timestamp, fundingRate)) + 
  geom_line(fitted, mapping = aes(timestamp, values), color = "green") + 
  labs(title = "Historic Funding Data for 2019 with Model Fitted")
```

![](EDA_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

Lets see how the model fairs out of sample

``` r
abbv_ytd2020 <- running_size %>%
  filter(timestamp <= ymd_hms("2020-01-07 20:00:00", tz = "US/Eastern"),
         timestamp >= ymd_hms("2020-01-01 00:00:00", tz = "US/Eastern"))


prediction <- predict(ar, n.ahead = 20)
forecasted <- tibble(timestamp = abbv_ytd2020$timestamp[1:20], pred = prediction[["pred"]] %>% as.numeric())

ggplot() + 
  geom_line(bind_rows(ytd2019 %>% filter(timestamp >= ymd_hms("2019-12-17 04:00:00", tz = "US/Eastern")), abbv_ytd2020), mapping = aes(timestamp, fundingRate)) + 
  geom_line(fitted %>% filter(timestamp >= ymd_hms("2019-12-17 04:00:00", tz = "US/Eastern")), mapping = aes(timestamp, values), color = "green") + 
  geom_line(forecasted, mapping = aes(timestamp, pred), color = "red") + 
  labs(title = "Zoomed in on Out of Sample prediction", subtitle = "This is not interesting because I don't have volatility. Need to pick a better sample.")
```

![](EDA_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->

Let me try this attempt to predict right at the beginning of a period of
volatility

``` r
ytd2020 <- running_size %>%
  filter(timestamp >= ymd_hms("2020-01-01 00:00:00", tz = "US/Eastern"))

ggplot(ytd2020, aes(timestamp, fundingRate)) + 
  geom_line() + 
  labs(title = "Historic Funding Rate for 2020", subtitle = "Lets specifically analyze the period beginning on 2020-09-07 04:00:00") + 
  annotate("text", x = ymd_hms("2020-09-07 04:00:00"), y = -0.001, label = "2020-09-07 04:00:00") + 
  annotate("point", x = ymd_hms("2020-09-07 04:00:00"), y = -0.00075)
```

![](EDA_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

Here is a model that is fit up until 2020-09-07 04:00:00. We will use
this to predict the next 40 funding periods and see what happens.

``` r
training <- ytd2020 %>%
  filter(timestamp < ymd_hms("2020-09-07 04:00:00"))

testing <- ytd2020 %>%
  filter(timestamp >= ymd_hms("2020-09-07 04:00:00"))

# Lets fit some models
acf(training$fundingRate)
```

![](EDA_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

``` r
pacf(training$fundingRate)
```

![](EDA_files/figure-gfm/unnamed-chunk-6-2.png)<!-- -->

when the funding rate deviates from +1bps either below or above, how
long did it take for the funding rate to revert back to +1bps when it
was below and how long did it take when it was above

``` r
running_size <- running_size %>%
  mutate(signal = if_else(fundingRate > 0.0001, 1, if_else(fundingRate < -0.0001, -1, 0)),
         section = rleid(signal)) %>%
  group_by(section) %>%
  mutate(csum = cumsum(fundingRate),
         csum = if_else(signal == 0, 0, csum),
         id = row_number(),
         id = ifelse(signal == 0, NA, id)) %>%
  arrange(desc(row_number()))
 
ggplot(running_size) + 
  geom_line(aes(x = timestamp, y = csum), color = "red") + 
  geom_line(aes(x = timestamp, y = fundingRate), color = "green")
```

![](EDA_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

``` r
running_size %>%
  summarize(max = max(id)) %>%
  ggplot(aes(x = max)) + 
  geom_histogram(color = "black")
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

    ## Warning: Removed 543 rows containing non-finite values (stat_bin).

![](EDA_files/figure-gfm/unnamed-chunk-7-2.png)<!-- -->
