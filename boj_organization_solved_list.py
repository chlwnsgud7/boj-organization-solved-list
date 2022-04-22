import json
from time import sleep
import requests
import sqlite3
from db_setting import db_setting


def get_profile(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user의 프로필 정보 중 일부를 반환해줌
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


def check_user(user_id):
    conn = sqlite3.connect(str(group_id)+'_unsolved.db')
    cur = conn.cursor()

    url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=level&direction=desc"
    r_solved = requests.get(url)
    if r_solved.status_code == requests.codes.ok:
        solved = json.loads(r_solved.content.decode('utf-8'))
        count = solved.get("count")
        pages = (count - 1) // 100 + 1
        cur.execute("SELECT solved FROM user WHERE name = ?", (user_id,))
        user_solved = cur.fetchone()
        if user_solved is None:
            cur.execute("INSERT INTO user (name, solved) VALUES (?, ?)", (user_id, count))
        elif user_solved[0] == count:
            pages = -1
        elif user_solved[0] != count:
            cur.execute("UPDATE user SET solved = ? WHERE name = ?", (count, user_id))
        conn.commit()
        cur.close()
        conn.close()
    else:
        print("푼 문제들 요청 실패")
        print(r_solved.status_code)
    return pages


def get_solved(user_id, pages):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user가 푼 문제들 번호(level 높은 순)를 list로 반환해줌
    :param str user_id: 사용자id
    :return: 해당 user가 푼 문제들 번호
    :rtype: list
    """
    url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=level&direction=desc"
    solved_problems = []
    for page in range(pages):
        sleep(5)
        page_url = f"{url}&page={page + 1}"
        print(page_url)
        r_solved = requests.get(page_url)
        if r_solved.status_code == requests.codes.ok:
            solved = json.loads(r_solved.content.decode('utf-8'))
            items = solved.get("items")
            for item in items:
                solved_problems.append(item.get("problemId"))
            # print("푼 문제수와 젤 고난이도 문제 1개만 >>>", count, solved_problems[0])
        else:
            print("푼 문제들 요청 실패")
            print(r_solved.status_code)
            print(url)
    return solved_problems


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


def get_solved_by_group(group_id):
    """
    정보 조회 - group_id를 입력하면 백준 사이트에서 해당 group의 user들이 푼 문제들을 반환해줌
    :param group_id: 그룹id
    :return: group에서 푼 총 문제
    :rtype: set
    """
    conn = sqlite3.connect(str(group_id)+'_unsolved.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM problem")
    problems = [row[0] for row in cur.fetchall()]
    group_users = get_user_in_group(group_id)
    group_problems = set()
    group_problems.update(problems)
    n = 1
    for user in group_users:
        sleep(5)
        print(n, " / ", len(group_users))
        pages = check_user(user)
        if pages == -1:
            continue
        get_solved_by_user = get_solved(user, pages)
        print(get_solved_by_user)
        group_problems.update(get_solved_by_user)
        n = n + 1
    return group_problems


def get_problem_by_level(level):
    """
    정보 조회 - level을 입력하면 백준 사이트에서 해당 level에 해당하는 문제들을 반환해줌
    :param level:
    :return: 해당 level의 문제들
    """
    url = f"https://solved.ac/api/v3/search/problem?query=tier%3A{level}"
    r_level_problem = requests.get(url)
    if r_level_problem.status_code == requests.codes.ok:
        level_problem = json.loads(r_level_problem.content.decode('utf-8'))
        pages = (level_problem.get("count") - 1) // 100 + 1
    else:
        print("난이도별  문제 요청 실패")

    problems = set()
    for page in range(pages):
        page_url = f"{url}&page={page + 1}"
        print(page_url)
        r_level_problem = requests.get(page_url)
        if r_level_problem.status_code == requests.codes.ok:
            level_problem = json.loads(r_level_problem.content.decode('utf-8'))
            items = level_problem.get("items")
            for item in items:
                problems.add(item.get("problemId"))
        else:
            print("난이도별  문제 요청 실패")
    return problems


def get_unsolved_by_group(group_id):
    """
    정보 조회 - group_id를 입력하면 백준 사이트에서 해당 group의 user들이 풀지 않은 문제들을 level별로 반환해줌
    :param group_id: 그룹id
    :return: 못 푼 문제가 20문제 초과로 존재하는 level의 풀지 않은 문제들
    :rtype: set
    """
    conn = sqlite3.connect(str(group_id)+'_unsolved.db')
    cur = conn.cursor()

    solved_problem = get_solved_by_group(group_id)
    for problem in solved_problem:
        cur.execute("INSERT OR IGNORE INTO problem(id) VALUES(?)", (problem,))
    conn.commit()
    cur.close()
    conn.close()
    for level in range(30):
        level_problem = get_problem_by_level(level + 1)
        unsolved_level_problem = level_problem - solved_problem
        if len(unsolved_level_problem) == 0:
            print(f"all solved level {level + 1}")
        elif len(unsolved_level_problem) <= 20:
            print(f"little left level {level + 1}")
            print(unsolved_level_problem)
        else:
            return unsolved_level_problem
    print(f"all solved boj")


user_id = "siontama"
group_id = "1007"

"""profile_dict = get_profile(user_id)
print(f"========{user_id}님의 프로필========")
print(profile_dict)

count, solved_list = get_solved(user_id)
print(f"========{user_id}님이 푼 문제들({count})========")
print(solved_list)

group_users = get_user_in_group(group_id)
print(f"========{group_id}에 속한 유저들========")
print(group_users)

group_problems = get_solved_by_group(group_id)
print(f"========{group_id}에 속한 유저들이 푼 문제들========")
print(group_problems)"""

db_setting(group_id)
print(get_unsolved_by_group(group_id))
