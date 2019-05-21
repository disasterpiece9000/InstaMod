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
                         KEY1_USERNAME + " TEXT PRIMARY KEY, " + KEY1_DATE_CREATED + " INTEGER, " +
                         KEY1_RATELIMIT_START + " INTEGER, " + KEY1_RATELIMIT_COUNT + " INTEGER, " +
                         KEY1_POST_KARMA + " INTEGER, " + KEY1_COMMENT_KARMA + " INTEGER, " +
                         KEY1_FLAIR_TEXT + " TEXT, " + KEY1_LAST_SCRAPED + " INTEGER" +
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
        select_str = ("SELECT " + self.KEY1_USERNAME + " FROM " + self.TABLE_ACCNT_INFO
                      + " WHERE " + self.KEY1_USERNAME + " = ?")
        
        exists = False
        for row in cur.execute(select_str, (username,)):
            exists = True
            break
            
        cur.close()
        return exists
    
    def insert_info(self, username, created, ratelimit_start, ratelimit_count, total_post_karma,
                    total_comment_karma, flair_txt, last_scraped):
    
        print("\nInserted user into accnt_info: " + username)
        print("Created: " + str(created))
        print("Ratelimit Start: " + str(ratelimit_start))
        print("Ratelimit Count: " + str(ratelimit_count))
        print("Total Post Karma: " + str(total_post_karma))
        print("Total Comment Karma: " + str(total_comment_karma))
        if flair_txt is not None:
            print("Flair Text: " + flair_txt)
        else:
            print("Flair Text: n/a")
        print("Last Scraped: " + str(last_scraped) + "\n")
        
        cur = self.conn.cursor()
        insert_str = ("INSERT INTO " + self.TABLE_ACCNT_INFO + "(" + self.KEY1_USERNAME + ", "
                      + self.KEY1_DATE_CREATED + ", " + self.KEY1_RATELIMIT_START + ", "
                      + self.KEY1_RATELIMIT_COUNT + ", " + self.KEY1_POST_KARMA + ", "
                      + self.KEY1_COMMENT_KARMA + ", " + self.KEY1_FLAIR_TEXT + ", "
                      + self.KEY1_LAST_SCRAPED + ") "
                      + "VALUES(?,?,?,?,?,?,?,?)")
        
        cur.execute(insert_str, (username, created, ratelimit_start, ratelimit_count, total_post_karma,
                    total_comment_karma, flair_txt, last_scraped))
        self.conn.commit()
        cur.close()
    
    def print_all_users(self):
        cur = self.conn.cursor()
        select_str = "SELECT " + self.KEY1_USERNAME + " FROM " + self.TABLE_ACCNT_INFO
        
        for row in cur.execute(select_str):
            print(row)
        
        cur.close()
