from flask import Flask, Response, request
# from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from sqlalchemy import create_engine
import pandas as pd
from random import randint

# How does the structure of this application work and how does it
# relate to Twilio.

# This file actually defines our server that generates html pages
# or whatever

# There are these decorates that specify the response method for
# certain things.

# Like the / seems to specify the defualt html route
# The /twilio route seems to specify that if there is a post request
# made to the /twilio url then get message and formulate
# the appropriate response. We then return the response which
# somehow get routes through twilio again and sent back to the
# phone.

# Let's start by just returning a random restuarant and a link
# to that restuarant

# It's probably a good idea to to build a restaurant intent
# classification system.

# It's not quite a goal-based system because a reservation doesn't
# have to be made, but it there is the weak goal of getting a
# suitable restauarant.

# Ideally want to make this available all the time so I can host
# on AWS and have it available all of the time.

# Location should be doable. Basically want to get get coordinates
# out of location and return restauarant within a decent range.

# location, cuisine, price_range, infatuation tags
# Near the 14 and 6th translate to location coordinates

# Neighborhoods, cross-streets, subway stops, boroughs.

# It's probably much easier to ask for specific things?

# What neighborhood are you looking to eat in?
# What kind of cuisine?
# Casual, neighborhood italian place near 14th and 6th that we don't
# need reservations for. A lot this more casual information can be extracted
# from the review itself.

app = Flask(__name__)

# https://demo.twilio.com/welcome/sms/reply/
# http://0876fca8.ngrok.io/

@app.route("/")
def check_app():
    # returns a simple string stating the app is working
    return Response("It works!"), 200

@app.route("/twilio", methods=["POST"])
def inbound_sms():
    # response = twiml.Response()
    response = MessagingResponse()

    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body")

    base_url = 'https://www.theinfatuation.com'

    con = create_engine('postgresql://jplynch:@localhost:5432/restaurant_db')

    row_num = randint(1,1014)
    query = "SELECT * FROM restaurants WHERE city = 'New York' LIMIT 1 OFFSET " + str(row_num)
    df = pd.read_sql(query, con)

    restaurant_name = df['name'].iloc[0]
    link = base_url + df['post.review_link'].iloc[0]
    excerpt = df['post.excerpt'].iloc[0]

    "You should try {0} ({1}). {2}".format(restaurant_name, link, excerpt)
    response.message("You should try {0} ({1}). {2}".format(restaurant_name, link, excerpt))

    # we can now use the incoming message text in our Python application
    # if inbound_message == "Hello":
    #     response.message("Hello back to you!")
    # else:
    #     response.message("Hi! Not quite sure what you meant, but okay.")

    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200

if __name__ == "__main__":
    app.run(debug=True)
