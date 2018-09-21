# coding: utf-8

# Python imports
import praw
import prawcore
import sys
import time
import json
import ast #https://stackoverflow.com/questions/35658160/python-script-to-parse-text-file-and-execute-inline-python-code
from collections import Counter, OrderedDict
from datetime import datetime, date
from dateutil import relativedelta
import dateutil.parser
import nltk
from nltk.tokenize import sent_tokenize
from tinydb import TinyDB, Query

# File system imports
from sub import Subreddit
from user import User

# Sub config imports
#import CryptoTechnology/config.py as CTConfig
from CryptoMarkets import config as CMConfig

# Save current time
current_time = datetime.now()

# Start instance of Reddit
reddit = praw.Reddit('InstaMod')

# Initiate TinyDB Querry
find_stuff = Query()

# List of subs for parsing folders
master_list = {
	#'CryptoTechnology' : CTConfig
	'CryptoMarkets' : CMConfig
}

# Returns Subreddit Object
def setSubs():
	sub_list = []
	
	for sub in master_list:
		sub_list.append(Subreddit(sub, master_list[sub]))
	return sub_list

# Ensures user is accessible to the bot
def setUser(username):
	try:
		return reddit.redditor(username)
	except (prawcore.exceptions.NotFound, AttributeError):
		return None
		
def checkIsInt(target_str):
	try:
		int(target_str)
		return True
	except ValueError:
		return False
		
def scrapeSub(parent_sub, cmnt_limit, post_limit):
	sub = parent_sub.sub_obj
	locked_threads = {}
	insta_flair = []
	
	print ('Scraping comments\n')
	comments = sub.comments(limit = cmnt_limit)
	for comment in comments:
		user = comment.author
		username = str(user)

		if parent_sub.checkUser(user) == True:
			#print (dir(parent_sub.sub_obj.flair(user)))
			flair = next(parent_sub.sub_obj.flair(user))['flair_text']
			print (flair)
			if flair != '' and flair != None:
				parent_sub.addExpired(user)
			else:
				insta_flair.append(user)
				print ('User: ' + username + ' added to instant flair list')
			
	print ('Scraping submissions\n')
	posts = sub.new(limit = post_limit)
	for post in posts:
		user = post.author
		username = str(user)

		if parent_sub.checkUser(user) == True:
			flair = list(parent_sub.sub_obj.flair(user))[0]
			if flair != '' and flair != None:
				parent_sub.addExpired(user)
			else:
				insta_flair.append(user)
		
		# Check if post has flair for thread locking and save post ID
		if parent_sub.main_config['thread_lock'] == True:
			if post.link_flair_text != None:
				lock_status = checkThreadLock(parent_sub, post.link_flair_text)
				if lock_status != None:
					locked_threads[post.fullname] = lock_status
					print ('Post: ' + post.fullname + ' was added to locked_threads\nLock Status: ' + lock_status)
	
	# Instantly flair users without any flair
	analyzeUsers(parent_sub, insta_flair)
		
	update_interval = parent_sub.main_config['update_interval']
	
	if update_interval == 'INSTANT':
		analyzeUsers(parent_sub, parent_sub.expired_users)
		parent_sub.dropExpired()
		
	elif len(parent_sub.expired_users) > update_interval:
			analyzeUsers(parent_sub, parent_sub.expired_users)
			parent_sub.dropExpired()
	
	if parent_sub.main_config['thread_lock'] == True or parent_sub.main_config['sub_lock'] == True:
		# Recheck comments for users who should have comments auto deleted or for comments in locked threads
		for comment in sub.comments(limit = cmnt_limit):
			user = comment.author
			username = str(user)
			post = comment.submission
			submis_id = post.fullname

			# TODO: Handel sublock
				
			# Check if comment is in a locked thread
			if submis_id in locked_threads and parent_sub.checkUser(user):
				lock_status = locked_threads[submis_id]
				user_info = parent_sub.getUserInfo(username)
				
				if handelThreadLock(parent_sub, lock_status, user_info):
					lock_type = parent_sub.threadlock_config[lock_status]
					action = lock_type['action']
					
					if action == 'REMOVE':
						message_info = parent_sub.threadlock_config['remove_message']
						if message_info != None:
							user.message(message_info[0], ("\n\nSubreddit: " + parent_sub.sub_name + "\n\nPost: " + post.title + "\n\nLock Type: " + lock_status + "\n\nComment: " + comment.body + "\n\n" + message_info[1]))
							comment.mod.remove()
							print ('Comment removed and user notified')
					elif action == 'SPAM':
						comment.mod.remove(spam=True)
							

