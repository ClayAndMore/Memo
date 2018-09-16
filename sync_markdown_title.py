#coding:utf-8
import os

TITLE_LIST = []

def write_local_mark_down():
    with open('struct.md', 'w') as f:
        f.writelines(TITLE_LIST)
        

def deal_title(file_content_list):
    for line in file_content_list:
        if line.startswith('#'):
            interval = 3 - line.count('#')
            if interval > 0:
                to_deal_list = list(line.strip())
                to_deal_list[0] = '#'*interval
                add = ''.join(to_deal_list)
            else:
                add = line.strip()[abs(interval):]
            TITLE_LIST.append('%s\n'%add)

def main():
    for dirpath, dirnames, filenames in os.walk('.'):
        dirpath = dirpath.replace('./', '') 
        if not 'A' <= dirpath[0] <= 'Z': 
            continue
        # 有几个目录先不处理
        if 'LANGUAGE' in dirpath or 'Unity' in dirpath:
            print '=====',dirpath
            continue
        print dirpath
        TITLE_LIST.append('# %s\n'%dirpath)
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as f:
                TITLE_LIST.append('## %s\n'%filename)        
                deal_title(f.readlines())

if __name__ == '__main__':
    """
    获取当下文件夹的所有md，生成层级关系，用于梳理结构目录。
    # 目录
    ## 文件名
    ### 文件内最高title
    #### 文件内次高title
    ...
    """
    main()
    write_local_mark_down()
