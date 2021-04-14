import os
from time import gmtime, strftime

# path = 'log_pic_2/'
# print(os.path.exists(path))

# if not os.path.exists(path):
#     print("There is no directory. Create a new directory.")
#     os.makedirs(path)


# print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))


import os.path 


fname = "log_stat/textfile.log"

if os.path.isfile(fname):
    mode = 'a'
else:
    mode = 'w'        

with open("log_stat/textfile.log", mode=mode) as file:
    words = ["Python\n", "YUNDAEHEE\n", "076923\n"]

    file.write("START\n")
    file.writelines(words)
    file.write("END")