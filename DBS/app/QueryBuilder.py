
import datetime
from turtle import update
from pypika import Query, Table, Field, Order
from pypika import functions as fn
import pandas as pd
import numpy as np
import random
import datetime as dt
import string
from .Queryrecommand import AboutOurQuery
from collections import defaultdict
#ALTER: Table 수정
lowercase_letters = string.ascii_lowercase
OnAndOff = True
def lowercase_word():
    word = ''
    random_word_length = random.randint(1,10)
    while len(word) != random_word_length:
        word += random.choice(lowercase_letters)
    return word

#유일key값을 뽑는 함수
def find_key(table, proper):
    answer = []
    for p in proper:
        if len(table[p]) ==  len(set(table[p])):
            answer.append(p)
    return answer
#메인키를 제외한 속성을 뱉기
def non_find_key(table, proper):
    answer = []
    for p in proper:
        if len(table[p]) !=  len(set(table[p])):
            answer.append(p)
    return answer


#속성과 테이블을 넣으면 랜덤한 해당속성의 데이터가 튀어나오는 함수
def pull_table_data(table, proper):
    table_list = table.objects.values(proper)
    table_list = list(table_list)
    count = len(table_list)
    result = table_list[random.randint(0, count-1)][proper]
    return result
#PK키 찾기 함수


def type_to_string(its_type):
    date=dt.datetime.now()
    t=''
    if its_type==int:
        t="INT"
    if its_type==str:
        t="STRING"
    if its_type==bool:
        t="BOOL"
    if its_type==float:
        t="FLOAT"
    if its_type==type(date):
        t="DATETIME"
    return t

def table_info(tableName, proper, proper_type):
    txt = tableName + "테이블이 있습니다. " + tableName +"테이블은 다음처럼 "
    for i in range(len(proper)):
        txt += "<span class='text-attribute'>" + str(proper[i]) +"(" + type_to_string(proper_type[i]) + ")</span>" + " "
    txt += "의 column(type) " + "구조로 이루여져 있습니다."
    return txt

def update_info(s):
    a=[]
    t=''
    for i in s:
        a.append(s[i])
    for i in a:
        t += str(i)+ " "
    return t

