# boj-organization-solved-list

boj 특정 조직 내 인원이 풀지 못한 문제 리스트를 출력해주는 프로젝트

## 사용법

1. boj_organization_solved_list.py의 group_id 변수 값을 수정해주세요
1-1. 특정 그룹의 id는 https://solved.ac/api/v3/search/user?query={유저id} api를 통해서 가입된 그룹들의 id를 알 수 있습니다.
2. boj_organization_solved_list.py를 실행하면 난이도 순으로 못푼 문제 리스트를 출력합니다.
2-1. 특정 난이도의 못 푼 문제가 20문제 이하라면 다음 난이도의 못 푼 문제 리스트까지 출력합니다.
