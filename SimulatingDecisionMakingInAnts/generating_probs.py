import numpy as np

# a function to compute probabiliites of an ant travelling between any two locations,
# given the mean journey time between the locations
# - you may come up with a better function than this, but I'd really rather you
# spent your time on more interesting tasks, so we can consider this to be good
# enoughprint(lhs)
def compute_probs(means, SD=0):
    #print(means)

    # caluculate probs based on mean journey times
    probs = np.sqrt(1/means)

    # add some variance to the calculated probs
    #   numpy.maximum is used to prevent negative values resulting from adding a
    #   random value drawn from a normal distribution with zero mean
    #   - thanks go to Alexis for test-driving an earlier version of the code and
    #   highlighting the need for this
    probs = probs + np.maximum(np.zeros(shape=np.shape(probs)),
                               np.random.normal(size=np.shape(probs)) * SD)

    # fix the sum over every column to be equal to 1, to obey rules of probability
    for i in range(np.shape(probs)[0]):
        col_sum = np.sum(probs[:,i])
        probs[:,i] = probs[:,i] / col_sum

    # return the probabilities
    return probs

# standard deviation for generating probabilities
#   setting this to 0 will mean the probabilities will always be the same
#   setting it to a small value will lead to some variance around the computed probs,
#       and to the probabilities between two nests not being the same for journeys
#       in both directions
#   setting it too big will lead to very odd results
# standard_dev = 0
'''
    To test the function, I copied the mean journey time arrays from the Robinson
    et al. paper, and computed probs for all.

    They are not a million miles away from the probabilities given in the paper,
    and so I think they are god enough for our purposes.
'''


################# mean time to get between each nest ##################

