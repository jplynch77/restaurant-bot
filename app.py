from flask import Flask, Response, request
# from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from sqlalchemy import create_engine
import pandas as pd
from random import randint

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

    # What type of cuisine are you looking for?
    # I'm looking for really cheap chinese food in Chinatown
    # Can't just use the user's location because they might be planning ahead?
    # Really want to build a location intent neural network for New York

    # How would this work manually?
    # Neighborhoods correspond to a certain set of location geo-coordinates

    "You should try {0} ({1}). {2}".format(restaurant_name, link, excerpt)
    # response.message("You should try {0} ({1}). {2}".format(restaurant_name, link, excerpt))

    response.message("Let me lay out how this works. First you need to tell me where you want to eat. You can give me a neighborhood or an intersection or be creative. I'll try to figure where you are talking about. So let's get to it. Where do you want to eat today?")

    # we can now use the incoming message text in our Python application
    # if inbound_message == "Hello":
    #     response.message("Hello back to you!")
    # else:
    #     response.message("Hi! Not quite sure what you meant, but okay.")

    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200

if __name__ == "__main__":
    app.run(debug=True)
