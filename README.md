# InstagramBot

#How does it work?

-This is a bot built in Python and Selenium that goes on the hashtags you specify, likes random posts, then follows the people who posted it. And you will get follow backs. Simple as that.

-It runs on your localhost.

-The bot will automatically unfollow them after the number of days you specify in the file settings.json.


An automated instagram bot for increasing number of followers

# Requierments:
- Python, obviously
- Selenium (use --> python -m pip install selenium) 
- Chrome driver (download link https://chromedriver.chromium.org/downloads)
- Mysql database (I recommend you download XAMP)
- Mysql connector (use --> python -m pip install mysql-connector)


# How do I set it up?

-First head to the settings.json file and enter the password and username of your IG account and speicfy the tags you wish to search for. And then go to your mysql database and create a database (name it instabot ) and create a table called 'followed_users' within the database with two fields (username, date_added) and save the database.

In the file instabot.py line 4, specify the path to your chromedriver executable to the variable 'chromedriver_path' in the single quotes (Just copy and paste do not touch anything else).You will have to specify like "C:\Path\to\chrome\driver\executable\chromedriver.exe".

If you have succesfully done all these then you are good to go..

Just Run the file InstaBot.py and that's all.

#Note
-This bot works even in the worst of network connections
