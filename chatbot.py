# Search message for location
# Search message for type of restuarant
# Search message for any relevant tags
# Search for breakfast, lunch, or dinner.
# Urgency
# Fancy, casual


# Understanding location language is going to be very difficult
# Near 16th and 6th (for example)
# Can get neighborhood information from the review html
# Need to understand very casual location information (UES = upper east side)
#  qq qqq



# Definitely need to have neighborhood information
# Definitely need to just focus on an NYC chatbot at first
# Unless i acquire an enormous more amount of data (yelp)
# this is mostly going to be an exercise in defining custom
# rules

# Bar
# Brunch
# Cafe
# Lunch
# Dinner

# Ideally the ability to clarify questions

cuisine
price_tier

ny_df = df[df['state'] == 'NY']
ny_df.groupby('post.rating').count()

# 583 restuarants don't have real ratings in NY
ny_df.columns
