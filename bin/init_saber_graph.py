# -*- coding: utf-8 -*-

import json
import os
import sys

from tag_graph import generater_graph


# 当前题目云图中展示题目：
# 1. 已解决题目
# 2. 未解决题目中，暂且按题号排序，选前 8 道增加到云图中

# 调用举例：

# python script/more_tag_questions.py binary-search sync

open_solver_flag = True
open_cpp_flag = True
open_java_flag = False
code_type = 'cpp'

LEETCODE_HOME = os.environ.get('LEETCODE_HOME')
BLOG_HOME = os.environ.get('BLOG_HOME')


def get_tag_slug_translated(problem, tag_slug):
    for tag in problem['topicTags']:
        if tag['slug'] == tag_slug:
            return tag['translatedName']
    return ''


def get_problems_by_tag(tag_slug):
    f = open(
        BLOG_HOME + '/script/20220828220600_questions_include_main_regular_user.json'
    )
    problems = json.load(f)

    rows = []
    for problem in problems:
        if problem['isPaidOnly']:
            continue
        for tag in problem['topicTags']:
            if tag['slug'] == tag_slug:
                rows.append(problem)
                break
    return rows


def get_ac_status():
    f = open(LEETCODE_HOME + '/tmp/problem.json')
    problem_content = json.load(f)
    pairs = problem_content['stat_status_pairs']
    ac_status_dict = {}
    for pair in pairs:
        stat = pair['stat']
        num = str(stat['frontend_question_id'])
        ac_status_dict[num] = pair['status']
    return ac_status_dict


def write_tag_graph_to_current_graph(tag_slug, graph):
    f = open(BLOG_HOME + '/script/question_graph.json')
    graphs = json.load(f)
    graphs[tag_slug] = dict(graph)
    f.close()

    with open(BLOG_HOME + '/script/question_graph.json', 'w') as write_f:
        json.dump(graphs, write_f, indent=4, ensure_ascii=False)
        write_f.close()


def get_current_graph_by_tag_slug(tag_slug):
    f = open(BLOG_HOME + '/script/question_graph.json')
    graphs = json.load(f)
    graph = {'problems': [], 'links': [], 'zh': ''}

    f.close()
    if tag_slug in graphs:
        graph = graphs[tag_slug]
    return graph


def object_array_to_dict(arr, id_key):
    dict = {}
    for item in arr:
        if not item[id_key]:
            continue
        dict[item[id_key]] = item
    return dict


def merge_ac_stat(problems_dict, ac_status):
    for id, problem in problems_dict.items():
        problem['ac_status'] = ac_status[id]
    return problems_dict


def filter_problems_by_ac_status(problems_dict):
    problems_ac = []
    problems_notac = []
    for _, problem in problems_dict.items():
        if problem['ac_status'] == 'ac':
            problems_ac.append(problem)
        else:
            problems_notac.append(problem)
    return problems_ac, problems_notac


def sync_tag_graph(tag_slug):

    # 获取 tag 的所有 question
    problems = get_problems_by_tag(tag_slug=tag_slug)
    problems_dict = object_array_to_dict(problems, 'questionFrontendId')

    # 获取 question 的 ac 状态
    ac_status = get_ac_status()
    problems_dict = merge_ac_stat(problems_dict, ac_status)
    problems_ac, problems_notac = filter_problems_by_ac_status(problems_dict)
    # 获取 云图中的题目列表，整理云图数据
    not_ac_cnt = 5 if len(problems_ac) < 30 else 10
    problems_to_graph = problems_ac[0:20] + problems_notac[0:not_ac_cnt]

    print('ac size:', len(problems_ac), 'notac size:', len(problems_notac))
    print('graph size', len(problems_to_graph))

    # 整理 云图数据
    graph = get_current_graph_by_tag_slug(tag_slug=tag_slug)

    if graph['zh'] is None:
        graph['zh'] = (
            '' if len(problems) == 0 else get_tag_slug_translated(problems[0], tag_slug)
        )
    graph['problems'] = []
    for problem in problems_to_graph:
        id = problem['questionFrontendId']
        graph['problems'].append(id)

    def merge_linked_problems(graph):
        for link in graph['links']:
            for id in link:
                if id in graph['problems']:
                    continue
                graph['problems'].append(id)

    merge_linked_problems(graph)

    # 写回 question_graph.json
    write_tag_graph_to_current_graph(tag_slug, graph)

    # 生成 graph html
    generater_graph(tag_slug)

    return graph


if __name__ == '__main__':

    if len(sys.argv) < 2:
        exit

    if len(sys.argv) > 2 and sys.argv[2] == 'sync':
        os.system('lc sync && python script/sync_ac_status.py')

    tag_slug = sys.argv[1]
    graph = sync_tag_graph(tag_slug)
    # print(json.dumps(graph, sort_keys=True, ensure_ascii=False, indent=2))
