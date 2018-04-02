url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=40.734770989672406&lng=-74.00390625000001&city=New%20York&view_distance=305849.5707222307&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=0&limit=40'

url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=40.734770989672406&lng=-74.00390625000001&city=New%20York&view_distance=305849.5707222307&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=0&limit=40'

url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=40.44694705960048&lng=-75.93750000000001&city=New%20York&view_distance=3306045.72634833&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=0&limit=100'

url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=40.44694705960048&lng=-75.93750000000001&city=New%20York&view_distance=3306045.72634833&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=0&limit=500'

-118.25, 34.05

url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=34.05&lng=-118.25&city=Los%20Angeles&view_distance=305849.5707222307&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=0&limit=200'

# url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=34.05&lng=-118.25&city=Los%20Angeles&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=0&limit=40'

r = requests.get(url)
r.json()['totalCount']
json_data = r.json()['data']
df = json_normalize(json_data)

range(0, 3000, 500)
list(range(0, 3000, 500))

df_list = []
for offset in range(0, 3000, 500):
    url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=40.44694705960048&lng=-75.93750000000001&city=new%20york&view_distance=3306045.72634833&sort_order=highest%20rated&category%5b%5d=restaurant&offset=' + str(offset) + '&limit=500'

    r = requests.get(url)

    json_data = r.json()['data']
    df = json_normalize(json_data)
    print(df.shape)
    df_list.append(df)

final_df = pd.concat(df_list)
# hours, post.perfectFor


url = 'https://www.theinfatuation.com/api/v1/navigation/citylists'
r = requests.get(url)

temp = r.json()[0]
temp2 = temp['list_items']
city_df = json_normalize(temp2)



city_names = list(city_df['city.slug'])
austin = city_scraper('austin')
chicago = city_scraper('chicago')
denver = city_scraper('denver')
london = city_scraper('london')
san_fran = city_scraper('san-francisco')
san_fran = city_scraper('seattle')
df = city_scraper('washington-dc')



'washington-dc'.title()












    re.sub('(^[a-z]{2})', r'\1', city_name)
    re.sub('(^[a-z]{2})', r'\1', city_name)

    re.search('(^[a-z])', city_name)[0].upper()
    re.search('(-[a-z])', city_name)[0].replace('-', '%20').upper()

 def re_repl(match):
     return match.group(1).upper(), match.group(2).replace('-', '%20').upper()


    re.sub('(^[a-z])', r'\1', city_name)

    city_name



    city
    max_num


# city_df.to_pickle('city_df.pickle')



r.json()[1]




final_df.to_pickle('new_york_data.pickle')