# Analyze a user's comments and posts and extract data from them
def analyzeHistory(parent_sub, user):
	# Data points
	username = str(user)
	date_created = user.created
	analysis_time = datetime.now()
	total_comment_karma = user.comment_karma
	total_post_karma = user.link_karma
	total_karma = total_comment_karma + total_post_karma
	
	comment_karma_counter = Counter()
	post_karma_counter = Counter()
	pos_comment_counter = Counter()
	neg_comment_counter = Counter()
	pos_post_counter = Counter()
	neg_post_counter = Counter()
	pos_QC_counter = Counter()
	neg_QC_counter = Counter()
	
	# Parse comments
	for comment in user.comments.new(limit = None):
		cmnt_sub = comment.subreddit
		sub_name = str(cmnt_sub)
		cmnt_score = comment.score
		word_count = countWords(comment.body)
		abbrev = None
		
		if sub_name.upper() in parent_sub.all_subs:
			abbrev = parent_sub.all_subs[sub_name.upper()]
		
		if abbrev != None:
			comment_karma_counter[abbrev] += cmnt_score
			if cmnt_score > 0:
				pos_comment_counter[abbrev] += 1
			elif cmnt_score < 0:
				neg_comment_counter[abbrev] += 1
			
			if cmnt_score >= parent_sub.QC_config['pos_karma']:
				if parent_sub.QC_config['pos_words'] == None:
					pos_QC_counter[abbrev] += 1
				elif word_count >= parent_sub.QC_config['pos_words']:
					pos_QC_counter[abbrev] += 1
			if cmnt_score <= parent_sub.QC_config['neg_karma']:
				if parent_sub.QC_config['neg_words'] == None:
					neg_QC_counter[abbrev] += 1
				elif word_count <= parent_sub.QC_config['neg_words']:
					neg_QC_counter[abbrev] += 1
					
	# Parse posts
	for post in user.submissions.new(limit = None):
		post_sub = post.subreddit
		sub_name = str(post_sub)
		post_score = post.score
		abbrev = None
		
		if sub_name in parent_sub.A_subs:
			abbrev = parent_sub.A_subs[sub_name.upper()]
		elif sub_name in parent_sub.B_subs:
			abbrev = parent_sub.B_subs[sub_name.upper()]
		
		if abbrev != None:
			post_karma_counter[abbrev] += cmnt_score
			
			if post_score > 0:
				pos_comment_counter[abbrev] += 1
			elif post_score < 0:
				neg_comment_counter[abbrev] += 1
				
	return parent_sub.makeUser(user, username, date_created, analysis_time, total_comment_karma, total_post_karma, total_karma, comment_karma_counter, post_karma_counter, pos_comment_counter, neg_comment_counter, pos_post_counter, neg_post_counter, pos_QC_counter, neg_QC_counter)
	

# Get users' history and process data based on info
def analyzeUsers(parent_sub, user_list):
	current_time = datetime.now()
	print ('Analyzing all users in current list: ' + str(len(user_list)) + '\n')
	
	for user in user_list:
		username = str(user)
		print ('\tAnalyzing user: ' + username)
		user_info = analyzeHistory(parent_sub, user)
		
		if parent_sub.main_config['sub_progression'] == True:
			for tier, config in parent_sub.progression_config.items():
				if tier.startswith('tier') and checkInfoTag(parent_sub, user_info, config):
					flair_text = config['flair_text']
					flair_css = config['flair_css']
					permissions = config['permissions']
					
					parent_sub.appendFlair(user, flair_text, flair_css)
					if permissions == 'CUSTOM_FLAIR':
						parent_sub.addWhitelist(username)
					elif permissions == 'FLAIR_ICONS':
						parent_sub.addImgFlair(username)
					break
		
		if parent_sub.main_config['sub_tags'] == True:
			for tag, config in parent_sub.subtag_config.items():
				if tag.startswith('subtag'):
					hold_subs = getSubTag(parent_sub, user_info, config)
					pre_text = config['pre_text']
					post_text = config['post_text']
					
					for sub in hold_subs:
						parent_sub.appendFlair(user, (pre_text + sub + post_text), None)
		
		if parent_sub.main_config['accnt_age'] != False:
			userCreated = user_info.date_created
			tdelta = relativedelta.relativedelta(datetime.now(), datetime.fromtimestamp(user_info.date_created))
			if tdelta.months <= parent_sub.main_config['accnt_age']:	
				#create flair with appropriate time breakdown
				if tdelta.years < 1:
					if tdelta.months < 1:
						days = tdelta.days
						flairText = str(days)
						if days == 1:
							parent_sub.appendFlair(username, flairText + ' day old', None)
						else:
							parent_sub.appendFlair(username, flairText + ' days old', None)
					elif tdelta.months < 6:
						months = tdelta.months
						flairText = str(months)
						if months == 1:
							parent_sub.appendFlair(user, flairText + ' month old', None)
					else:
						parent_sub.appendFlair(user, flairText + ' months old', None)
		"""		
		if parent_sub.main_config['etc_tags'] == True:
			for tag, config in parent_sub.tag_config:
				if tag.startswith("tag"):
					conditional_str = config[0]
					flair_text = config[1]
					flair_css = config[2]
		"""
	parent_sub.flairUsers()
	
