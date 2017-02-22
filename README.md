# Python_Reddit_Collector  
A set of Python scripts that poll Reddit (Poller.py), sift through data (Sifter.py), and format it into a WordDoc (Creator.py). Interaction between user and script is typically done through the custom shell (Definer.py).  

# Description
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Used in my Undergraduate Research group as well as a data collection unit in a Senior group's AI project, this somewhat small independent programming project focuses on collecting popular Reddit posts. Through Definer.py, users can specify the keywords to search for and categorize those keywords into topics. Currently, it is restricted to the /r/WorldNews subreddit for post collection. However, there are plans to build the option to customize what subreddits are searched through into the Definery.py shell. To ensure no data is lost, copies of the .txt files are archived in a separate folder.  

**These scripts function in Windows**. It's been tested in Linux, but has failed (mostly due to the difference in "/" vs "\" within filepaths).  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Furthermore, while the script *should* prompt users to install the necessary tools to run these scripts, in case it doesn't, the required packages are: PRAW (Python Reddit API Wrapper) for Poller.py and python-docx for Creator.py.  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Small disclaimer, the initial purpose of this was to simply learn about Python. From that it grew into what it is today, so it is very possible that there are many inefficiencies/non-standard practices.

# What does Poller.py do?  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Poller.py is the script that polls Reddit.com using the PRAW (Public Reddit API Wrapper) package. Poller currently only polls the "/r/worldnews" subreddit. It categorizes the subreddit into the "top" posts of the "day" and takes the top 10 of those posts. Furthermore, it searches the subreddit for any search terms defined by the user (explained in more detail in **Definer.py**). Poller is meant to be run two times a day, like at midnight and noon. This is to ensure no popular posts are overlooked. Because of this, however, duplicate posts are bound to appear. These duplicate posts are handled by **Sifter.py**.   

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Since (for my initial purposes, at least) a list of events is supposed to be generated weekly, Poller creates two separate .txt files, one for "Global Events" (these are the top 10 posts of the day on the subreddit) and one for "Topic Specific Events" (these are the posts that are searched for, as defined by the user). The .txt files are named as such "Global Events - MM.DD.YY to MM.DD.YYRAW.txt", so for example the list that was sent out two weeks ago had a file name of "Global Events - 12.29.16 to 01.04.17RAW.txt".  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is where the base.txt file comes in. Poller references the base.txt file when determining both the interval of tracking and the search terms to search. For example, a date of "01/12/17" means that Poller will put posts from 01.12.17 to 01.18.17 into their own file. Furthermore, a search term list of "{'School Shooting': ['Shooting'], 'Saudi Arabia': ['Saudi', 'Arabia']}" will search for the terms "Shooting" and put those search results under the 'school shooting' category and will search for the terms "Saudi" and "Arabia" and put those search results under the 'saudi arabia' category.  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Poller will automatically create a base.txt file with the current date and no search terms if one does not exist already. Modification of this file should typically not be done by hand, but through **Definer.py**

# What does Sifter.py do?  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sifter.py is the script that removes duplicate posts from the RAW.txt files. It moves all unique posts from the RAW.txt to just a .txt file, then archives the RAW.txt file into a "PAST_POLLS" directory. If this directory does not already exist, Sifter will create it. For example, the unique contents of the files "Global Events - 12.29.16 to 01.04.17RAW.txt" and "Topic Sepcific Events - 12.29.16 to 01.04.17RAW.txt" would be moved to "Global Events - 12.29.16 to 01.04.17.txt" and "Topic Specific Events - 12.29.16 to 01.04.17.txt" respectively, while the RAW.txt files would be moved into the "PAST_POLLS" directory.  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sifter is meant to be run the day after the last Poller day. For example, for the file "Global Events - 12.29.16 to 01.04.17RAW.tx", Sifter should be run on 01.05.17, as this would be the start day of the next Poller cycle.  

# What does Definer.py do?  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Definer.py is what is supposed to modify the base.txt file. When ran, Definer operates much like Git Bash, in the sense that you type in commands and Definer will execute the commands. Much of the info on the commands, their functionality, and their syntax can be displayed through Definer's "help" command, so I won't explain that. However, one thing to note is that Definer does not auto-save changes.  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Much like you have to commit and push changes in Git, you have to store and update the changes you made through Definer. You can think of the "store" command much like Git's "commit" (it stages changes made thus far) and the "update" command much like Git's "push" command (it pushes the stored changes onto the base.txt file). A short hand command for doing both of these functions this is "save". 


# What does Creator.py do?  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Creator.py is not *fully* complete. Creator moves the .txt files into a more aesthetically pleasing Microsoft Word document. This is mostly to make the contents easier to read. To my knowledgeable, the python-docx package I utilize does not have the capabilities to create links in word docs, yet. So when transferring contents from .txt to  .docx, the links will appear in plain text.  

# Use  
Want to use/build upon/modify? Feel free to. This project it licensed under the MIT opensource license, so go at it. While not necessary, notifying me that you'll be using it in something would be cool. Mostly just so I can think to myself 'Wow cool! Someone is actually using this thing I made!'.
