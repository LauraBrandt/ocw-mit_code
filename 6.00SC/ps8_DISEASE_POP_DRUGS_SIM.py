# 6.00 Problem Set 8


import numpy
import random
import pylab
from ps7_DISEASE_POPULATION_SIM import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex':False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resistances:
            return self.resistances[drug]
        return False

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()
        probReproduce = self.maxBirthProb * (1 - popDensity)
        randomProb = random.random()
        if randomProb < probReproduce:
            newResistances = {}
            for drug in self.resistances:
                if random.random() < self.mutProb:
                    newResistances[drug] = not self.resistances[drug]
                else:
                    newResistances[drug] = self.resistances[drug]
            return ResistantVirus(self.maxBirthProb, self.clearProb, newResistances, self.mutProb)
        else:
            raise NoChildException()   

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        SimplePatient.__init__(self, viruses, maxPop)
        self.administeredDrugs = []
    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.administeredDrugs:
            self.administeredDrugs.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.administeredDrugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count = 0
        for virus in self.viruses:
            resistant = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistant = False
                    break
            if resistant:
                count += 1
        return count                   


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        viruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                viruses.append(virus)
        self.viruses = viruses
        
        popDensity = len(viruses)/float(self.maxPop)

        childViruses = []

        #print "num viruses:", len(self.viruses), "/", "num reproduced:", 
        #reproductions = 0
        for virus in self.viruses:
            childViruses.append(virus)
            try:
                newVirus = virus.reproduce(popDensity, self.administeredDrugs)
                #reproductions += 1
                childViruses.append(newVirus)
            except NoChildException:
                pass
        #print reproductions, "/",
        #print "resist pop:", self.getResistPop(['guttagonol'])
        self.viruses = childViruses

        return self.getTotalPop()




#
# PROBLEM 2
#

def runSimulationWithDrug(delay, nTrials=100):
    """
    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """

    avgViruses = None
    avgResistant = None

    for n in range(nTrials):
        nViruses, nResistant = simulationWithDrug(delay)
        
        if avgViruses == None:
            avgViruses = nViruses
        else:
            for m in range(len(nViruses)):
                avgViruses[m] += nViruses[m]
                
        if avgResistant == None:
            avgResistant = nResistant
        else:
            for m in range(len(nResistant)):
                avgResistant[m] += nResistant[m]

    for i in range(len(avgViruses)):
        avgViruses[i] = avgViruses[i]/float(nTrials)
        avgResistant[i] = avgResistant[i]/float(nTrials)

    return avgViruses, avgResistant, nTrials

def plotSimulationWithDrug(nTrials=50):
    avgViruses, avgResistant, nTrials = runSimulationWithDrug(150, nTrials)
    pylab.subplot(211)
    pylab.plot(avgViruses)
    title = "Viruses in Patient over Time \n Averaged over " +str(nTrials)+ " Trials"
    pylab.title(title)
    #pylab.xlabel("Timesteps")
    pylab.ylabel("Num. Viruses in Patient")
    
    pylab.subplot(212)
    pylab.plot(avgResistant)
    #title = "Number of Viruses Resistant to the Administered Drugs \n Averaged over "+str(nTrials)+" Trials"
    pylab.xlabel("Timesteps (drug introduced at t=150)")
    pylab.ylabel("Num. Drug-Resistant Viruses")
    
    pylab.show()
    
    

def simulationWithDrug(delay):
    patient = initializePatient()
    nViruses = []
    nResistant = []
    
    for n in range(delay):
        nViruses.append(patient.update())
        nResistant.append(patient.getResistPop(["guttagonol"]))
        
    patient.addPrescription("guttagonol")
    
    for n in range(150):
        nViruses.append(patient.update())
        nResistant.append(patient.getResistPop(["guttagonol"]))

    return nViruses, nResistant


def initializePatient():
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {"guttagonol":False, "grimpex":False}
    mutProb = 0.005
    
    viruses = []
    for n in range(100):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    
    maxPop = 1000
    
    patient = Patient(viruses, maxPop)
    return patient

#plotSimulationWithDrug()

#
# PROBLEM 3
#        

def simulationDelayedTreatment(nTrials):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    finalResults = {}
    delays = [300, 150, 75, 0]

    for delay in delays:
        finalNumViruses = []
        for n in range(nTrials):
            nViruses, nResistant = simulationWithDrug(delay)
            finalNumViruses.append(nViruses[-1])
        finalResults[delay] = finalNumViruses
        

    pylab.figure(1)
    pylab.xlabel("Num. Viruses")
    pylab.ylabel("Num. Patients with that many Viruses")
    pylab.suptitle("Effect of adding drug after a variety of delays")

    plotNum = 1
    for delay in delays:
        pylab.subplot(2,2,plotNum)
        pylab.title("Delay of "+str(delay)+" timesteps")
        pylab.hist(finalResults[delay], bins = 12, range=(0,600))
        plotNum += 1

    pylab.show()
    
      
