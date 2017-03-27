# PRAW - https://praw.readthedocs.io/en/latest/index.html
# Script is ran at approximately 11:59 P.M. and 11:59 A.M. EST each day
# Removal of duplicates done by the Sifter.py
# Formatting into a .docx is done elsewhere

import sys
import os

file_path = os.path.dirname(os.path.realpath(__file__)) + "/" # Obtains the scripts file path

# A simple print with a system flush afterwards
def printFlush(string = ''):
	print(string)
	sys.stdout.flush()

# Ensures the PRAW package is installed
def checkImports():
	try:
		import praw
	except ImportError as e:
		# Asks user to install PRAW if they do not have it
		printFlush("The Python Reddit API Wrapper (PRAW) package is not currently installed on this machine."
				+ "\n The PRAW package is needed in order for this script to run.")
		resp = input("Would you like to install the PRAW package?\n\t[Y]es or [N]o:")
		
		# If invalid reponse is given, continuing asking until a valid response is given
		while (resp.upper() != "Y" and resp.upper() != "YES"
			and resp.upper() != "N" and resp.upper() != "NO"):
			resp = input("Invalid response.\nWould you like to install the PRAW package?\n\t[Y]es or [N]o: ")
		
		# Install PRAW with pip if the user allows it, exit the script otherwise
		if (resp.upper() == "Y" or resp.upper() == "YES"):
			printFlush("Installing PRAW...")
			import pip
			pip.main(['install', 'praw'])
			printFlush("**PRAW installed.")
		else:
			import time
			printFlush("Unable to run script without appropriate packages.\nExiting...")
			time.sleep(1)
			sys.exit(0)

def getCurDate():
	import datetime

	return datetime.datetime.strptime(datetime.date.today().strftime("%m/%d/%y"), "%m/%d/%y")

# Ensures that there are two lines in base.txt without erasing it's data
# Fills empty lines with their appropriate data
# ie. Line one should contain a "MM/DD/YY" and line two should contain a search list
def checkBaseText():
	printFlush("Searching for base.txt file...")

	cur_date = getCurDate()

	try:
		base_txt = open(file_path + "base.txt", "r")
		
		printFlush("**base.txt file found, checking contents...")
		lines = base_txt.readlines()

		if len(lines) > 0:
			first_line = lines[0]
		else:
			first_line = ""

		if len(lines) > 1:
			second_line = lines[1]
		else:
			second_line = ""

		base_txt.close()

		# If there is no data for the Date data line
		# Erases the file, re-creates it, and adds the current date to it
		if first_line.rstrip() == "":
			base_txt = open(file_path + "base.txt" , "w")
			
			printFlush("No initial date found, setting '" + cur_date.strftime('%x') + "' as initial date...")
			set_date = cur_date.strftime('%x')
			base_txt.write(set_date + "\n")
			first_line = set_date
			printFlush("**Initial date set.")
			
			base_txt.close()

		base_txt = open(file_path + "base.txt", "w")
		base_txt.write(first_line.rstrip() + "\n")
		# If there was no preset search list, add an empty one
		if second_line.rstrip() == "":
			printFlush("No search terms found. Use the Definer.py script to define search terms.")
			base_txt.write("{}\n")
		# Otherwise write the original search list into the file
		else:
			base_txt.write(second_line.rstrip() + "\n")
		base_txt.close()

	# If there is no base.txt file, create it and
	# fill it with the current date data and empty search list data
	except FileNotFoundError as e:
		printFlush("No base.txt file found, creating file...")
		base_txt = open(file_path + "base.txt", "w")
		printFlush("**base.txt file created.")

		printFlush("No initial date found, setting '" + cur_date.strftime('%x') + "' as initial date...")
		base_txt.write(cur_date.strftime('%x') + "\n")
		printFlush("**Initial date set.")

		printFlush("No search terms found. Use the Definer.py script to define search terms.")
		base_txt.write("\{\}\n")
		
		base_txt.close()
	printFlush("**base.txt file correctly configured.")

# Defines a dictionary of general search categories mapping to more specific key-words
# Not case-sensitive
def getSearchTerms():
	import ast

	base_txt = open(file_path + "base.txt", "r")
	
	terms = {}

	# The search list dictionary is on the second line of base.txt
	base_txt.readline()
	search_list = base_txt.readline().strip()

	base_txt.close()

	try:
		terms = ast.literal_eval(search_list)
	except Exception as e:
		print(e)

	return terms

