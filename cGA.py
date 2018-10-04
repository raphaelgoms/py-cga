import random
from operator import itemgetter

MAXGEN = 240

def _round(c):
	_c = []
	for i in range(len(c)):
		_c.append(int(round(c[i])))
	return _c

def fitness(c):
	return sum(c) # One-max problem

def generate(p):
	c = []
	for i in range(len(p)):
		r = random.random()
		if r < p[i]:
			c.append(1)
		else:
			c.append(0)
	return c

def cgenerate(p, q):
	c = []

	r = random.random()
	if (r < p[0]):
		c.append(1)
	else:
		c.append(0)

	for i in range(1, len(p)):
		r = random.random()
		#print p[i], q[i-1][c[i-1]],  q[i-1][c[i-1]] * p[i-1]
		if (r < p[i] + q[i-1][c[i-1]] * p[i-1]):
			c.append(1)
		else:
			c.append(0)
	return c

def compete(a, b):
	fa = fitness(a)
	fb = fitness(b)

	if fa > fb:
		return a, b
	else:
		return b, a

def converged(c):
	rest = 0.0
	for i in range(len(c)):
		rest += c[i] - int(c[i])
	if rest > 0.0:
		return False
	else:
		return True

def crossover(chrom1, chrom2):
	c1a = chrom1[:50]
	c1b = chrom1[50:]
	
	c2a = chrom1[:50]
	c2b = chrom1[50:]

	child1 = c1a + c2b
	child2 = c2a + c1b

	return child1 if fitness(child1) > fitness(child2) else child2 

def mutate(chrom):
	if random.uniform(0, 1) < 0.1:
		idx = random.choice(range(len(chrom)))
		chrom[idx] = abs(chrom[idx]-1)
	return chrom

def sGA(n, l):
	p = [] #population
	for i in range(n):
		idv = [random.choice((0,1)) for i in range(l)]
		p.append([idv, fitness(idv)])
	
	it = 0
	while True:
		#selection
		p = sorted(p, key=itemgetter(1))
		p.reverse()

		if it > MAXGEN:
			print (len(p[0][0]))
			return p[0][0]

		#print("selection")
		#for i in range(n):
		#	print(p[i][0])

		#crossover
		for i in range(int(n/2)):
			child = crossover(p[i][0], p[i+1][0]) 
			loser = i if (p[i][1] > p[i+1][1]) else i+1
			fc = fitness(child)
			if fc > p[loser][1]:
				p[loser] = [child, fc]

		#mutation
		for i in range(n):
			p[i][0] = mutate(p[i][0])
			p[i][1] = fitness(p[i][0])

		it+=1

