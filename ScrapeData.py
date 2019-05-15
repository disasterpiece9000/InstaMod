def get_data(comment, sub):
    user = comment.author
    username = str(user)
    
    user_in_db = sub.db.exists_in_db(username)
    if not user_in_db:
        print("User not found in database")

    total_post_karma = user.link_karma
    total_comment_karma = user.comment_karma
    