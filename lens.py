import meep as mp
import numpy as np
import math
import matplotlib.pyplot as plt
import random

b=1.25/100
h=1.25                                             
ht=[b*random.randint(1, 100) for i in range(200)]    #随机生成每个环的高度,200个环

## at least 8 pixels per smallest wavelength, i.e. np.floor(8/wvl_min)
resolution = 25           

dpml=2.0                                #PML厚度               
dpad =2.0                               #透镜与PML间距
width = 0.25                            #环的宽度
r=50                                    #透镜的半径
focal_length = 40                       #焦距
ff_res = 8

pml_layers = [mp.PML(thickness=dpml)]

sr=r+dpad+dpml
sz=dpml+dpad+h+dpad+dpml
cell_size =mp.Vector3(sr,0,sz) 


geometry = [mp.Block(material=mp.vacuum,
                     size=mp.Vector3(sr-dpad,0,h+dpad),
                     center=mp.Vector3(0.5*(sr-dpad),0,-0.5*sz+dpml+0.5*(dpad+h)))]
 

photoresist = mp.Medium(index=1.654)   #波长为500nm时光刻胶的折射率      

for n in range (200):
	geometry.append(mp.Block(material=photoresist,
                     size=mp.Vector3(width,0,ht[n]),
                     center=mp.Vector3(width*n+0.5*width,0,-0.5*sz+dpml+dpad+0.5*ht[n])))  #透镜的结构

wvl_cen = 0.5
frq_cen = 1/wvl_cen
dfrq = 0.2*frq_cen

sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
                     component=mp.Er,
                     center=mp.Vector3(0.5*(sr-dpml),0,-0.5*sz+dpml+0.5*dpad),     
                     size=mp.Vector3(sr)),
           mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
                     component=mp.Ep,
                     center=mp.Vector3(0.5*(sr-dpml),0,-0.5*sz+dpml+0.5*dpad),
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

ff_r = sim.get_farfields(n2f_obj, ff_res, center=mp.Vector3(0.5*(sr-dpml),0,-0.5*sz+dpml+dpad+h+focal_length),size=mp.Vector3(sr-dpml))

E2_r = np.absolute(ff_r['Ex'])**2+np.absolute(ff_r['Ey'])**2+np.absolute(ff_r['Ez'])**2

m=max(E2_r)
E2_r = E2_r/m
plt.figure(dpi=200)
plt.subplot(1,1,1)
plt.semilogy(np.linspace(0,sr-dpml,len(E2_r)),E2_r,'ro-')
plt.xlim(0,50)
plt.xticks([t for t in np.arange(0,55,5)])
plt.grid(True,axis="y",which="both",ls="-")
plt.xlabel(r'$r$ coordinate (μm)')
plt.tight_layout()
plt.savefig("lens_farfields.png")
plt.ylabel(r'energy density of far fields, |E|$^2$')