def cGA(n, l):
	p = [0.5 for x in range(l)]  	# probability vector

	it = 0
	while True:
		if it > MAXGEN: 
			return _round(p)
		#print "p: ", p
		a = generate(p)
		#print "a", a
		b = generate(p)
		#print "b", b

		winner, loser = compete(a, b)

		for i in range(l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					p[i] += 1.0/n
				else:
					p[i] -= 1.0/n

		if (converged(p)):
			return _round(p)

		it+=1

def fb_cGA(n, l):
	p = [0.5 for x in range(l)]  	# probability vector
	
	ufreq = [0 for x in range(l)]  # number of increment updates
	dfreq = [0 for x in range(l)]  # number of decrement updates
	ucon = [0 for x in range(l)]  	# number of continuous increment updates
	dcon = [0 for x in range(l)]  	# number of continuous decrement updates

	gen = 0 						# number of generations
	while True:
		if gen > MAXGEN: 
			return _round(p)
		#print "p: ", p
		a = generate(p)
		#print "a", a
		b = generate(p)
		#print "b", b

		winner, loser = compete(a, b)

		for i in range(l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					ufreq[i] += 1
					ucon[i] += 1
					dcon[i] = 0
					if ufreq[i] > dfreq[i] and gen > n/3:
						p[i] += (1.0/n + (p[i] * ucon[i]/100))
					else:
						p[i] += 1.0/n
				else:
					dfreq[i] += 1
					dcon[i] += 1
					ucon[i] = 0
					if dfreq[i] > ufreq[i] and gen > n/3:
						p[i] -= (1.0/n + (p[i] * dcon[i]/100))
					else:
						p[i] -= 1.0/n

		if (converged(p)):
			return _round(p)

		gen+=1

def ls_cGA(n, l):
	p = [0.5 for x in range(l)]  	# probability vector

	gen = 0
	while True:
		if gen > MAXGEN: 
			return _round(p)
		#print "p: ", p
		a = generate(p)
		#print "a", a
		b = generate(p)
		#print "b", b

		winner, loser = compete(a, b)

		for i in range(l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					p[i] += 1.0/n
				else:
					p[i] -= 1.0/n

		## Local Search ##
		if gen > n/3:
			for i in range(l):
				new = winner
				new[i] = 1 - winner[i]
				fwin = fitness(winner)
				fnew = fitness(new)
				if fnew > fwin:
					winner[i] = new[i]
					if new[i] == 1:
						p[i] += 1.0/n
					else:
						p[i] -= 1.0/n
		##################	

		if (converged(p)):
			return _round(p)

		gen+=1 

def pe_cGA(n, l):
	p = [0.5 for x in range(l)]  	# probability vector
	echrom = [] 					# elite chromosome
	gen = 0
	while True:
		if gen > MAXGEN: 
			return _round(p)
		#print "p: ", p

		if gen == 0:
			echrom = generate(p)
		#print "a", a
		nchrom = generate(p)
		#print "b", b

		winner, loser = compete(echrom, nchrom)
		echrom = winner	

		for i in range(l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					p[i] += 1.0/n
				else:
					p[i] -= 1.0/n

		if (converged(p)):
			return _round(p)

		gen+=1

def ne_cGA(n, l):
	p = [0.5 for x in range(l)]  	# probability vector
	echrom = [] 					# elite chromosome
	theta = 0
	eta = 0.1*n
	gen = 0
	while True:
		if gen > MAXGEN: 
			return _round(p)
		#print "p: ", p

		if gen == 0:
			echrom = generate(p)
		#print "a", a
		nchrom = generate(p)
		#print "b", b

		winner, loser = compete(echrom, nchrom)

		if theta < eta:
			echrom = winner	
			theta+=1
		else:
			echrom = generate( [0.5 for x in range(l)] )
			theta = 0

		for i in range(l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					p[i] += 1.0/n
				else:
					p[i] -= 1.0/n

		if (converged(p)):
			return _round(p)

		gen+=1

def cp_cGA(n, l):
	p = [0.5 for x in range(l)]  	# probability vector
	q = [[0.5, 0.5] for x in range(l-1)]

	gen = 0
	while True:
		if gen > MAXGEN: 
			return _round(p)
		#print "p: ", p
		a = cgenerate(p, q)
		#print "a", a
		b = cgenerate(p, q)
		#print "b", b

		winner, loser = compete(a, b)

		for i in range(l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					p[i] += 1.0/n
				else:
					p[i] -= 1.0/n

		for i in range(1, l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					q[i-1][winner[i-1]] += 1.0/n
					if q[i-1][winner[i-1]] > 1.0:
						q[i-1][winner[i-1]] = 1.0
				else:
					q[i-1][winner[i-1]] -= 1.0/n
					if q[i-1][winner[i-1]] < 0.0:
						q[i-1][winner[i-1]] = 0.0

		#print winner
		if (converged(p)):
			return _round(p)

		gen+=1

def cpe_cGA(n, l):
	p = [0.5 for x in range(l)]  	# probability vector
	q = [[0.5, 0.5] for x in range(l-1)]
	echrom = [] 					# elite chromosome
	gen = 0
	while True:
		if gen > MAXGEN: 
			return _round(p)
		#print "p: ", p

		if gen == 0:
			echrom = cgenerate(p, q)
		#print "a", a
		nchrom = cgenerate(p, q)
		#print "b", b

		winner, loser = compete(echrom, nchrom)
		echrom = winner	

		for i in range(l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					p[i] += 1.0/n
				else:
					p[i] -= 1.0/n

		for i in range(1, l):
			if winner[i] != loser[i]:
				if winner[i] == 1:
					q[i-1][winner[i-1]] += 1.0/n
					if q[i-1][winner[i-1]] > 1.0:
						q[i-1][winner[i-1]] = 1.0
				else:
					q[i-1][winner[i-1]] -= 1.0/n
					if q[i-1][winner[i-1]] < 0.0:
						q[i-1][winner[i-1]] = 0.0

		if (converged(p)):
			return _round(p)

		gen+=1

'''
n = 40   # population size
l = 100  # chromossome lenght

p = cGA(n, l)
print "cGA: ", fitness(p)

p = fb_cGA(n, l)
print "fb_cGA: ", fitness(p)

p = ls_cGA(n, l)
print "ls_cGA: ", fitness(p)

p = pe_cGA(n, l)
print "pe_cGA: ", fitness(p)

p = pe_cGA(n, l)
print "ne_cGA: ", fitness(p)

p = cp_cGA(n, l)
print "cp_cGA: ", fitness(p)

p = cpe_cGA(n, l)
print "cpe_cGA: ", fitness(p)
'''