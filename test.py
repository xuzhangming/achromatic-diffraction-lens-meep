import threading
from time import sleep,ctime
import numpy as np
import random
from diff_thread import diff

h = 1.25

b = h/100
n = 50
#ht = (np.random.randint(1,n+1,size = (n)))*b    #随机生成每个环的高度
num = 3          #线程个数


ht=[0.5625, 0.275,  0.2125, 0.2375, 0.4375, 0.2, 0.1625,0.5125, 0.4375, 0.2625
, 0.5125, 0.5 , 0.0375, 0.025,  0.025  ,0.025,  0.55,   0.5875, 0.3625, 0.1
 ,0.1125, 0.025  ,0.55  , 0.4125, 0.3125 ,0.5875 ,0.5625 ,0.475 , 0.3   , 0.0625
 ,0.1375, 0.4875, 0.2375, 0.575 , 0.5875, 0.075 , 0.15  , 0.5625 ,0.45  , 0.4375
 ,0.0625, 0.25 ,  0.2375, 0.5625, 0.15,   0.4125, 0.05  , 0.125 , 0.375 , 0.4375]


wvl=[0.45,0.55,0.65]

r=np.zeros(num)
lock = threading.Lock()


threads=[]
for m in range (num):
	t=threading.Thread(target=diff,args=(ht,wvl[m],r,m))           #循环 实例化num个Thread类，传递函数及其参数，并将线程对象放入一个列表中
	threads.append(t)
for i in range (num):
	threads[i].start()                                                   #循环 开始线程
for i in range (num):
	threads[i].join()                                                    #循环 join()方法可以让主线程等待所有的线程都执行完毕。

res_max=(r[0]+r[1]+r[2])/num
res = res_max
print ('r1 = %.4f' % r[0])
print ('r2 = %.4f' % r[1])
print ('r3 = %.4f' % r[2])
print (ht)
print ('res = %.4f' % res)


for k in range (2):
	print ('============================================================================================')
	print ('k = %d' % k)
	print ('============================================================================================')
	c = random.sample(range(0,n),n)		
	for j in range (n):
		print ('j = %d' % j)
		i = c[j]
		ht[i] = ht[i]+b
		
		threads=[]
		
		for m in range (num):
			t=threading.Thread(target=diff,args=(ht,wvl[m],r,m))           #循环 实例化num个Thread类，传递函数及其参数，并将线程对象放入一个列表中
			threads.append(t)
		for i in range (num):
			threads[i].start()                                                   #循环 开始线程
		for i in range (num):
			threads[i].join()                                                    #循环 join()方法可以让主线程等待所有的线程都执行完毕。
		
		res=(r[0]+r[1]+r[2])/num;
		print ('r1 = %.4f' % r[0])
		print ('r2 = %.4f' % r[1])
		print ('r3 = %.4f' % r[2])
		print ('res = %.4f' % res)
		
		if ((ht[i] <= h) and (res > res_max)):
			res_max = res
			print ('============================================================================================')
			print (ht)
			print ('j = %d' % j)
			print ('r1 = %.4f' % r[0])
			print ('r2 = %.4f' % r[1])
			print ('r3 = %.4f' % r[2])
			print ('avg_diff = %.4f' % res_max)
			print ('============================================================================================')
		else:
			ht[i] = ht[i]-2*b
			
			threads=[]
		
			for m in range (num):
				t=threading.Thread(target=diff,args=(ht,wvl[m],r,m))           #循环 实例化num个Thread类，传递函数及其参数，并将线程对象放入一个列表中
				threads.append(t)
			for i in range (num):
				threads[i].start()                                                   #循环 开始线程
			for i in range (num):
				threads[i].join() 
			
			res=(r[0]+r[1]+r[2])/num;
			print ('r1 = %.4f' % r[0])
			print ('r2 = %.4f' % r[1])
			print ('r3 = %.4f' % r[2])
			print ('res = %.4f' % res)
			
			if ((ht[i] >= b) and (res > res_max)):
				res_max = res
				print ('============================================================================================')
				print (ht)
				print ('j = %d' % j)
				print ('r1 = %.4f' % r[0])
				print ('r2 = %.4f' % r[1])
				print ('r3 = %.4f' % r[2])
				print ('avg_diff = %.4f' % res_max)
				print ('============================================================================================')

				
				
			else:
				ht[i] = ht[i]+b


