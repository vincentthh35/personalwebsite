import sys
import os
import argparse

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        print(f'error: {message}\n')
        self.print_help()
        sys.exit(2)

parser = MyParser(description='add {{< math >}} before and after latex math statements')
parser.add_argument('-p', '--post', help='process the WHOLE post directory')
parser.add_argument('-n', '--new', nargs='+', help='render only new post(s) (designated by user)')

def processFile(raw_filename, target_filename):
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

# print(f'{len(sys.argv)}')
# argv[0] is name of this program
if __name__ == '__main__':
    '''
    usage 1, processing ALL posts:
        python3 preprocessing_markdown.py -p /path_to_post/

    usage 2, processing only the input post:
        python3 preprocessing_markdown.py -n /path_to_individual_post/ /path_to_another_individual_post/

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
                    │   └── index.md
                    ├── index.md
                    └── other_things
        This script will overwrite 'post_name/index.md' with the preprocessed version of index.md

    ANY USAGE THAT IS NOT UNDER THE ABOVE SITUATION MIGHT CAUSE SOME UNPREDICTABLE RESULTS!!!
    '''
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if (args.post is None and args.new is None) or (args.post is not None and args.new is not None):
        parser.print_help()
        sys.exit(1)

    if args.post is not None:
        print('start processing ALL posts')
        all_posts = os.listdir(args.post)
        for post_name in all_posts:
            raw_filename = os.path.join(args.post, post_name, 'raw', 'index.md')
            target_filename = os.path.join(args.post, post_name, 'index.md')
            processFile(raw_filename, target_filename)
    if args.new is not None:
        for post_name in args.new:
            print(f'start processing post: {post_name}')
            raw_filename = os.path.join(post_name, 'raw', 'index.md')
            target_filename = os.path.join(post_name, 'index.md')
            processFile(raw_filename, target_filename)
