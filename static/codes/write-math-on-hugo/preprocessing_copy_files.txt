import sys
import os
import shutil

if __name__ == '__main__':
    '''
    This script copies all files except .md files in the raw directory to the upper directory
    usage:
        python3 ./scripts/preprocessing_copy_files.py /path_to_post/

    example:
        python3 ./scripts/preprocessing_copy_files.py ./content/post 
    '''
    if len(sys.argv) != 2:
        print(f'[USAGE]: python3 {sys.argv[0]} /path_to_post')
        print('ending this script...')
        exit(0)
    elif not os.path.isdir(sys.argv[1]):
        print(f'{sys.argv[1]} is not a directory!!')
        print('ending this script...')
        exit(0)
    post_directory = sys.argv[1]
    for post_name in os.listdir(post_directory):
        target_directory = os.path.join(post_directory, post_name)
        raw_directory = os.path.join(target_directory, 'raw')
        if not os.path.isdir(raw_directory):
            print(f'[preprocessing_copy_files.py] {raw_directory} is not a directory!!')
            continue
        print(f'[preprocessing_copy_files.py] copying {target_directory}...')
        for raw_filename in os.listdir(raw_directory):
            if raw_filename.endswith('.md'):
                continue
            # copy those files
            shutil.copyfile(os.path.join(raw_directory, raw_filename),
                            os.path.join(target_directory, raw_filename))
