from collections import Counter


def get_data(comment, sub, ps):
    user = comment.author
    username = str(user)
    
    print("Getting data for " + username + "...")
    
    user_in_db = sub.db.exists_in_db(username)
    if not user_in_db:
        return get_all_data(comment, sub, ps)


def get_all_data(comment, sub, ps):
    author = comment.author
    username = str(author)
    
    total_post_karma = author.link_karma
    total_comment_karma = author.comment_karma
    
    comment_results = ps.search_comments(author=author,
                                         filter=["id", "score", "subreddit", "body"],
                                         limit=10)
    
    sub_comment_karma = Counter()
    sub_pos_comments = Counter()
    sub_neg_comments = Counter()
    sub_neg_qc = Counter()
    sub_pos_qc = Counter()
    
    for comment in comment_results:
        data = comment[6]
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
                                         limit=10)
    sub_post_karma = Counter()
    sub_pos_posts = Counter()
    sub_neg_posts = Counter()
    
    for post in post_results:
        data = post[5]
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
