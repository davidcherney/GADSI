"""To reduce computation time, a relatively small data set of relevant data 
is extracted from the full data set in the program"""
import csv 
import json
from datetime import datetime

n_lines = 39_000 #number of lines to read #45,957 in file.
# why cant I read all the lines? 

def passes_cleaning_tests(in_row):
    # does a line pass the tests to be called clean?
    passed = True #default is yes
    passed = passed and isinstance(in_row[3], str)
    passed = passed and in_row[6] in {'failed', 'successful'}
    # passed = passed and isinstance(int(in_row[7]),int)
    passed = passed and 500 <= float(in_row[7]) <= 500_000
    # passed = passed and isinstance(float(in_row[9]),float)
    passed = passed and float(in_row[9])<=4
    return passed

in_fname = 'DSI_kickstarterscrape_dataset.csv'
out_fname = 'relevant_data.csv'

with open(in_fname,'r',newline='') as f:
    reader = csv.reader(f,dialect='excel') 
    # header_row = next(reader)
    # print(dict(enumerate(header_row)))
    # Desired output data:
    # 3:category
    # 6:status
    # 7:goal
    # 9:funded percent
    # 16:duration
    # keeping 5 of 17 columns for a 1/3 reduction in dataset size.
    keeper_indices = {3,6,7,9,16}
    # sets to keep track of errors and cleaning:
    unicode_error_indiceds = set()
    index_error_indices = set()
    removed_for_cleaning = set()

    with open(out_fname,'w',newline='') as g:
        writer = csv.writer(g, delimiter=',')
        # write header row
        in_row = next(reader)
        out_row = [in_row[k] for k in keeper_indices]
        writer.writerow(out_row)
        # write data rows
        for i in range(n_lines):
            # bypass errors, don't write lines: keep only clean lines
            try:
                in_row = next(reader) #gives unicode error IDK
                out_row = [in_row[k] for k in keeper_indices] #gives Index error                
            except UnicodeDecodeError: 
                unicode_error_indiceds.add(i)
            except IndexError:
                index_error_indices.add(i)
            except StopIteration: #raised when next line doesn't exist.
                last_index = i #=number data lines read, since loop started at 0
                break
            else:
                #write if cleanliness tests are passed
                if  passes_cleaning_tests(in_row):
                    writer.writerow(out_row)
                else:
                    removed_for_cleaning.add(i)
print(f'Unicode errors: {len(unicode_error_indiceds)} of {last_index} \n') #\nat lines in \n{unicode_error_indiceds}\n')
print(f'index errors: {len(index_error_indices)} of {last_index}\n') # \nat lines in \n{index_error_indices}\n')
print(f'Removed for cleaning: \n{len(removed_for_cleaning)} of {last_index}\n')
print(f'Last line read at index value {last_index}\n')

print(f'{last_index - len(removed_for_cleaning)-len(index_error_indices) -len(unicode_error_indiceds)} lines printed')