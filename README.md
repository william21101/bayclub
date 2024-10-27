v0.1

This is a script to automatically book a court at Bay Club. If there is no open slot, the script will continue to run until a court is available.

Directions:
1. run `pip install -r requirements.txt`
2. download the compatible chromedriver for your Chrome browser and place it in the directory
3. Run the command as such `python3 ./bayclub.py –username “myuser” –password “mypassword” -d 2 --start_time "6:00pm"`

Args:
--username: username to bay club.
--password: password to bay club.
-d: Day of the week to book. 0 is Sunday and so on.
--start_time: The earliest ending time to book. "6:00pm" means book any slot ending at 6pm or later.

TODO:
fix popup survey
fix day selection not working sometimes 

# bayclub