def insert_col(proper):
    txt=''
    for i in range(len(proper)):
        txt += "<span class='text-attribute'>" + (proper[i]) + "</span>" + " "
    return txt

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
        dic={}
        dic=dict()
        # print(random_proper[0])

        proper_type=[]
        for i in range(len(proper)):
                tm = target_table.objects.values(proper[i])
                for check in tm:
                    ctype=(check[proper[i]])
                    proper_type.append(type(ctype))
                    break

        # if type(date_type) == type(col_type): #날짜 변수인 경우에는
        #      print()
        #아래함수부터 본격 쿼리문 뽑기
        textres = []
        txt1=[]
        query_num = 1
        if query_num == 0:#기본테이블 전체 출력
           q = Query.from_(tableName).select("*")
           result.add(str(q))
           txt1.append(table_info(tableName, proper, proper_type))
           txt1.append(str(tableName) + " 테이블에서 모든 테이블을 조회하는 SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다")
           if OnAndOff == True:
            txt1.append(AboutOurQuery(str(q)).Similar())
           elif OnAndOff == False:
            txt1.append("하")
           dic[str(q)]=txt1

           txt1=[]
           textres=[]

        
        if query_num == 0:#필요한 요소만 출력
           input_proper = ",".join(random_proper)
           q = Query.from_(tableName).select(input_proper)
           result.add(str(q))
           txt1.append(table_info(tableName, proper, proper_type))
           txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" + str(input_proper) + " column</span>에서 데이터를 조회하는 SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
           if OnAndOff == True:
            txt1.append(AboutOurQuery(str(q)).Similar())
           elif OnAndOff == False:
            txt1.append("하")
           dic[str(q)]=txt1
           txt1=[]
           textres=[]
        if query_num == 0: #중복없이 출력하기
           input_proper = ",".join(random_proper)
           input_tem = input_proper
           input_proper = "DISTNCT("+ input_proper + ")"
           q = Query.from_(tableName).select(input_proper)
           result.add(str(q))
           txt1.append(table_info(tableName, proper, proper_type))
           txt1.append(str(tableName) + " 테이블에서 " + str(input_tem) + " column에서 데이터를 <span class='text-attribute'>중복값 없이 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
           if OnAndOff == True:
            txt1.append(AboutOurQuery(str(q)).Similar())
           elif OnAndOff == False:
            txt1.append("하")
           dic[str(q)]=txt1
           txt1=[]
           textres=[]
        #group by 와 having은 일단 보류
        while len(result) !=  query_count:
            random_proper = []
            random_proper = random.sample(proper, random.randint(1, count))  # randomNum 리스트에 proper 요소를 랜덤갯수만큼 추출해서 넣기
            # print(proper)
            tmp = target_table.objects.values(random_proper[0])  # tmp에는 col_type의 모든 테이블 보유중
            for check in tmp:
                col_type = (check[random_proper[0]])  # 랜덤으로 고른 속성의 값의 변수 type 체크
                break


            sel_random = random.randint(1, count)
            select_str = ""
            tmp_set = {} #랜덤한 속성명을 담는 set 집합
            tmp_set = set()
            while len(tmp_set) != sel_random:
                tmp_set.add(proper[random.randint(0, count - 1)])

            tmp_set = str(tmp_set).strip('{}')
            tmp_set = tmp_set.replace('\'', "")
            r_num = random.randint(0, 16)
            #랜덤으로 고른 속성이 int인 경우? 0속성 인덱스의 0번 -> between, AVG, MAX, MIN,SUM
            if type(col_type) is int or type(col_type) is float:
                num = pull_table_data(target_table, random_proper[0])  # num에는 현재 랜덤한 int형 테이블값이 들어있다.
                num2 = pull_table_data(target_table, random_proper[0])  # 숫자 범위자료형을 위한 변수 num2
                while num == num2:  # 같지않은것이 뽑힐때까지 계속 뽑는다.
                    num2 = pull_table_data(target_table, random_proper[0])


                if r_num == 0:#num 이상인 테이블 출력
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q.replace("\"",'')
                    q += " WHERE " + random_proper[0] + " >= " + str(num)
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 "+ random_proper[0] + " column에서 " + "<span class='text-attribute'>" + str(num) + " 이상인 값들을 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 1: #이하
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q.replace("\"",'')
                    q += " WHERE " + random_proper[0] + " <= " + str(num)
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>" + str(num) + " 이하인 값들을 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 2: #같은경우
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q.replace("\"",'')
                    q += " WHERE " + random_proper[0] + " = " + str(num)
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>" + str(num) + " 과 같은 값들을 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 3: #MAX값
                    input_proper = "MAX("+random_proper[0]+")"
                    q = Query.from_(tableName).select(input_proper)
                    q= str(q)
                    q = q.replace("\"",'')
                    result.add(str(q))
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + " <span class='text-attribute'>최대값을 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column의 최대값을 출력하시오")
                elif r_num == 4:  # MIN값
                    input_proper = "MIN(" + random_proper[0] + ")"
                    q = Query.from_(tableName).select(input_proper)
                    q= str(q)
                    q = q.replace("\"",'')
                    result.add(str(q))
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>최솟값을 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1

                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column의 최솟값을 출력하시오")
                elif r_num == 5: #MAX와 MIN의 차이를 출력하라
                    input_proper = "MAX(" + random_proper[0] + ")" + " - MIN(" + random_proper[0] + ")"
                    q = Query.from_(tableName).select(input_proper)
                    q= str(q)
                    q = q.replace("\"",'')
                    result.add(str(q))
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + " <span class='text-attribute'>최대값과 최솟값의 차이를 나타내는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column의 최대값과 최솟값의 차이를 출력하시오")
                elif r_num == 6:# tmp2 ~ tmp1 사이에 있는 테이블을 출력
                    tmp1, tmp2 = max(num,num2), min(num,num2)
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q.replace("\"",'')
                    q += " WHERE " + random_proper[0] + " BETWEEN " + str(tmp2) + " AND " + str(tmp1)
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>" + str(tmp2) + "과" + str(tmp1) + " 사이값들을 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + str(tmp2) + "과" + str(tmp1) + " 사이값인 데이터들을 출력하시오")
                elif r_num == 7: #tmp2 ~ tmp1 사이가 아닌 테이블을 출력
                    tmp1, tmp2 = max(num, num2), min(num, num2)
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q.replace("\"",'')
                    q += " WHERE " + random_proper[0] + " NOT BETWEEN " + str(tmp2) + " AND " + str(tmp1)
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>" + str(tmp2) + "과" + str(tmp1) + " 사이에 있지 않는 값들을 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + str(tmp2) + "과" + str(tmp1) + " 사이에 있지 않는 데이터들을 출력하시오")
                elif r_num == 8:#내림차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0], order=Order.desc)
                    q = str(q)
                    q = q.replace("\"",'')
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "데이터들을 <span class='text-attribute'>내림차순으로 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 내림차순으로 정렬하시오")
                elif r_num == 9:#오름차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0])
                    q = str(q)
                    q = q.replace("\"",'')
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" +random_proper[0] +"</span>" + " column에서 " + "데이터들을 <span class='text-attribute'>오름차순으로 조회하는</span> SQL문을 작성해 주세요. SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 오름차순으로 정렬하시오")
                elif r_num == 10: #rank 함수 활용 random_proper[0] 은 무조건 int 그리고 사전 정렬할 속성을 뽑아야한다.
                    #random_proper[0]의 수가 작은것부터 1~n까지의 순위를 매기고 (수가 같으면 순위도 같음 공동1등 가능) order type를 str이면 사전순으로 or 오름차순으로 정렬하시오
                    order_type = proper[random.randint(0, count - 1)]
                    q = Query.from_(tableName).select(tmp_set).orderby(order_type)
                    q = str(q)
                    q = q.split("FROM")
                    rank_str = ", rank() over(order by " + random_proper[0] + ") as ranking FROM"
                    q.insert(1, rank_str)
                    q = "".join(q)
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" + random_proper[0] +"</span>" + " column에서 " + "<span class='text-attribute'>작은수부터 순위를 매기고</span> " + "<span class='text-attribute'>" + str(order_type) +"</span>" + "는 <span class='text-attribute'>사전순으로(오름차순)</span> " + "조회하는 SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 11: #rank 함수 활용 random_proper[0] 은 무조건 int 그리고 사전 정렬할 속성을 뽑아야한다.
                    #random_proper[0]의 수가 큰 수부터 1~n까지의 순위를 매기고 (수가 같으면 순위도 같음 공동1등 가능) order type를 str이면 사전순으로 or 오름차순으로 정렬하시오
                    order_type = proper[random.randint(0, count - 1)]
                    q = Query.from_(tableName).select(tmp_set).orderby(order_type)
                    q = str(q)
                    q = q.split("FROM")
                    rank_str = ", rank() over(order by " + random_proper[0] + " DESC) as ranking FROM"
                    q.insert(1, rank_str)
                    q = "".join(q)
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" + random_proper[0] +"</span>" + " column에서 " + "<span class='text-attribute'>큰수부터 순위를 매기고</span> " + "<span class='text-attribute'>" + str(order_type) +"</span>" + "는 <span class='text-attribute'>사전순으로(오름차순)</span> " + "조회하는 SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 12: #rank 함수 활용 random_proper[0] 은 무조건 int 그리고 사전 정렬할 속성을 뽑아야한다.
                    #random_proper[0]의 수가 작은 수부터 1~n까지의 순위를 매기고 (수가 같으면 순위도 같음 공동1등 가능) order type를 str이면 사전역순으로 or 내림차순으로 정렬하시오
                    order_type = proper[random.randint(0, count - 1)]
                    q = Query.from_(tableName).select(tmp_set).orderby(order_type, order=Order.desc)
                    q = str(q)
                    q = q.split("FROM")
                    rank_str = ", rank() over(order by " + random_proper[0] + ") as ranking FROM"
                    q.insert(1, rank_str)
                    q = "".join(q)
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" + random_proper[0] +"</span>" + " column에서 " + "<span class='text-attribute'>작은수부터 순위를 매기고</span> " + "<span class='text-attribute'>" + str(order_type) +"</span>" + "는 <span class='text-attribute'>사전역순으로(내림차순)</span> " + "조회하는 SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 13: #rank 함수 활용 random_proper[0] 은 무조건 int 그리고 사전 정렬할 속성을 뽑아야한다.
                    #random_proper[0]의 수가 큰 수부터 1~n까지의 순위를 매기고 (수가 같으면 순위도 같음 공동1등 가능) order type를 str이면 사전역순으로 or 내림차순으로 정렬하시오
                    order_type = proper[random.randint(0, count - 1)]
                    q = Query.from_(tableName).select(tmp_set).orderby(order_type, order = Order.desc)
                    q = str(q)
                    q = q.split("FROM")
                    rank_str = ", rank() over(order by " + random_proper[0] + " DESC) as ranking FROM"
                    q.insert(1, rank_str)
                    q = "".join(q)
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" + random_proper[0] +"</span>" + " column에서 " + "<span class='text-attribute'>큰수부터 순위를 매기고</span> " + "<span class='text-attribute'>" + str(order_type) +"</span>" + "는 <span class='text-attribute'>사전역순으로(내림차순)</span> " + "조회하는 SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 14:
                    #random_proper[0]의 값의 평균보다 random_proper[0]의 속성이 크거나 같은 테이블 random_proper 의 오름차순으로 출력
                    q = Query.from_(tableName).select('*')
                    q = str(q)
                    q += " where " + random_proper[0] + " >= (SELECT avg(" + random_proper[0] + ") FROM " + tableName + ") "+ "ORDER BY " + random_proper[0]
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" + random_proper[0] + "</span>" + " column에서 " + "해당 column의 <span class='text-attribute'>평균보다 " + "크거나 같은</span> 데이터를 <span class='text-attribute'>오름차순으로 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                elif r_num == 15:
                    #random_proper[0]의 값의 평균보다 random_proper[0]의 속성이 크거나 같은 테이블 random_proper 의 내림차순으로 출력
                    q = Query.from_(tableName).select('*')
                    q = str(q)
                    q += " where " + random_proper[0] + " >= (SELECT avg(" + random_proper[0] + ") FROM " + tableName + ") "+ "ORDER BY " + random_proper[0] +" DESC"
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" +  random_proper[0] + "</span>" + " column에서 " + "해당 column의 <span class='text-attribute'>평균보다 " + "크거나 같은</span> 데이터를 <span class='text-attribute'>내림차순으로 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]

                elif r_num == 16:
                    #random_proper[0]의 값의 평균보다 random_proper[0]의 속성이 크거나 같은 테이블의 갯수를 출력
                    q = Query.from_(tableName).select('count(*)')
                    q = str(q)
                    q += " where " + random_proper[0] + " >= (SELECT avg(" + random_proper[0] + ") FROM " + tableName + ") "
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + "<span class='text-attribute'>" + random_proper[0] + "</span>" + " column에서 " + "해당 column의 <span class='text-attribute'>평균보다 " + "크거나 같은 테이블의 갯수를 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]


            elif type(col_type) is str:#문자열인 경우
                r_num = random.randint(0, 4)
                if r_num == 0:  # 내림차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0], order=Order.desc)
                    q = str(q)
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>내림차순으로 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 내림차순으로 정렬하시오")
                elif r_num == 1:  # 오름차순 정렬
                    q = Query.from_(tableName).select(tmp_set).orderby(random_proper[0])
                    q = str(q)
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>오름차순으로 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 데이터들을 오름차순으로 정렬하시오")
                elif r_num == 2: #문자열일 경우 첫번째 문자열로 시작하는 같은 데이터 조회
                    meta_data = str(pull_table_data(target_table , random_proper[0]))
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q + " WHERE " + random_proper[0] +" LIKE " + "\'" + meta_data[0] + "%\'"
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>" + "'" +meta_data[0]+"'" + "인 문자로 시작하는 데이터를 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "'"+meta_data[0]+"'" + "인 문자로 시작하는 데이터를 조회하시오")
                elif r_num == 3: #문자열일 경우 해당 문자가 들어가는 테이블 조회
                    meta_data = str(pull_table_data(target_table, random_proper[0]))
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q + " WHERE " + random_proper[0] + " LIKE " + "\'%" + meta_data[0] + "%\'"
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>" + "'" +meta_data[0]+"'" + "인 문자를 포함하는 데이터를 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "'"+meta_data[0]+"'" + "인 문자가 포함되는 데이터를 조회하시오")
                elif r_num == 4: #문자열일 경우 랜덤한 데이터를 뽑아서 같은 끝 문자로 끝나는 데이터
                    meta_data = str(pull_table_data(target_table, random_proper[0]))
                    q = Query.from_(tableName).select(tmp_set)
                    q = str(q)
                    q = q.replace("\"", "")
                    q = q + " WHERE " + random_proper[0] + " LIKE " + "\'%" + meta_data[len(meta_data) - 1] + "\'"
                    q = q.replace("\"", "")
                    result.add(q)
                    txt1.append(table_info(tableName, proper, proper_type))
                    txt1.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "<span class='text-attribute'>" + "'" +meta_data[len(meta_data) -1]+"'" + "인 문자로 끝나는 데이터를 조회하는</span> SQL문을 작성해 주세요. " + "SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                    if OnAndOff == True:
                        txt1.append(AboutOurQuery(str(q)).Similar())
                    elif OnAndOff == False:
                        txt1.append("하")
                    dic[str(q)]=txt1
                    textres=[]
                    txt1=[]
                    #textres.append(str(tableName) + " 테이블에서 " + random_proper[0] + " column에서 " + "'" + meta_data[len(meta_data) - 1] + "'" + "인 문자로 끝나는 데이터를 조회하시오")
        result = list(result)
        for i in range(len(result)):
            result[i] = result[i].replace("\"","")
        
        return dic


    #INSERT
    def insert_query(self):
        target_table = self.table
        tableName = self.tableName
        result = []
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
        pd_table = pd.DataFrame(Q)
        table_dict = defaultdict(list)
        query_proper = []
        proper_type = []
        txt1=[]
        dic = {}
        dic = dict()
        for i in range(len(proper)):
            for data in pd_table[proper[i]]:
                table_dict[proper[i]].append(data)
        
        for i in range(len(proper)):
                tm = target_table.objects.values(proper[i])
                for check in tm:
                    ctype=(check[proper[i]])
                    proper_type.append(type(ctype))
                    break

        for p in proper:
            if p == 'id':
                query_proper.append(str(len(table_dict[p]) + 1))
                continue
            if type(pull_table_data(target_table, p)) is str:
                query_proper.append("\"" + lowercase_word() + "\"")
            else:
                temp1 = max(table_dict[p])
                temp2 = min(table_dict[p])
                query_proper.append(str(random.randint(temp1, temp1+(temp1 - temp2))))

        query_proper = ", ".join(query_proper)
        query = "INSERT INTO " + tableName + " VALUES(" + query_proper + ")"
        print(query)
        result.append(query)
        txt1.append(table_info(tableName, proper, proper_type))
        txt1.append(str(tableName) + "테이블에서 " + insert_col(proper) + "column에 순차적으로 " + query_proper + "의 데이터를 삽입하는 SQL문을 작성해 주세요." + " SQL을 실행하면 다음과 같이 출력되어야 합니다.")
        if OnAndOff == True:
            txt1.append(AboutOurQuery(str(query)).Similar())
        elif OnAndOff == False:
            txt1.append("하")
        dic[str(query)] = txt1
        txt1=[]
        return dic

    #DELETE
    def delete_query(self):
        target_table = self.table
        tableName = self.tableName
        tablecount = self.count
        #table로 부터 속성의 이름을 알아내는 과정
        Q = target_table.objects.values()
        #table의 속성명 저장
        proper = []
        dic={}
        dic=dict()
        call_random = 0
        for key in Q[0]:
            proper.append(key)
        count = len(proper)
        result = [] #완성된 쿼리문을 담는 결과 리스트
        random_proper = []
        random_proper = random.sample(proper, random.randint(1, count)) #randomNum 리스트에 proper 요소를 랜덤갯수만큼 추출해서 넣기
        tmp = target_table.objects.values(random_proper[0]) #tmp에는 col_type의 모든 테이블 보유중
        proper_type=[]
        txt1=[]
        textres=[]
        for i in range(len(proper)):
                tm = target_table.objects.values(proper[i])
                for check in tm:
                    ctype=(check[proper[i]])
                    proper_type.append(type(ctype))
                    break

        while len(result) != tablecount:
            update_query = Q[random.randint(0, len(Q) - 1)]#랜덤한 테이블의 행을 골라서 가져오기
            #print(update_query , "에 해당하는 쿼리문을 삭제")
            proper_num =random.randint(0, len(random_proper)-1)
            query = "DELETE FROM " + str(tableName) +" WHERE " + str(random_proper[proper_num]) + " = \'"+ str(update_query[random_proper[proper_num]]) + "\'"
            #print(random_proper[proper_num], " 속성이 " , update_query[random_proper[proper_num]] , " 에 해당하는 값의 테이블을 삭제")
            result.append(query)
            txt1.append(table_info(tableName, proper, proper_type))
            txt1.append(str(tableName) +"테이블에서 " + "<span class='text-attribute'>" + str(random_proper[proper_num]) + "에 해당하는 데이터를 삭제하는</span>" + " SQL문을 작성해주세요." + " SQL을 실행하면 다음과 같이 출력되어야 합니다.")
            if OnAndOff == True:
                txt1.append(AboutOurQuery(str(query)).Similar())
            elif OnAndOff == False:
                txt1.append("하")
            dic[str(query)]=txt1
            textres=[]
            txt1=[]
        return dic
    #UPDATE
    def update_query(self):
        target_table = self.table
        tableName = self.tableName
        query_count = self.count
        #table로 부터 속성의 이름을 알아내는 과정
        Q = target_table.objects.values()
        #table의 속성명 저장
        proper = []
        dic={}
        dic=dict()
        call_random = 0
        for key in Q[0]:
            proper.append(key)
        table_proper=[]
        for key in Q[0]:
            table_proper.append(key)
        table_proper_type=[]
        result = {} #완성된 쿼리문을 담는 결과 리스트
        result = set()
        random_proper = []
        txt1=[]
        textres=[]
        count = len(proper)
        random_proper = random.sample(proper, random.randint(1, count)) #randomNum 리스트에 proper 요소를 랜덤갯수만큼 추출해서 넣기
        tmp = target_table.objects.values(random_proper[0]) #tmp에는 col_type의 모든 테이블 보유중
        table = pd.DataFrame(Q)
        mainkey = find_key(table,proper)
        proper = non_find_key(table,proper)
        count = len(proper)
        for i in range(len(table_proper)):
                tm = target_table.objects.values(table_proper[i])
                for check in tm:
                    ctype=(check[table_proper[i]])
                    table_proper_type.append(type(ctype))
                    break
        while query_count != len(result):
            tmp_set = {}  # 랜덤한 속성명을 담는 set 집합
            tmp_set = set()
            a={}
            sel_random = random.randint(1, count)
            while len(tmp_set) != sel_random:
                tmp_set.add(proper[random.randint(0, count - 1)])

            tmp_set = str(tmp_set).strip('{}')
            tmp_set = tmp_set.replace('\'', "")
            update_query = Q[random.randint(0, len(Q)-1)]
            tmp_set = tmp_set.replace(' ',"").split(',')
            for i in range(len(tmp_set)):
                if type(update_query[tmp_set[i]]) is int:
                    a[i] = (tmp_set[i] + " 값을 "+ str(random.randint(1, update_query[tmp_set[i]])))
                    tmp_set[i] = (tmp_set[i] + " = " + str(random.randint(1, update_query[tmp_set[i]])))
                else:
                    random_word = lowercase_word()
                    a[i] = (tmp_set[i] + " 값을 " + str(random_word))
                    tmp_set[i] = (tmp_set[i] + " = " + "\"" + str(random_word)) + "\""
            sel_key = random.randint(0, len(mainkey)-1)
            if type(pull_table_data(target_table, mainkey[sel_key])) is int or type(pull_table_data(target_table, mainkey[sel_key])) is float:
                query = "UPDATE "+ str(tableName) + " SET "+ str(tmp_set) + " WHERE " + mainkey[sel_key] + " = " + str(pull_table_data(target_table, mainkey[sel_key]))
            else:
                query = "UPDATE " + str(tableName) + " SET " + str(tmp_set) + " WHERE " + mainkey[sel_key] + " = " + "\"" +str(pull_table_data(target_table, mainkey[sel_key])) +"\""
            k=query.split('WHERE')
            kk=k[1].split('=')
            bb=kk[1]
            bb=bb.replace('\'',"")
            bb=bb.replace(' ',"")
            query = query.replace('\'',"")
            query = query.replace('[', "")
            query = query.replace(']', "")
            result.add(query)
            txt1.append(table_info(tableName, table_proper, table_proper_type))
            txt1.append(str(tableName) + "테이블에서 " + str(mainkey[sel_key]) + "필드의 값이 " + bb + "인 모든 레코드의 " + update_info(a) +"로 변경하는 SQL문을 작성해주세요." + " SQL을 실행하면 다음과 같이 출력되어야 합니다.")
            if OnAndOff == True:
                txt1.append(AboutOurQuery(str(query)).Similar())
            elif OnAndOff == False:
                txt1.append("하")
            dic[str(query)]=txt1
            textres=[]
            txt1=[]
            #print(update_query, "해당하는 행을 변경하는 쿼리문입니다.")
            
        return dic
    def join_query(self, right_table, right_table_name):
        target_table = self.table
        tablename = self.tableName
        query_count = self.count
        left_table = target_table.objects.values()
        right_table = right_table.objects.values()
        lproper = []
        rproper = []
        lproper_type=[]
        rproper_type=[]
        txt1=[]
        txt2=''
        dic={}
        dic=dict()
        for key in left_table[0]:
            lproper.append(key)
        
        for key in right_table[0]:
            rproper.append(key)
        
        for i in range(len(lproper)):
            tm = target_table.objects.values(lproper[i])
            for check in tm:
                ctype = (check[lproper[i]])
                lproper_type.append(type(ctype))
                break
        for i in range(len(rproper)):
            tm = right_table.values(rproper[i])
            for check in tm:
                ctype = (check[rproper[i]])
                rproper_type.append(type(ctype))
                break
        
        left_table = pd.DataFrame(left_table)
        right_table = pd.DataFrame(right_table)
        if query_count == 1:
            r_num = random.randint(0, 1)
            if r_num == 0:
                #inner join
                tmp = pd.merge(left = left_table, right = right_table, how = 'inner', on = 'id')
                query = "SELECT * FROM " + tablename + " INNER JOIN " + right_table_name + " ON " + tablename +".id = " + right_table_name + ".id"
                txt2 += table_info(tablename, lproper, lproper_type) + table_info(right_table_name, rproper, rproper_type)
                txt1.append(txt2)
                txt1.append(str(tablename) + "테이블과 " + str(right_table_name) + "테이블에는 id 속성이 공통으로 있습니다. " + "이 속성을 기준으로 하여 " + insert_col(lproper) + insert_col(rproper) + "데이터들을 조회하는 SQL문을 작성해주세요." + " SQL을 실행하면 다음과 같이 출력되어야 합니다.")
                if OnAndOff == True:
                    txt1.append(AboutOurQuery(str(query)).Similar())
                elif OnAndOff == False:
                    txt1.append("하")
                dic[str(query)] = txt1
                txt1=[]
                txt2=''
                return dic
            elif r_num == 1:
                #LeftOuterJoin
                tmp = pd.merge(left=left_table, right=right_table, how='left', on='id')
                query = "SELECT * FROM " + tablename + " LEFT OUTER JOIN " + right_table_name + " ON " + tablename + ".id = " + right_table_name + ".id"
                txt2 += table_info(tablename, lproper, lproper_type) + table_info(right_table_name, rproper, rproper_type)
                txt1.append(txt2)
                txt1.append(str(tablename) + "테이블과 " + str(
                    right_table_name) + "테이블에는 id 속성이 공통으로 있습니다. " + "이 속성을 기준으로 하여 " + insert_col(lproper) + insert_col(rproper) + "데이터들을 조회하는 SQL문을 작성해주세요." + " 단, id 값이 존재하지 않다면 NULL값으로 대신합니다." + " SQL을 실행하면 다음과 같이 출력되어야 합니다.")

                if OnAndOff == True:
                    txt1.append(AboutOurQuery(str(query)).Similar())
                elif OnAndOff == False:
                    txt1.append("하")
                dic[str(query)] = txt1
                txt1=[]
                txt2=''
                return dic
        else:
            # inner join
            tmp = pd.merge(left=left_table, right=right_table, how='inner', on='id')
            query = "SELECT * FROM " + tablename + " INNER JOIN " + right_table_name + " ON " + tablename + ".id = " + right_table_name + ".id"
            txt2 += table_info(tablename, lproper, lproper_type) + table_info(right_table_name, rproper, rproper_type)
            txt1.append(txt2)
            txt1.append(str(tablename) +"테이블과 " + str(right_table_name) + "테이블에는 id 속성이 공통으로 있습니다. " + "이 속성을 기준으로 하여 " + insert_col(lproper) + insert_col(rproper) + "데이터들을 조회하는 SQL문을 작성해주세요." + " SQL을 실행하면 다음과 같이 출력되어야 합니다.")
            if OnAndOff == True:
                txt1.append(AboutOurQuery(str(query)).Similar())
            elif OnAndOff == False:
                txt1.append("하")
            dic[str(query)] = txt1
            txt1 = []
            txt2 = ''
            # LeftOuterJoin
            tmp = pd.merge(left=left_table, right=right_table, how='left', on='id')
            query = "SELECT * FROM " + tablename + " LEFT OUTER JOIN " + right_table_name + " ON " + tablename + ".id = " + right_table_name + ".id"
            txt2 += table_info(tablename, lproper, lproper_type) + table_info(right_table_name, rproper, rproper_type)
            txt1.append(txt2)
            txt1.append(str(tablename) +"테이블과 " + str(right_table_name) + "테이블에는 id 속성이 공통으로 있습니다. " + "이 속성을 기준으로 하여 " + insert_col(lproper) + insert_col(rproper) + "데이터들을 조회하는 SQL문을 작성해주세요." + " 단, id 값이 존재하지 않다면 NULL값으로 대신합니다." + " SQL을 실행하면 다음과 같이 출력되어야 합니다.")
            if OnAndOff == True:
                txt1.append(AboutOurQuery(str(query)).Similar())
            elif OnAndOff == False:
                txt1.append("하")
            dic[str(query)] = txt1
            txt1 = []
            txt2 = ''
            return dic