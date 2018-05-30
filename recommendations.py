from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = { \
	'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},\
	'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 4.5},\
	'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0}, \
	'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},\
	'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},\
	'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},\
	'Dni': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}\
	}


def sim_euclid_distance(prefs, person1, person2):
	#common items ranked by both persons:
	ci = []
	for item in prefs[person1]:
		if item in prefs[person2]: ci.append(item)
	if len(ci) == 0: return 0

	Sum = (sum([pow((prefs[person1][item] - prefs[person2][item]), 2) for item in ci]))
	return 1 /(1 + Sum)

def sim_pearson_corelation(prefs, person1, person2):
	ci = []
	for item in prefs[person1]:
		if item in prefs[person2]: ci.append(item)
	if len(ci) == 0: return 0

	sum1 = sum([prefs[person1][item] for item in ci])
	sum2 = sum([prefs[person2][item] for item in ci])
	sum1sq = sum([pow(prefs[person1][item], 2) for item in ci])
	sum2sq = sum([pow(prefs[person2][item], 2) for item in ci])
	sumpr = sum([prefs[person1][item] * prefs[person2][item] for item in ci])
	n = len(ci)

	num = sumpr - (sum1 * sum2 / n)
	den = sqrt((sum1sq - pow(sum1, 2)/n) * (sum2sq - pow(sum2, 2)/n))

	if den == 0: return 0
	return num/den

def topMatches(prefs, person, n = 5, similarity = sim_pearson_corelation):
	scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
	scores.sort()
	scores.reverse()
	return scores[0:n]
	
# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson_corelation):
	totals={}
	simSums={}
	for other in prefs:
		# don't compare me to myself
		if other==person: continue
		sim=similarity(prefs,person,other)
		
		# ignore scores of zero or lower
		if sim<=0: continue
		for item in prefs[other]:
			# only score movies I haven't seen yet
			if item not in prefs[person] or prefs[person][item]==0:
				# Similarity * Score
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				# Sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+=sim
	# Create the normalized list
	rankings=[(total/simSums[item],item) for item,total in totals.items( )]
	# Return the sorted list
	rankings.sort( )
	rankings.reverse( )
	return rankings

def transformPrefs(prefs):
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})
			result[item][person] = prefs[person][item]
	return result