#simulationDelayedTreatment(300)

#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment(delay):

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    patient = initializePatient()
    nViruses = []
    nResistant = []
    nResistGuttagonol = []
    nResistGrimpex = []
    
    for n in range(150):
        nViruses.append(patient.update())
        nResistant.append(patient.getResistPop(["guttagonol", "grimpex"]))
        nResistGuttagonol.append(patient.getResistPop(["guttagonol"]))
        nResistGrimpex.append(patient.getResistPop(["grimpex"]))                        
        
    patient.addPrescription("guttagonol")
    
    for n in range(delay):
        nViruses.append(patient.update())
        nResistant.append(patient.getResistPop(["guttagonol", "grimpex"]))
        nResistGuttagonol.append(patient.getResistPop(["guttagonol"]))
        nResistGrimpex.append(patient.getResistPop(["grimpex"]))

    patient.addPrescription("grimpex")

    for n in range(150):
        nViruses.append(patient.update())
        nResistant.append(patient.getResistPop(["guttagonol", "grimpex"]))
        nResistGuttagonol.append(patient.getResistPop(["guttagonol"]))
        nResistGrimpex.append(patient.getResistPop(["grimpex"]))

    return nViruses, nResistant, nResistGuttagonol, nResistGrimpex

def runSimulationTwoDrugsDelayedTreatment(nTrials):
    finalResults = {}
    delays = [300, 150, 75, 0]

    for delay in delays:
        finalViruses = []
        for n in range(nTrials):
            nViruses, nResistant = simulationTwoDrugsDelayedTreatment(delay)
            finalViruses.append(nViruses[-1])
        finalResults[delay] = finalViruses

    pylab.figure(1)
    pylab.xlabel("Num. Viruses")
    pylab.ylabel("Num. Patients with that many Viruses")
    pylab.suptitle("Effect of adding drug after a variety of delays")

    plotNum = 1
    for delay in delays:
        pylab.subplot(2,2,plotNum)
        pylab.title("Delay of "+str(delay)+" timesteps")
        pylab.hist(finalResults[delay], bins = 12, range=(0,600))
        plotNum += 1

    pylab.show()

#runSimulationTwoDrugsDelayedTreatment(100)

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations(nTrials):

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """

    delays = [300, 0]

    avgViruses = None
    avgResistant = None
    avgResistGuttagonol = None
    avgResistGrimpex = None

    fig = 1
    for delay in delays:
        for n in range(nTrials):
            nViruses, nResistant, nResistGuttagonol, nResistGrimpex = simulationTwoDrugsDelayedTreatment(delay)
            if avgViruses == None:
                avgViruses = nViruses
                avgResistant = nResistant
                avgResistGuttagonol = nResistGuttagonol
                avgResistGrimpex = nResistGrimpex            
            else:
                for n in range(len(nViruses)):
                    avgViruses[n] += nViruses[n]
                    avgResistant[n] += nResistant[n]
                    avgResistGuttagonol[n] += nResistGuttagonol[n]
                    avgResistGrimpex[n] += nResistGrimpex[n]

        for i in range(len(avgViruses)):
            avgViruses[i] = avgViruses[i]/float(nTrials)
            avgResistant[i] = avgResistant[i]/float(nTrials)
            avgResistGuttagonol[i] = avgResistGuttagonol[i]/float(nTrials)
            avgResistGrimpex[i] = avgResistGrimpex[i]/float(nTrials)

        pylab.figure(fig)
        pylab.suptitle("Effect of Adding Guttagonol and then Grimpex "+str(delay)+" Timesteps Later")

        pylab.subplot(221)
        pylab.title("Number of Viruses in Patient over Time")
        pylab.plot(avgViruses)
        pylab.ylabel("Num. Viruses")
    
        pylab.subplot(222)
        pylab.title("Number of Viruses Resistant to the Administered Drugs")
        pylab.plot(avgResistant)

        pylab.subplot(223)
        pylab.title("Number of Viruses Resistant to Guttagonol")
        pylab.plot(avgResistGuttagonol)
        pylab.xlabel("Timesteps")
        pylab.ylabel("Num. Viruses")
        
        pylab.subplot(224)
        pylab.title("Number of Viruses Resistant to Grimpex")
        pylab.plot(avgResistGrimpex)
        pylab.xlabel("Timesteps")

        fig+=1
    
    pylab.show()



simulationTwoDrugsVirusPopulations(100)
