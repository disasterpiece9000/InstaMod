from collections import Counter
from datetime import datetime
import time


def get_data(comment, sub, ps, r):
    user = comment.author
    username = str(user)
    
    user_in_db = sub.db.exists_in_db(username)
    if not user_in_db:
        print("Getting all data for " + username + "...")
        return get_all_data(comment, sub, ps)
    else:
        print("Skipped user: " + username)


def get_all_data(comment, sub, ps):
    author = comment.author
    username = str(author)
    created = author.created_utc
    total_post_karma = author.link_karma
    total_comment_karma = author.comment_karma
    flair_txt = next(sub.sub.flair(username))["flair_text"]
    last_scraped = int(time.time())
    
    # Temp values
    ratelimit_count = 0
    ratelimit_start = time.time()
    
    # Update accnt_info table
    sub.db.insert_info(username, created, ratelimit_start, ratelimit_count, total_post_karma,
                       total_comment_karma, flair_txt, last_scraped)
    
    comment_results = ps.search_comments(author=author,
                                         filter=["id", "score", "subreddit", "body"],
                                         limit=1000)
    
    sub_comment_karma = Counter()
    sub_pos_comments = Counter()
    sub_neg_comments = Counter()
    sub_neg_qc = Counter()
    sub_pos_qc = Counter()
    
    for comment in comment_results:
        try:
            data = comment[6]
        except IndexError:
            print(data)
            
        score = data["score"]
        subreddit = data["subreddit"].lower()
        body = data["body"]
        
        sub_comment_karma[subreddit] += score
        if score > 0:
            sub_pos_comments[subreddit] += 1
        else:
            sub_neg_comments[subreddit] += 1
        
        # Quality Comments
        # Positive QC
        # Posivite QC: Score
        if sub.qc_config["positive score"] != "None":
            pos_qc_score = score >= int(sub.qc_config["positive score"])
        else:
            pos_qc_score = True
        
        # Positive QC: Word Count
        if sub.qc_config["positive word count"] != "None":
            pos_qc_words = count_words(body) >= int(sub.qc_config["positive word count"])
        else:
            pos_qc_words = True
        
        # Positive QC: Result
        if sub.qc_config["positive criteria type"] == "AND":
            if pos_qc_words and pos_qc_score:
                sub_pos_qc[subreddit] += 1
        else:
            if pos_qc_words or pos_qc_score:
                sub_pos_qc[subreddit] += 1
        
        # Negative QC
        # Negative QC: Score
        if sub.qc_config["negative score"] != "None":
            neg_qc_score = score <= int(sub.qc_config["negative score"])
        else:
            neg_qc_score = True
        
        # Negative QC: Word Count
        if sub.qc_config["negative word count"] != "None":
            neg_qc_words = count_words(body) >= int(sub.qc_config["negative word count"])
        else:
            neg_qc_words = True
        
        # Negative QC: Result
        if sub.qc_config["negative criteria type"] == "AND":
            if neg_qc_words and neg_qc_score:
                sub_neg_qc[subreddit] += 1
        else:
            if neg_qc_words or neg_qc_score:
                sub_neg_qc[subreddit] += 1
    
    post_results = ps.search_submissions(author=author,
                                         filter=["id", "score", "subreddit"],
                                         limit=1000)
    sub_post_karma = Counter()
    sub_pos_posts = Counter()
    sub_neg_posts = Counter()
    
    for post in post_results:
        try:
            data = post[5]
        except IndexError:
            print(data)
            
        score = data["score"]
        subreddit = data["subreddit"].lower()
        
        sub_post_karma[subreddit] += score
        if score > 0:
            sub_pos_posts[subreddit] += 1
        else:
            sub_neg_posts[subreddit] += 1


def count_words(body):
    body_list = body.split()
    return len(body_list)
