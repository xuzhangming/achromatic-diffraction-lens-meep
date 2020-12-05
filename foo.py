
import meep as mp
import numpy as np
import math
import random
import matplotlib.pyplot as plt

#450	 1.674	
#550     1.642
#650     1.629

#ht = [0.7,2.8 , 2.65 ,2.95, 4.1 , 1.9 , 3.4 , 0.9 , 2.7  ,4, 2.9 , 0.8 , 3.85, 2,
# 2, 3.2,  1.05, 1,0.8 ,1.8,  1.65, 2.9,  1.35, 1.4 , 0.2,  0.8,  3.9,  3.7,
# 1.05 ,1,3.7 , 2.15 ,0.65, 3.2 , 2.3 , 3.5 , 1.35, 3.3 , 2.35 ,3.2 , 0.45 ,3.3,
# 3.55 ,3.2 , 0.2,  1.85 ,3.1 , 1.5,  3, 1.15, 0.2,  2.95, 1.45, 0.15, 0.65, 3.2,
# 2.25 ,3.7 , 0.1 , 4, 2.7 , 0.9  ,1.3 , 3.05 ,1.3  ,3.9 , 0.75 ,2.85 ,0.65 ,3.45,
# 4.1 , 0.05, 1.2,  3.45, 4.1 , 3.85, 0.9,  2.9,  1.7,  1.85]

ht = [0.75, 2.8,  2.65, 2.95, 4.1,  1.95, 3.4,  0.9 , 2.7,  4, 2.9,  0.8,  3.9,  2.05,
 2.05 ,3.2 , 1.05, 1, 0.8 , 1.8 , 1.65, 2.9 , 1.35, 1.4 , 0.2 , 0.85, 3.9 , 3.7,
 1.05 ,1,3.7, 2.15, 0.65, 3.2,  2.3,  3.5,  1.35, 3.3,  2.35, 3.2,  0.45, 3.3,
 3.55, 3.2 , 0.2 , 1.85 ,3.15 ,1.55, 3,1.15 ,0.2 , 2.95, 1.45, 0.15, 0.65 ,3.25,
 2.25 ,3.7 , 0.1,  4, 2.7 , 0.9 , 1.3,  3.05, 1.3 , 3.9 , 0.75, 2.85, 0.65, 3.45,
 4.1 , 0.1 , 1.25 ,3.45, 4.1,  3.9 , 0.9 , 2.95, 1.7 , 1.85]



#if (wvl_cen == 0.45):
	#photoresist = mp.Medium(index=1.674)   #波长为450nm时光刻胶的折射率 
#elif (wvl_cen == 0.55):
	#photoresist = mp.Medium(index=1.642)   #波长为550nm时光刻胶的折射率 
#else:
	#photoresist = mp.Medium(index=1.629)   #波长为650nm时光刻胶的
	 

#wvl_cen = 0.45
#photoresist = mp.Medium(index=1.674)

wvl_cen = 0.55
photoresist = mp.Medium(index=1.642)

#wvl_cen = 0.65
#photoresist = mp.Medium(index=1.629)
## at least 8 pixels per smallest wavelength, i.e. np.floor(8/wvl_min)
resolution = 25.0          

dpml=1.0                                #PML厚度               
dpad =2.0                               #透镜与PML间距
#dsub = 2.0                             # substrate thickness
width = 0.25                            #环的宽度
r= width*len(ht)                        #透镜的半径
focal_length = 20.0                      #焦距
ff_res = 10.0
h = 5

NA = math.sin(math.atan(r/focal_length))
NA = round(NA, 3)


pml_layers = [mp.PML(thickness=dpml)]

sr=r+dpad+dpml
sz=dpml+dpad+h+dpad+dpml
#sz=dpml+dsub+h+dpad+dpml
cell_size =mp.Vector3(sr,0,sz) 

#glass = mp.Medium(index=1.5)                    # substrate
#geometry = [mp.Block(material=glass,
#	             size=mp.Vector3(sr,0,dpml+dsub),
#	             center=mp.Vector3(0.5*sr,0,-0.5*sz+0.5*(dpml+dsub)))]
# 
#for n in range (len(ht)):
#	geometry.append(mp.Block(material=photoresist,
#	             size=mp.Vector3(width,0,ht[n]),
#	             center=mp.Vector3(width*n+0.5*width,0,-0.5*sz+dpml+dsub+0.5*ht[n])))  #透镜的结构
geometry = [mp.Block(material=photoresist,
     		size=mp.Vector3(width,0,ht[0]),
   		 center=mp.Vector3(0.5*width,0,-0.5*sz+dpml+dpad+0.5*ht[0]))]
for n in range (1,len(ht)):
	geometry.append(mp.Block(material=photoresist,
	     size=mp.Vector3(width,0,ht[n]),
	     center=mp.Vector3(width*n+0.5*width,0,-0.5*sz+dpml+dpad+0.5*ht[n])))  #透镜的结构
#wvl_cen = 0.5
frq_cen = 1/wvl_cen
dfrq = 0.2*frq_cen

sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
	             component=mp.Er,
	             center=mp.Vector3(0.5*(sr),0,-0.5*sz+dpml+dpad),     
	             size=mp.Vector3(sr)),
	   mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
	             component=mp.Ep,
	             center=mp.Vector3(0.5*(sr),0,-0.5*sz+dpml+dpad),
	             size=mp.Vector3(sr),
	             amplitude=-1j)]

sim = mp.Simulation(cell_size=cell_size,
	            boundary_layers=pml_layers,
	            resolution=resolution,
	            sources=sources,
	            geometry=geometry,
	            dimensions=mp.CYLINDRICAL,         
	            m=-1)

## near-field monitor
n2f_obj = sim.add_near2far(frq_cen, 0, 1,
	                   mp.Near2FarRegion(center=mp.Vector3(0.5*(sr-dpml),0,0.5*sz-dpml),size=mp.Vector3(sr-dpml)))
	                   
sim.run(until_after_sources=100)

ff_r = sim.get_farfields(n2f_obj, ff_res, center=mp.Vector3(0.5*(sr-dpml),0,-0.5*sz+dpml+dpad+focal_length),size=mp.Vector3(sr-dpml))
E2_r = np.absolute(ff_r['Ex'])**2+np.absolute(ff_r['Ey'])**2+np.absolute(ff_r['Ez'])**2

E_sum = sum(E2_r)
print(E_sum)
n = round((1.5*(wvl_cen/(2*NA)))/(r/len(E2_r)))
#print ('n = %d' % n)
E = 0.0
print(E2_r)
for i in range (n):
	E += E2_r[i]
print(E)
print ('============================================================================================')
print(E/E_sum)  
print ('============================================================================================')
plt.figure(dpi=200)
plt.subplot(1,1,1)
plt.semilogy(np.linspace(0,sr-dpml,len(E2_r)),E2_r,'ro-')
plt.xlim(0,20)
plt.xticks([t for t in np.arange(0,25,5)])
plt.grid(True,axis="y",which="both",ls="-")
plt.xlabel(r'$r$ coordinate (μm)')
plt.tight_layout()
plt.savefig("lens_farfields.png")
plt.ylabel(r'energy density of far fields, |E|$^2$')








































