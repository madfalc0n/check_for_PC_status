import os.path
from time import strftime, localtime

# path = 'log_pic_2/'
# print(os.path.exists(path))

# if not os.path.exists(path):
#     print("There is no directory. Create a new directory.")
#     os.makedirs(path)
# print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

def logging(fullname, logtext):
    # filename = strftime("%Y%m%d", localtime()) + '_log.log'
    # fullname = path + filename
    if os.path.isfile(fullname): #aleady exist, appending
        mode = 'a'
    else: # not exist, create and logging
        mode = 'w'
    with open(fullname, mode=mode) as file:
        file.writelines(logtext + "\n")

if __name__ == "__main__":
    
    logging(fullname, logtext)