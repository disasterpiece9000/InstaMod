# InstaMod
## An Automoderator-like bot which allows moderators to create a custom rule set based on a user's account history

### InstaMod is capable of automatically assigning users' flair, advanced thread locking, subreddit-wide filtering, creating a subreddit progression system, and more. It can work in conjunction with AutoMod via user flair text, or outright replace it. Below I will describe the different rule types and give an example of how some of them work.

-----
### Automatic User Flair:
Features, such as the subreddit progression system, can be displayed in a user's flair and keep it continuously updated. These flairs consist of a serries of tags that moderators can design rules for. Everything, from the rule to the flair text, is able to be customized from the provided configuration file. Each rule can use one data point from this list of possible user information:
* Total comment karma/total post karma/total karma
* Comment/Post karma borken down by subreddit
* Positive/Negative posts/comments broken down by subreddit
* Comment count based on a custom comment filter

### Subreddit Tags:
Moderators can provide lists of subreddits which the bot will collect information on. This information can be used to create tags for users' flair. The sub tag's rules can be set to display a user's top 3 most used communities from a list of related subreddits. It could also be designed to show all the subreddits where a user has been consistently downvoted. Here are some of this tag's unique characteristics:
* Abbreviations for subreddit names
* Grouping subreddits into groups
* Sorting results of each rule from high to low, or low to high

### Subreddit Progression:
As a user participates more and more in the community, their flair can change to represent their involvement. Certain tags, or levels of user participation, can grant the user access to special priveledges. This includes the ability to assign themself custom flair and the ability to append their automatic flair with a designated list of :images:. For instance, you could give every user with less than 25 positive comments in your subreddit a tag that says "New Here". While every user with over 100 positive comments gets to overwrite their automatic flair.

### Etc Tags:
In case that wasn't enough, I have an Ace up my sleeve. Tags in this section allow you to replace the configuration file's rule settings and inject code directly into the program. This allows for the highest level of customization, but also requires knowledge of Python and a somewhat good understanding of the documentation. You are essentially writing the block of code that assigns the tag manually, instead of using the configuration file to define the tag.

### Advanced Thread/Sub Locking:
Traditional thread locking is all-or-nothing and AutoModerator can only filter users' comments based on flair text and account age. With InstaMod, a post's comment section can be filtered through a rule. If a user doesn't meet the requirements, then their comment can either be removed or marked spam. There is also a way to automatically notify the user of their comment's deletion. Moderators simply have to assign a post a specific flair for it to be locked. This type of rule can also be applied to the subreddit as a whole, and is activated/deactivated via PM.

-----
# Configuration File Documentation
Here I will describe each element of the provided config file, list the possible options for each setting, and provide some example cases

### SUB_CONFIG: Primary settings for toggling on/off features, as well as other meta options
* **name** - Name of the subreddit InstaMod is running on
* **abbrev** - Abbreviation of the subreddit
* **mods** - Comma seperated list () of usernames. Each username shold be encased in ''
* **thread_lock** to **ub_tags** - Accepts True/False values to turn on/off the feature
* **tag_expiration** - Number of days until a user's flair is reassessed 
* **accnt_age** - Represents number of months. If an account is younger than this, then they will get a tag for it. Change it to None to disable
* **update_interval** - set to 'INSTANT' for users to be analyzed as they are seen, or set it to any number <= 500 to flair users in batches. Once the stored lis of users is >= this number, they will be flaired
* **approved_icons** - a comma seperated list () of flair :images: that users with 'FLAIR_ICONS' permission will be able to use.

### QC_CONFIG: Filtered comment counter
* **pos_karma** - comments must have a score thats >= this number
* **pos_words** - comments must contain an amount of words >= this number
* **pos_karma** and **pos_words** - Comments with values >= both of these numbers count as 1 positive QC
* **neg_karma** - comments must have a score thats <= this number
* **neg_words** - comments must contain an amount of words <= this number
* **neg_karma** and **neg_words** - Comments with values <= both of these numbers count as 1 negative QC
-----
## Options for different rule settings: 
Each term must be used inbetween '' and typed the same way

### metric
* **total_comment_karma, total_post_karma, total_karma** - Self explanatory. These values are for across all subreddits and will ignore the 'target_sub' rule setting. They will not be totaled like other data points.
* **comment_karma_counter** and **post_karma_counter** - Total comment/post karma by subreddit
 **pos_comment_counter** and **neg_comment_counter** - Count of comments with a score < 0 or > 0 by subreddit
* **pos_post_counter** and **neg_post_counter** - Count of posts with a score < 0 or > 0 by subreddit
* **pos_QC_counter**, **neg_QC_counter**, **net_QC_counter** - The number of QC by subreddit. net_QC_counter consists of the negative QC subtracted from the positive QC by subreddit
