from pypika import Query, Table, Database, Order
from random import *

#ALTER: Table 수정

#속성과 테이블을 넣으면 랜덤한 해당속성의 데이터가 튀어나오는 함수
def pull_table_data(table, proper):
    table_list = table.objects.values(proper)
    table_list = list(table_list)
    count = len(table_list)
    result = table_list[randint(0, count-1)][proper]
    return result
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
        randomNum = randint(0, count-1) #property 개수 index 안에서 난수발생
        randomNum2 = randint(0, count-1) #radomNum과 같지않은 다른 랜덤한 요소 뽑기
        while randomNum == randomNum2:
            randomNum2 = randint(0, count - 1)

        tmp = target_table.objects.values(proper[randomNum])
        for check in tmp:
            col_type = (check[proper[randomNum]])#랜덤으로 고른 속성의 값의 변수 type 체크
            break



        #간단 Select 1
        q = Query.from_(tableName).select(proper[randomNum])
        result.append(str(q))

        q = Query.from_(tableName).select(proper[randomNum], proper[randomNum2])
        result.append(str(q))
        return result
        # #랜덤으로 고른 속성이 int인 경우? -> between, AVG, MAX, MIN,SUM
        # if col_type == "<class 'int'>":
        #     call_random = randint(0,4)
        #     if call_random == 0: #beteen
        #         q = Query.from_(tableName).select(proper[randomNum])
        #         query = str(q)
        #     elif call_random == 1:#AVG
        #         q = Query.from_(tableName).select(proper[randomNum])
        #         query = str(q)
        #     elif call_random == 2:#MAX
        #         q = Query.from_(tableName).select(proper[randomNum])
        #         query = str(q)
        #     elif call_random == 3:#MIN
        #         q = Query.from_(tableName).select(proper[randomNum])
        #         query = str(q)
        #     elif call_random == 4:#SUM
        #         q = Query.from_(tableName).select(proper[randomNum])
        #         query = str(q)
