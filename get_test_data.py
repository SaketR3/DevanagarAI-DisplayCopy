import os
import random

test_portion = 0.1

total = 2000
test_number = (int)(test_portion * total)

path = "./archive/Images"
test_path = "./archive/test_data"
train_path = "./archive/training_data"
for i in os.listdir(path):
    rand_numbers = random.sample(range(1, total), test_number)
    count = 0
    subdictionary_path = os.path.join(path, i)
    if i != '.DS_Store':
   #if os.path.isfile(subdictionary_path):
        os.makedirs(os.path.join(test_path, i))
        os.makedirs(os.path.join(train_path, i))
        print(subdictionary_path)
        for j in os.listdir(subdictionary_path):
          if j != '.DS_Store':
            count = count + 1
            if rand_numbers.count(count) != 0:
                os.rename(os.path.join(subdictionary_path, j), os.path.join(test_path, i, j))
            else:
                os.rename(os.path.join(subdictionary_path, j), os.path.join(train_path, i, j))