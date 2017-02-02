import math
import matplotlib.pyplot as plt

"""
The nice way to work:
    - every 6 hours, we will make 36 (6 hours * 6 10min) decision calculation over the last 100 relevant values
    - We will need a tag relevant residu
"""

def get_power_model(WdSpeed10Min, Pn=1683, Vn=10.83, Ksi=0.38, Omega=0.27998, AFactor=0.46, PCons=-5):
    """
    This function return the power of the model
    :param WdSpeed10Min: the avg 10 min wind speed value
    :param Pn: Nominal power
    :param Vn: Nominal wind speed
    :param Ksi: For damping
    :param Omega: for retard
    :param AFactor: dont know
    :param PCons: What the turbine consume out of production
    :return: model power fct of wind speed avg 10 min
    """

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
    """
    return residu
    :param PModelList: list of Pmodel values
    :param P10MinList: list of real power to compare with
    :return: list of residu
    """
    retList=[]

    for i in range(len(PModelList)):
        res=float(P10MinList[i])-float(PModelList[i])
        retList.append(res)

    return retList

def get_relevant_residual(P10MinList, ResList, VList, Vn=10.83, PLim=1683, PRelevant=75):
    """
    The function return the relevant residu list
    :param P10MinList: The real power
    :param ResList: The residu list
    :param VList: The wind speed 10 min list
    :param Vn: The nominal wind speed (if V < Vn: not relevant)
    :param PLim: The nominal power if we have a limitation
    :param PRelevant: The power output from which we consider it is relevant
    :return: list of relevant residu
    """
    RetList=[]
    WRetList=[]

    for i in range(len(P10MinList)):

        if P10MinList[i] > PRelevant and VList[i]<Vn and P10MinList[i]<PLim:
            RetList.append(ResList[i])
            WRetList.append(VList[i])

    return RetList, WRetList

def get_decision(ResListRelevant, Dev=100, MinAmount=0):
    """
    This function return the decision made over the relevant residu list
    :param ResListRelevant: list of residu
    :param Dev: if Dev >>>> the result will trand to be negative (good condition), we allow Dev as normal
    :param MinAmount: The minimum amount of data to consider this calculation relevant
    :return: False if not enough data, result decision if enough, if >0 --> error, if < 0 --> ok
    """
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
