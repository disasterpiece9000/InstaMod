import praw
import prawcore
import json
from collections import Counter
from datetime import datetime, date
from dateutil import relativedelta
import dateutil.parser
from tinydb import TinyDB, Query

#save current time
current_time = datetime.now()

#start instance of Reddit
reddit = praw.Reddit('InstaMod')

#initialize sub specific global variables
find_stuff = Query()

#convert datetime so databse can read it
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def setUser(username):
	try:
		return reddit.redditor(username)
	except (prawcore.exceptions.NotFound, AttributeError):
		return None

class User:
	def __init__(user_info, parent_sub, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter):
		user_info.parent_sub = parent_sub
		user_info.username = username
		user_info.date_created = date_created
		user_info.analysis_time = analysis_time
		user_info.total_comment_karma = total_comment_karma
		user_info.total_post_karma = total_post_karma
		user_info.total_karma = total_karma
		
		user_info.comment_karma_counter = comment_karma_counter
			
		user_info.post_karma_counter = post_karma_counter
		
		user_info.pos_comment_counter = pos_comment_counter
			
		user_info.neg_comment_counter = neg_comment_counter
			
		user_info.pos_post_counter = pos_post_counter
			
		user_info.neg_post_counter = neg_post_counter
			
		user_info.pos_QC_counter = pos_QC_counter
			
		user_info.neg_QC_counter = neg_QC_counter
			
		user_info.net_QC_counter = Counter()
		for sub in pos_QC_counter:
			user_info.net_QC_counter[sub] = pos_QC_counter[sub]
		for sub in neg_QC_counter:
			user_info.net_QC_counter[sub] -= neg_QC_counter[sub]
		

		tdelta = relativedelta.relativedelta(datetime.now(), user_info.date_created)
		months_old = tdelta.months
		
		user_info.info_dict = {
			'parent_sub' : parent_sub,
			'username' : username,
			'date created' : date_created,
			'months old' : months_old,
			'analysis time' : analysis_time,
			'comment karma' : comment_karma_counter,
			'post karma' : post_karma_counter,
			'total comment karma' : total_comment_karma,
			'total post karma' : total_post_karma,
			'total karma' : total_karma,
			'positive comments' : pos_comment_counter,
			'negative comments' : neg_comment_counter,
			'positive posts' : pos_post_counter,
			'negative posts' : neg_post_counter,
			'positive QC' : pos_QC_counter,
			'negative QC' : neg_QC_counter,
			'net QC' : user_info.net_QC_counter
		}	
		
		userDB = TinyDB(parent_sub.sub_name + '/userInfo.json')
		if userDB.search(find_stuff.username == username):
			pass
		else:
			comment_karma_str = ''
			for sub in comment_karma_counter:
				comment_karma_str += (sub + ' ' + str(comment_karma_counter[sub]) + ' ')
				
			post_karma_str = ''
			for sub in post_karma_counter:
				post_karma_str += (sub + ' ' + str(post_karma_counter[sub]) + ' ')
				
			pos_comment_str = ''
			for sub in pos_comment_counter:
				pos_comment_str += (sub + ' ' + str(pos_comment_counter[sub]) + ' ')
			
			neg_comment_str = ''
			for sub in neg_comment_counter:
				neg_comment_str += (sub + ' ' + str(neg_comment_counter[sub]) + ' ')
				
			pos_post_str = ''
			for sub in pos_post_counter:
				pos_post_str += (sub + ' ' + str(pos_post_counter[sub]) + ' ')
				
			neg_post_str = ''
			for sub in neg_post_counter:
				neg_post_str += (sub + ' ' + str(neg_post_counter[sub]) + ' ')
				
			pos_QC_str = ''
			for sub in pos_QC_counter:
				pos_QC_str += (sub + ' ' + str(pos_QC_counter[sub]) + ' ')
				
			neg_QC_str = ''
			for sub in neg_QC_counter:
				neg_QC_str += (sub + ' ' + str(neg_QC_counter[sub]) + ' ')
			
			net_QC_str = ''
			for sub in user_info.net_QC_counter:
				net_QC_str += (sub + ' ' + str(user_info.net_QC_counter[sub]) + ' ')
				
			#str_created = json_serial(date_created)
			str_analyzed = json_serial(analysis_time)
			userDB.insert({'username' : username, 'date_created' : date_created, 'analysis_time' : str_analyzed, 'total_comment_karma' : total_comment_karma, 'total_post_karma' : total_post_karma, 'total_karma' : total_karma, 'comment_karma_counter' : comment_karma_str, 'post_karma_counter' : post_karma_str, 'pos_comment_counter' : pos_comment_str, 'neg_comment_counter' : neg_comment_str, 'pos_post_counter' : pos_post_str, 'neg_post_counter' : neg_post_str, 'pos_QC_counter' : pos_QC_str, 'neg_QC_counter' : neg_QC_str, 'net_QC_counter' : net_QC_str})
			