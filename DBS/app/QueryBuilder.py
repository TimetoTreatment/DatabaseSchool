import datetime

from pypika import Query, Table, Field, Order
from pypika import functions as fn
import random
import datetime as dt
import string
#ALTER: Table 수정
lowercase_letters = string.ascii_lowercase
def lowercase_word():
    word = ''
    random_word_length = random.randint(1,10)
    while len(word) != random_word_length:
        word += random.choice(lowercase_letters)
    return word

#속성과 테이블을 넣으면 랜덤한 해당속성의 데이터가 튀어나오는 함수
def pull_table_data(table, proper):
    table_list = table.objects.values(proper)
    table_list = list(table_list)
    count = len(table_list)
    result = table_list[random.randint(0, count-1)][proper]
    return result
#PK키 찾기 함수

class OurQuery:
    def __init__(self, table, tableName, count):
        self.table = table
        self.tableName = tableName
        self.count = count

    def select_query(self):
        target_table = self.table
        tableName = self.tableName
        query_count = self.count
        #table로 부터 속성의 이름을 알아내는 과정
        Q = target_table.objects.values()
        #table의 속성명 저장
        proper = []
        date_type = dt.datetime.now()
        call_random = 0
        for key in Q[0]:
            proper.append(key)
        count = len(proper)
        result = {} #완성된 쿼리문을 담는 결과 리스트
        result = set()

        # print(random_proper[0])


        # if type(date_type) == type(col_type): #날짜 변수인 경우에는
        #      print()
        #아래함수부터 본격 쿼리문 뽑기
        textres = []
        query_num = 1
        # if query_num == 0:#기본테이블 전체 출력
        #     q = Query.from_(tableName).select("*")
        #     result.add(str(q))
        #     textres.append(str(tableName)+ " 테이블에서 모든 데이터를 조회하시오")
        # if query_num == 0:#필요한 요소만 출력
        #     input_proper = ",".join(random_proper)
        #     q = Query.from_(tableName).select(input_proper)
        #     result.add(str(q))
        #     textres.append(str(tableName) + " 테이블에서" + str(input_proper) + " column에서만 데이터를 조회하시오")
        # if query_num == 0: #중복없이 출력하기
        #     input_proper = ",".join(random_proper)
        #     input_proper = "DISTNCT("+ input_proper + ")"
        #     q = Query.from_(tableName).select(input_proper)
        #     result.add(str(q))
        #     textres.append(str(tableName) + " 테이블에서 " + str(input_proper) + " column에서 데이터를 중복값 없이 출력하시오")
        #group by 와 having은 일단 보류
        while len(result) !=  query_count:
            random_proper = []
            random_proper = random.sample(proper, random.randint(1, count))  # randomNum 리스트에 proper 요소를 랜덤갯수만큼 추출해서 넣기
            # print(proper)
            tmp = target_table.objects.values(random_proper[0])  # tmp에는 col_type의 모든 테이블 보유중
            for check in tmp:
                col_type = (check[random_proper[0]])  # 랜덤으로 고른 속성의 값의 변수 type 체크
                # print(type(col_type))
                break

            r_num = random.randint(0, 9)
            num = pull_table_data(target_table, random_proper[0])  # num에는 현재 랜덤한 int형 테이블값이 들어있다.
            num2 = pull_table_data(target_table, random_proper[0])  # 숫자 범위자료형을 위한 변수 num2
            while num == num2:  # 같지않은것이 뽑힐때까지 계속 뽑는다.
                num2 = pull_table_data(target_table, random_proper[0])
            sel_random = random.randint(1, count)
            select_str = ""
            tmp_set = {} #랜덤한 속성명을 담는 set 집합
            tmp_set = set()
            while len(tmp_set) != sel_random:
                tmp_set.add(proper[random.randint(0, count - 1)])

            tmp_set = str(tmp_set).strip('{}')
            tmp_set = tmp_set.replace('\'', "")
            #랜덤으로 고른 속성이 int인 경우? 0속성 인덱스의 0번 -> between, AVG, MAX, MIN,SUM
            if type(col_type) is int or type(col_type) is float:
                if r_num == 0:#num 이상인 테이블 출력
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q += " WHERE " + random_proper[0] + " >= " + str(num)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column중 " + str(num) + " 이상인 값들을 출력하시오")
                elif r_num == 1: #이하
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q += " WHERE " + random_proper[0] + " <= " + str(num)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column중 " + str(num) + " 이하인 값들을 출력하시오")
                elif r_num == 2: #같은경우
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q += " WHERE " + random_proper[0] + " = " + str(num)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column중 " + str(num) + " 과 같은 값들을 출력하시오")
                elif r_num == 3: #MAX값
                    input_proper = "MAX("+random_proper[0]+")"
                    q = Query.from_(tableName).select(input_proper)
                    result.add(str(q))
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column의 최대값을 출력하시오")
                elif r_num == 4:  # MIN값
                    input_proper = "MIN(" + random_proper[0] + ")"
                    q = Query.from_(tableName).select(input_proper)
                    result.add(str(q))
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column의 최솟값을 출력하시오")
                elif r_num == 5: #MAX와 MIN의 차이를 출력하라
                    input_proper = "MAX(" + random_proper[0] + ")" + " - MIN(" + random_proper[0] + ")"
                    q = Query.from_(tableName).select(input_proper)
                    result.add(str(q))
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column의 최대값과 최솟값의 차이를 출력하시오")
                elif r_num == 6:# tmp2 ~ tmp1 사이에 있는 테이블을 출력
                    tmp1, tmp2 = max(num,num2), min(num,num2)
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q += " WHERE " + random_proper[0] + " BETWEEN " + str(tmp2) + " AND " + str(tmp1)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + str(tmp2) + "과" + str(tmp1) + " 사이값인 데이터들을 출력하시오")
                elif r_num == 7: #tmp2 ~ tmp1 사이가 아닌 테이블을 출력
                    tmp1, tmp2 = max(num, num2), min(num, num2)
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q += " WHERE " + random_proper[0] + " NOT BETWEEN " + str(tmp2) + " AND " + str(tmp1)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + str(tmp2) + "과" + str(tmp1) + " 사이에 있지 않는 데이터들을 출력하시오")
                elif r_num == 8:#내림차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0], order=Order.desc)
                    q = str(q)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 내림차순으로 정렬하시오")
                elif r_num == 9:#오름차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0])
                    q = str(q)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 오름차순으로 정렬하시오")

            elif type(col_type) is str:#문자열인 경우
                r_num = random.randint(0, 4)
                if r_num == 0:  # 내림차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0], order=Order.desc)
                    q = str(q)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 내림차순으로 정렬하시오")
                elif r_num == 1:  # 오름차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0])
                    q = str(q)
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 오름차순으로 정렬하시오")
                elif r_num == 2: #문자열일 경우 첫번째 문자열로 시작하는 같은 데이터 조회
                    meta_data = str(pull_table_data(target_table , random_proper[0]))
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q + " WHERE " + random_proper[0] +" LIKE " + "\'" + meta_data[0] + "%\'"
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "'"+meta_data[0]+"'" + "인 문자로 시작하는 데이터를 조회하시오")
                elif r_num == 3: #문자열일 경우 해당 문자가 들어가는 테이블 조회
                    meta_data = str(pull_table_data(target_table, random_proper[0]))
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q + " WHERE " + random_proper[0] + " LIKE " + "\'%" + meta_data[0] + "%\'"
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "'"+meta_data[0]+"'" + "인 문자가 포함되는 데이터를 조회하시오")
                elif r_num == 4: #문자열일 경우 랜덤한 데이터를 뽑아서 같은 끝 문자로 끝나는 데이터
                    meta_data = str(pull_table_data(target_table, random_proper[0]))
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q + " WHERE " + random_proper[0] + " LIKE " + "\'%" + meta_data[len(meta_data) - 1] + "\'"
                    result.add(q)
                    textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "'" + meta_data[len(meta_data) - 1] + "'" + "인 문자로 끝나는 데이터를 조회하시오")
        result = list(result)
        for i in range(len(result)):
            result[i] = result[i].replace("\"","")
        return result


    #INSERT
    def insert_query(self):
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

    #DELETE
    def delete_query(self):
        target_table = self.table
        tableName = self.tableName
        tablecount = self.count
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

        while len(result) != tablecount:
            update_query = Q[random.randint(0, len(Q) - 1)]#랜덤한 테이블의 행을 골라서 가져오기
            print(update_query , "에 해당하는 쿼리문을 삭제")
            proper_num =random.randint(0, len(random_proper)-1)
            query = "DELETE FROM " + str(tableName) +" WHERE " + str(random_proper[proper_num]) + " = "+ str(update_query[random_proper[proper_num]])
            print(random_proper[proper_num], " 속성이 " , update_query[random_proper[proper_num]] , " 에 해당하는 값의 테이블을 삭제")
            result.append(query)
        return result
    #UPDATE
    def update_query(self):
        target_table = self.table
        tableName = self.tableName
        query_count = self.count
        #table로 부터 속성의 이름을 알아내는 과정
        Q = target_table.objects.values()
        #table의 속성명 저장
        proper = []
        call_random = 0
        for key in Q[0]:
            proper.append(key)
        count = len(proper)
        result = {} #완성된 쿼리문을 담는 결과 리스트
        result = set()
        random_proper = []
        random_proper = random.sample(proper, random.randint(1, count)) #randomNum 리스트에 proper 요소를 랜덤갯수만큼 추출해서 넣기
        tmp = target_table.objects.values(random_proper[0]) #tmp에는 col_type의 모든 테이블 보유중


        while query_count != len(result):
            tmp_set = {}  # 랜덤한 속성명을 담는 set 집합
            tmp_set = set()
            sel_random = random.randint(1, count)
            while len(tmp_set) != sel_random:
                tmp_set.add(proper[random.randint(0, count - 1)])

            tmp_set = str(tmp_set).strip('{}')
            tmp_set = tmp_set.replace('\'', "")
            update_query = Q[random.randint(0, len(Q)-1)]

            tmp_set = tmp_set.replace(' ',"").split(',')
            for i in range(len(tmp_set)):
                if type(update_query[tmp_set[i]]) is int:
                    tmp_set[i] = (tmp_set[i] + "=" + str(random.randint(1, update_query[tmp_set[i]])))
                else:
                    random_word = lowercase_word()
                    tmp_set[i] = (tmp_set[i] + "=" +str(random_word))

            query = "UPDATE "+ str(tableName) + " SET "+ str(tmp_set)
            query = query.replace('\'',"")
            query = query.replace('[', "")
            query = query.replace(']', "")
            result.add(query)
            print(update_query, "해당하는 행을 변경하는 쿼리문입니다.")
        return result