import pymysql
import re

"""
类名：MysqlHelper
connect（）：连接数据库
close() :关闭数据库
get_one(self,sql,params=())：查询一条数据
get_one(self,sql,params=())：查询多条数据
get_all(self,sql,params=())：查询全部数据
insert(self,sql,params=())：插入数据（含插入多条）
update(self,sql,params=())：修改数据
delete(self,sql,params=())：删除数据
create_table(self,sql,params=())：删除数据库表

MysqlHelper(USER,PASSWD,HOST,PORT,DB)
"""


class MysqlHelper(object):
    def __init__(self,USER,PASSWD,HOST,PORT,DB,charset='utf8'):
        self.user=USER
        self.passwd=PASSWD
        self.host=HOST
        self.port=PORT
        self.db=DB
        self.charset=charset
    #     self.cursor=self.cursor()
    #
    # def conn(self):
    #     conn = pymysql.connect(user=self.user, passwd=self.passwd, host=self.host, port=self.port, db=self.db,
    #                            charset=self.charset)
    #     return conn
    #
    # def cursor(self):
    #     self.conn()
    #     cursor = self.conn.cursor()
    #     return cursor

    def connect(self):
        self.conn=pymysql.connect(user=self.user,passwd=self.passwd,host=self.host,port=self.port,db=self.db,charset=self.charset)
        self.cursor=self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close

    def get_one(self,sql,params=()):
        result=None
        try:
            self.connect()
            self.cursor.execute(sql,params)
            result=self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def get_all(self,sql,params=()):
        list=()
        try:
            self.connect()
            self.cursor.execute(sql,params)
            list=self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list

    def get_many(self,sql,params=(),size=None):
        result=None
        try:
            self.connect()
            self.cursor.execute(sql,params)
            result=self.cursor.fetchmany(size)
            self.close()
        except Exception as e:
            print(e)
        return result
    '''
    插入多行的示例
    sql4= "INSERT INTO student(xm,age,price)VALUES (%s, %s, %s)"
    data = (('Jane', 60,9.09 ),('Jane', 60,9.09 ))
    a = py.insert(sql4, data)
    插入单行的示例
    sql4= "INSERT INTO student(xm,age,price)VALUES (%s, %s, %s)"
    data = ('Jane', 60,9.09 )
    a = py.insert(sql4, data)
    '''

    def insert(self,sql,params=()):
        if isinstance(params[0],tuple):
            return self.__edits(sql,params)
        elif not isinstance(params[0],tuple) or params==():
            return self.__edit(sql,params)
        else:
            rule="params实例params=(('e','60'),('d','70')),参数非法"
            return rule

    def update(self,sql,params=()):
        return self.__edit(sql,params)

    def delete(self,sql,params=()):
        return self.__edit(sql,params)

    def create_table(self,sql,params=()):
        return self.__edit(sql,params)

    def table_truncate(self,table_name):
        sql = 'TRUNCATE TABLE '+ table_name
        self.__edit(sql)
        return {"code":1,'msg':'suc'}

    def table_exists(self,table_name):  # 这个函数用来判断表是否存在
        self.connect()
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = [self.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0  # 不存在返回0
        self.close()

    def __edit(self,query,params=()):
        count=0
        try:
            self.connect()
            count=self.cursor.execute(query,params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count

    def __edits(self,sql,params=()):
        count=0
        try:
            self.connect()
            count=self.cursor.executemany(sql,params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return len(params)

    def __edit_v1(self,query,params=()):
        count=0
        try:
            self.connect()
            count=self.cursor.execute(query,params)
        except Exception as e:
            print(e)
        return count

    def __edits_v1(self,sql,params=()):
        count=0
        try:
            self.connect()
            count=self.cursor.executemany(sql,params)
        except Exception as e:
            print(e)
        return len(params)

    def insert_v1(self,sql,params=()):
        if isinstance(params[0],tuple):
            return self.__edits_v1(sql,params)
        elif not isinstance(params[0],tuple) or params==():
            return self.__edit_v1(sql,params)
        else:
            rule="params实例params=(('e','60'),('d','70')),参数非法"
            return rule

    def insert_v1_close(self):
        self.conn.commit()
        self.close()



#sql='create table hiyang2(nameno int primary key not null auto_increment,name varchar(3) not null ,age int not null)'

if __name__=='__main__':
    py=MysqlHelper()
    # sql = "select * from condition_goods where id = %s "
    # # last=('a','y')
    # sql2 = "select * from hiyang where name in(%s,%s) "
    # last = ('a', 'y')
    # sql3='insert into hiyang(name,age) values(%s,%s)'
    # params=(('k','60'),('k','70'))
    # sql4='select * from hiyang'
    # # params=['z',10]
    # # mysqlhelper.MysqlHelper.insert(sql, params)
    # a=MysqlHelper().get_many(sql4,size=5)
    # print(a)
    sql="insert into student(xm,age,price)values('%s', %d, %.2f)"
    sql1="insert into student (xm,age,price) values('jia2',60,4.09)"
    sql2 = "insert into student(xm,age,price)values(xm='%s',age= %d, price=%.2f)"
    sql3='select * from student'
    sql4= "INSERT INTO test(xm,age,price)VALUES (%s, %s, %s)"
    xms=['jia2','jia5','jia6']
    touple_01=[]
    for xm in xms:
        age=70
        price01=6.09
    # params=((xm,age,price01),)
        data = (xm, age,price01)
        touple_01.append(data)
    for t0 in touple_01:
        t1=tuple(t0)
    t2=tuple(touple_01)



    py.insert(sql4,t2)

    # a=py.get_one(sql3)
    # print(a)
    # print(a['price'])

"""
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
user="u1"
passwd="u1pass"
#执行参数化查询
row_count=cursor.execute("select user,pass from tb7 where user=%s and pass=%s",(user,passwd))
row_1 = cursor.fetchone()
print row_count,row_1
 
conn.commit()
cursor.close()
conn.close()

作者：水月々轩辕
链接：https://www.jianshu.com/p/dec5701da2f3
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

'''
import pymysql
#3.更新操作
db= pymysql.connect(host="localhost",user="root",
 	password="123456",db="test",port=3307)
 
# 使用cursor()方法获取操作游标
cur = db.cursor()
 
sql_update ="update user set username = '%s' where id = %d"
 
try:
	cur.execute(sql_update % ("xiongda",3))  #像sql语句传递参数
	#提交
	db.commit()
except Exception as e:
	#错误回滚
	db.rollback() 
finally:
	db.close()
'''

'''
import pymysql.cursors

# 连接数据库
connect = pymysql.Connect(
    host='localhost',
    port=3310,
    user='woider',
    passwd='3243',
    db='python',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()

# 插入数据
sql = "INSERT INTO trade (name, account, saving) VALUES ( '%s', '%s', %.2f )"
data = ('雷军', '13512345678', 10000)
cursor.execute(sql % data)
connect.commit()
print('成功插入', cursor.rowcount, '条数据')

# 修改数据
sql = "UPDATE trade SET saving = %.2f WHERE account = '%s' "
data = (8888, '13512345678')
cursor.execute(sql % data)
connect.commit()
print('成功修改', cursor.rowcount, '条数据')

# 查询数据
sql = "SELECT name,saving FROM trade WHERE account = '%s' "
data = ('13512345678',)
cursor.execute(sql % data)
for row in cursor.fetchall():
    print("Name:%s\tSaving:%.2f" % row)
print('共查找出', cursor.rowcount, '条数据')

# 删除数据
sql = "DELETE FROM trade WHERE account = '%s' LIMIT %d"
data = ('13512345678', 1)
cursor.execute(sql % data)
connect.commit()
print('成功删除', cursor.rowcount, '条数据')

# 事务处理
sql_1 = "UPDATE trade SET saving = saving + 1000 WHERE account = '18012345678' "
sql_2 = "UPDATE trade SET expend = expend + 1000 WHERE account = '18012345678' "
sql_3 = "UPDATE trade SET income = income + 2000 WHERE account = '18012345678' "

try:
    cursor.execute(sql_1)  # 储蓄增加1000
    cursor.execute(sql_2)  # 支出增加1000
    cursor.execute(sql_3)  # 收入增加2000
except Exception as e:
    connect.rollback()  # 事务回滚
    print('事务处理失败', e)
else:
    connect.commit()  # 事务提交
    print('事务处理成功', cursor.rowcount)

# 关闭连接
cursor.close()
connect.close()
'''