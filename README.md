# InstaMod

## **Note**: InstaMod 2.0 is the successor to this project and can be found [here](https://github.com/disasterpiece9000/InstaMod-2.0)

### InstaMod is capable of automatically assigning users' flair, advanced thread locking, subreddit-wide filtering, creating a subreddit progression system, and more. 

InstaMod is a fully customizable suite of automated moderator actions. These actions are editable through a configuration file that is stored on the subreddit's wiki page. This allows for on the fly changes by a mod team, much like AutoModerator. Unlike AutoModerator, InstaMod is capable of preforming actions based on a user's account activity. InstaMod also allows for further control via PM commands. Below I will briefly go over each of it's features.

-----
### Automatic User Flair:
Features, such as the subreddit progression system and subreddit tags, can be displayed in a user's flair and are consistently kept up to date. InstaMod continuously looks for new comments to ensure that all users have the appropriate flair. Certain users can be exempted from the automatic flair, and can be granted the ability to assign their own custom flair through a PM command.

### Quality Comments:
Quality Comments is a metric that can be used to gague user participation in specified subreddits. This is reffered to as QC for short. Moderators can specify a criteria, using a comment's score and word count, and the bot will count comments that meet the criteria. There is an option to define a "good comment" and a "bad comment". Each of those data points can be used by the bot, or they can be combined into net QC. Net QC consists of the number of good comments minus the number of bad comments. This is the most accurate way to gague user participation through InstaMod.

### Subreddit Tags:
Moderators can provide lists of subreddits which the bot will collect information on. This information can be used to create tags for users' flair. The sub tag's rules can be set to display a user's top 3 most used communities from a list of related subreddits. It could also be designed to show all the subreddits where a user has been consistently downvoted. These are just a few examples of the possibilities.

### Subreddit Progression:
As a user participates more and more in the community, their flair can change to represent their involvement. Certain tags, or levels of user participation, can grant the user access to special priveledges. This includes the ability to assign themself custom flair and the ability to append their automatic flair with a designated list of :images:

### Advanced Thread Locking:
Traditional thread locking is inherantly all-or-nothing. With InstaMod, a post's comment section can be filtered through a requirement based on the user's account activity. If a user doesn't meet the requirements, then their comment can either be removed or marked spam. There is an option to automatically notify the user of their comment's deletion. Moderators simply have to assign a post a specific flair for it to be locked.

### Subreddit Locking:
Comments across the entire subreddit can be filtered by a requirement. While this is possible through AutoModerator, InstaMod allows moderators to fine tune their requirements. Users can be filtered by karma, post count, negative comment count, etc. from specific subreddits. This is activated via a PM command.

### Custom Comment Rate-limiting:
Reddit has a built in rate-limit system to prevent spam, but with InstaMod this can be expanded and customized to ensure that new users in your subreddit cannot spam comments. Moderators can design the bot to prevent users with less than 20 positive comments from submitting more than 5 comments in a day, or it could prevent users with more negative than positive comments from commenting more than once a day. Once again, this is just a few of the endless posibilities that InstaMod is capable of implementing.

### PM Commands
Moderators and users can have even more fine tuned control over InstaMod's actions by sending it a PM command. Each PM must contain "!SubredditName" in the subject and one of these commands in the body:
* **!whitelist /u/someuser** - This command is reserved for moderators only. It exempts a user from recieving automatic flair and allows them to assign their own flair via PM commands. The user mentioned in the moderator's PM will be notified of their whitelisted status automatically.
* **!greylist /u/someuser** - This command is also reserved for moderators only. It exempts a user from automatic flair, but does not grant them custom flair permissions.
* **!flair some flair text** - This command allows whitelisted users to assign themselves custom flair. Since the automatic flair option requires a subreddit disable user assigned flair, this option restores some of that usability.
* **!wipe** - This command is for moderators only. When this command is recieved, InstaMod will purge all of its databases to allow configuration changes to be applied instantly. After this is done, all users will be reanalyzed, and their flair will be reassessed.
