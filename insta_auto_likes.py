# need to explicitly wait till the page loads
# Deal with "Page not available" for wrong tags

""" Instagram Liking Bot
This instagram bot is able to login to an account with provided credentials
Then go to the desired hashtags and click on the like buttons of a number of photos under that hashtag
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import time
import numpy as np
import random

from insta_credentials import eric_cred as ERIC
from insta_credentials import leen_cred as LEEN
# from insta_credentials import USERNAME, PASSWORD

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

class InstagramLikes:
    def __init__(self, username, password):
        self.count = 0
        self.username = username
        self.pw = password
        self.bot = webdriver.Firefox(executable_path = "/Users/eric8/Downloads/geckodriver.exe", options=options)

    def login(self):
        self.bot.get('https://instagram.com/accounts/login')
        time.sleep(2)
        self.bot.find_element(By.NAME,'username').send_keys(self.username)
        self.bot.find_element(By.NAME,'password').send_keys(self.pw + Keys.RETURN)
        time.sleep(10)

    def search_hashtag(self, hashtag):
        self.bot.get('https://www.instagram.com/explore/tags/' + hashtag)
        time.sleep(6)

    def search_explore(self):
        self.bot.get('https://www.instagram.com/explore')
        time.sleep(3)
        self.bot.execute_script("window.scrollTo(0, 2160)")
        time.sleep(2)
        # self.bot.execute_script("window.scrollTo(0, 4320)") # Scrolling twice gives us 55 posts
        # time.sleep(2)

    def like_photos(self, amount = np.nan):
        images = self.bot.find_elements(By.CLASS_NAME, '_aagw')
        while len(images) == 0:
            time.sleep(2)
            images = self.bot.find_elements(By.CLASS_NAME, '_aagw')
        images[0].click()
        time.sleep(2)

        if np.isnan(amount):
            amount = len(images) - 1
        for i in range(amount): # or range(amount)
            like_bttn = self.bot.find_elements(By.CLASS_NAME, "_aamw")
            if len(like_bttn) != 0:
                # time.sleep(2)
                # like_bttn = self.bot.find_elements(By.CLASS_NAME, "_aamw")
                like_bttn[0].click()
                if self._photo_unliked():
                    like_bttn[0].click()
                else:
                    self.count += 1
            time.sleep(random.randint(2,3))            
            next_bttn = self.bot.find_elements(By.CLASS_NAME, "_aaqg")
            if len(next_bttn) == 0: # If there isn't a next button
                break
            else:
                next_bttn[0].click()
            time.sleep(random.randint(2,3))

    # def like_feed(self):
    #     """Like the posts in Home feed"""
    #     self.bot.get('https://www.instagram.com')
    #     time.sleep(3)
    #     self.bot.find_element(By.XPATH, "//button[contains( text(),'Not Now')]").click()    # Deal with the Notification window
    #     # like_bttn = self.bot.find_elements(By.CLASS_NAME, "_aamw")
    #     # for bttn in like_bttn:
    #     #     bttn.click()
    #     # like_bttn = self.bot.find_elements(By.CLASS_NAME, "_aamw")
    #     self.bot.execute_script("window.scrollTo(0, 10000)")
    #     time.sleep(2)
    #     like_bttn = self.bot.find_elements(By.CLASS_NAME, "_aamw")
    #     for bttn in like_bttn:
    #         bttn.click()
    #     _ = 0



    def _photo_unliked(self):
        """ Check if the post is unliked"""
        liked = self.bot.find_elements(By.CLASS_NAME, "_aame")
        # The liked button would be at location (565, 516)
        if len(liked) == 0:
            return True
        else:
            if liked[0].location['x'] == 0:
                # it is not yet liked
                return True
        return False

 
ric_tags = ["photography","architecture","shotoniphone","travelphotography","urban","toronto","ottawa","travel",
            "film","cinematicphotography","ontario","mcmaster","nikon","like4like","likeforlike","follow4follow",
            "explorepage","autumn","fall","nikon","cinematic","streetphotography","35mm","love","art","nature"]
            
leen_tags = ["cuteboys","asianboys","handsomeman","bollywoodboys","instaboys","follow4follow",
            "followforfollow","like4like","likeforlike","likeforlikes","recentforrecent",
            "instaboys","selfie","nice","instaselfie","asianguy","chineseboy","under1k","chinese",
            "philippines","indian","indianboy","gym","gymselfie","malemodel","random", "menfashion",
            "me","gamerboy","likeme","nerd","eboy","candid","tattooboys","koreanboys","followers","asiangirls"]

ERIC["TAGS"] = ric_tags
LEEN["TAGS"] = leen_tags

def run_bot(user):
    insta = InstagramLikes(user["USERNAME"], user["PASSWORD"])
    insta.login()
    for tag in user["TAGS"]:
        print(f"In {tag}\n")
        insta.search_hashtag(tag)
        insta.like_photos()

    insta.search_explore()
    insta.like_photos()

    print(f"Liked {insta.count} posts in total.")
    return

# insta = InstagramLikes(ERIC["USERNAME"], ERIC["PASSWORD"])
# insta.login()
# insta.like_feed()

for cred in [ERIC,LEEN]:
    run_bot(cred)
