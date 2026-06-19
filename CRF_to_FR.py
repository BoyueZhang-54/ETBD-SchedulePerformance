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


def Selection(BehFitPair):
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

    
#main--------------------------------
#mu:mean fitness of parents,MutRate: probability of mutation
for name, value in zip(["FR 5","FR 10","FR 20","FR40","FR80","FR200"], [5, 10, 20, 40, 80, 200]):
    for mr in [0.01,0.05,0.1,0.15,0.2,0.3]:
        #phase1---CRF-----------------------------------------
        mu = 20
        MutRate = mr
        tick = 0
        n = 1000
        block = 0

        midpoint = 491

        populationN = 100

        CumRecord = 0
        CumRes = 0

        RefLoad = 1
        timer = 0

        ScheValue = value
        ScheduleName = name
        phase = 1

        data = [{"ticks":tick,"blocks":block,"response":"Null","TargetRes":"Null","CumRecord":CumRecord,"CumRes":CumRes,
                    "reinforcement":"Null","mu":mu,"MutRate":MutRate,"Schedule":ScheduleName}]

        #initial population
        pop = []
        for _ in range(populationN):
            b = random.randint(0,1023)
            pop.append(b)


            
        #target behavior:471-511
        for  i in range(n):
            reinforcement = 0
            resp = 0
            tick += 1
            timer += 1
            block = ((tick - 1)//500) + 1

            EB = random.choice(pop) #EB:emitted behavior


            RefLoad = 1


            NewPop = []
            if EB >=471 and EB <= 511:
                resp = 1
                CumRecord += 1
                CumRes += 1

                if RefLoad == 1:
                    reinforcement = 1
                    timer = 0

                if CumRecord >= 300:
                    CumRecord = 0
                
                if reinforcement == 1:
                    BehFitPair = {}
                    #create dict {behavior:fitness}
                    for b in pop:
                        FitValue = fitness(EB, b)
                        BehFitPair[b] = FitValue

                    
                    #selection and reproduction
                    for _ in range(populationN//2):
                        p1,p2 = Selection(BehFitPair)
                        c1, c2 = ReprS(p1, p2)
                        NewPop.append(c1)
                        NewPop.append(c2)

                    

                        
                if reinforcement == 0:
                    
                    for _ in range(populationN//2):
                        p1, p2 = random.sample(pop,2)
                        c1, c2 = ReprS(p1, p2)
                        NewPop.append(c1)
                        NewPop.append(c2)

                    

                
            else:

                #selection and reproduction
                for _ in range(populationN//2):
                    p1, p2 = random.sample(pop,2)
                    c1, c2 = ReprS(p1, p2)
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




    
        #phase 2-----------------------------------------------------------------
        mu = 20
        phase = 2
        MutRate = mr
        tick2 = 0
        n2 = 5000
        block2 = 0

        CumRecord2 = 0
        CumRes2 = 0

        ScheduleName = name
        ScheValue = value
        
        RefLoad = 0
        respcount = 0


        for  i in range(n2):
            reinforcement = 0
            resp = 0
            tick2 += 1
            block2 = ((tick2 - 1)//500) + 1

            EB = random.choice(pop) #EB:emitted behavior


            if respcount >= ScheValue:
                RefLoad = 1


            NewPop = []
            if EB >=471 and EB <= 511:
                resp = 1
                respcount += 1
                CumRecord2 += 1
                CumRes2 += 1

                if RefLoad == 1:
                    reinforcement = 1
                    RefLoad = 0
                    respcount = 0

                if CumRecord2 >= 300:
                    CumRecord2 = 0
                
                if reinforcement == 1:
                    BehFitPair = {}
                    #create dict {behavior:fitness}
                    for b in pop:
                        FitValue = fitness(EB, b)
                        BehFitPair[b] = FitValue

                    
                    #selection and reproduction
                    for _ in range(populationN//2):
                        p1,p2 = Selection(BehFitPair)
                        c1, c2 = ReprS(p1, p2)
                        NewPop.append(c1)
                        NewPop.append(c2)

                    

                        
                if reinforcement == 0:
                    
                    for _ in range(populationN//2):
                        p1, p2 = random.sample(pop,2)
                        c1, c2 = ReprS(p1, p2)
                        NewPop.append(c1)
                        NewPop.append(c2)

                    

                
            else:

                #selection and reproduction
                for _ in range(populationN//2):
                    p1, p2 = random.sample(pop,2)
                    c1, c2 = ReprS(p1, p2)
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
            data.append(
                {"ticks":tick2,"blocks":block2,"response":EB,"TargetRes":resp,"CumRecord":CumRecord2,"CumRes":CumRes2,
                                "reinforcement":reinforcement,"mu":mu,"MutRate":MutRate,"Schedule":ScheduleName}
                                )

            
        df = pd.DataFrame(data)    
        df.to_excel(f"CrfTo{ScheduleName}_{mu}_{MutRate}_phase{phase}.xlsx",index=False)