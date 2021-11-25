import ExampleUsingRobinsonCode_func as ef
import numpy as np
import matplotlib.pyplot as plt

#means = np.linspace(4, 6, num=11)
#for m in means:
#	good_sims = 0
#	bad_sims = 0
#	
#	for i in range(1000):
#		print("Simulation",i)
#		ants1,ants2 = ef.runIt(m)
#		print(ants1)
#		print(ants2)
#		if (len(ants1) < ((n*41)/100)):
#			good_sims += 1
#			#plt.plot(i,ratios[i],'bo')
#		else:
#			bad_sims += 1
#			#plt.plot(i,ratios[i],'r*')
#		ratios.append(len(ants2)/len(ants1))

#returned = []
ratios = []
ants1 = []
ants2 = []
n = ef.setNumAnts()
#for m in means:
    #returned.append(ef.runIt(m))
#mean_each_sim = []
"""for i in range(10):
	print(i,"out of 10 sets of 100 simulations",)
	for i in range(1000):
		#print("Processing ant",i)
		ants1,ants2 = ef.runIt(5)
		ratios.append(len(ants2)/len(ants1))
	mean_each_sim.append(np.mean(ratios))
	#print("1",ants1)
	#print("2",ants2)
	#print("ratio",ratios)

	#plt.xlabel("Sims")
	#plt.ylabel("Ratio")
	#plt.plot(ratios,'o')
	#plt.show()
print("Mean of each simulation",mean_each_sim)
plt.plot(mean_each_sim,'o')
plt.show()"""
good_sims = 0
bad_sims = 0

for i in range(10000):
	print("Simulation",i)
	ants1,ants2 = ef.runIt(5)
	print(ants1)
	print(ants2)
	if (len(ants1) < ((n*41)/100)):
		good_sims += 1
		#plt.plot(i,ratios[i],'bo')
	else:
		bad_sims += 1
		#plt.plot(i,ratios[i],'r*')
	if (len(ants1)!=0):
		ratios.append(len(ants2)/len(ants1))
	else:
		ratios.append(len(ants2))

#for i in range(len(ratios)):
#	if (len(ants1) < 11):
#		good_steps += 1
#		#plt.plot(i,ratios[i],'bo')
#	else:
#		bad_steps += 1
#		#plt.plot(i,ratios[i],'r*')

#print("Ratio",good_steps,":",bad_steps)

plt.title("GoodSims vs BadSims "+str(good_sims)+":"+str(bad_sims))
plt.xlabel("Sims")
plt.ylabel("Ratio")
plt.plot(ratios)
plt.show()