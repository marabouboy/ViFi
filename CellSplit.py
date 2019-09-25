#!/usr/bin/python3
import time, sys, os


# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

    
#Input command. May have to change if the thing does not allow for an interactive shell.
file_name = input('Enter file name: ')
f = open(file_name, "r")


#Variables                     
UNIQUEBC = dict()
UNIQUERN = dict()
RN2R_nr = ()


#Update bar at the start.
print("progress : 'Beginning'")
update_progress(0)
time.sleep(0.1)


#Write something that will create a new file with all the fastq files.
PWD = os.getcwd()
#os.makedirs( PWD + "/cellsplit_%s/" % file_name, mode=0o777)
os.makedirs( PWD + "/cellsplit_%s/cellsplit_fastq" % file_name, mode=0o777)
os.makedirs( PWD + "/cellsplit_%s/cellsplit_analytics" % file_name, mode=0o777)


for WHOLEREAD in f.read().split("\n@"):
    
    #Getting the Dict system where the ReadNumber is the Key and the Whole read is the value.
    RN2R_READ = ("@" + WHOLEREAD)
    RN2Rcontent = WHOLEREAD.split()
    RN2R_nr = RN2Rcontent[1]
    if not RN2R_nr in UNIQUERN:
        UNIQUERN[RN2R_nr]=[RN2R_READ]
    else:
        UNIQUERN[RN2R_nr].append(RN2R_READ)
    
    #Getting the Dict system where the Barcode is the Key and the ReadNumber is the value(s).
    if WHOLEREAD != []:
        BC2R_bc = WHOLEREAD.split("_")[1]
        BC2R_rn = WHOLEREAD.split()[1]
        if not BC2R_bc in UNIQUEBC:
            UNIQUEBC[BC2R_bc]=[BC2R_rn]
        else:
            UNIQUEBC[BC2R_bc].append(BC2R_rn)


#Updatebar
print("progress : 'Set up both Dictionaries'")
update_progress(0.5)
time.sleep(0.1)


#Function to fuse the two dictionaries together to create a massive dictionary where the Key is the Unique Barcode and the values are a list where all the reads are contained.
for k, v in UNIQUEBC.items():
    for x in v:
        TRANS = [UNIQUERN[x] for x in v]
        UNIQUEBC[k] = TRANS

        
#Function to count the number of reads to each Barcode(Meaning unique cell) Comment out if you don't need it.
os.chdir(PWD + "/cellsplit_%s/cellsplit_analytics" % file_name )
COUNT = open("%s_COUNT" % file_name , "w+")
for k, v in UNIQUEBC.items():
    COUNT.write("\n" + str((k, len([item for item in v if item]))))
COUNT.close()


#Updatebar
print("progress : 'Fused the Dictionaries'")
update_progress(0.75)
time.sleep(0.1)
        

#Write the individual cells .fastq files:
#Add something that creates a specific directory?
os.chdir(PWD + "/cellsplit_%s/cellsplit_fastq" % file_name)
for k, v in UNIQUEBC.items():
    READER = open("%s.fastq" % k, "w+")
    for L in v:
        JOINEDL = ''.join(L)
        READER.writelines("%s" % JOINEDL + "\n")
    READER.close()


#Updatebar
print("progress : 'Created the files'")
update_progress(99)
time.sleep(0.1)


#Write a file containing all the Titles, makes it easier for downstream scripts.
os.chdir(PWD + "/cellsplit_%s/cellsplit_analytics" % file_name)
TITLE = open("%s_TITLES" % file_name , "w+")
for k, v in UNIQUEBC.items():
    TITLE.write("%s" % k + "\n")
TITLE.close()


#Updatebar
print("progress : 'Finishing the script'")
update_progress(99)
time.sleep(0.1)
