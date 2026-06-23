import random
import math
import pandas as pd

#fitness function
def fitness(EmittedBehavior, behavior):
    return abs(EmittedBehavior - behavior)

#slice wise Reproduction
def ReprS(p1,p2):
    p1G, p2G = str(format(p1,"010b")), str(format(p2,"010b"))
    SliceBit = random.randint(1,9)
    p1G1 , p1G2 = p1G[ : SliceBit], p1G[SliceBit : ]
    p2G1 , p2G2 = p2G[ : SliceBit], p2G[SliceBit : ]
    c1 = int(p1G1 + p2G2, 2)
    c2 = int(p2G1 + p1G2, 2)
    return c1,c2


def ReprB(p1,p2):
    p1G, p2G = str(format(p1,"010b")), str(format(p2,"010b"))
    c = []
    for i in range(10):
        if random.random() < 0.5:
            c.append(p1G[i])
        else:
            c.append(p2G[i])
    c = int("".join(c), 2)
    return c



def Exp(mu):
    u = random.random()
    x = -mu * math.log(1-u)
    return x

def lnr(mu):
    u = random.random()
    x = 3*mu * (1 - math.sqrt(1-u))
    return x


def ExpSelection(BehFitPair):
    parents = []
    i = 0
    while True:
        x = lnr(mu)
        for b,f in BehFitPair.items():
            if abs(f-x) <= 0.01:
                i += 1
                parents.append(b)
                if i ==2:
                    break
        if i == 2:
            break
    return parents


def mutate(b):
    gene = list(str(format(b,"010b")))
    p = random.randint(0,9)
    gene[p] = str(abs(int(gene[p]) - 1))
    gene = "".join(gene)
    return int(gene,2)



#null distribution, one tailed
#trialN trials per condition
TrialN = 1000
CVList = [] 
alpha = 0.05

for mr in [0.01,0.05,0.1,0.2,0.3]:
    Distribution = []
    for _ in range(TrialN):
        #EXT-----------------------------------------------------------------
        MutRate = mr
        tick = 0
        n = 1000

        CumRes = 0

        populationN = 100


        pop = []
        for _ in range(populationN):
            b = random.randint(0,1023)
            pop.append(b)

        

        for  i in range(n):

            EB = random.choice(pop) #EB:emitted behavior

            NewPop = []
            if EB >=471 and EB <= 511:
                CumRes += 1
            
            #selection and reproduction
            for _ in range(populationN//2):
                p1, p2 = random.sample(pop,2)
                c1,c2 = ReprS(p1, p2)
                NewPop.append(c1)
                NewPop.append(c2)

            #mutation
            NP = []
            for b in NewPop:
                if random.random() <= MutRate:
                    b = mutate(b)
                NP.append(b) 
            NewPop = NP
            pop = NewPop

        ResponseRate = CumRes/n
        Distribution.append(ResponseRate)
    rank = math.ceil(TrialN * alpha)
    CriticalValue = sorted(Distribution, reverse=True)[rank - 1]
    CVList.append({"mutation rate":mr,"critical value(alpha = 0.05)": CriticalValue})

print(CVList)