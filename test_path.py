import os


path = 'log_pic_2/'
print(os.path.exists(path))

if not os.path.exists(path):
    print("There is no directory. Create a new directory.")
    os.makedirs(path)