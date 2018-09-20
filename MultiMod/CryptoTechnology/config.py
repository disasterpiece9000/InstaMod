# Main configuration setting for turining on/off different features as well as other 'big picture' settings
SUB_CONFIG = {
	# Name of subreddit InstaMod is running in
	'name' : 'CryptoTechnology'
	# Abbreviation for use in flair
	'abbrev' : 'CT'
	'mods' : (davidvanbeveren, _CapR_, bLbGoldeN, AtHeartEngineer, TheRetroguy, turtleflax, LacticLlama, ndha1995, Neophyte-, AutoModerator, CryptoTechnologyMod, publicmodlogs, shimmyjimmy97, DrunkLegere, IronProdigyOfficial, Ginstranger, Turtlecrapus, PrinceKael)
	# Values can only be True or False
	'thread_lock' : True
	'sub_lock' : True
	'sub_progression' : True
	'etc_tags' : False
	'sub_tags' : True
	# Number of days until a user's flair is reassesed
	'tag_expiration' : 7
	# Represents number of months. If an account is younger than this, then they will get a tag for it. Change it to None to disable
	'accnt_age' : 6
	# Determines when users' flair is assigned
		# Possible options: 
			#'INSTANT' - instantly flairs users on each sweep
			# A number <= 500 - flairs users in batches once the stored list is >= this number
	'update_interval' : 500
	# List of icons users who have the permissions class "FLAIR_ICONS" are allowed to append to their automatic flair
	'approved_icons' : ()
}

# Quality comment settings - customizable data point based on a comment's karma and word length
# Created lists for # of positive QC, # of negative QC, and net QC (pos QC - neg QC)
QC_CONFIG = {
	# Comments with values >= both of these numbers count as 1 positive QC
	'pos_karma' : 3
	'pos_words' : 5
	# Comments with values <= both of these numbers count as 1 negative QC
	'neg_karma' : -1
	'neg_words' : None
	# Currently only word options have the ability to be toggled off with a None value
}


# Options for different tag rule settings. Must be written exactly as they are below, inbetween '':

	# 'metric' : total_comment_karma, total_post_karma, total_karma
						#these are across all subreddits and will ignore the 'target_sub' rule setting
				#comment_karma_counter, post_comment_counter
						#total comment/post karma by subreddit
				#pos_comment_counter, neg_comment_counter
						#the count of comments with a score < 0 or > 0 by subreddit
				#pos_post_counter, neg_post_counter
						#the count of all posts with a score < 0 or > 0 by subreddit
				#pos_QC_counter, neg_QC_counter, net_QC_counter
						#the number of QC by subreddit
	
	# 'target_subs' : GOOD_SUBS, BAD_SUBS
						#2 lists of subreddits and abbreviations that are defined below
					# ALL_SUBS
						#the combination of GOOD_SUBS and BAD_SUBS
					# A list of subreddit abbreviations that are comma seperated and contained in (). These subreddits must be present in at least one of the sub lists.
						# If multiple subreddits are given, each of their metrics will be totaled together for the comparison
					
	# 'comparison' : GREATER_THAN, LESS_THAN, EQUAL_TO, NOT_EQUAL_TO, GREATER_THAN_EQUAL_TO, LESS_THAN_EQUAL_TO
					# >				<			=			!=				>=					<=
	
	# 'value' : Any number that will be used with the metric and the comparison to determine if a user meets the rule
				# Ex: if METRIC is COMPARISON the VALUE then they get the tag
	
	# 'flair_text' : Text that will be appended to a user's flair if they meet the rule's requirements
	
	# 'flair_css' : CSS class that will be applied to a user's flair if they meet the rule's requirements
	
	# 'permissions' : FLAIR_ICONS - the user can append their flair with a set list of flair :images:
					# CUSTOM_FLAIR - the user will no longer be flaired by the bot and can assign custom flair through PMs


# Subreddit Progression Tags
# Unique characteristics:
	# User's can only be assigned 1 of these flairs. They are assessed from top -> bottom
	# User's can be granted one set of permissions based on their tag
PROGRESS_CONFIG = {
	
	'tier1' : {'metric' : 'net_QC', 'target_subs' : ('CT'), 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : 20, 'flair_text' : 'New Arrival', 'flair_css' : None, 'permissions' : None}
	'tier2' : {'metric' : 'net_QC', 'target_subs' : ('CT'), 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : 50, 'flair_text' : 'Crypto Nerd', 'flair_css' : None, 'permissions' : None}
	'tier3' : {'metric' : 'net_QC', 'target_subs' : ('CT'), 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : 100, 'flair_text' : 'Crypto Expert', 'flair_css' : None, 'permissions' : 'FLAIR_ICONS'}
	'tier4' : {'metric' : 'ELSE', 'comparison' : None, 'value' : None, 'flair_text' : 'Crypto God', 'flair_css' : None, 'permissions' : 'CUSTOM_FLAIR'}
}

