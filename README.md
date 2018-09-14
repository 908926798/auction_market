auction_market 拍卖系统
--- 
### 最终要实现的系统：  
* 一台主服务器，负责账号登录，拍卖一览，发起与卖家会话功能，用http             --梁鹏  
* 一台拍卖服务器，负责拍卖的流程，用tcp链接（再做下两人私聊的tcp）				--吕书邻  
* 一台数据服务器，负责数据库，nosql                                       --吴之玥  
* 客户端使用python编写图形化界面，有登录界面，私聊界面，拍卖一览界面和拍卖界面  --陈星霖  

###每个人做出各自负责的服务器和相应的客户端测试代码，最后再整合到一起


  
---------------------吴之玥----------------------  
###数据库表
* 商品：商品名，卖家账户名，底价，开拍时间，状态（未开卖，正拍卖，已卖出），最终成交价（未卖出为NULL），买家账户名（未卖出为NULL）
* 用户：账户名，密码，昵称，资金
* 角色：账户名，角色
* 拍卖情况：商品名，最新出价买家账户名（未卖出为NULL），最新价

最终给出对数据库操作的所有命令的格式，比如添加商品的insert命令

###NoSQL
暂未确定使用哪个？

----------------------梁鹏----------------------  
###主服务器
* 处理用户登录和会话保持，ip管理（用于建立tcp）
* 处理商品信息的获取（分三种，未开卖，正拍卖，已卖出）
* 处理客户端与拍卖服务器建立tcp连接过程
* 处理客户端与另一个客户端（卖家）建立tcp连接

---------------------吕书邻---------------------  
###拍卖流程  
* 一个房间只拍卖一个商品  
* 当一段时间T之后没有人出价就竞拍结束
* 每当有人出价，发送用户名和价格给服务器，服务器重置倒计时
* 倒计时实时刷新，精确到秒，房间里的所有买家实时接收倒计时

###买家和卖家私聊的tcp链接

---------------------陈星霖---------------------  
###客户端
* 登录和注册界面
* 商品浏览界面（分三栏，未开卖，正拍卖，已卖出）
* 竞拍界面
* 与卖家私聊界面

###避免单点失效

###最后整合大家的功能