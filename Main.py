from Subreddit import Subreddit
from Database import Database
import praw

r = praw.Reddit("InstaMod")
db = Database()
sub = Subreddit("CryptoCurrency", r)