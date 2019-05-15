import sqlite3


class Database:
    TABLE_ACCNT_INFO = "accnt_info"
    KEY1_USERNAME = "username"
    KEY1_DATE_CREATED = "date_created"
    KEY1_RATELIMIT_START = "ratelimit_start"
    KEY1_RATELIMIT_COUNT = "ratelimit_count"
    KEY1_POST_KARMA = "total_post_karma"
    KEY1_COMMENT_KARMA = "total_comment_karma"
    KEY1_FLAIR_TEXT = "flair_text"
    KEY1_LAST_SCRAPED = "last_scraped"
    CREATE_ACCNT_INFO = ("CREATE TABLE IF NOT EXISTS " + TABLE_ACCNT_INFO + " (" +
                         KEY1_USERNAME + " TEXT, " + KEY1_DATE_CREATED + " TEXT, " +
                         KEY1_RATELIMIT_START + " TEXT, " + KEY1_RATELIMIT_COUNT + " INTEGER, " +
                         KEY1_POST_KARMA + " INTEGER, " + KEY1_COMMENT_KARMA + " INTEGER, " +
                         KEY1_FLAIR_TEXT + " TEXT, " + KEY1_LAST_SCRAPED + " TEXT" +
                         ")")
    
    TABLE_ACCNT_HISTORY = "accnt_history"
    KEY2_USERNAME = "username"
    KEY2_SUB_NAME = "sub_name"
    KEY2_POSITIVE_POSTS = "positive_posts"
    KEY2_NEGATIVE_POSTS = "negative_posts"
    KEY2_POSITIVE_COMMENTS = "positive_comments"
    KEY2_NEGATIVE_COMMENTS = "negative_comments"
    KEY2_POSITIVE_QC = "positive_qc"
    KEY2_NEGATIVE_QC = "negative_qc"
    KEY2_POST_KARMA = "post_karma"
    KEY2_COMMENT_KARMA = "comment_karma"
    CREATE_ACCNT_HISTORY = ("CREATE TABLE IF NOT EXISTS " + TABLE_ACCNT_HISTORY + " (" +
                            KEY2_USERNAME + " TEXT PRIMARY KEY, " + KEY2_SUB_NAME + " TEXT, " +
                            KEY2_POSITIVE_POSTS + " INTEGER, " + KEY2_NEGATIVE_POSTS + " INTEGER, " +
                            KEY2_POSITIVE_COMMENTS + " INTEGER, " + KEY2_NEGATIVE_COMMENTS + " INTEGER, " +
                            KEY2_POSITIVE_QC + " INTEGER, " + KEY2_NEGATIVE_QC + " INTEGER, " +
                            KEY2_POST_KARMA + " INTEGER, " + KEY2_COMMENT_KARMA + " INTEGER" +
                            ")")
    
    def __init__(self, sub_name):
        self.conn = sqlite3.connect(sub_name + "/master_databank.db")
        cur = self.conn.cursor()
        cur.execute(self.CREATE_ACCNT_INFO)
        cur.execute(self.CREATE_ACCNT_HISTORY)
        cur.close()
    
    def exists_in_db(self, username):
        cur = self.conn.cursor()
        select_str = ("SELECT EXISTS (SELECT 1 FROM " + self.TABLE_ACCNT_INFO +
                      " WHERE " + self.KEY1_USERNAME + "=?)")
        exists = cur.execute(select_str, (username,))
        
        return exists == 1
