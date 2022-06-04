import torch
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn.cluster import KMeans

class QueryInfo:
    def __init__(self, quer, dif, table_name):
        self.quer = quer
        self.dif = dif
        self.table_name = table_name


Qlist = [
            QueryInfo("SELECT e1.Name AS 'Employee' FROM Employee e1 WHERE 3> ",  "하", "EMP"),
            QueryInfo("SELECT * FROM User",  "하", "User"),
            QueryInfo("SELECT * FROM ID ORDER BY",  "중", "Student"),
            QueryInfo("SELECT FirstName, LastName, City, State FROM Person LEFT JOIN Address ON Person.PersonId = Address.PersonId", "중", "Address"),
            QueryInfo("SELECT DISTINCT Salary AS SecondHighestSalary FROM Employee ORDER BY Salary DESC LIMIT 1 OFFSET 1","중", "Employee"),
            QueryInfo("SELECT DISTINCT l1.Num AS ConsecutiveNums FROM Logs l1, Logs l2, Logs l3 WHERE l1.Id = l2.Id - 1 AND l2.Id = l3.Id - 1 AND l1.Num = l2.Num AND l2.Num = l3.Num", "중", "Logs"),
            QueryInfo("SELECT * FROM Employee AS a WHERE a.ManagerID=b.Id", "하", "Employee"),
            QueryInfo("SELECT customers.name AS 'Customers' FROM customer WHERE customer.id NOT IN (SELECT customerid FROM orders)","상","Customer"),
            QueryInfo("DELETE p1 FROM Person p1, Person p2 WHERE p1.Email = p2.Email AND p1.ID > p2.ID", "하", "Person"),
            QueryInfo("SELECT weather.id AS 'ID' FROM weather JOIN weather w ON DATEDIFF(weather.recordDate, w.recodDate)=1 AND wather.Temprature > w.Temprature", "상", "Weather"),
            QueryInfo("SELECT DISTINCT t1.* FROM stadium t1, stadium t2, stadium t3 WHERE t1.people >= 100 AND t2.people >=100 AND t3.people >=100 AND ((t1.id-t2.id=1 AND t1.id-t3.id=2 AND t2.id-t3.id=1)) OR (t2.id - t1.id = 1 AND t2.id - t3.id = 2 AND t1.id - t3.id =1) OR (t3.id - t2.id = 1 AND t2.id - t1.id =1 AND t3.id - t1.id = 2)) ORDER BY t1.id", "상", "stadium"),
            QueryInfo("SELECT name FROM school WHERE studentnum NOT BETWEEN 23 AND 32", "중","school"),
            QueryInfo("SELECT classnum, tel, studentnum , rank() over(order by classnum DESC) as ranking FROM table_school ORDER BY tel","상","school"),
            QueryInfo("UPDATE table_school SET classnum = 1 WHERE name = 성수", "하", "school"),
            QueryInfo("SELECT count(*) FROM table_school where id >= (SELECT avg(id) FROM table_school)","상","school"),
            QueryInfo("SELECT MAX(id) - MIN(id) FROM table_school","하","school"),
            QueryInfo("SELECT address FROM table_school WHERE tel LIKE '0%'","하","school"),
            QueryInfo("UPDATE table_school SET classnum = 4, studentnum = 28 WHERE tel = 063-521-1234","하","school"),
            QueryInfo("SELECT * FROM User ORDER BY Name DESC","하", "User"),
            QueryInfo("SELECT DISTINCT(Email,IsTeacher,ID,Password) FROM User", "하", "User"),
            QueryInfo("INSERT INTO User VALUES(3, m, w, ykrzpvwdw, 1)", "하", "User"),
            QueryInfo("SELECT * FROM table_school INNER JOIN seoul ON table_school.id = seoul.id", "하", "s"),
            QueryInfo("SELECT * FROM table_school LEFT OUTER JOIN seoul ON table_school.id = seoul.id", "하", "s")
        ]

class AboutOurQuery:
    def __init__(self, quer):
        self.quer=quer
        
    def Similar(self):
        Qgram=['SELECT', 'AS', 'FROM', 'WHERE', 'ORDER', 'BY', 'DISTINCT', 'MAX', 'MIN' , '*', 'BETWEEN', 'AND', 'DESC', '>', '<', 'LEFT', 'RIGHT', 'JOIN', 'DELETE', 'LIMIT', 'OFFSET', 'DATEDIFF', 'OR', 'NOT', 'IN', 'LIKE']
        txt=''
        ComLabel=[]
        Docs=[]
        OurLabel=''
        s=[]
        recommand=''
        recommand_table=''
        man_scores=[]

        for i in Qlist:
            Docs.append(i.quer)

        for i in Qlist:
            words = word_tokenize(i.quer)
            for j in words:
                if j in Qgram:
                    txt += ' ' + j
            ComLabel.append(txt)
            txt=''
        Ourwords = word_tokenize(self.quer)
        for i in Ourwords:
            if i in Qgram:
                OurLabel += ' ' + i
            
    
        model = SentenceTransformer('sentence-transformers/msmarco-MiniLM-L6-cos-v5')
        document_embeddings = model.encode(ComLabel)

        Our_embedding = model.encode(OurLabel)

        top_k = min(5, len(Qlist))
        cos_scores = util.pytorch_cos_sim(Our_embedding, document_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)
        

        # print(f"입력 문장: {OurLabel}")
        # print(f"\n<입력 문장과 유사한 {top_k} 개의 문장>\n")

        # for i, (score, idx) in enumerate(zip(top_results[0], top_results[1])):
        #     print(f"{i+1}: {Qlist[idx].quer} {'(유사도: {:.4f})'.format(score)}\n")

        diff = Qlist[top_results[1][0]].dif
        return diff
        