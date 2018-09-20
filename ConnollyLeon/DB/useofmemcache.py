#coding:utf8
import memcache
#连接缓存服务
mc = memcache.Client(['localhost:11211'],debug=True)
#插入set设置一个键值对，如果Key不存在，则创建，如果key存在，则修改
mc.set("name","python",time=1000)
#读取
ret = mc.get('name')
print(ret)

#set_multi : 设置多个键值对，如果key不存在，则创建，如果key存在，则修改。
dic = {'name':'tom','age':'19','job':'IT'}
mc.set_multi(dic)  #设置多个键值对
#或者mc.set_multi({'name':'tom','age':'19','job':'IT'})
ret = mc.get('name')
print(ret)

#get_multi : 获取多个键值对
regetmu=mc.get_multi(['name','age','job'])
print('get_multi',regetmu) #获取多个键值对的值

#add添加一条键值对，如果已经存在的key，重复执行add操作会出现异常
mc.add('k1','v1',time=1000)
#读取
ret = mc.get('k1')
print(ret)


#replace修改某个key的值，如果key不存在，则异常
rereplace = mc.replace('name','jack')
re = mc.get('name')
print(rereplace,re)

#append : 修改指定key的值，在该值后面追加内容。
#prepend : 修改指定key的值，在该值前面插入内容
mc.append('name','second') #在第一后面追加
re = mc.get('name')
print(re)
mc.prepend('name','first')  #在第一前面追加
re = mc.get('name')
print(re)

#delete : 在Memcached中删除指定的一个键值对
mc.delete('k1')
re = mc.get('k1')
print('删除',re)  #删除一个键值对



