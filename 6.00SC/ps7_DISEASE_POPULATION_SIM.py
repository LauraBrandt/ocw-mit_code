# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        cleared = random.random()
        return cleared<self.clearProb

    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        prob = self.maxBirthProb*(1-popDensity)
        randNum = random.random()
        if randNum<prob:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        raise NoChildException



class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)     

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        returns: The total virus population at the end of the update (an
        integer)
        """
        ## Determine whether each virus particle survives and updates the list
        ## of virus particles accordingly.
        viruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                viruses.append(virus)
        self.viruses = viruses
        
        ## The current population density is calculated. This population density
        ##  value is used until the next call to update()
        popDensity = len(viruses)/float(self.maxPop)

        ## Determine whether each virus particle should reproduce and add
        ## offspring virus particles to the list of viruses in this patient.
        childViruses = []
        for virus in self.viruses:
            childViruses.append(virus)
            try:
                newVirus = virus.reproduce(popDensity)
                childViruses.append(newVirus)
            except NoChildException:
                pass
        self.viruses = childViruses
        
        ## Return the total virus population at the end of the update
        return self.getTotalPop()



#
# PROBLEM 2
#
def simulationWithoutDrug(maxBirthProb, clearProb, maxPop, numViruses, numSteps):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    virusPops = []

    ## Instantiate a patient with the given parameters
    viruses = []
    for n in range(numViruses):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))
    patient = SimplePatient(viruses, maxPop)

    ## Run the simulation on the patient for the given number of timesteps
    ## and accumulate a list of the virus population at each step
    for step in range(numSteps):
        currentVirusPop = patient.update()
        virusPops.append(currentVirusPop)

##    ## Plot the virus population over time
##    pylab.plot(virusPops)
##    pylab.xlabel('time steps')
##    pylab.ylabel('virus population')
##    pylab.title('population of a SimpleVirus over time')
##    pylab.show()
    return virusPops

def runSimulation(maxBirthProb, clearProb, maxPop, numViruses, numSteps, numTrials):
    allResults = []
    for trial in range(numTrials):
        allResults.append(simulationWithoutDrug(maxBirthProb, clearProb, maxPop, numViruses, numSteps))

    averages = []
    for i in range(len(allResults[0])):
        total = 0
        for j in range(len(allResults)):
            total += allResults[j][i]
        averages.append(total/float(len(allResults)))
    
    pylab.plot(averages)
    pylab.xlabel('time steps')
    pylab.ylabel('virus population')
    pylab.title('Population of a SimpleVirus over time, \n averaged over 10 trials')
    pylab.show()


#runSimulation(0.1, 0.05, 1000, 100, 300, 10)
