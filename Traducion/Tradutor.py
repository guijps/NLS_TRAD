
#Creator:  Guilherme Jorge Paes da Silva Amad
#github: https://github.com/guijps
import glob
from logging import exception
from googletrans import Translator
import re
import time

#========================CAUTION=============================================
#   During some tests without the 'sleep' time, the code shut down my router.
#   I think that it full filled the router's buffer, and stoped the services.
#   So inside the code it has one counter that for each 300 lines 
#   read, it stops for 3 seconds. You may adjust it as you wish.
#========================CAUTION=============================================
#In order to use the code, in that path you must have the .py file, and two more: 'ParaTraduzir' and 'Traduzidos'.
#At 'ParaTraduzir' there must be the Source Langue files, doesn't matter what 'Traduzidos' contains, but it is the destination folder.
#In each .txt at 'ParaTraduzir', it is forbidden to exist only one quitation marks, so in order to the script works
#each line must contain 2 or none quotation marks

#Check for googletrans reference to find your language code
sourceLangue ='' 
destinationLangue = ''
pathToPy = "C:\\Users\\Energia\\Documents\\gui\\Traducion\\"#Your path to python file


fil = glob.glob(pathToPy+"ParaTraduzir\\*.txt")# find every .txt in 'ParaTraduzir'
sizeList = len(fil)
indxGlobal = 0
for file in fil:
    pct = indxGlobal/sizeList
    #Read and Stores the lines.

    with open(file,mode='r',encoding='utf-8-sig') as t:
        lines = t.readlines()
        t.close()

    #The .txt template is -NLSKEY- "NLSTEXT", the GetToTr Function will return the NLSTEXT without quotation marks
    def GetToTr(s):
        indices = [i.start() for i in re.finditer('"', s)]
        # The len(indices) tells if: the line is a line without NLSTEXT, in some cases the line will be ONLY a quotation mark
        #So To avoid any problem on importing, it is given that there will be given that in a line, there will be only 2 quotation marks or none.
        if(len(indices)==0):
            #Good
            return [0,0],s 
        elif(len(indices)==1):
            #Bad
            print("Formatação errada, linha com apenas 1 aspas")
            return exception,exception
        elif(len(indices)==2):
            # Good
            ma = max(indices)
            mi = min(indices)
            return [mi,ma],s[mi+1:ma]
        else: 
            #Really Bad
            print("Erro Sem razão")
            return exception,exception


    #It assumes that you are translating from english to Portuguese
    with open(file.replace("ParaTraduzir\\EN_","Traduzidos\\PT_"),mode='w',encoding='utf-8')as w:
        trad = Translator()
        indx=0 
        
    
        for line in lines:
            vec,strToTr = GetToTr(line)
            if(vec[0]==0):
                #There is only 4 cases that this is acceptable: STRINGTABLE,BEGIN,END or empty lines
            
                w.write(line)
                print('No Quotes: '+str(indx))
            else:
                traducao = trad.translate(strToTr,src='en',dest='pt') 
                mi = vec[0]
                
                ma=vec[1]
                
                strToWrite = line[0:mi+1]+traducao.text + line[ma:]
                
                print(str(file)+' = '+str(indx))
                
                w.write(strToWrite.encode("utf-8").decode('utf-8'))
            indx+=1
        #This can full fill your routers buffers
        #========================CAUTION=============================================
        #without it, in some large files, this code may shut down your router
            if(indx%300==0):
                print('sleeping for safety')
                time.sleep(3)
        #========================CAUTION=============================================
        w.close()
    indxGlobal+=1
    


