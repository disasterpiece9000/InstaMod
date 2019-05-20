import ScrapeData
from psaw import PushshiftAPI


def fetch_queue(r, q, lock, sub_list):
    ps = PushshiftAPI()
    
    for sub in sub_list:
        sub.make_db()
        
    while True:
        comment = q.get()
        q.task_done()
        print(str(comment.author))
        
        # Find sub that the comment was placed in
        target_sub = None
        comment_sub = str(comment.subreddit).lower()
        for sub in sub_list:
            if sub.sub_name.lower() == comment_sub:
                target_sub = sub
                break
        if target_sub is not None:
            ScrapeData.get_data(comment, target_sub, ps)