def readPMs(parent_sub):
	messages = reddit.inbox.unread()
	for message in messages:
		author = message.author
		username = str(author)
		if message.subject.startswith('!' + parent_sub.sub_name) and username in parent_sub.mods:
			print('Message accepted: ' + message.body)
			message_words = message.body.split()
			
			if len(message_text) != 2:
				message.reply('More or less than 2 arguments were found in the body of the message. Please try again with the proper syntax. If you believe this is an error, please contact /u/shimmyjimmy97')
				message.mark_read()
				print ('Message resolved without action: Invalid number of arguments')
				continue
			
			else:
				target_username = message_words[1]
				user = setUser(target_username)
				if user == None:
					message.reply("The user was not able to be accessed by InstaMod. This could be becasue they don't exist, are shadowbanned, or a server error. If you feel that this is a mistake, please contact /u/shimmyjimmy97.")
					message.mark_read()
					print ('Message resolved without action: Target user not accessible')
					continue
				
				if message_words[0] == "!whitelist":
					if str(user) not in parent_sub.whitelist:
						parent_sub.addWhitelist(target_username)
						message.reply('The user: ' + target_username + ' has been added to the whitelist and will no longer recieve new flair. They are also now eligible for custom flair. The user will be notified of their whitelisted status now.')
						message.mark_read()
						
						user.message('You have been granted permission to assign custom flair! A moderator of r/' + parent_sub.sub_name + ' has granted your account permission to assign custom flair. To choose your flair, send me (/u/InstaMod) a private message with the syntax:\n\nSubject:\n\n    !SubredditName\n\nBody:    !flair flair text here\n\nFor example, if you want your flair to say "Future Proves Past" then your PM should look like this:\n\n    !flair Future Proves Past\n\n If you have any questions, please send /u/shimmyjimmy97 a PM, or contact the moderators.')
						print ('Message resolved successfully')
					else:
						message.reply('The user: ' + target_username + ' is already in the whitelist')
						message.mark_read()
						print ('Message resolved without action: User already in whitelist')
				
				if message_words[0] == "!greylist" or message_words[0] == '!graylist':
					if str(user) not in parent_sub.graylist:
						parent_sub.addGraylist(target_username)
						message.reply('The user: ' + target_username + ' has been added to the graylist and will no longer recieve new flair.')
						message.mark_read()
						print ('Message resolved successfully')
					else:
						message.reply('The user: ' + target_username + ' is already in the graylist')
						message.mark_read()
						print ('Message resolved without action: User already in graylist')
				
				if message_words[0] == '!flair':
					if target_username in parent_sub.whitelist or username in parent_sub.mods:
						new_flair = message.body[7:]
						parent_sub.flairUser(user, new_flair)
						message.reply('Your flair has been set! It should now read:\n\n' + new_flair)
						message.mark_read()
						print ('Message resolved successfully')
					else:
						message.reply('You are not on the list of approved users for custom flair. If you feel that this is a mistake, please contact /u/shimmyjimmy97 or message the moderators.')
						message.mark_read()
						print ('Message resolved without action: User not approved for custom flair')
						continue
					
				
		
def checkThreadLock(parent_sub, link_flair):
	for lock in parent_sub.threadlock_config:
		if lock.startswith('threadlock') and link_flair == parent_sub.threadlock_config[lock]['flair_ID']:
			return lock
	return None
						
