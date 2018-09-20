import praw
import prawcore
import json
from datetime import datetime, date
from dateutil import relativedelta
import dateutil.parser
from tinydb import TinyDB, Query
from user import User

#save current time
current_time = datetime.now()

#start instance of Reddit
reddit = praw.Reddit('InstaMod')

#initialize sub specific global variables
find_stuff = Query()

def setUser(username):
	try:
		return reddit.redditor(username)
	except (prawcore.exceptions.NotFound, AttributeError):
		return None

# Subreddit objectclass Subreddit:
class Subreddit:
	def __init__(sub, sub_name, sub_config):
		sub.main_config = sub_config.SUB_CONFIG
		sub.QC_config = sub_config.QC_CONFIG
		sub.progression_config = sub_config.PROGRESS_CONFIG
		sub.tag_config = sub_config.ETCTAG_CONFIG
		sub.subtag_config = sub_config.SUBTAG_CONFIG
		sub.threadlock_config = sub_config.THREADLOCK_CONFIG
		sub.sublock_config = sub_config.SUBLOCK_CONFIG
		
		sub.good_subs = sub_config.GOOD_SUBS
		sub.bad_subs = sub_config.BAD_SUBS
		sub.all_subs = sub_config.BAD_SUBS
		sub.all_subs.update(sub.good_subs)
		
		sub.whitelist = []
		sub.graytlist = []
		sub.current_users = []
		sub.expired_users = []
		sub.users_and_flair = {}
		sub.flair_img = []
		
		sub.sub_name = sub_name
		sub.sub_abbrev = sub_config.SUB_CONFIG['abbrev']
		sub.sub_obj = reddit.subreddit(sub_name)
		
		whitelistDB = TinyDB(sub_name + '/whitelist.json')
		for username in whitelistDB:
			user = setUser(username['username'])
			if user != None:
				sub.whitelist.append(user)
		print ('All users read from whitelist\n')
		
		graylistDB = TinyDB(sub_name + '/graylist.json')
		for username in graylistDB:
			user = setUser(username['username'])
			if user != None:
				sub.graylist.append(user)
		print ('All users read from greylist\n')
		
		currentDB = TinyDB(sub_name + '/userInfo.json')
		for user_info in currentDB:
			tdelta = current_time - dateutil.parser.parse(user_info['analysis_time'])
			exp_length = sub.main_config['tag_expiration']
			#remove users with expired flair and add current users to list
			if tdelta.days > exp_length:
				print (user_info['username'] + ' has old flair')
				currentDB.remove(find_stuff['username'] == user_info['username'])
			else:
				user = setUser(user_info['username'])
				#check if user is valid
				if user != None:
					sub.current_users.append(user)
		print ('Read all current users\n')
		
		expiredDB = TinyDB(sub_name + '/expired.json')
		for username in expiredDB:
			user = setUser(username['username'])
			if user != None:
				sub.expired.append(user)
		print ('All users read from expired list\n')
		
		flair_imgDB = TinyDB(sub_name + '/flair_img.json')
		for username in flair_imgDB:
			user = setUser(username['username'])
			if user != None:
				sub.flair_img.append(user)
		print ('All users read from flair image permission list\n')
		
	
	# Flair all users in users_and_flair
	def flairUsers(sub):
		print ('Users and corresponding flair:\n')
		for username in sub.users_and_flair:
			user = setUser(username)
			flair = sub.users_and_flair[username]['text']
			css = sub.users_and_flair[username]['css']
			parent_sub.flair.set(user, flair, css)
			print (username + ': ' + flair)
		sub.users_and_flair.clear()
	
	# Flair one user from users_and_flair
	def flairUser(sub, user, flair_text):
		sub_obj = sub.sub_obj
		sub_obj.flair.set(user, flair_text)
		print('Flaired user: ' + username + '\tFlair: ' + flair_text)
	
	# Concatonate flair with existing
	def appendFlair(sub, user, new_flair, css):
		username = str(user)
		if username in sub.users_and_flair:
			hold_flair = sub.users_and_flair[username]['text']
			hold_flair += ' | ' + new_flair
			flair_info = {'text' : hold_flair, 'css' : css}
			sub.users_and_flair.update({username : flair_info})
		else:
			sub.users_and_flair[username] = {'text' : new_flair, 'css' : css}
	
	# Add user to sub whitelist
	def addWhitelist(sub, username):
		whitelistDB = TinyDB(sub_name + '/whitelist.json')
		whitelitDB.insert({'username' : username})
		sub.whitelist.append(username)
		print (username + ' added to whitelist')
	
	# Add user to sub graylist
	def addGraylist(sub, username):
		graylistDB = TinyDB(sub_name + '/graylist.json')
		graylistDB.insert({'username' : username})
		sub.graylist.append(username)
		print (username + ' added to graylist')
		
	def addExpired(sub, username):
		expiredDB = TinyDB(sub_name + '/expired.json')
		expiredDB.insert({'username' : username})
		sub.expired_users.append(username)
		print (username + ' added to expired list')
		
	def addImgFlair(sub, username):
		flair_imgDB = TinyDB(sub_name + '/flair_img.json')
		flair_imgDB.insert({'username' : username})
		sub.flair_img.append(username)
		print (username + ' added to flair image permission list')
		
	def makeUser(sub, user, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter)
		return User(sub, user, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter)
	
	def makeDict(sub, info_str):
		info_counter = Counter()
		info_list = info_str.split()
		while len(info_list) >= 2:
			info_counter[info_list.pop(0)] = info_list.pop(0)
		return info_counter
	
	def getUserInfo(sub, username):
		userDB = TinyDB(parent_sub.sub_name + '/userInfo.json')
		info_dict = userDB.search(find_stuff['username'] == username)[0]
		
		date_created = info_dict['date_created']
		analysis_time = info_dict['analysis_time']
		total_comment_karma = info_dict['total_comment_karma']
		total_post_karma = info_dict['total_post_karma']
		total_karma = info_dict['total_karma']
		comment_karma_counter = makeDict(info_dict['comment_karma_counter']
		post_karma_counter = makeDict(info_dict['post_karma_counter'])
		pos_comment_counter = makeDict(info_dict['pos_comment_counter'])
		neg_comment_counter = makeDict(info_dict['neg_comment_counter'])
		pos_post_counter = makeDict(info_dict['pos_post_counter'])
		neg_post_counter = makeDict(info_dict['neg_post_counter'])
		pos_QC_counter = makeDict(info_dict['pos_QC_counter'])
		neg_QC_counter = makeDict(info_dict['neg_QC_counter'])
		
		return User(sub, user, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter)
		
		
	def checkUser(sub, user):
		if user not in sub.whitelist and user not in sub.graylist and user not in sub.expired_users and str(user) not in sub.mods:
			try:
				user.fullname
			except (prawcore.exceptions.NotFound, AttributeError):
				return False
			return True
		else:
			return False
		