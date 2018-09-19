# -*- coding:utf-8 -*-

import mysql.connector
# 打开数据库连接（请根据自己的用户名、密码及数据库名称进行修改）
config = {
    'host': '192.168.43.23',
    'user': 'root',
    'password': 'yueyue',
    'port': 3306,
    'database': 'auc',
    'charset': 'utf8'
}
cnn = mysql.connector.connect(**config)
# 使用cursor()方法获取操作游标
cursor = cnn.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
print("Database version : %s " % data)

# 执行sql语句
cnn.close()
#显示的结果应该如下：

#Database version : 8.0.12