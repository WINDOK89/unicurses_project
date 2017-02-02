import math
import matplotlib.pyplot as plt

def get_power_model(WdSpeed10Min, Pn=1683, Vn=10.83, Ksi=0.38, Omega=0.27998, AFactor=0.46, PCons=-5):
    VDiff=Vn-WdSpeed10Min
    ExpTerm=math.exp(-Ksi*Omega*VDiff)
    RootTerm=math.sqrt(1-math.pow(Ksi,2))
    SinTerm=Omega*RootTerm*VDiff+math.atan((RootTerm/Ksi))
    y=1-(ExpTerm/RootTerm)*math.sin(SinTerm)
    Ret=Pn*(1-math.pow(y,AFactor))
    if y>=1:
        y=1
    ValueToReturn=0
    if WdSpeed10Min > Vn:
        ValueToReturn=Pn
    elif Ret<PCons:
        ValueToReturn=PCons
    else:
        ValueToReturn=Ret

    return ValueToReturn

def get_residual(PModelList, P10MinList):
    retList=[]
    for i in range(len(PModelList)):
        res=float(P10MinList[i])-float(PModelList[i])
        retList.append(res)
    return retList

def get_relevant_residual(P10MinList, ResList, VList, Vn=10.83, Pn=1683, PLim=1683, PRelevant=75):
    RetList=[]
    WRetList=[]
    for i in range(len(P10MinList)):
        if P10MinList[i] > PRelevant and VList[i]<Vn and P10MinList[i]<PLim:
            RetList.append(ResList[i])
            WRetList.append(VList[i])
    return RetList, WRetList

def get_decision(ResListRelevant, Dev=100, MinAmount=0):
    if len(ResListRelevant)>MinAmount:
        Result=0
        for elt in ResListRelevant:
            Result += math.fabs(elt)-math.fabs(elt + Dev)
        return Result
    else:
        return False



def frange(start,stop,step):
    result=[]
    while start < stop:
        result.append(start)
        start=start+step
    return result


if __name__=="__main__":
    xlist=frange(0.0,20.0,0.1)
    ylist=[]
    for elt in xlist:
        ylist.append(get_power_model(elt))

    plt.ylabel("Power (Kw)")
    plt.xlabel("Wind Speed (m/s)")
    plt.grid()
    plt.plot(xlist, ylist, 'r.')
    plt.show()
