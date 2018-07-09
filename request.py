import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#this acesss token for owner of instabot
ACCESS_TOKEN="5733139455.ae1e665.bb1402860e13410fa09b3a7587c50e3b"
#this is base url for every api in instabot
BASE_URL = "https://api.instagram.com/v1/"

# this function create for take data from rl
def get_url_data(url):
    r= requests.get(url)
    return r.json()

#this function create for self information
def self_info():
    url = (BASE_URL) +( "users/self/?access_token= %s") %(ACCESS_TOKEN)
    r=get_url_data(url)
    if r['meta']['code']==200:
        if len(r['data']):
            print"username %s"%(r["data"]["username"])
            print"no. of followers %s"%(r["data"]["counts"]["followed_by"])
            print"no. of people following %s"%(r["data"]["counts"]["follows"])
            print"no. of posts %s"%(r['data']['counts']['media'])
        else:
            print"user does not exit"
    else:
        print"status code othet than 200"


#this function create for get any user id which is add your sandbox mode
def get_user_id(user_name):
    url=BASE_URL+"users/search?q=%s&access_token=%s"%(user_name,ACCESS_TOKEN)
    r=requests.get(url).json()
    print"request url %s"%(url)
    if r['meta']['code']==200:
        if len(r['data']):
            return r['data'][0]['id']
        else:
            return None
    else:
        print"status code other than 200"
        exit()

#this fnction create for any user information if the user is add their sandbox
def get_user_info(user_name):
    # make first url
    #first we get user id from get_user_id function
    user_id=get_user_id(user_name)
    if user_id==None:
        print"user does not exist"
        exit()
    url=BASE_URL+("users/%s?access_token=%s") %(user_id,ACCESS_TOKEN)
    print url
    user_info=get_url_data(url)
    print user_info
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print"username %s" %(user_info["data"]["username"])
            print"no. of followers %s" %(user_info["data"]["counts"]["followed_by"])
            print"no. of posts %s" %(user_info["data"]["counts"]["media"])
        else:
            print"user does not exist"
    else:
        print"meta code other than 200"



#this fnction for create downloading image
def download_image(item):

    urllib.urlretrieve(item['url'],item['name'])
    return None

# in this function we download their image from instagram app through coding
def get_own_post():
    url=BASE_URL+("users/self/media/recent?access_token=%s")%ACCESS_TOKEN
    print url
    own_media=get_url_data(url)
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name =own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            #here we call urlib function which tell image link and image name
            urllib.urlretrieve(image_url, image_name)

            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:

        print 'Status code other than 200 received!'

#in this function we download any user post which add their sand box mode
def get_user_post(user_name):
    user_id=get_user_info(user_name)
    if user_id==None:
        print"user does not exit"
        exit()

    url=BASE_URL+("users/%s/media/recent?access_token=%s")%(user_id,ACCESS_TOKEN)
    user_media=requests.get(url).json()
    if user_media['meta']['code'] ==200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 receieve'

# in this function  we get their post id. this first post
def get_post_id(user_name):
    #here we create get user id for get post id
    user_id = get_user_id(user_name)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()



#this function create for like their post
def like_a_post(user_name):
    #media is the post id
    media_id=get_post_id(user_name)
    url=BASE_URL+"media/%s/likes/?"%(media_id)
    print url
    pramas={

        "access_token":ACCESS_TOKEN
    }

    post_a_like=requests.post(url,pramas).json()
    if post_a_like["meta"]["code"]==200:
        print "like successful"
    else:
        print"like was unsuccesful"

def post_a_comment(user_name):
    media_id=get_post_id(user_name)
    url=BASE_URL+"media/%s/comments"%(media_id)
    pramas={ 
        'access_token':ACCESS_TOKEN,
        'text':"every one not perfect"
    }
    make_comment=requests.post(url,pramas).json()
    if make_comment['meta']['code']==200:
        print"comment succesfully"
    else:
        print"unsuccesfull"

#in this function we drag post_id through user name
def get_post_id(user_name):

    #fiest drag user_id fom get user id function
    user_id = get_user_id(user_name)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

def delete_negative_comment(user_name):
    media_id = get_post_id(user_name)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

#here our bot is start

def start_bot():

    #we have some menu
        while True:
            print'\n'
            print 'Hey! Welcome to instaBot!'
            print 'Here are your menu options:'
            print "a.Get your own details\n"
            print "b.Get details of a user by username\n"
            print "c.Get your own recent post\n"
            print "d.Get the recent post of a user by username\n"
            print "e.Get a list of people who have liked the recent post of a user\n"
            print "f.Like the recent post of a user\n"
            print "g.Get a list of comments on the recent post of a user\n"
            print "h.Make a comment on the recent post of a user\n"
            print "i.Delete negative comments from the recent post of a user\n"
            print "j.Exit"


            choice=raw_input("enter your choice")
            if choice=="a":
                self_info()
            elif choice=="b":
                user_name=raw_input("enter your user name:")
                get_user_info(user_name)
            elif choice=="c":
                get_own_post()
            elif choice=="d":
                user_name=raw_input("enter your user name :")
                get_user_post(user_name)
            elif choice=="f":
                user_name=raw_input("enter the user name")
                like_a_post(user_name)
            elif choice=="h":
                user_name=raw_input("enter the user name")
                post_a_comment(user_name)
            elif choice=="i":
                user_name=raw_input("enter the user name")
                delete_negative_comment(user_name)

            else:
                print"wrong choice"



start_bot()









