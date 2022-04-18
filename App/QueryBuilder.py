from pypika import Query, Table, Field, Order
from pypika import functions as fn
import random
#ALTER: Table 수정

#속성과 테이블을 넣으면 랜덤한 해당속성의 데이터가 튀어나오는 함수
def pull_table_data(table, proper):
    table_list = table.objects.values(proper)
    table_list = list(table_list)
    count = len(table_list)
    result = table_list[random.randint(0, count-1)][proper]
    return result
#PK키 찾기 함수

class OurQuery:
    def __init__(self, table, tableName):
        self.table = table
        self.tableName = tableName

    def select_query(self):
        target_table = self.table
        tableName = self.tableName
        #table로 부터 속성의 이름을 알아내는 과정
        Q = target_table.objects.values()
        #table의 속성명 저장
        proper = []
        call_random = 0
        for key in Q[0]:
            proper.append(key)
        count = len(proper)
        result = [] #완성된 쿼리문을 담는 결과 리스트
        random_proper = []
        random_proper = random.sample(proper, random.randint(1, count)) #randomNum 리스트에 proper 요소를 랜덤갯수만큼 추출해서 넣기

        tmp = target_table.objects.values(random_proper[0]) #tmp에는 col_type의 모든 테이블 보유중
        for check in tmp:
            col_type = (check[random_proper[0]])#랜덤으로 고른 속성의 값의 변수 type 체크
            print(type(col_type))
            break




        #아래함수부터 본격 쿼리문 뽑기
        query_num = 0
        if query_num == 0:#기본테이블 전체 출력
            q = Query.from_(tableName).select("*")
            result.append(str(q))
        if True:#필요한 요소만 출력
            input_proper = ",".join(random_proper)
            q = Query.from_(tableName).select(input_proper)
            result.append(str(q))
        if True: #중복없이 출력하기
            input_proper = ",".join(random_proper)
            input_proper = "DISTNCT("+ input_proper + ")"
            q = Query.from_(tableName).select(input_proper)
            result.append(str(q))
        #group by 와 having은 일단 보류


        #랜덤으로 고른 속성이 int인 경우? 0속성 인덱스의 0번 -> between, AVG, MAX, MIN,SUM
        if type(col_type) is int or type(col_type) is float:
            num = pull_table_data(target_table, random_proper[0]) #num에는 현재 랜덤한 int형 테이블값이 들어있다.
            num2 = pull_table_data(target_table, random_proper[0]) #숫자 범위자료형을 위한 변수 num2
            while num == num2: #같지않은것이 뽑힐때까지 계속 뽑는다.
                num2 = pull_table_data(target_table, random_proper[0])
            if True:#num 이상인 테이블 출력
                q = Query.from_(tableName).select("*")
                q = str(q)
                q += " WHERE " + random_proper[0] + " >= " + str(num)
                result.append(q)
            if True: #이하
                q = Query.from_(tableName).select("*")
                q = str(q)
                q += " WHERE " + random_proper[0] + " <= " + str(num)
                result.append(q)
            if True: #같은경우
                q = Query.from_(tableName).select("*")
                q = str(q)
                q += " WHERE " + random_proper[0] + " = " + str(num)
                result.append(q)
            if True: #MAX값
                input_proper = "MAX("+random_proper[0]+")"
                q = Query.from_(tableName).select(input_proper)
                result.append(str(q))
            if True:  # MIN값
                input_proper = "MIN(" + random_proper[0] + ")"
                q = Query.from_(tableName).select(input_proper)
                result.append(str(q))
            if True: #MAX와 MIN의 차이를 출력하라
                input_proper = "MIN(" + random_proper[0] + ")" + " - MIN(" + random_proper[0] + ")"
                q = Query.from_(tableName).select(input_proper)
                result.append(str(q))
            if True:# tmp2 ~ tmp1 사이에 있는 테이블을 출력
                tmp1, tmp2 = max(num,num2), min(num,num2)
                q = Query.from_(tableName).select("*")
                q = str(q)
                q += " WHERE " + random_proper[0] + " BETWEEN " + str(tmp2) + " AND " + str(tmp1)
                result.append(q)
            if True: #tmp2 ~ tmp1 사이가 아닌 테이블을 출력
                tmp1, tmp2 = max(num, num2), min(num, num2)
                q = Query.from_(tableName).select("*")
                q = str(q)
                q += " WHERE " + random_proper[0] + " NOT BETWEEN " + str(tmp2) + " AND " + str(tmp1)
            if True:#내림차순 정렬
                q = Query.from_(tableName).select("*").orderby(random_proper[0], order=Order.desc)
                q = str(q)
                result.append(q)
            if True:#오름차순 정렬
                q = Query.from_(tableName).select("*").orderby(random_proper[0])
                q = str(q)
                result.append(q)

        if type(col_type) is str:#문자열인 경우
            if True:  # 내림차순 정렬
                q = Query.from_(tableName).select("*").orderby(random_proper[0], order=Order.desc)
                q = str(q)
                result.append(q)
            if True:  # 오름차순 정렬
                q = Query.from_(tableName).select("*").orderby(random_proper[0])
                q = str(q)
                result.append(q)
        return result




        #INSERT
        #DELETE
        #UPDATE