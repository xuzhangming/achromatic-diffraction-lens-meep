import matplotlib.pyplot as plt
import meep as mp
import numpy as np
import math
import random

#450	 1.674	
#550     1.642
#650     1.629


wvl_cen = 0.65
photoresist = mp.Medium(index=1.629)

ht = [0.9,1.6,2.1,2.15,0.75,0.8,0.35,2.15,2.95,0.15,0.9,3.95,3.95,3.35,
2.25,2.4,3.85,2.3,2.9,1.05,2.25,0.3,3.65,1.95,2.15,1.25,3.55,0.7,
0.7,0.75,3.5,3.6,1.25,2.7,2.7,1.85,0.75,2.95,3.4,3.15,2.65,1.05,
3.3,1.6,1.25,3.55,0.4,1.35,3.95,4.1,2.75,0.55,1.45,2.25,2.35,2.6,
2.55,0.75,2.2,0.8,0.5,0.6,3.3,0.3,2.95,2.0,3.65,1.35,0.8 ,0.55,
2.65,1.95,1.15,1.7,0.3,1.55,0.75,1.05,3.25,3.3]
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

#geometry = [mp.Block(material=mp.vacuum,
#		     size=mp.Vector3(sr,0,dpml+dpad),
#                    center=mp.Vector3(0.5*sr,0,-0.5*sz+0.5*(dpml+dpad)))]

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

E2_r = E2_r/max(E2_r)
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
#plt.semilogy(np.linspace(0,sr-dpml,n,E2_r,'ro-')
plt.xlim(-2,5)
plt.ylim(0,1)
plt.xticks([t for t in np.arange(0,6,1)])
plt.grid(True,axis="y",which="both",ls="-")
plt.xlabel(r'$r$ coordinate (μm)')
plt.tight_layout()
plt.savefig("lens_farfields.png")
plt.ylabel(r'energy density of far fields, |E|$^2$')


	
	
	
	
	
	
	
	
	
	
	
	
	
	