# Super Custom Tags
# Unique characteristics:
	# Instead of a serries of settings, an entire block of code is used to define a rule. This allows for the highest level of customization, since the code is
		# executes, as written, inside the program. This feature is not yet implemented yet
ETCTAG_CONFIG = {
}

# Subreddit Activity Tags
# Unique characteristics:
	# Custom flair text is replaced with 'pre_text' and 'post_text' which go before and after each subreddits abbreviations. To disable these, use an empty string '' and not None
	# Results can be soted in order from highest to lowest (MOST_COMMON) or lowest to highest (LEAST_COMMON)
	# The number of subreddits listed can be capped using the tag_cap setting
SUBTAG_CONFIG = {
	'subtag1' : {'metric' : 'net_QC', 'target_subs' : ('GOOD_SUBS'), 'sort' : 'MOST_COMMON', 'tag_cap' : 3, 'comparison' : 'GREATER_THAN_EQUAL_TO', 'value' : 10, 'pre_text' : 'r/', 'post_text' : ''}
	'subtag2' : {'metric' : 'net_QC', 'target_subs' : ('GOOD_SUBS'), 'sort' : 'LEAST_COMMON', 'tag_cap' : 3, 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : -15, 'pre_text' : 'Trolls r/', 'post_text' : ''}
}

# Advanced Thread Locking
# Unique characteristics:
	# Looks for posts that have a flair matching with a rule's flair_ID, and applies the rule to all comments under the post
	# Each rule has a corresponding action, which determines how commentors that violate the rule are dealth with
		# REMOVE - remove the comment and PM the user with remove_message
		# SPAM - mark the comment as spam and do not notify the user
THREADLOCK_CONFIG = {
	'threadlock1' : {'metric' : 'net_QC', 'target_subs' : ('CT'), 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : 20, 'flair_ID' : 'lvl 1 Lock', 'action' : 'REMOVE'}
	'threadlock2' : {'metric' : 'net_QC', 'target_subs' : ('CT'), 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : 50, 'flair_ID' : 'lvl 2 Lock', 'action' : 'REMOVE'}
	'threadlock3' : {'metric' : 'net_QC', 'target_subs' : ('CT'), 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : 100, 'flair_ID' : 'lvl 3 Lock', 'action' : 'REMOVE'}
	
	'remove_message' : ('Automatic comment removal notice', 'Your account is not approved to post in this locked thread. If you have any questions, comments, or concerns, please message the moderators. This is an automated message.')
}

# Subreddit Locking
# Unique characteristics:
	# This set of rules are applied to all comments on the subreddit. A SubLock can be activated and deactivated by PMing the bot
SUBLOCK_CONFIG = {
	'sublock1' : {'metric' : 'parent_QC', 'comparison' : 'LESS_THAN_EQUAL_TO', 'value' : 20, 'lock_ID' : 'SUBLOCK 1', 'action' : 'SPAM'}
	
	'remove_message' : None
}

