import praw
import random
from prawcore import NotFound

class redditHandler:

  def __init__(self, id, secret, us_agent):
    self.reddit = praw.Reddit(client_id=id, client_secret=secret, user_agent=us_agent)
    self.posts = {}

  def getPostFromSubreddit(self, subreddit):
    if subreddit in self.posts and self.posts.get(subreddit):
      if not self.posts[subreddit]:
        if self.refreshSubreddit(subreddit) == False:
          return False
      index = random.randrange(len(self.posts[subreddit]))
      element = self.posts.get(subreddit)[index]
      del self.posts.get(subreddit)[index]
      return element
    else:
      if self.refreshSubreddit(subreddit) == False:
        return False
      return self.getPostFromSubreddit(subreddit)

  def refreshSubreddit(self, subreddit):
    subs = self.reddit.subreddit(subreddit).hot(limit=25)
    if not self.subredditExists(subreddit):
      return False
    arrOfSubs = []
    for i in subs:
      arrOfSubs.append(i)  
    self.posts[subreddit] = arrOfSubs
  
  def subredditExists(self, subreddit):
    exists = True
    try:
        self.reddit.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
        exists = False
    return exists

    
