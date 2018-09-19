# -*- coding:utf-8 -*-
import mysql.connector

config = {
    'host': '192.168.43.23',
    'user': 'root',
    'password': 'yueyue',
    'port': 3306,
    'database': 'auc',
    'charset': 'utf8'
}
cnn = mysql.connector.connect(**config)

cursor = cnn.cursor()


cursor.execute("SELECT VERSION()")


data = cursor.fetchone()
print("Database version : %s " % data)




#Database version : 8.0.12


cursor.close()
cursor = cnn.cursor(buffered=True)
cursor.execute('select goods_name from database_goods WHERE status="in"')
values = cursor.fetchall()

print(values)


cursor.close()
cursor = cnn.cursor(buffered=True)
cursor.execute('UPDATE database_goods SET lastbid_username = "Alex" WHERE goods_name = "huluwa"')
cursor.execute('UPDATE database_goods SET lastprice = "5" WHERE goods_name = "huluwa"')
cursor.execute('update database_goods set lastbid_time = now() where goods_name = "huluwa"')
#values = cursor.fetchall()
cnn.commit()
#print(values)

cnn.close()