def pollReddit():
	checkImports()
	import datetime
	import praw
	import time

	max_num_posts = 10 # Max amount of posts to collect per day
	search_terms = getSearchTerms()
	
	printFlush("Starting Poller.py script...")

	# Obtains a Reddit instance
	# client_id and client_secret are reddit user's application's credentials
	# user_agent is the general purpose of this script
	reddit = praw.Reddit(client_id='1sBmgGrhe_PtkA',
						 client_secret='jeII_nOtB1_xsFNCqd3H-irTc5M',
						 user_agent='/r/WorldNews url+title collector by GETAR_Events_Bot')

	# Obtains a Subreddit instance of /r/worldnews
	subreddit_worldnews = reddit.subreddit('worldnews')
	
	printFlush("Obtaining base information...")

	# Used to determine the starting point of weekly polling intervals
	# ie. If date in base.txt is 12/20/16 the intervals would start from the 20th
	base_txt = open(file_path + "base.txt", "r")
	increment_date = base_txt.readline().strip()
	base_txt.close()

	printFlush("**Base information obtained.")

	# Stores current date as MM/DD/YY
	cur_date = getCurDate()

	# Creates a start_date and end_date based off base.txt file
	start_date = datetime.datetime.strptime(increment_date, "%m/%d/%y")
	end_date = start_date + datetime.timedelta(days=6)

	# Terminal date is a day after the end date
	terminate_date = end_date + datetime.timedelta(days=1)

	printFlush("Checking date cycle...")

	# Determines if the next interval cycle is to begin
	# Overwrites base.txt with appropriate date
	if cur_date >= terminate_date:
		write_date = datetime.datetime.strftime(cur_date, "%m/%d/%y")
		start_date = cur_date

		printFlush("Creating new cycle...")

		base_txt = open(file_path + "base.txt", "w")
		base_txt.write(write_date + "\n")
		base_txt.write(str(search_terms) + "\n")
		base_txt.close()

		printFlush("**New cycle created.")

		end_date = start_date + datetime.timedelta(days=6)
	else:
		printFlush("**No new cycle needed.")


	# Creates a string representation of the dates in MM.DD.YY format
	str_start_date = str(start_date.strftime("%m.%d.%y"))
	str_end_date = str(end_date.strftime("%m.%d.%y"))

	# Creates a string from the start to the end date
	timeframe = str_start_date + " to " + str_end_date

	printFlush("Starting general searches...")

	# Creates and opens a weekly .txt file 
	weekly_title = "Global Events - " + timeframe + "RAW.txt"
	weekly_draft = open(file_path + weekly_title, "a")

	index = 1

	# Obtains a Submission instance from a specified Subreddit category
	for submission in subreddit_worldnews.top('day', limit = max_num_posts):
		weekly_draft.write(submission.id + "\n")
		weekly_draft.write(submission.title + "\n")
		weekly_draft.write(submission.url + "\n\n")
		printFlush("Post #" + str(index) + " written to file...")
		index += 1

	weekly_draft.close()

	printFlush("**General searches complete.")
	printFlush("Starting topic-specific searches...")

	index = 1
	topic_index = 1

	# Creates and opens a weekly, topic-specific .txt file
	# Topic-specific refers to the topics in the search_terms dictionary
	topic_title = "Topic Specific Events - " + timeframe + "RAW.txt"
	topic_draft = open(file_path + topic_title, "a")

	# Search /r/worldnews for articles containing a search_terms term
	# Only searches for articles created in past 24 hours
	for key in search_terms:
		topic_draft.write("Search results for \"" + key + "\" search set - " + str(cur_date) + "\n")
		for term in search_terms.get(key):
			for submission in subreddit_worldnews.search(term, 'relevance', 'cloudsearch', 'day'):
				topic_draft.write(submission.id + "\n")
				topic_draft.write(submission.title + "\n")
				topic_draft.write(submission.url + "\n\n")
				printFlush("Topic " + str(topic_index) + ", post #" + str(index) + " written to file...")
				index += 1
		topic_index += 1
		index = 1
		topic_draft.write("\n")

	topic_draft.close()
	printFlush("**Topic-specific searches complete.")

	printFlush("**Script complete.")

	time.sleep(1.5)
def main():
	try:
		checkBaseText()
		pollReddit()
	except SystemExit as e:
		printFlush("**EXITING SCRIPT**")
	except Exception as e:
		import time
		import traceback
		traceback.print_exc()
		time.sleep(3)

if __name__ == "__main__":
	main()