import sys
import os

# print(f'{len(sys.argv)}')
# argv[0] is name of this program
if __name__ == '__main__':
    '''
    usage:
        python3 preprocessing_markdown.py /path_to_post/*/*/*.md

    example:
        python3 ./scripts/preprocessing_markdown.py \
                ./content/post/*/raw/index.md // this will get paths like './content/post/post_name/raw/index.md'

    BEFORE YOU USE:
        The below is the path of my hugo project:
        (It should be like this after correctly running this script)
            content
            └── post
                └── post_name
                    ├── raw
                    │   ├── other_things
                    │   └── index.md
                    ├── index.md
                    └── other_things
        If currently, the directory structure is like this:
            content
            └── post
                └── post_name
                    ├── index.md
                    └── other_things
        You have to copy index.md and other_things into a 'raw' directory before you run the script:
            content
            └── post
                └── post_name
                    ├── raw
                    │   ├── other_things
                    │   └── index.md
                    ├── index.md
                    └── other_things
        This script will overwrite 'post_name/index.md' with the preprocessed version of index.md

    ANY USAGE THAT IS NOT UNDER THE ABOVE SITUATION MIGHT CAUSE SOME UNPREDICTABLE RESULTS!!!
    '''
    if len(sys.argv) <= 1:
        print(f'[USAGE]: python3 {sys.argv[0]} /path_to_post/*/*/*.md')
        print('ending this script...')
        exit(0)
    for i in range(1, len(sys.argv)):
        # raw_filename is the original markdown file
        raw_filename = sys.argv[i]
        # target_filename is the filename we will write to
        target_filename = os.path.join(os.path.split(os.path.split(raw_filename)[0])[0], 'index.md')
        with open(raw_filename, 'r') as in_file:
            print(f'[preprocessing_markdown.py] processing {target_filename}...')
            with open(target_filename, 'w') as out_file:
                print(f'[preprocessing_markdown.py] overwrite {target_filename}!!')
                lines = in_file.readlines()
                found = False
                double = False # $$ or $
                for line in lines:
                    find_result = line.find('$')
                    while find_result != -1:
                        # this $ is possibily escaped
                        # (depends, but its sufficient for my markdown)
                        if line[find_result - 1] == '\\':
                            find_result = line.find('$', find_result + 1)
                            continue
                        if double: # double must be found
                            line = line[ :find_result + 2] + '{{< /math >}}' + line[find_result + 2: ]
                            double = False
                            found = False
                            find_result = line.find('$', find_result + 2)
                        elif line[find_result + 1] == '$': # double $
                            line = line[ :find_result] + '{{< math >}}' + line[find_result: ]
                            double = True
                            found = True
                            find_result = line.find('$', find_result + 15)
                        else:
                            if found: # tail of one $
                                line = line[ :find_result + 1] + '{{< /math >}}' + line[find_result + 1: ]
                                found = False
                                find_result = line.find('$', find_result + 1)
                            else: # head of one $
                                line = line[ :find_result] + '{{< math >}}' + line[find_result: ]
                                found = True
                                find_result = line.find('$', find_result + 14)
                    out_file.write(line)
                    # rule-based (replacement)
                    # # replace '\\' to '\\\\'
                    # find_result = line.find('\\')
                    # while find_result != -1:
                    #     # '\\\\\n' -> '\\\\\\\\\n'
                    #     if line[find_result+1] == '\\':
                    #         line = line[:find_result] + '\\\\' + line[find_result:]
                    #         find_result = line.find('\\', find_result+4)
                    #     # escape the force newline '\\\n'
                    #     elif line[find_result+1] == '\n':
                    #         find_result = line.find('\\', find_result+2)
                    #     else:
                    #         line = line[:find_result] + '\\' + line[find_result:]
                    #         find_result = line.find('\\', find_result+2)
                    # # replace '_' to '\\_'
                    # find_result = line.find('_')
                    # while find_result != -1:
                    #     line = line[:find_result] + '\\' + line[find_result:]
                    #     find_result = line.find('_', find_result+2)
