# Overview

* scraper.py contains the scraping functions and downloads json details 
individual restuarants
* review_scraper.py downloads reviews from all cities

The first thing we scraped was the all_city_data file which gives on the links
to the individual reviews we want to scrape.

What are all of the data files?

* `review_response_list.pickle` is a list of raw review responses generated by
the `review_scraper.py` file. 
* `author_review_dict.pickle` contains combinations of reviews and authors in 
a dictionary format
* `all_city_data.pickle` contains data on individual restuarants in all cities
* `city_data_df.pickle` is only 9 rows long and just contains some basic information
on all of the cities that are covered

The restaurants database in sql has a column called `geo.point_coordinates` which contains
coordinates of all of the restuarants. Unforunately they are stored as strings. The coordinate
order appears to be the longitude first, then the latitude.

For example dell'anima has coordinates {-74.004285, 40.738002} according to the database so it has lat = 40.738002 and long = -74.004285.

Here are some helpful urls:

* 'https://www.google.com/maps/place/40%C2%B044'16.8%22N+74%C2%B000'15.4%22W/@40.738006,-74.0064737,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d40.738002!4d-74.004285'
* 'https://www.google.com/maps/place/dell'anima/@40.73798,-74.0062207,17z/data=!3m1!4b1!4m5!3m4!1s0x89c259957b8d312f:0x36dccd8a877a5334!8m2!3d40.737976!4d-74.004032'
* 'https://support.google.com/maps/answer/18539?co=GENIE.Platform%3DDesktop&hl=en'

