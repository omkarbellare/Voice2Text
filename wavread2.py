import wave
import audioop
import math
import os
import urllib2,urllib
import json
import sys

def split(FileName,OutputFileName,rate,username):
        finalWrite = open(OutputFileName,'w')

        os.system("sox "+ FileName +" -n trim 0 1.5 noiseprof speech.noise-profile")
        os.system("sox "+ FileName + " " + FileName[:-4]+"_c.wav noisered speech.noise-profile 0.3")
        os.remove("speech.noise-profile")
                
        waveRead = wave.open(FileName[:-4]+"_c.wav",'r')
        
        readParams=  waveRead.getparams()

        channels = waveRead.getnchannels()
        sampleWidth = waveRead.getsampwidth()
        numberFrames = waveRead.getnframes()
        frameRate = waveRead.getframerate()

        chunkSize = frameRate * sampleWidth / 2
        size = sampleWidth * numberFrames
        numberOfChunks = size / chunkSize

        Sum = 0

        for i in range(numberFrames):
                frame = waveRead.readframes(1)
                
                for j in range(len(frame)):
                        byte = ord(frame[j])
                        Sum += byte*byte

        mean = Sum/size
        rms = math.sqrt(mean)

        waveRead.rewind()
        fragment = waveRead.readframes(numberFrames)
        rms2 = audioop.rms(fragment,sampleWidth)
        
        waveRead.rewind()
        startTime = 0
        endTime = 0
        t=0
        c=0
        i=0

        while True:
            frame = waveRead.readframes(chunkSize/sampleWidth)
            Sum=0
            for j in range(len(frame)):
                byte = ord(frame[j]);
                square  = byte * byte
                Sum += square

            mean = Sum / chunkSize
            chunkRMS = math.sqrt(mean)

            if chunkRMS < rms:
                c = (i+1)* (chunkSize/sampleWidth) 
                t = c/frameRate
                while chunkRMS < rms: #silence
                    frame = waveRead.readframes(chunkSize/sampleWidth)
                    Sum=0
                    for j in range(len(frame)):
                            byte = ord(frame[j]);
                            square  = byte * byte
                            Sum += square

                    mean = Sum / chunkSize
                    chunkRMS = math.sqrt(mean)
                    i+=1
                    if i >= numberOfChunks:
                        break

            if i >= numberOfChunks:
                waveRead.close()
                break

            else:
                c = (i+1)* (chunkSize/sampleWidth) 
                t = c/frameRate
                startTime = t
                waveWrite = wave.open('dummy.wav','w')
                waveWrite.setparams(readParams)

                while chunkRMS >= rms:
                    waveWrite.writeframes(frame)
                    frame = waveRead.readframes(chunkSize/sampleWidth)
                    Sum=0
                    for j in range(len(frame)):
                            byte = ord(frame[j]);
                            square  = byte * byte
                            Sum += square

                    mean = Sum / chunkSize
                    chunkRMS = math.sqrt(mean)
                    i+=1

                    c = (i+1)* (chunkSize/sampleWidth) 
                    t = c/frameRate
                    
                    if i >= numberOfChunks:
                        break

                waveWrite.close()
                c = (i+1)* (chunkSize/sampleWidth) 
                t = c/frameRate
                endTime = t
                newFileName = str(startTime) + "_" + str(endTime) + ".wav"
                os.rename('dummy.wav',newFileName)
                
                textofspeech = speech2text(newFileName,rate,FileName,username)
                if textofspeech:
                    data_string = textofspeech+"\n"
                    finalWrite.write(data_string)
                os.remove(newFileName)

                if i >= numberOfChunks:
                    waveRead.close()
                    break
                
        waveRead.close()
        os.remove(FileName[:-4]+"_c.wav")
        finalWrite.close()
        

def speech2text(newFileName,rate,FileName,username):
        flacFileName=newFileName[:-4]+'.flac'
        os.system('sox '+newFileName+' '+flacFileName)
        
        url = "https://www.google.com/speech-api/v1/recognize?client=chromium&lang=en-us"
        flac=open(flacFileName,"rb").read()
        os.remove(flacFileName)
        header = {'Content-Type' : 'audio/x-flac; rate='+str(rate)}
        req = urllib2.Request(url, flac, header)

        find_underscore = newFileName.find('_')
        first = int(newFileName[:find_underscore])
        last = int(newFileName[find_underscore+1:-4])
        
        try:
                data = urllib2.urlopen(req)
                json_output=data.read()
                start=json_output.find('utterance":')+len("utterance:")+1
                end=json_output.find('"',start+1)
                utterance = json_output[start+1:end]
                start=json_output.find('confidence":')+len("confidence:")+1
                end=json_output.find('}',start+1)
                confidence=float(json_output[start+1:end])
                data = [{'user':username, 'start':first, 'end':last, 'text':utterance, 'confidence':confidence}]
                
        except urllib2.HTTPError:
                print "Unrecognized audio from file "+FileName+" from: "+str(first)+" to "+str(last)+" seconds"
                return
        
        data_string = json.dumps(data)

        return data_string

def main():
        os.chdir(sys.argv[1])
        split('input.wav','input_json.txt',16000,sys.argv[2])
        split('output.wav','output_json.txt',16000,sys.argv[3])
        #split('friends.wav','friends.txt',8000)
        #split('friendswiki.wav','friendswiki.txt',8000)
        #split('python.wav','python.txt',8000)
        #split('wavclean.wav','wavclean.txt',8000)
        #split('yahoo.wav','yahoo.txt',8000)

main()

        
        
        
