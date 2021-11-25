import numpy as np
import PlotSummaryDataRobinson as psdr
import OutputRobinsonDataExcel as orde
import RobinsonCode as rc
import generating_probs as gen_prob
import lhs_sim as lhsSim

# ExampleUsingRobinsonCodeNew

# this sets the name of the outp[ut file. It stores the data for each of
# your tests so you'll need to call it something that indicates what
# experiment it is
# output_file='RobinsonTestExperimentTest1.mat'
output_file_xls = 'RobinsonTestExperimentTest1_LHS.xlsx'

# mean time to get between each nest
time_means = np.array([[1, 36, 143], [36, 1, 116], [143, 116, 1]]) #The paper mentions that ants tend to reject the low-quality nest and will continue searching for the good quality nest even if its far.
#time_means = np.array([[1, 50, 50], [50, 1, 50], [50, 50, 1]])

# these parameters are for the first experiment
#
# probabilities of visiting each site from each other
probs = gen_prob.compute_probs(time_means,0.2)
#probs = np.array([[0.91, 0.15, 0.03], [0.06, 0.8, 0.06], [0.03, 0.05, 0.9]])
#probstt = np.array([[0.92, 0.15, 0.08], [0.03, 0.83, 0.05], [0.04, 0.08, 0.86]]) #The mean time from site 1 - site 0 is way less than site1-site2 then why is the prob of going to both of them from site1 same? (The site1-site0 prob should be greater implement and check (The error increases and a high number of ants select site 1 instead of site 2))
#probst = np.array([[np.round(np.random.uniform(0.91,0.99,1)[0],2), np.round(np.random.uniform(0.1,0.19,1)[0],2), np.round(np.random.uniform(0.02,0.09,1)[0],2)], [np.round(np.random.uniform(0.03,0.09,1)[0],2), np.round(np.random.uniform(0.8,0.9,1)[0],2), np.round(np.random.uniform(0.03,0.09,1)[0],2)], [np.round(np.random.uniform(0.03,0.09,1)[0],2), np.round(np.random.uniform(0.05,0.09,1)[0],2), np.round(np.random.uniform(0.8,0.99,1)[0],2)]])
#print(probst)
#print(probs)
#probs = np.array([[0.91, 0.5, 0.5], [0.5, 0.8, 0.5], [0.5, 0.5, 0.91]]) #Ants have equal prob to visit sites.

# standard deviation of time to get between each nest
time_stddevs = time_means / 5

# mean quality of each nest. Note home is -infinity so it never gets picked
quals = np.array([-np.inf, 3, 6]) #The ants will always select site 1 if the probability of visiting from site 1 to site 2 is same and site 2 has significantly good quality than site 1

# standard deviation of quality: essentially this controls
# how variable the ants assessment of each nest is. This is currently set
# as in the 1st experiment where the variability is the same for each nest
qual_stddev = np.array([1, 1, 1])
# However, if you want to change is so nests perceived w different accuracy
# you could do eg qual_stddev = [1, 1, 4]

# set the number of ants
n = 27

# these govern the ant's threshold
threshold_mean = 5
threshold_stddev = 1

current_time, discovers, visits, accepts, Ants, rnd_seed, antsSelectedOne, antSelectedTwo, preqtimes, preqdiscovers, preqvisits, preqaccepts = \
    rc.RobinsonCode(n, quals, probs, threshold_mean, threshold_stddev, qual_stddev, time_means, time_stddevs, [], [])

# note: I have changed the order of saving data and plotting, as the matplotlib figure was blocking execution as long
# as it was open

# save the data as matlab variables - NOT IMPLEMENTED IN PYTHON
# save(output_file)

# save some of the data as excel
orde.OutputRobinsonDataExcel(output_file_xls, Ants, current_time, accepts, discovers, visits)

# Plot Summary data
psdr.PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants)

print("Ants that selected the poor site ", antsSelectedOne)

if (len(antsSelectedOne)!=0):
	print("Do you want them to move to the better nest (y/n)?")
	ans = input()
	if(ans == 'y'):
		current_time, discovers, visits, accepts, Ants, rnd_seed, preqtimes, preqdiscovers, preqvisits, preqaccepts = \
			lhsSim.lhsSim(len(antsSelectedOne), quals, probs, threshold_mean, threshold_stddev, qual_stddev, time_means, time_stddevs, [], [])
		psdr.PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants)

	else:
		print("Ants do not leave their own behind!")


"""ants_site1 = []
ants_site2 = []
ratio = []
for i in range(3):
	current_time, discovers, visits, accepts, Ants, rnd_seed, preqtimes, preqdiscovers, preqvisits, preqaccepts = \
		rc.RobinsonCode(n, quals, probs, threshold_mean, threshold_stddev, qual_stddev, time_means, time_stddevs, [], [])

	#psdr.PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants)

	for i in range(len(accepts)):
		if (accepts[i] == 1):
			ants_site1.append(accepts[i])
		else:
			ants_site2.append(accepts[i])

ratio.append(len(ants_site2)/len(ants_site1))"""
