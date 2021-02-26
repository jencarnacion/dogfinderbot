#dogfinderv2
#import a bunch of libraries to do a bunch of things
#requests to return requests from url, keys.py for personal api keys, json to read json returns
import requests, keys, json, datetime

#setting up a bunch of variables so i don't have to type them out later
#we imported keys.py earlier, which contains our public and secret keys, the url is the oauth url for petfinder.com
public_key =  keys.public_key
secret_key = keys.secret_key
pet_auth_url = 'https://api.petfinder.com/v2/oauth2/token'

#setting up data json to post to the petfinder.com oauth token generator
data = {
"grant_type" : 'client_credentials',
"client_id" : public_key,
"client_secret" : secret_key
}

#use requests.post to send over data to the petfinder.com oauth token generator, set auth_token as the access_token part of the json response we got from the petfinder api post
auth_response = requests.post(pet_auth_url, data = data)
auth_response_json = auth_response.json()
auth_token = auth_response_json['access_token']

#setting the url to use for requests.get
pet_get_url = 'https://api.petfinder.com/v2/animals'

#setting a json object to pass in headers for requests.get
pet_get_auth = {
"Authorization" : 'Bearer {}'.format(auth_token)
}

#setting pet_get_query json object to pass in params for requests.get
pet_get_query = {
"type" : 'Dog',
"size" : 'small',
"good_with_children" : 'true',
"good_with_dogs" : 'true',
"location" : 'San Francisco, CA',
"distance" : '50',
"sort" : 'recent',
"page" : '1',
"limit" : '20'
}

#running requests.get to pull a list of pets, converting that list to a json, then creating a json dictionary
pet_get_response = requests.get(pet_get_url, params = pet_get_query, headers = pet_get_auth)
pet_get_response_json = pet_get_response.json()
pet_data = pet_get_response_json["animals"]

#turns out pet_get_response_json is a dictionary, pet_data is a list OF DICTIONARIES. so pet_data[i] is a dictionary.

#the goal here is to iterate over pet_data for however long it is, and for each i pull out the dictionary pairing for url, name, description, published_at
#set i=0 as a starting point for iterating. also, set up some variables outside of the while loop so that they stay "static"
#also - doing some stuff with time. now object subtracts 5 minutes from current time, script runs every 5 minutes, so we're checking if any
#dog has been posted in the last 5 minutes (with pet_now_obj >= now)
pet_now = pet_data[0]["published_at"]
pet_now_obj = datetime.datetime.strptime(pet_now, '%Y-%m-%dT%H:%M:%S+%f')
current_time = datetime.datetime.now()
now = current_time - datetime.timedelta(minutes=5)

i = 0

if pet_now_obj >= now:
        today = datetime.datetime.now().date()
        #email_create = open("email_text_{}.txt".format(today), "a+")
        email_create = open("email_text.txt", "a+")
        email_create.write('To:dogfinderbot@gmail.com\nFrom:dogfinderbot@gmail.com\nSubject: NEW DOG ALERT \n \n')
        email_create.close()
        #print (len(pet_data))
        
        while i < len(pet_data):
                pet_timestamp = pet_data[i]["published_at"]
                pet_timestamp_obj = datetime.datetime.strptime(pet_timestamp, '%Y-%m-%dT%H:%M:%S+%f')
                #pet_date = pet_timestamp_obj.date()
                name = pet_data[i]["name"]
                url = pet_data[i]["url"]
                email_text = open("email_text.txt", "a")
                
                if pet_timestamp_obj >= now:
                #print ('Dog number {}'.format(i))
                #print ('Name: {}'.format(name))
                #print ('Link: {}'.format(url))
                #print ('Date: {}'.format(pet_date))
                #print (pet_timestamp)
                #print ()
                        email_text.write('Name - {}\nLink - {} \n \n'.format(name,url))
                        email_text.close()
                i = i+1
