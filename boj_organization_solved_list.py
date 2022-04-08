import json
from time import sleep

import requests


def get_profile(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user의 프로필 정보 중 일부를 반환해줌.
    :param str user_id: 사용자id
    :return: 백준 프로필 정보
    :rtype: dict
    """
    url = f"https://solved.ac/api/v3/user/show?handle={user_id}"
    r_profile = requests.get(url)
    if r_profile.status_code == requests.codes.ok:
        profile = json.loads(r_profile.content.decode('utf-8'))
        profile = \
            {
                "tier": profile.get("tier"),
                "rank": profile.get("rank"),
                "solvedCount": profile.get("solvedCount"),
                "rating": profile.get("rating"),
                "exp": profile.get("exp"),
            }
    else:
        print("프로필 요청 실패")
    return profile


def get_solved(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user가 푼 총 문제수, 문제들 정보(level 높은 순)를 튜플(int, list)로 반환해줌.
    :param str user_id: 사용자id
    :return: 내가 푼 문제수, 내가 푼 문제들 정보
    :rtype: int, list
    """
    url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=level&direction=desc"
    r_solved = requests.get(url)
    if r_solved.status_code == requests.codes.ok:
        solved = json.loads(r_solved.content.decode('utf-8'))
        pages = (solved.get("count") - 1) // 100 + 1
    else:
        print("푼 문제들 요청 실패")

    solved_problems = []
    for page in range(pages):
        sleep(10)
        page_url = f"{url}&page={page + 1}"
        print(page_url)
        r_solved = requests.get(page_url)
        if r_solved.status_code == requests.codes.ok:
            solved = json.loads(r_solved.content.decode('utf-8'))
            count = solved.get("count")
            items = solved.get("items")
            for item in items:
                solved_problems.append(item.get("problemId"))
            # print("푼 문제수와 젤 고난이도 문제 1개만 >>>", count, solved_problems[0])
        else:
            print("푼 문제들 요청 실패")
            print(r_solved.status_code)
            print(url)
    return count, solved_problems


def get_user_in_group(group_id):
    """"
    :param group_id: 그룹id
    :return: 그룹에 속한 총 user
    :rtype: list
    """
    url = f"https://solved.ac/api/v3/ranking/in_organization?organizationId={group_id}"
    r_user_in_group = requests.get(url)
    if r_user_in_group.status_code == requests.codes.ok:
        user_in_group = json.loads(r_user_in_group.content.decode('utf-8'))
        pages = (user_in_group.get("count") - 1) // 100 + 1
    else:
        print("그룹 내 유저 요청 실패")

    users = []
    for page in range(pages):
        page_url = f"{url}&page={page + 1}"
        print(page_url)
        r_user_in_group = requests.get(page_url)
        if r_user_in_group.status_code == requests.codes.ok:
            user_in_group = json.loads(r_user_in_group.content.decode('utf-8'))
            items = user_in_group.get("items")
            for item in items:
                users.append(item.get("handle"))
        else:
            print("그룹 내 유저 요청 실패")
    return users


def get_count_by_level(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user가 푼 문제들에 대한 level별 문제수 정보를 level 높은 순으로 반환해줌.
    :param str user_id: 사용자id
    :return: level별 총 문제수, 내가 푼 문제수
    :rtype: list
    """
    url = f"https://solved.ac/api/v3/user/problem_stats?handle={user_id}"
    r_count_by_level = requests.get(url)
    if r_count_by_level.status_code == requests.codes.ok:
        count_by_level = json.loads(r_count_by_level.content.decode('utf-8'))
        filted_count_by_level = [{"level": dict_['level'], "total": dict_['total'], "solved": dict_['solved'], } for
                                 dict_ in count_by_level if dict_.get('solved') != 0]
        filted_count_by_level = sorted(filted_count_by_level, key=lambda x: x['level'], reverse=True)
    else:
        print("레벨별, 전체 문제수, 푼 문제수  요청 실패")
    return filted_count_by_level


def get_solved_by_group(group_id):
    group_users = get_user_in_group(group_id)
    group_problems = set()
    n = 1
    for user in group_users:
        sleep(10)
        print(n, " / ", len(group_users))
        get_solved_by_user = get_solved(user)[1]
        print(get_solved_by_user)
        group_problems.update(get_solved_by_user)
        n = n + 1
    return group_problems


def get_problem_by_level(level):
    url = f"https://solved.ac/api/v3/search/problem?query=tier%3A{level}"
    r_level_problem = requests.get(url)
    if r_level_problem.status_code == requests.codes.ok:
        level_problem = json.loads(r_level_problem.content.decode('utf-8'))

        items = level_problem.get("items")
        problems = set()
        for item in items:
            problems.add(item.get("problemId"))
    else:
        print("난이도 별 문제 요청 실패")
    return problems


def get_unsolved_by_group(group_id):
    solved_problem = get_solved_by_group(group_id)
    for level in range(30):
        level_problem = get_problem_by_level(level + 1)
        unsolved_level_problem = level_problem - solved_problem
        if len(unsolved_level_problem) > 0:
            return unsolved_level_problem
        print(f"all solved level {level + 1}")
    print(f"all solved boj")


user_id = "siontama"
group_id = "385"

"""profile_dict = get_profile(user_id)
print(f"========{user_id}님의 프로필========")
print(profile_dict)

count, solved_list = get_solved(user_id)
print(f"========{user_id}님이 푼 문제들({count})========")
print(solved_list)

print(f"========{user_id}님이 푼 문제들의 레벨별 갯수========")
count_by_level_list = get_count_by_level(user_id)
print(count_by_level_list)

group_users = get_user_in_group(group_id)
print(f"========{group_id}에 속한 유저들========")
print(group_users)

group_problems = get_solved_by_group(group_id)
print(f"========{group_id}에 속한 유저들이 푼 문제들========")
print(group_problems)"""

print(get_unsolved_by_group(group_id))
