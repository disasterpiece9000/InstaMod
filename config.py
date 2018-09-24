
SUB_CONFIG = {
	'name' : 'CryptoMarkets',
	'abbrev' : 'CM',
	'mods' : ('_CapR_', 'turtleflax', 'PrinceKael', 'Christi123321', 'publicmodlogs', 'AutoModerator', 'CryptoMarketsMod', 'davidvanbeveren', 'trailblazerwriting', 'golden-china', 'shimmyjimmy97', 'seristras', 'IronProdigyOfficial', 'Ginstranger', 'broccolibadass', 'Turtlecrapus', 'InstaMod'),
	'thread_lock' : True,
	'sub_lock' : False,
	'sub_progression' : True,
	'etc_tags' : False,
	'sub_tags' : True,
	'ratelimit' : False,
	'tag_expiration' : 7,
	'accnt_age' : 6,
	'update_interval' : 'INSTANT',
	'approved_icons' : ()
}

QC_CONFIG = {
	# Comments with values >= both of these numbers count as 1 positive QC
	'pos_karma' : 3,
	'pos_words' : None,
	# Comments with values <= both of these numbers count as 1 negative QC
	'neg_karma' : -1,
	'neg_words' : None
	# Currently only word options have the ability to be toggled off with a None value
}

PROGRESS_CONFIG = {
	
	'tier1' : {'metric' : 'positive comments', 
				'target_subs' : ('A_SUBS'), 
				'comparison' : 'LESS_THAN_EQUAL_TO', 
				'value' : 20, 
				'flair_text' : 'New to Crypto', 
				'flair_css' : None, 
				'permissions' : None},
				
	'tier2' : {'metric' : 'positive comments', 
				'target_subs' : ('A_SUBS'), 
				'comparison' : 'LESS_THAN_EQUAL_TO', 
				'value' : 50, 
				'flair_text' : 'Crypto Nerd', 
				'flair_css' : None, 
				'permissions' : None},
				
	'tier3' : {'metric' : 'positive comments', 
				'target_subs' : ('A_SUBS'), 
				'comparison' : 'LESS_THAN_EQUAL_TO', 
				'value' : 100, 
				'flair_text' : 'Crypto Expert', 
				'flair_css' : None, 
				'permissions' : None},
				
	'tier4' : {'metric' : 'ELSE', 
				'target_subs' : (None), 
				'comparison' : None, 
				'value' : None, 
				'flair_text' : 'Crypto God', 
				'flair_css' : None, 
				'permissions' : None}
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
	'subtag1' : {'metric' : 'net QC', 
				'target_subs' : ('A_SUBS'), 
				'sort' : 'MOST_COMMON', 
				'tag_cap' : 3, 
				'comparison' : 'GREATER_THAN_EQUAL_TO', 
				'value' : 15, 
				'pre_text' : 'r/', 
				'post_text' : ''},
				
	'subtag2' : {'metric' : 'net QC', 
				'target_subs' : ('A_SUBS'), 
				'sort' : 'LEAST_COMMON', 
				'tag_cap' : 3, 
				'comparison' : 'LESS_THAN_EQUAL_TO', 
				'value' : -10, 
				'pre_text' : 'Trolls r/', 
				'post_text' : ''}
}

RATELIMIT_CONFIG = {
	'COMMENTS' : {'metric' : 'net QC',
					'target_subs' : ('CM'),
					'comparison' : 'LESS_THAN_EQUAL_TO',
					'value' : 10,
					'max' : 5,
					'interval' : 24},
	
	'SUBMISSIONS' : {'metric' : 'net QC',
					'target_subs' : ('CM'),
					'comparison' : 'LESS_THAN_EQUAL_TO',
					'value' : 10,
					'max' : 1,
					'interval' : 24},
					
	'comment_remove_message' : ('Automatic comment removal notice', 'Your account has exceeded the allowed number of comments in this subreddit. If you have any questions, comments, orl concerns, please message the moderators. This is an automated message.')
}					

