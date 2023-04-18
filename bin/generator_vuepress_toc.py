# -*- coding: utf-8 -*-

import os
import json

toc = []

file_dir = os.environ.get('BLOG_HOME') + '/docs'
sub_toc = '/算法/力扣通关之路'
for _, _, files in os.walk(file_dir + sub_toc):
    files.sort()
    for file in files:
        toc.append([sub_toc + '/' + file[:-3], file[:-3]])


toc = json.dumps(toc, ensure_ascii=False, indent=4)

print(toc)
