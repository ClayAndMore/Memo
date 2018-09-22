#coding:utf-8
import os
import sys 

TITLE_LIST = []

def write_local_mark_down(filename):
    with open(filename, 'w') as f:
        f.writelines(TITLE_LIST)
        

def deal_title(file_content_list, filename):
    for line in file_content_list:
        line = line.strip()
        if line.startswith('##'):
            #interval = 3 - line.count('#')
            #if interval > 0:
            #    to_deal_list = list(line)
            #    to_deal_list[0] = '#'*interval
            #    add = ''.join(to_deal_list)
            #else:
            #    add = line[abs(interval):]
            #TITLE_LIST.append('%s\n'%add)
            # 为了让文件名和文件顶层标题不重合
            if line.replace('#','').strip().lower() == filename.strip().split('.')[0].lower():
                continue
            TITLE_LIST.append('%s\n'%line)

def main(moudle):
    for dirpath, dirnames, filenames in os.walk('.'):
        dirpath = dirpath.replace('./', '') # ./Ab__Python -> Ab__python
        moudle_list = [ x.lower() for x in dirpath.split('___')] # Ab__Python -> ['ab', 'python']
        for moudle_name in moudle_list:
            if moudle in moudle_name:
                TITLE_LIST.append('# %s\n'%dirpath)
                # 按字母排序, 中文放后面
                if filenames:
                    put_behind = []
                    for index, filename in enumerate(filenames):
                        if not 'A'<filename[0]<'z':
                            put_behind.append(filename)
                            del filenames[index]
                    filenames.sort(key=str.lower)
                    filenames.extend(put_behind)
                for filename in filenames:
                    with open(os.path.join(dirpath, filename)) as f:
                        TITLE_LIST.append('## %s\n'%filename)        
                        deal_title(f.readlines(), filename)

if __name__ == '__main__':
    """
    获取当下文件夹的所有md，生成层级关系，用于梳理结构目录。
    # 目录
    ## 文件名
    ### 文件内最高title
    #### 文件内次高title

    传参格式,eg： 获得Ab__Python模块的层级：
    python sync_markdown_title.py python
    ...
    """
    main(sys.argv[1])
    write_local_mark_down(sys.argv[1] + '_mindmap.md')
