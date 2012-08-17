This is code developed by my two classmates Ameya Zambre, Neeraj Joshi and me. 
It consists of C# code to create a window that is able to connect to an already running instance of Skype and record the conversations.
Please create a folder called SkypeConversations inside your My Music which is the default for the software.
Copy the wavread2.py and final_combine.py to this folder.
Now on a record, two wav files get created, one for each side of the conversation.
wavread2.py is run to read this wav file and break it by silence periods. These parts are now transcribed using Google's API to retrieve text.
final_combine.py is next run to combine these two conversation text files with username of the person involved in that dialogue

The final output file will look like:
User1: Dialogue1byUser1
User2: Dialogue1byUser2
User1: Dialogue2byUser1
User2: Dialogue2byUser2
...
