def diff(ht,wvl_cen):
	import meep as mp
	import numpy as np
	import math
	import random
	
	#450	 1.674	
	#550     1.642
	#650     1.629
	
	if (wvl_cen == 0.45):
		photoresist = mp.Medium(index=1.674)   #波长为450nm时光刻胶的折射率 
	elif (wvl_cen == 0.55):
		photoresist = mp.Medium(index=1.642)   #波长为550nm时光刻胶的折射率 
	else:
		photoresist = mp.Medium(index=1.629)   #波长为650nm时光刻胶的折射率 
	
	
	## at least 8 pixels per smallest wavelength, i.e. np.floor(8/wvl_min)
	resolution = 25.0          

	dpml=1.0                                #PML厚度               
	dpad =2.0                               #透镜与PML间距
	dsub = 2.0                             # substrate thickness
	width = 0.5                            #环的宽度
	r= width*len(ht)                        #透镜的半径  50um
	focal_length = 100.0                      #焦距
	spot_length=100                         #far-field line length
	ff_res = 10.0                           #far-field resoluton
	h = 1.25
	
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
	#geometry = [mp.Block(material=photoresist,
	#     		size=mp.Vector3(width,0,ht[0]),
	#  		 center=mp.Vector3(0.5*width,0,-0.5*sz+dpml+dpad+0.5*ht[0]))]
	#for n in range (1,len(ht)):
	#	geometry.append(mp.Block(material=photoresist,
	#	     size=mp.Vector3(width,0,ht[n]),
	#	     center=mp.Vector3(width*n+0.5*width,0,-0.5*sz+dpml+dpad+0.5*ht[n])))  #透镜的结构
	
	geometry = [mp.Block(material=photoresist,
	     		size=mp.Vector3(sr,0,dpml+dsub),
	 		 center=mp.Vector3(0.5*sr,0,-0.5*sz+0.5*(dpml+dsub)))]
	for n in range (0,len(ht)):
		geometry.append(mp.Block(material=photoresist,
	                                 size=mp.Vector3(width,0,ht[n]),
		                          center=mp.Vector3((width*(n)+0.5*width),0,-0.5*sz+dpml+dsub+0.5*ht[n])))  #透镜的结构
	
	
	#wvl_cen = 0.5
	frq_cen = 1/wvl_cen
	dfrq = 0.2*frq_cen

	sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
		             component=mp.Er,
		             center=mp.Vector3(0.5*(sr),0,-0.5*sz+dpml),     
		             size=mp.Vector3(sr)),
		   mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
		             component=mp.Ep,
		             center=mp.Vector3(0.5*(sr),0,-0.5*sz+dpml),
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
		                  # mp.Near2FarRegion(center=mp.Vector3(sr-dpml,0,0.5*sz-0.5*(dsub+zh+dpad)),size=mp.Vector3(z=dsub+zh+dpad)))
		                   
	sim.run(until_after_sources=100)

	ff_r = sim.get_farfields(n2f_obj, ff_res, center=mp.Vector3(0.5*(sr-dpml),0,-0.5*sz+dpml+dsub+h+focal_length),size=mp.Vector3(sr-dpml))
	E2_r = np.absolute(ff_r['Ex'])**2+np.absolute(ff_r['Ey'])**2+np.absolute(ff_r['Ez'])**2
	
	E_sum = sum(E2_r)
	n = round((1.5*(wvl_cen/(2*NA)))/(r/(len(E2_r)-1)))
	#print ('n = %d' % n)
	E = 0.0
	for i in range (n):
		E += E2_r[i]
	
	return E/E_sum  
	
	