# Advanced Thread Locking
# Unique characteristics:
	# Looks for posts that have a flair matching with a rule's flair_ID, and applies the rule to all comments under the post
	# Each rule has a corresponding action, which determines how commentors that violate the rule are dealth with
		# REMOVE - remove the comment and PM the user with remove_message
		# SPAM - mark the comment as spam and do not notify the user
THREADLOCK_CONFIG = {
	'threadlock1' : {'metric' : 'positive comments', 
					'target_subs' : ('CM'), 
					'comparison' : 'LESS_THAN_EQUAL_TO', 
					'value' : 20, 
					'flair_ID' : 'lvl 1 Lock', 
					'action' : 'REMOVE'},
					
	'threadlock2' : {'metric' : 'positive comments', 
					'target_subs' : ('CM'), 
					'comparison' : 'LESS_THAN_EQUAL_TO', 
					'value' : 50, 
					'flair_ID' : 'lvl 2 Lock', 
					'action' : 'REMOVE'},
					
	'threadlock3' : {'metric' : 'positive comments', 
					'target_subs' : ('CM'), 
					'comparison' : 'LESS_THAN_EQUAL_TO', 
					'value' : 100, 
					'flair_ID' : 'lvl 3 Lock', 
					'action' : 'REMOVE'},
	
	'remove_message' : ('Automatic comment removal notice', 'Your account is not approved to post in this locked thread. If you have any questions, comments, or concerns, please message the moderators. This is an automated message.')
}

# Subreddit Locking
# Unique characteristics:
	# This set of rules are applied to all comments on the subreddit. A SubLock can be activated and deactivated by PMing the bot
SUBLOCK_CONFIG = {
	'sublock1' : {'metric' : 'parent_QC', 
					'comparison' : 'LESS_THAN_EQUAL_TO', 
					'value' : 20, 
					'lock_ID' : 'SUBLOCK 1', 
					'action' : 'SPAM'},
	
	'remove_message' : None
}

