# -*- coding: utf-8 -*-
import json
import os

from init_saber_graph import sync_tag_graph

BLOG_HOME = os.environ.get('BLOG_HOME')

if __name__ == '__main__':

    tags = [
        {'name': '数组', 'slug': 'array', 'value': 1351},
        {'name': '字符串', 'slug': 'string', 'value': 635},
        {'name': '排序', 'slug': 'sorting', 'value': 303},
        {'name': '矩阵', 'slug': 'matrix', 'value': 204},
        {'name': '模拟', 'slug': 'simulation', 'value': 112},
        {'name': '枚举', 'slug': 'enumeration', 'value': 42},
        {'name': '字符串匹配', 'slug': 'string-matching', 'value': 20},
        {'name': '桶排序', 'slug': 'bucket-sort', 'value': 8},
        {'name': '计数排序', 'slug': 'counting-sort', 'value': 6},
        {'name': '基数排序', 'slug': 'radix-sort', 'value': 3},
        {'name': '动态规划', 'slug': 'dynamic-programming', 'value': 465},
        {'name': '深度优先搜索', 'slug': 'depth-first-search', 'value': 308},
        {'name': '贪心', 'slug': 'greedy', 'value': 265},
        {'name': '广度优先搜索', 'slug': 'breadth-first-search', 'value': 244},
        {'name': '二分查找', 'slug': 'binary-search', 'value': 221},
        {'name': '回溯', 'slug': 'backtracking', 'value': 119},
        {'name': '递归', 'slug': 'recursion', 'value': 62},
        {'name': '分治', 'slug': 'divide-and-conquer', 'value': 54},
        {'name': '记忆化搜索', 'slug': 'memoization', 'value': 39},
        {'name': '归并排序', 'slug': 'merge-sort', 'value': 12},
        {'name': '快速选择', 'slug': 'quickselect', 'value': 11},
        {'name': '哈希表', 'slug': 'hash-table', 'value': 480},
        {'name': '树', 'slug': 'tree', 'value': 239},
        {'name': '二叉树', 'slug': 'binary-tree', 'value': 204},
        {'name': '栈', 'slug': 'stack', 'value': 158},
        {'name': '堆（优先队列）', 'slug': 'heap-priority-queue', 'value': 137},
        {'name': '图', 'slug': 'graph', 'value': 126},
        {'name': '链表', 'slug': 'linked-list', 'value': 101},
        {'name': '二叉搜索树', 'slug': 'binary-search-tree', 'value': 55},
        {'name': '单调栈', 'slug': 'monotonic-stack', 'value': 54},
        {'name': '有序集合', 'slug': 'ordered-set', 'value': 53},
        {'name': '队列', 'slug': 'queue', 'value': 42},
        {'name': '拓扑排序', 'slug': 'topological-sort', 'value': 35},
        {'name': '最短路', 'slug': 'shortest-path', 'value': 19},
        {'name': '双向链表', 'slug': 'doubly-linked-list', 'value': 12},
        {'name': '单调队列', 'slug': 'monotonic-queue', 'value': 11},
        {'name': '最小生成树', 'slug': 'minimum-spanning-tree', 'value': 5},
        {'name': '欧拉回路', 'slug': 'eulerian-circuit', 'value': 3},
        {'name': '双连通分量', 'slug': 'biconnected-component', 'value': 2},
        {'name': '强连通分量', 'slug': 'strongly-connected-component', 'value': 2},
        {'name': '并查集', 'slug': 'union-find', 'value': 77},
        {'name': '字典树', 'slug': 'trie', 'value': 51},
        {'name': '线段树', 'slug': 'segment-tree', 'value': 33},
        {'name': '树状数组', 'slug': 'binary-indexed-tree', 'value': 24},
        {'name': '后缀数组', 'slug': 'suffix-array', 'value': 6},
        {'name': '双指针', 'slug': 'two-pointers', 'value': 188},
        {'name': '位运算', 'slug': 'bit-manipulation', 'value': 173},
        {'name': '前缀和', 'slug': 'prefix-sum', 'value': 102},
        {'name': '计数', 'slug': 'counting', 'value': 96},
        {'name': '滑动窗口', 'slug': 'sliding-window', 'value': 84},
        {'name': '状态压缩', 'slug': 'bitmask', 'value': 40},
        {'name': '哈希函数', 'slug': 'hash-function', 'value': 26},
        {'name': '滚动哈希', 'slug': 'rolling-hash', 'value': 18},
        {'name': '扫描线', 'slug': 'line-sweep', 'value': 5},
        {'name': '数学', 'slug': 'math', 'value': 433},
        {'name': '几何', 'slug': 'geometry', 'value': 37},
        {'name': '博弈', 'slug': 'game-theory', 'value': 24},
        {'name': '数论', 'slug': 'number-theory', 'value': 18},
        {'name': '组合数学', 'slug': 'combinatorics', 'value': 18},
        {'name': '随机化', 'slug': 'randomized', 'value': 14},
        {'name': '概率与统计', 'slug': 'probability-and-statistics', 'value': 9},
        {'name': '水塘抽样', 'slug': 'reservoir-sampling', 'value': 4},
        {'name': '拒绝采样', 'slug': 'rejection-sampling', 'value': 2},
        {'name': '数据库', 'slug': 'database', 'value': 209},
        {'name': '设计', 'slug': 'design', 'value': 146},
        {'name': '数据流', 'slug': 'data-stream', 'value': 22},
        {'name': '交互', 'slug': 'interactive', 'value': 18},
        {'name': '脑筋急转弯', 'slug': 'brainteaser', 'value': 11},
        {'name': '迭代器', 'slug': 'iterator', 'value': 10},
        {'name': '多线程', 'slug': 'concurrency', 'value': 9},
    ]

    f = open(BLOG_HOME + '/script/question_graph.json')
    graphs = json.load(f)
    for tag in tags:
        # if tag['slug'] not in graphs:
        #     sync_tag_graph(tag['slug'])
        os.system('python script/init_saber_graph.py ' + tag['slug'])
