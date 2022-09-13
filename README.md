
## [Python](https://www.python.org/downloads/)

![Example](http://i.imgur.com/bMjO8UA.png)

## intall
windows

🔗 **pip install selenium**

🔗 **pip install wget**

## Usage
* **!ghelp** - Provides the bot's commands via Direct Message
* **!gcreate** - Interactive giveaway setup
* **!gstart \<time> [winners] [prize]** - Starts a new giveaway in the current channel. Users can react with a 🎉 to enter the giveaway. The time can be in seconds, minutes, hours, or days. Specify the time unit with an "s", "m", "h", or "d", for example `30s` or `2h`. If you include a number of winners, it must be in the form #w, for example `2w` or `5w`.
* **!greroll [messsageId]** - Re-rolls a winner. If you provided a message ID, it rerolls the giveaway at that ID. If you leave it blank, it looks in the current channel for the most recent giveaway and rerolls from that.
* **!gend [messageId]** - Ends a giveaway immediately. If you provided a message ID it will end the giveaway at that ID. If you leave it blank, it looks in the current channel for the most recent giveaway and ends that.
* **!glist** - Lists currently-running giveaways on the server.
