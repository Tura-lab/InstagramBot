from time import sleep
import datetime
import DBUsers, Constants
import traceback
import random

def login(webdriver):
    #Open the instagram login page
    while True:
        try:
            webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
            break
        except:
            pass
    #sleep for 3 seconds to prevent issues with the server
    sleep(7)
    #Find username and password fields and set their input using our constants
    username = webdriver.find_element_by_name('username')
    username.send_keys(Constants.INST_USER)
    
    password = webdriver.find_element_by_name('password')
    
    password.send_keys(Constants.INST_PASS)
    #Get the login button
    while True:
            
        try:
            button_login = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
            break
        except:
            pass
        
    #sleep again
    sleep(2)
    #click login
    button_login.click()
    sleep(8)
    #In case you get a popup after logging in, press not now.
    #If not, then just return
    try:
        notnow = webdriver.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
        sleep(2)
        notnow.click()
        
    except:
        return


def unfollow_people(webdriver, people):

    #if only one user, append in a list
    if not isinstance(people, (list,)):
        p = people
        people = []
        people.append(p)

    for user in people:
        try:
            sleep(3)
            while True:
                try:
                    webdriver.get('https://www.instagram.com/' + user + '/')
                    break

                except:
                    pass
            unfollow_xpath = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button'
            while True:
                try:
                    unfollow_confirm_xpath = '/html/body/div[3]/div/div/div[3]/button[1]'
                    break
                except:
                    pass
            if webdriver.find_element_by_xpath(unfollow_xpath).text == "Following":
                sleep(random.randint(4, 15))
                webdriver.find_element_by_xpath(unfollow_xpath).click()
                webdriver.find_element_by_xpath(unfollow_confirm_xpath).click()
            DBUsers.delete_user(user)
            sleep(7)
        except Exception:
            traceback.print_exc()
            continue


def follow_people(webdriver):
    #all the followed user
    prev_user_list = DBUsers.get_followed_users()
    #a list to store newly followed users
    new_followed = []
    #counters
    followed = 0
    likes = 0
    #Iterate theough all the hashtags from the constants
    for hashtag in Constants.HASHTAGS:

        #Visit the hashtag
        while True:
            try:
                webdriver.get('https://www.instagram.com/explore/tags/' + hashtag+ '/')
                break
            except:
                pass
        sleep(5)
        #Get the first post thumbnail and click on it
        while True:
            try:
                first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
                break
            except:
                pass
        first_thumbnail.click()
        sleep(random.randint(1,3))
        try:
            #iterate over the first 200 posts in the hashtag
            for x in range(1,200):
                t_start = datetime.datetime.now()
                #Get the poster's username
                print(" in for ")
                
                while True:
                    try:
                        username = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a').text
                        break
                    except:
                        pass
                likes_over_limit = False
                print('good')
                try:
                    
                    #get number of likes and compare it to the maximum number of likes to ignore post
                    while True:
                        try:
                            likes = int(webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text)
                            break
                        except:
                            pass
                    
                    while True:
                        try:
                            if likes > Constants.LIKES_LIMIT:
                                print("likes over {0}".format(Constants.LIKES_LIMIT))
                                likes_over_limit = True
                            break
                        except:
                            pass
                        


                    print("Detected: {0}".format(username))
                    #If username isn't stored in the database and the likes are in the acceptable range
                    if username not in prev_user_list and not likes_over_limit:
                        #Don't press the button if the text doesn't say follow
                        while True:
                            try:
                                if webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                                    #Use DBUsers to add the new user to the database
                                    DBUsers.add_user(username)
                                    #Click follow
                                    webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                                    followed += 1
                                    print("Followed: {0}, #{1}".format(username, followed))
                                    new_followed.append(username)
                                break

                            except:
                                pass


                        # Liking the picture
                        while True:
                            try:
                                button_like = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
                                break        
                            except:
                                pass
                        sleep(3)
                        while True:
                            try:
                                button_like.click()
                                break
                            except:
                                pass
                        likes += 1
                        print("Liked {0}'s post, #{1}".format(username, likes))
                        sleep(5)


                    # Next picture
                    while True:
                        try:
                            webdriver.find_element_by_link_text('Next').click()
                            break
                        except:
                            pass
                    sleep(5)
                    print("went to next")
                    
                except:
                    traceback.print_exc()
                    continue
                t_end = datetime.datetime.now()

                #calculate elapsed time
                t_elapsed = t_end - t_start
                print("This post took {0} seconds".format(t_elapsed.total_seconds()))


        except:
            traceback.print_exc()
            continue

        #add new list to old list
        for n in range(0, len(new_followed)):
            prev_user_list.append(new_followed[n])
        print('Liked {} photos.'.format(likes))
        print('Followed {} new people.'.format(followed))
