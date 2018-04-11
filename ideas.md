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

# How things might work

How does the structure of this application work and how does it
relate to Twilio.

This file actually defines our server that generates html pages
or whatever

There are these decorates that specify the response method for
certain things.

Like the / seems to specify the defualt html route
The /twilio route seems to specify that if there is a post request
made to the /twilio url then get message and formulate
the appropriate response. We then return the response which
somehow get routes through twilio again and sent back to the
phone.

Let's start by just returning a random restuarant and a link
to that restuarant

It's probably a good idea to to build a restaurant intent
classification system.

It's not quite a goal-based system because a reservation doesn't
have to be made, but it there is the weak goal of getting a
suitable restauarant.

Ideally want to make this available all the time so I can host
on AWS and have it available all of the time.

Location should be doable. Basically want to get get coordinates
out of location and return restauarant within a decent range.

location, cuisine, price_range, infatuation tags
Near the 14 and 6th translate to location coordinates

Neighborhoods, cross-streets, subway stops, boroughs.

It's probably much easier to ask for specific things?

What neighborhood are you looking to eat in?
What kind of cuisine?
Casual, neighborhood italian place near 14th and 6th that we don't
need reservations for. A lot this more casual information can be extracted
from the review itself.

# Building a Recomendation Engine

This is usually done when there is more data on the actual user