def getTargetSubs(parent_sub, target_subs):
	# Makes a list of subs to total data from
	sub_list = []
	if target_subs == 'A_SUBS':
		for sub in parent_sub.A_subs:
			sub_list.append(parent_sub.A_subs[sub])
	elif target_subs == 'B_SUBS':
		for sub in parent_sub.B_subs:
			sub_list.append(parent_sub.B_subs[sub])
	elif target_subs == 'ALL_SUBS':
		for sub in parent_sub.all_subs:
			sub_list.append(parent_sub.all_subs[sub])
	else:
		for abbrev in target_subs:
			if abbrev != None:
				sub_list.append(abbrev)
	return sub_list
	
def checkComparison(comparison, total_value, value):
	if comparison == 'LESS_THAN':
		if total_value < value:
			return True
		return False
	elif comparison == 'GREATER_THAN':
		if total_value > value:
			return True
		return False
	elif comparison == 'EQUAL_TO':
		if total_value == value:
			return True
		return False
	elif comparison == 'NOT_EQUAL_TO':
		if total_value != value:
			return True
		return False
	elif comparison == 'GREATER_THAN_EQUAL_TO':
		if total_value >= value:
			return True
		return False
	elif comparison == 'LESS_THAN_EQUAL_TO':
		if total_value <= value:
			return True
		return False
	else:
		return False
		
def getLeastCommon(array, to_find=None):
    counter = collections.Counter(array)
    if to_find is None:
        return sorted(counter.items(), key=itemgetter(1), reverse=False)
    return heapq.nsmallest(to_find, counter.items(), key=itemgetter(1))
		
def handelThreadLock(parent_sub, lock_status, user_info):
	lock_type = parent_sub.threadlock_config[lock_status]
	metric = lock_type['metric']
	target_subs = lock_type['target_subs']
	comparison = lock_type['comparison']
	value = lock_type['value']
	
	user_data = user_info.info_dict[metric]
	sub_list = getTargetSubs(parent_sub, target_subs)
	total_value = 0
	
	if 'total' in metric:
		total_value = user_data
	else:
		for abbrev in sub_list:
			total_value += user_data[abbrev]
			
	return checkComparison(comparison, total_value, value)
	
				
def getSubTag(parent_sub, user_info, config):
	metric = config['metric']
	target_subs = config['target_subs']
	sort = config['sort']
	tag_cap = config['tag_cap']
	comparison = config['comparison']
	value = config['value']
	
	# Makes a list of subs to total data from
	sub_list = getTargetSubs(parent_sub, target_subs)
	user_data = user_info.info_dict[metric]
	hold_subs = []
	
	if sort == 'MOST_COMMON':
		tag_count = 0
		for sub in user_data.most_common(5):
			if tag_count >= tag_cap:
				break
			abbrev = sub[0]
			data = sub[1]
			if abbrev in sub_list:
				if checkComparison(comparison, data, value):
					hold_subs.append(abbrev)
					tag_count += 1
			else:
				print('Sub not in sub list')
		return hold_subs
	if sort == 'LEAST_COMMON':
		tag_count = 0
		sorted_data = user_data.most_common()[:-tag_cap-1:-1]
		for sub in sorted_data:
			if tag_count >= tag_cap:
				break
			abbrev = sub[0]
			data = sub[1]
			if abbrev in sub_list:
				if checkComparison(comparison, data, value):
					print ('Sub accepted')
					hold_subs.append(sub[0])
					tag_count += 1
			else:
				print('Sub not in list')
		return hold_subs
				
				
						
def checkInfoTag(parent_sub, user_info, config):
	metric = config['metric']
	if metric == 'ELSE':
		return True
	target_subs = config['target_subs']
	comparison = config['comparison']
	value = config['value']
	
	# Makes a list of subs to total data from
	sub_list = getTargetSubs(parent_sub, target_subs)
	
	user_data = user_info.info_dict[metric]
	total_value = 0
	if 'total' in metric:
		total_value = user_data
	else:
		for abbrev in sub_list:
			total_value += user_data[abbrev]
		
	return checkComparison(comparison, total_value, value)
		
def countWords(text):
	word_count = 0
	sentences = sent_tokenize(text)
	
	for sentence in sentences:
		words = sentence.split(' ')
		for word in words:
			if word.isalpha():
				word_count += 1
				
	return word_count
	
command = sys.argv[1]

if command == 'auto':
	while True:
		sub_list = setSubs()
		for sub in sub_list:
			print('Scraping subreddit: ' + sub.sub_name)
			readPMs(sub)
			scrapeSub(sub, 15, 10)
			print('Finished subreddit: ' + sub.sub_name)