# List of subreddits with a corresponding abbreviation. Subreddits with the same abbreviation will have their data points combined/totaled
GOOD_SUBS = {
	'CRYPTOCURRENCY' : 'CC'
	'CRYPTOMARKETS' : 'CM'
	'CRYPTOTECHNOLOGY' : 'CT'
	'BLOCKCHAIN' : 'BC'
	'ALTCOIN' : 'ALT'
	'BITCOIN' : 'BTC'
	'BITCOINMARKETS' : 'BTC'
	'LITECOIN' : 'LTC'
	'LITECOINMARKETS' : 'LTC'
	'BITCOINCASH' : 'BCH'
	'BTC' : 'BTC'
	'ETHEREUM' : 'ETH'
	'ETHTRADER' : 'ETH'
	'RIPPLE' : 'Ripple'
	'STELLAR' : 'XLM'
	'VECHAIN' : 'VEN'
	'VERTCOIN' : 'VTC'
	'VERTCOINTRADER' : 'VTC'
	'DASHPAY' : 'Dashpay'
	'MONERO' : 'XMR'
	'XRMTRADER' : 'XRM'
	'NANOCURRENCY' : 'NANO'
	'WALTONCHAIN' : 'WTC'
	'IOTA' : 'MIOTA'
	'IOTAMARKETS' : 'MIOTA'
	'LISK' : 'LSK'
	'DOGECOIN' : 'DOGE'
	'DOGEMARKET' : 'DOGE'
	'NEO' : 'NEO'
	'NEOTRADER' : 'NEO'
	'CARDANO' : 'ADA'
	'VERGECURRENCY' : 'XVG'
	'ELECTRONEUM' : 'ETN'
	'DIGIBYTE' : 'DGB'
	'ETHEREUMCLASSIC' : 'ETC'
	'OMISE_GO' : 'OMG'
	'NEM' : 'XEM'
	'MYRIADCOIN' : 'XMY'
	'NAVCOIN' : 'NAV'
	'NXT' : 'NXT'
	'POETPROJECT' : 'poetproject'
	'ZEC' : 'ZEC'
	'GOLEMPROJECT' : 'GNT'
	'FACTOM' : 'FCT'
	'QTUM' : 'QTUM'
	'AUGUR' : 'AU'
	'CHAINLINK' : 'LINK'
	'LINKTRADER' : 'LINK'
	'XRP' : 'XRP'
	'TRONIX' : 'Tronix'
	'EOS' : 'EOS'
	'0XPROJECT' : 'ZRX'
	'ZRXTRADER' : 'ZRX'
	'KYBERNETWORK' : 'KNC'
	'ZILLIQA' : 'ZIL'
	'STRATISPLATFORM' : 'STRAT'
	'WAVESPLATFORM' : 'WAVES'
	'WAVESTRADER' : 'WAVES'
	'ARDOR' : 'ARDR'
	'SYSCOIN' : 'SYS'
	'PARTICL' : 'PART'
	'BATPROJECT' : 'BATProject'
	'ICON' : 'ICX'
	'HELLOICON' : 'ICX'
	'GARLICOIN' : 'GRLC'
	'BANCOR' : 'BNT'
	'PIVX' : 'PIVX'
	'WANCHAIN' : 'WAN'
	'KOMODOPLATFORM' : 'KMD'
	'ENIGMAPROJECT' : 'ENG'
	'ETHOS_IO' : 'ETHOS'
	'DECENTRALAND' : 'MANA'
	'NEBULAS' : 'NAS'
	'ARKECOSYSTEM' : 'ARK'
	'FUNFAIRTECH' : 'FUN'
	'STATUSIM' : 'SNT'
	'DECRED' : 'DCR'
	'DECENTPLATFORM' : 'DCT'
	'ONTOLOGY' : 'ONT'
	'AETERNITY' : 'AE'
	'SIACOIN' : 'SC'
	'SIATRADER' : 'SC'
	'STORJ' : 'STORJ'
	'SAFENETWORK' : 'SafeNetwork'
	'PEERCOIN' : 'PPC'
	'NAMECOIN' : 'NMC'
	'STEEM' : 'STEEM'
	'REQUESTNETWORK' : 'REQ'
	'OYSTER' : 'PRL'
	'KINFOUNDATION' : 'KIN'
	'ICONOMI' : 'ICN'
	'GENESISVISION' : 'GVT'
	'BEST_OF_CRYPTO' : 'BestOf'
	'BITCOINMINING' : 'BitcoinMining'
	'CRYPTORECRUITING' : 'CryptoRecruting'
	'DOITFORTHECOIN' : 'DoItForTheCoin'
	'JOBS4CRYPTO' : 'Jobs4Crypto'
	'JOBS4BITCOIN' : 'Jobs4Bitcoin'
	'LITECOINMINING' : 'LTC'
	'OPENBAZAAR' : 'OpenBazzar'
	'GPUMINING' : 'GPUMining'
	'BINANCEEXCHANGE' : 'BNB'
	'BINANCE' : 'BNB'
	'ICOCRYPTO' : 'icocrypto'
	'LEDGERWALLET' : 'LW'
	'CRYPTOTRADE' : 'CryptoTrade'
	'BITCOINBEGINNERS' : 'BTC'
	'ETHERMINING' : 'ETH'
	'MONEROMINING' : 'XRM'
	'ETHEREUMNOOBIES' : 'ETH'
	'KUCOIN' : 'Kucoin'
	'COINBASE' : 'Coinbase'
	'ETHERDELTA' : 'EtherDelta'
	'NUBITS' : 'NBT'
	'ANTSHARES' : 'NEO'
}

# Another list of subreddits
BAD_SUBS = {
}
	