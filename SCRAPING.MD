# How to scrape

Go the the url 'https://www.theinfatuation.com/new-york#finder', scroll to the bottom of the page
and click on the 'next 40 results button'. Then bring up the XHR requests dashboard and look
for search api url which is 'https://www.theinfatuation.com/api/v1/venues/search?lat='

This will give you a nice json response which can be used to grab the links for
all of the reviews and other useful information.

There seems to be problems with loading this '#finder' url quite often which means
it might be beign depreciated right now?

Even before calling the search api you need to get all of the city names in order to 
get the city name and the coordinates of the city. This information is grabbed from another
api which gives basic city information with url 'https://www.theinfatuation.com/api/v1/navigation/citylists'. This url shows up on a lot of pages and contains all of the city information that we need.
