
from avg_diff import avg_diff
import numpy as np
import random


h = 1.25
b = 1.25/100

n = 80
ht = (np.random.randint(1,n+1,size = (n)))*b    #随机生成每个环的高度,200个环


r = avg_diff(ht)    #平均衍射效率
res_max = (r[0]+r[1]+r[2])/3
print ('============================================================================================')
print ('r1 = %.4f' % r[0])
print ('r2 = %.4f' % r[1])
print ('r3 = %.4f' % r[2])
print ('avg_diff = %.4f' % res_max)
print ('============================================================================================')


for k in range (5):
	print ('============================================================================================')
	print ('k = %d' % k)
	print ('============================================================================================')
	c = random.sample(range(0,n),n)		
	for j in range (n):
		i = c[j]
		ht[i] = ht[i]+b
		r = avg_diff(ht)    #平均衍射效率
		print ('r1 = %.4f' % r[0])
		print ('r2 = %.4f' % r[1])
		print ('r3 = %.4f' % r[2])
		res = (r[0]+r[1]+r[2])/3
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
			r = avg_diff(ht)    #平均衍射效率
			print ('r1 = %.4f' % r[0])
			print ('r2 = %.4f' % r[1])
			print ('r3 = %.4f' % r[2])
			res = (r[0]+r[1]+r[2])/3
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
    	