# List of subreddits with a corresponding abbreviation. Subreddits with the same abbreviation will have their data points combined/totaled
A_SUBS = {
	'CRYPTOCURRENCY' : 'CC',
	'CRYPTOMARKETS' : 'CM',
	'CRYPTOTECHNOLOGY' : 'CT',
	'BLOCKCHAIN' : 'BC',
	'ALTCOIN' : 'ALT',
	'BITCOIN' : 'BTC',
	'BITCOINMARKETS' : 'BTC',
	'LITECOIN' : 'LTC',
	'LITECOINMARKETS' : 'LTC',
	'BITCOINCASH' : 'BCH',
	'BTC' : 'BTC',
	'ETHEREUM' : 'ETH',
	'ETHTRADER' : 'ETH',
	'RIPPLE' : 'Ripple',
	'STELLAR' : 'XLM',
	'VECHAIN' : 'VEN',
	'VERTCOIN' : 'VTC',
	'VERTCOINTRADER' : 'VTC',
	'DASHPAY' : 'Dashpay',
	'MONERO' : 'XMR',
	'XRMTRADER' : 'XRM',
	'NANOCURRENCY' : 'NANO',
	'WALTONCHAIN' : 'WTC',
	'IOTA' : 'MIOTA',
	'IOTAMARKETS' : 'MIOTA',
	'LISK' : 'LSK',
	'DOGECOIN' : 'DOGE',
	'DOGEMARKET' : 'DOGE',
	'NEO' : 'NEO',
	'NEOTRADER' : 'NEO',
	'CARDANO' : 'ADA',
	'VERGECURRENCY' : 'XVG',
	'ELECMRONEUM' : 'ETN',
	'DIGIBYTE' : 'DGB',
	'ETHEREUMCLASSIC' : 'ETC',
	'OMISE_GO' : 'OMG',
	'NEM' : 'XEM',
	'MYRIADCOIN' : 'XMY',
	'NAVCOIN' : 'NAV',
	'NXT' : 'NXT',
	'POETPROJECM' : 'poetproject',
	'ZEC' : 'ZEC',
	'GOLEMPROJECM' : 'GNT',
	'FACMOM' : 'FCM',
	'QTUM' : 'QTUM',
	'AUGUR' : 'AU',
	'CHAINLINK' : 'LINK',
	'LINKTRADER' : 'LINK',
	'XRP' : 'XRP',
	'TRONIX' : 'Tronix',
	'EOS' : 'EOS',
	'0XPROJECM' : 'ZRX',
	'ZRXTRADER' : 'ZRX',
	'KYBERNETWORK' : 'KNC',
	'ZILLIQA' : 'ZIL',
	'STRATISPLATFORM' : 'STRAT',
	'WAVESPLATFORM' : 'WAVES',
	'WAVESTRADER' : 'WAVES',
	'ARDOR' : 'ARDR',
	'SYSCOIN' : 'SYS',
	'PARTICL' : 'PART',
	'BATPROJECM' : 'BATProject',
	'ICON' : 'ICX',
	'HELLOICON' : 'ICX',
	'GARLICOIN' : 'GRLC',
	'BANCOR' : 'BNT',
	'PIVX' : 'PIVX',
	'WANCHAIN' : 'WAN',
	'KOMODOPLATFORM' : 'KMD',
	'ENIGMAPROJECM' : 'ENG',
	'ETHOS_IO' : 'ETHOS',
	'DECENTRALAND' : 'MANA',
	'NEBULAS' : 'NAS',
	'ARKECOSYSTEM' : 'ARK',
	'FUNFAIRTECH' : 'FUN',
	'STATUSIM' : 'SNT',
	'DECRED' : 'DCR',
	'DECENTPLATFORM' : 'DCM',
	'ONTOLOGY' : 'ONT',
	'AETERNITY' : 'AE',
	'SIACOIN' : 'SC',
	'SIATRADER' : 'SC',
	'STORJ' : 'STORJ',
	'SAFENETWORK' : 'SafeNetwork',
	'PEERCOIN' : 'PPC',
	'NAMECOIN' : 'NMC',
	'STEEM' : 'STEEM',
	'REQUESTNETWORK' : 'REQ',
	'OYSTER' : 'PRL',
	'KINFOUNDATION' : 'KIN',
	'ICONOMI' : 'ICN',
	'GENESISVISION' : 'GVT',
	'BEST_OF_CRYPTO' : 'BestOf',
	'BITCOINMINING' : 'BitcoinMining',
	'CRYPTORECRUITING' : 'CryptoRecruting',
	'DOITFORTHECOIN' : 'DoItForTheCoin',
	'JOBS4CRYPTO' : 'Jobs4Crypto',
	'JOBS4BITCOIN' : 'Jobs4Bitcoin',
	'LITECOINMINING' : 'LTC',
	'OPENBAZAAR' : 'OpenBazzar',
	'GPUMINING' : 'GPUMining',
	'BINANCEEXCHANGE' : 'BNB',
	'BINANCE' : 'BNB',
	'ICOCRYPTO' : 'icocrypto',
	'LEDGERWALLET' : 'LW',
	'CRYPTOTRADE' : 'CryptoTrade',
	'BITCOINBEGINNERS' : 'BTC',
	'ETHERMINING' : 'ETH',
	'MONEROMINING' : 'XRM',
	'ETHEREUMNOOBIES' : 'ETH',
	'KUCOIN' : 'Kucoin',
	'COINBASE' : 'Coinbase',
	'ETHERDELTA' : 'EtherDelta',
	'NUBITS' : 'NBT',
	'ANTSHARES' : 'NEO'
}

# Another list of subreddits
B_SUBS = {
}
	