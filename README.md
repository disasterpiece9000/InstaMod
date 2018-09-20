# InstaMod
## An Automoderator-like bot which allows moderators to create a custom rule set based on a user's account history

### InstaMod is capable of automatically assigning users' flair, advaned thread locking, subreddit-wide filtering, creating a subreddit progression system, and more. It can work in conjunction with AutoMod via user flair text, or outright replace it. Below I will describe the different rule types and give an example of how some of them work.

-----
### Automatic User Flair:
Features, such as the subreddit progression system, can be displayed in a user's flair and be continuously updated. These flairs consist of a serries of tags that moderators can design rules for. Everything, from the rule to the flair text, is able to be customized from the provided configuration file. Each rule can use one data point from this list of possible user information:
* Total comment karma/total post karma/total karma
* Comment/Post karma borken down by subreddit
* Positive/Negative posts/comments broken down by subreddit
* Comment count based on a custom comment filter

### Subreddit Tags:
Moderators can provide lists of subreddits which the bot will collect information on. This information can be used to create tags for users' flair. These rules can be set to display a users top 3 most used communities from a list of related subreddits. It could also be designed to show all the subreddits where a user has been consistently downvoted. Here are some of this tag's unique characteristics:
* Abbreviations for subreddit names
* Grouping subreddits into groups
* Sorting results of each rule from high to low, or low to high

### Subreddit Progression:
As a user participates more and more in the community, their flair can change to represent their involvement. Certain tags, or levels of user participation, can grant the user access special priveledges. Currently this includes the ability to assign themself custom flair and the ability to append their flair with a designated list of :images:. For instance, you could give every user with less than 25 positive comments in your subreddit with a tag that says "New Here". While every user with over 100 positive comments gets to overwrite the flair.

### Etc Tags:
In case that wasn't enough, I have an Ace up my sleeve. Tags in this section allow you to replace the configuration file's settings and inject code directly into the program. This allows for the highest level of customization, but also requires knowledge of Python and a somewhat good understanding of the documentation.

### Advanced Thread/Sub Locking:
Traditional thread locking is all-or-nothing and AutoModerator can only filter users' comments based on flair text and account age. With InstaMod, a post's comment section can be filtered through a rule. If a user doesn't meet the requirements, then their comment can either be removed or marked spam. There is also a way to automatically notify the user of their comment's deletion. Moderators simply have to assign a post a specific flair for it to be locked. This type of rule can also be applied to the subreddit as a whole, and is activated/deactivated via PM.
