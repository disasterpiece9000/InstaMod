import praw
import prawcore
import json
from datetime import datetime, date
from dateutil import relativedelta
import dateutil.parser
from tinydb import TinyDB, Query
from collections import Counter
from user import User
from ast import literal_eval

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

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# Subreddit objectclass Subreddit:
class Subreddit:
	def __init__(sub, sub_name):
		sub.updateSub(sub_name)
		sub.start_interval = datetime.now()

	# Checks if the ratelimit dict needs to be cleared
	def checkInterval(sub):
		tdelta = datetime.now() - sub.time_created
		hour_delta = tdelta.seconds / 3600.0
		if hour_delta >= sub.ratelimit_config['comments']['interval']:
			sub.ratelimit.clear()
			sub.start_interval = datetime.now()
			print('Ratelimit interval updated')

	# Flair all users in users_and_flair
	def flairUsers(sub):
		sub_obj = sub.sub_obj
		print ('Users and corresponding flair:')
		for username in sub.users_and_flair:
			user = setUser(username)
			if user not in sub.customflair:
				new_flair = sub.users_and_flair[username]['text']
				css = sub.users_and_flair[username]['css']

				if css == None or css == '':
					css = 'noflair'

				sub_obj.flair.set(user, new_flair, css)
				print ('\t' + username + ': ' + new_flair)
		sub.users_and_flair.clear()

	# Flair one user from users_and_flair
	def flairUser(sub, user, flair_text, css):
		sub_obj = sub.sub_obj
		try:
			sub_obj.flair.set(user, flair_text, css)
		except praw.exceptions.APIException:
			return False
		print('Flaired user: ' + str(user) + '\tFlair: ' + flair_text + '\tCSS:' + css)
		return True

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
		user = setUser(username)
		if user != None:
			whitelistDB = TinyDB(sub.sub_name + '/whitelist.json')
			whitelistDB.insert({'username' : username})
			sub.whitelist.append(username)
			whitelist_pm = sub.pm_config['whitelist']
			user.message(whitelist_pm['subject'], whitelist_pm['body'])
			print (username + ' added to whitelist and notified')

	# Add user to sub customflair list
	def addCustomList(sub, username):
		customflairDB = TinyDB(sub.sub_name + '/customflair.json')
		customflairDB.insert({'username' : username})
		sub.customflair.append(username)
		print (username + ' added to customflair list')

	# Add user to sub graylist
	def addGraylist(sub, username):
		graylistDB = TinyDB(sub.sub_name + '/graylist.json')
		whitelistDB = TinyDB(sub.sub_name + '/whitelist.json')

		graylistDB.insert({'username' : username})
		whitelistDB.remove(find_stuff['username'] == username)
		sub.graylist.append(username)
		print (username + ' added to graylist')

	# Add user to sub blacklist
	def addBlacklist(sub, username):
		blacklistDB = TinyDB(sub.sub_name + '/blacklist.json')
		whitelistDB = TinyDB(sub.sub_name + '/whitelist.json')

		blacklistDB.insert({'username' : username})
		whitelistDB.remove(find_stuff['username'] == username)
		sub.blacklist.append(username)
		print (username + ' added to blacklist')

	# Add a user to the expired list and database
	def addExpired(sub, user):
		username = str(user)
		expiredDB = TinyDB(sub.sub_name + '/expired.json')
		expiredDB.insert({'username' : username})
		sub.expired_users.append(user)
		print ('User: ' + username + ' added to expired list')

	# Add an image flair option to the image flair list
	def addImgFlair(sub, username):
		flair_imgDB = TinyDB(sub.sub_name + '/flair_img.json')
		flair_imgDB.insert({'username' : username})
		sub.flair_img.append(username)
		print (username + ' added to flair image permission list')

	# Turn user data into a user object
	def makeUser(sub, user, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter):
		sub.current_users.append(user)
		return User(sub, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter)

	# Turn a string into a dictionary
	def makeDict(sub, info_str):
		info_counter = Counter()
		info_list = info_str.split()
		while len(info_list) >= 2:
			info_counter[info_list.pop()] = int(info_list.pop())
		return info_counter
	# Retrieve a user's data from the database
	def getUserInfo(sub, username):
		userDB = TinyDB(sub.sub_name + '/userInfo.json')
		try:
			info_dict = userDB.search(find_stuff['username'] == username)[0]
		except IndexError:
			return None

		date_created = info_dict['date_created']
		analysis_time = info_dict['analysis_time']
		total_comment_karma = info_dict['total_comment_karma']
		total_post_karma = info_dict['total_post_karma']
		total_karma = info_dict['total_karma']
		comment_karma_counter = sub.makeDict(info_dict['comment_karma_counter'])
		post_karma_counter = sub.makeDict(info_dict['post_karma_counter'])
		pos_comment_counter = sub.makeDict(info_dict['pos_comment_counter'])
		neg_comment_counter = sub.makeDict(info_dict['neg_comment_counter'])
		pos_post_counter = sub.makeDict(info_dict['pos_post_counter'])
		neg_post_counter = sub.makeDict(info_dict['neg_post_counter'])
		pos_QC_counter = sub.makeDict(info_dict['pos_QC_counter'])
		neg_QC_counter = sub.makeDict(info_dict['neg_QC_counter'])

		return User(sub, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter)

	# Check if user should be analyzed and if they are accessible
	def checkUser(sub, user):
		if user not in sub.customflair and user not in sub.graylist and user not in sub.expired_users and str(user) not in sub.mods and user not in sub.current_users:
			try:
				user.fullname
			except (prawcore.exceptions.NotFound, AttributeError):
				return False
			return True
		else:
			return False
	# Clear the expired database after the users are analyzed
	def dropExpired(sub):
		expiredDB = TinyDB(sub.sub_name + '/expired.json')
		expiredDB.purge()
		sub.expired_users.clear()

	# Deletes all the contents of the user info database
	def wipePM(sub):
		remInfoDB = TinyDB(sub_name + '/userInfo.json')
		remInfoDB.purge()
		remExpiredDB = TinyDB(sub_name + '/expired.json')
		remExpiredDB.purge()
		sub.updateSub()

	def updateSub(sub, sub_name):
		print('Updating ' + sub_name)
		current_time = datetime.now()

		# Read current settings from wiki page
		str_config = reddit.subreddit(sub_name).wiki['InstaModSettings'].content_md
		sub_config = literal_eval(str_config)

		# Sort configuration settings
		sub.main_config = sub_config['SUB_CONFIG']
		sub.QC_config = sub_config['QC_CONFIG']
		sub.progression_config = sub_config['PROGRESS_CONFIG']
		sub.subtag_config = sub_config['SUBTAG_CONFIG']
		sub.threadlock_config = sub_config['THREADLOCK_CONFIG']
		sub.sublock_config = sub_config['SUBLOCK_CONFIG']
		sub.ratelimit_config = sub_config['RATELIMIT_CONFIG']
		sub.pm_config = sub_config['PM_CONFIG']

		# Get subreddit lists
		sub.A_subs = sub_config['A_SUBS']
		sub.B_subs = sub_config['B_SUBS']
		sub.all_subs = sub_config['B_SUBS']
		sub.all_subs.update(sub.A_subs)

		# Create lists for user databases
		sub.whitelist = []
		sub.customflair = []
		sub.graylist = []
		sub.blacklist = []
		sub.current_users = []
		sub.expired_users = []
		sub.users_and_flair = {}
		sub.flair_img = []
		sub.lock_mode = None
		sub.ratelimit = Counter()

		# Store subreddit info
		sub.mods = sub.main_config['mods']
		sub.sub_name = sub_name
		sub.sub_abbrev = sub_config['SUB_CONFIG']['abbrev']
		sub.sub_obj = reddit.subreddit(sub_name)

		# Read whitelist
		whitelistDB = TinyDB(sub_name + '/whitelist.json')
		for username in whitelistDB:
			user = setUser(username['username'])
			if user != None:
				sub.whitelist.append(user)
		print ('\tRead ' + str(len(sub.whitelist)) + ' users from whitelist')

		# Read customflair
		customflairDB = TinyDB(sub_name + '/customflair.json')
		for username in customflairDB:
			user = setUser(username['username'])
			if user != None:
				sub.customflair.append(user)
		print ('\tRead ' + str(len(sub.customflair)) + ' users from customflair')

		# Read graylist
		graylistDB = TinyDB(sub_name + '/graylist.json')
		for username in graylistDB:
			user = setUser(username['username'])
			if user != None:
				sub.graylist.append(user)
		print ('\tRead ' + str(len(sub.graylist)) + ' users from greylist')

		# Read blacklist
		blacklistDB = TinyDB(sub_name + '/blacklist.json')
		for username in blacklistDB:
			user = setUser(username['username'])
			if user != None:
				sub.blacklist.append(user)
		print ('\tRead ' + str(len(sub.blacklist)) + ' users from blacklist')

		# Read current users
		currentDB = TinyDB(sub_name + '/userInfo.json')
		for user_info in currentDB:
			tdelta = current_time - dateutil.parser.parse(user_info['analysis_time'])
			exp_length = sub.main_config['tag_expiration']
			#remove users with expired flair and add current users to list
			if tdelta.days > exp_length:
				print ('\t' + user_info['username'] + ' has old flair')
				currentDB.remove(find_stuff['username'] == user_info['username'])
			else:
				user = setUser(user_info['username'])
				#check if user is valid
				if user != None:
					sub.current_users.append(user)
		print ('\tRead ' + str(len(sub.current_users)) + ' current users')

		# Read expired users
		expiredDB = TinyDB(sub_name + '/expired.json')
		for username in expiredDB:
			user = setUser(username['username'])
			if user != None:
				sub.expired_users.append(user)
		print ('\tRead ' + str(len(sub.expired_users)) + ' users from expired list')

		# Read users with image flair permissions
		flair_imgDB = TinyDB(sub_name + '/flair_img.json')
		for username in flair_imgDB:
			user = setUser(username['username'])
			if user != None:
				sub.flair_img.append(user)
		print ('\tRead ' + str(len(sub.flair_img)) + ' users from flair image permission list\n')
