# -*- coding: utf-8 -*-

from time import sleep
import requests
import json
import os
import sys
import re

open_solver_flag = True
open_cpp_flag = True
open_java_flag = False
code_type = 'cpp'

LEETCODE_HOME = os.environ.get('LEETCODE_HOME')
LEETCODE_CODE_HOME = os.environ.get('LEETCODE_CODE_HOME')

config = {
    'solve_dir': LEETCODE_HOME + '/algorithms',
    'java_dir': LEETCODE_HOME,
    'cpp_dir': LEETCODE_HOME,
}


def print_question_url(question):
    questionId = question['questionFrontendId']
    translatedTitle = question['translatedTitle']
    titleSlug = question['titleSlug']
    title = f"""\n原题链接🔗 [{questionId}.{translatedTitle}](https://leetcode.cn/problems/{titleSlug}/)\n\n"""
    print(title)


def content_in_file(file_name, content):
    if os.path.exists(file_name) is False:
        return False
    with open(file_name) as f:
        s = f.read()
    return content in s


def open_solution(file_name):
    os.system(f"""open {file_name}""")


class reUnit:
    """
    通过正则表达式获取指定字符串值方法，如果结果不唯一，则返回多个
    """

    def reUnit(anyStr, leftBoundaryStr, rigjtBoundaryStr):
        """
        :param str: 完整的字符串str
        :param leftBoundaryStr: 左边界str
        :param rigjtBoundaryStr: 右边界str
        :return:返回正则取值结果list
        """
        return re.findall('{}(.+?){}'.format(leftBoundaryStr, rigjtBoundaryStr), anyStr)


def parse_cpp_method(solution_code_cpp):
    str = solution_code_cpp.replace('\n', ' ')
    simple = reUnit.reUnit(str, 'class Solution { public:     ', '\) {')
    if len(simple) == 0:
        return simple
    arr = re.split(' |, |\\(|& ', simple[0])
    return arr


def case_input_formatter(line):
    line = line.replace('[', '{').replace(']', '}')
    line = line.replace('\r', '')
    return line


def case_is_array(line):
    letter = line.find('[')
    return letter == 0


def case_is_string(line):
    letter = line.find('"')
    return letter == 0


def get_slug_by_frontened_id(fronted_id):
    fronted_id = str(fronted_id)
    f = open(LEETCODE_HOME + '/tmp/problem.json')
    problem = json.load(f)

    pairs = problem['stat_status_pairs']
    for pair in pairs:
        stat = pair['stat']
        num = str(stat['frontend_question_id'])
        if num == fronted_id:
            return pair
    return ''


def crawler_problem(question__title_slug):
    data = {
        'operationName': 'questionData',
        'variables': {'titleSlug': question__title_slug},
        'query': 'query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    categoryTitle\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    envInfo\n    book {\n      id\n      bookName\n      pressName\n      source\n      shortDescription\n      fullDescription\n      bookImgUrl\n      pressImgUrl\n      productUrl\n      __typename\n    }\n    isSubscribed\n    isDailyQuestion\n    dailyRecordStatus\n    editorType\n    ugcQuestionId\n    style\n    exampleTestcases\n    jsonExampleTestcases\n    __typename\n  }\n}\n',
    }
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN',
        'content-type': 'application/json',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-csrftoken': 'AoZmaswgG6XancLZzI2rWcxlqQ0gwT8hb8hDldfM38bAGvMNmOySa6qNCpuefSxu',
        'x-definition-name': 'question',
        'x-operation-name': 'questionData',
        'x-timezone': 'Asia/Shanghai',
    }
    res = requests.post(
        url='https://leetcode.cn/graphql/', data=json.dumps(data), headers=headers
    )
    body = json.loads(res.text)
    return body['data']['question']


def check_dir(dir):
    if os.path.exists(dir) is False:
        print('create folder ' + dir)
        os.makedirs(dir)


def check_file(file_path):
    return os.path.exists(file_path)


def create_and_write_file(file_name, content):
    print('create file', file_name)
    file = open(file_name, 'w', encoding='utf-8')
    file.write(content)
    file.close()


def save_json_to_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()


if __name__ == '__main__':

    os.system('lc sync')

    f = open(LEETCODE_HOME + '/tmp/problem.json')
    problem_file = json.load(f)
    problems = {}
    pairs = problem_file['stat_status_pairs']
    for pair in pairs:
        question_id = pair['stat']['frontend_question_id']
        info = {
            's': 1 if pair['status'] == 'ac' else 0,
            'l': pair['difficulty']['level'],
            # 'name': str(question_id) + '. ' + pair['stat']['question__title'],
            # 'link': 'https://leetcode.cn/problems/' + pair['stat']['question__title_slug']+'/',
        }
        problems[question_id] = info

    content = f"""// l: level 1,2,3 简单、中等、困难
// s: 1: 已解决；0：未解决
var all_problems = {json.dumps(problems, sort_keys=True, ensure_ascii=False)}"""
    print(content)
    f = open('docs/.vuepress/public/problems.js', 'w')
    f.write(content)
    f.close()
