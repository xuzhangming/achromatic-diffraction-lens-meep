from avg_diff import avg_diff
import numpy as np
import random


h = 1.25
b = h/100

n = 50
#ht = (np.random.randint(1,n+1,size = (n)))*b    #随机生成每个环的高度


ht=[0.625,0.5625,0.625 , 0.125,  0.2375, 0.075 , 0.575 , 0.2625, 0.3,0.3125
,0.1625,0.3, 0.075, 0.3375, 0.4,0.55,0.2125, 0.125,0.25, 0.025
,0.325,0.625,0.3,0.075,0.55, 0.225,  0.575,  0.1875, 0.4, 0.0875
, 0.05 ,0.5,0.5625, 0.0125, 0.325,  0.0125, 0.6125 ,0.3125, 0.475, 0.55
,0.3875, 0.4375, 0.4625 ,0.5 ,   0.45 ,  0.1625 ,0.35,   0.4125, 0.325 , 0.5]


#ht=[0.625, 0.575, 0.6375, 0.125, 0.2375, 0.075, 0.5875, 0.275, 0.3, 0.325, 0.175, 0.3, 0.075, 0.325, 0.3875, 0.55, 0.2125, 0.1125, 0.2375, 0.025, 0.3125, 0.625, 0.3, 0.0875, 0.5375, 0.225, 0.575, 0.1875, 0.4125, 0.1, 0.0375, 0.5125, 0.575, 0.0125, 0.325, 0.0125, 0.625, 0.3125, 0.4875, 0.55, 0.375, 0.45, 0.475, 0.4875, 0.45, 0.1625, 0.35, 0.4125, 0.325, 0.5125]

r = avg_diff(ht)    #平均衍射效率
res_max = (r[0]+r[1]+r[2])/3
print ('============================================================================================')
print ('r1 = %.4f' % r[0])
print ('r2 = %.4f' % r[1])
print ('r3 = %.4f' % r[2])
print (ht)
print ('avg_diff = %.4f' % res_max)
print ('============================================================================================')


for k in range (1):
	print ('============================================================================================')
	print ('k = %d' % k)
	print ('============================================================================================')
	c = random.sample(range(0,n),n)		
	
	for j in range (n):
		print ('j = %d' % j)
		i = c[j]
		ht[i] = round(ht[i]+b,4)
		
		if (ht[i]<=h):
			r = avg_diff(ht)    #平均衍射效率
			res = (r[0]+r[1]+r[2])/3
			if(res > res_max):
				res_max = res
				print ('============================================================================================')
				print (ht)
				print ('r1 = %.4f' % r[0])
				print ('r2 = %.4f' % r[1])
				print ('r3 = %.4f' % r[2])
				print ('avg_diff = %.4f' % res_max)
				print ('============================================================================================')
			else:
				ht[i] = round(ht[i]-2*b,4)
				if (ht[i] >= b):
					r = avg_diff(ht)    #平均衍射效率
					res = (r[0]+r[1]+r[2])/3
					if(res > res_max):
						res_max = res
						print ('============================================================================================')
						print (ht)
						print ('r1 = %.4f' % r[0])
						print ('r2 = %.4f' % r[1])
						print ('r3 = %.4f' % r[2])
						print ('avg_diff = %.4f' % res_max)
						print ('============================================================================================')
					else:
						ht[i] = round(ht[i]+b,4)
				else:
					ht[i] = round(ht[i]+b,4)
				
		else:
			ht[i] = round(ht[i]-2*b,4)
			if (ht[i] >= b):
				r = avg_diff(ht)    #平均衍射效率
				res = (r[0]+r[1]+r[2])/3
				if (res > res_max):
					res_max = res
					print ('============================================================================================')
					print (ht)
					print ('r1 = %.4f' % r[0])
					print ('r2 = %.4f' % r[1])
					print ('r3 = %.4f' % r[2])
					print ('avg_diff = %.4f' % res_max)
					print ('============================================================================================')
				else:
					ht[i] = round(ht[i]+b, 4)
			else:
				ht[i] = round(ht[i]+b, 4)		

	
