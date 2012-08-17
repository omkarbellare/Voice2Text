import json
import sys,os
import time

def combine():
    if len(sys.argv)>1:
        os.chdir(sys.argv[1])
    input_file = open('input_json.txt','r')
    output_file = open('output_json.txt','r')
    final_combined_output = open('speech2text.txt','w')

    final_combined_output.write("Log recorded at: "+time.asctime(time.localtime(time.time()))+"\n\n")

    timestamp_text = []

    for line in input_file.readlines():
        decoded = json.loads(line)
        user = decoded[0]['user']
        start = decoded[0]['start']
        text = decoded[0]['text']
        timestamp_text.append([start,user,text])

    for line in output_file.readlines():
        decoded = json.loads(line)
        user = decoded[0]['user']
        start = decoded[0]['start']
        text = decoded[0]['text']
        timestamp_text.append([start,user,text])

    timestamp_text.sort()

    for item in timestamp_text:
        user = item[1]
        text = item[2]
        final_combined_output.write(user+" : "+text)
        final_combined_output.write("\n")

    input_file.close()
    output_file.close()
    final_combined_output.close()

combine()
        
