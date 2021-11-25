time_means = np.array([[1, 36, 143], [36, 1, 116], [143, 116, 1]]) #Initial time it takes to visit a site.
probs = gen_prob.compute_probs(time_means,0.2) #Initialize probabilities dependent on time means.
time_stddevs = time_means / 5 #Standard deviation of time means.
quals = np.array([-np.inf, 3, 6]) #Initialize nest qualities.
qual_stddev = np.array([1, 1, 1]) #Standard deviation of nest qualities
n = 27 #Initialize number of ants
threshold_mean = 5 #Initial Mean threshold of ants
threshold_stddev = 1 #Standard deviation of ant threshold

current_time, discovers, visits, accepts, Ants, rnd_seed, antsSelectedOne, antSelectedTwo = \
    rc.RobinsonCode(n, quals, probs, threshold_mean, threshold_stddev, qual_stddev, time_means, time_stddevs) #Call Robinson code function

func RobinsonCode(n, quals, probs, threshold_mean, threshold_stddev, qual_stddev, time_means, time_stddevs):
    nestNum = probs.shape[0]            #Get number of nests (3 in this case)
    accepts = np.zeros([n], dtype=int)  #Initialize variable to store accepted site
    current_time = np.zeros([n])        #Initialize varaibale to store current time
    discovers = np.zeros([nestNum, n])  #Initialize variable to store site discovery
    visits = np.zeros([nestNum, n])     #Initialize variable to store site visits
    Ants = []                           #Dictionary of ants to store information.
    for i in range(n):
        ant = {'path': [],      #Complete path ant took while selecting a site
               't': [],         #Time taken to select the path
               'thresh': 0,     #Final threshold with std.dev. calculation
               'selected': 0}   #If the ant has selected a site
        Ants.append(ant)

    rnd_seed = int(time.time())
    np.random.seed(rnd_seed)    #Set changing random seed as the current time
    Max_num_steps = 1000        #Max steps allowed to explore the sites
    for i in range(n): 
        current_time[i] = 0
        accepts[i] = 0          #Ant is at home site (0)
        discovers[0,i] = -1     #Ant has discovered home site
        visits[0,i] = 1         #Ant has visited home site
        for j in range(1, nestNum):
            discovers[j,i] = 0  #Ant has not discovered other sites
            visits[j,i] = 0     #Ant has not visited other sites

        thresh = threshold_stddev * np.random.randn() + threshold_mean #Final ant threshold calculation
        num_step = 0                            #Count of steps to selcect the final site
        Ants[i]['path'].append(accepts[i])      #Initialize current ant path (starting from 0)
        Ants[i]['t'].append(current_time[i])    #Initialize current ant time
        Ants[i]['thresh'] = thresh              #Initialize current ant threshold (calculated from above)
        Ants[i]['selected'] = 0                 #Initialize current ant site selection (starting from 0)

        while Ants[i]['selected'] == 0:                 #This look runs till the ant has not selected a site or reached max steps
            perceivedQuality = qual_stddev[accepts[i]] * np.random.randn() + quals[accepts[i]]  #Calculate perceived quality
            if perceivedQuality >= Ants[i]['thresh']:   #Check if perceived quality is higher than ant threshold and select that site
                Ants[i]['selected'] = 1                 #NB: -inf(for the first site)
                break

            if num_step > Max_num_steps:                #Check if max steps is reached and break the loop
                Ants[i]['selected'] = 0                 #I have found that generally no site is selected in this case
                break

            ran = np.random.uniform()                   #Random sampling to start visiting sites (Monte Carlo)

            newsite = 0                                 #Initial site is 0

            while ran > probs[newsite, accepts[i]]:     #Explore until the sample exceeds the probabilty of visiting the site
                ran = ran - probs[newsite, accepts[i]]  #Subtract the sample
                newsite = newsite + 1                   #Move on to the new site

            delta = max(1, time_stddevs[newsite, accepts[i]] * np.random.randn() + time_means[newsite, accepts[i]])
            current_time[i] = current_time[i] + delta
            accepts[i] = newsite                        #Set the current site as temporarily accepted to check percieved quality.

            if discovers[newsite, i] == 0:              #If site not discoverd already
               discovers[newsite, i] = current_time[i]  #Insert discovery time for that site

            visits[newsite, i] = visits[newsite, i] + 1 #Increment the number of visits to that site

            num_step = num_step + 1                     #Increment number of steps
            Ants[i]['path'].append(accepts[i])          #Map path of the ant
            Ants[i]['t'].append(current_time[i])        #Append time taken by the ant

        Ants[i]['numSteps'] = num_step

    return current_time, discovers, visits, accepts, Ants, rnd_seed, antSelectedOne, antSelectedTwo

    engine = LatinHypercube(d=1)                                                                                        #Initialze the generator
    thresh = threshold_stddev * engine.random(n=1)[0][0] * random.choice([-1,1]) + threshold_mean                       #Ant final threshold with LHS
    perceivedQuality = qual_stddev[accepts[i]] * engine.random(n=1)[0][0] * random.choice([-1,1]) + quals[accepts[i]]   #Percieved nest quality with LHS
    ran = engine.random(n=1)[0][0]                                                                                      #Random sampling with LHS
    delta = max(1, time_stddevs[newsite, accepts[i]] * engine.random(n=1)[0][0] + time_means[newsite, accepts[i]])      #Delta calculatino with LHS


for i in range(100):                            #Number of simulations to run
    print("Simulation",i)
    ants1,ants2 = ef.runIt(5)                   #Get the ants selecting site1 and site2 from RobinsonCode
    print(ants1)
    print(ants2)
    if (len(ants1) < ((n*41)/100)):             #Determine if simulation was good or bad (41% ants selecting poor site move on to better site [9])
        good_sims += 1
    else:
        bad_sims += 1

    if (len(ants1)!=0):
        ratios.append(len(ants2)/len(ants1))    #Calculating how many ants selected better nest
    else:
        ratios.append(len(ants2))

plt.title("GoodSims vs BadSims "+str(good_sims)+":"+str(bad_sims))
plt.xlabel("Sims")
plt.ylabel("Ratio")
plt.plot(ratios)
plt.show()


if (len(antsSelectedOne)!=0):                                       #Get ants that selected site1
    print("Do you want them to move to the better nest (y/n)?")     
    ans = input()
    if(ans == 'y'):
        current_time, discovers, visits, accepts, Ants, rnd_seed, preqtimes, preqdiscovers, preqvisits, preqaccepts = \
            lhsSim.lhsSim(len(antsSelectedOne), quals, probs, threshold_mean, threshold_stddev, qual_stddev, time_means, time_stddevs, [], [])
        psdr.PlotSummaryDataRobinson(current_time, accepts, discovers, visits, Ants) #Pass the ants to LHS if user wants

    else:
        print("Ants do not leave their own behind!")

func compute_probs(means, SD=0):
    # caluculate probs based on mean journey times
    probs = np.sqrt(1/means)

    # add some variance to the calculated probs
    probs = probs + np.maximum(np.zeros(shape=np.shape(probs)),
                               np.random.normal(size=np.shape(probs)) * SD)

    # fix the sum over every column to be equal to 1, to obey rules of probability
    for i in range(np.shape(probs)[0]):
        col_sum = np.sum(probs[:,i])
        probs[:,i] = probs[:,i] / col_sum

    # return the probabilities
    return probs