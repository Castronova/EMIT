__author__ = 'Mario'
import random
import operator

ProfitDictionary = {}

# Note that q is weekly production
# We start the code here to iterate by integer amounts of production q
for q in range(0, 100, 1):

    # We insert the cost function here
    Cost = .5 * q*q + 5*q +100

    # Store Monte Carlo results here per iteration TODO: Fix the memory issues
    pricelist = []

    # Monte Carlo simulation starts here, assume uniform distribution, 20 iterations per q
    # weather in i +1 not dependent on i
    for i in range(0, 1000, 1):

        weather = random.uniform(0.0,1.0)
        # weather = .9
        if weather > .5:
            pricegood = 30
            pricelist.append(pricegood)

        else:
            pricebad = 20
            pricelist.append(pricebad)

    price = float(sum(pricelist) / float(len(pricelist)))
    # print weather, price
    # print pricelist
    print price

    # Profit Function is as follows
    Profit = q * price - Cost

    ProfitDictionary[q] = Profit


# Build system to concatenate and pull max value from dictionary
stats = ProfitDictionary
maximumvalue = max(stats.iteritems(), key = operator.itemgetter(1))[0]

print 'The maximum amount of caviar we should harvest is: ' + str(maximumvalue) + \
      'lbs, The projected profit is: $' + str(ProfitDictionary[maximumvalue])
