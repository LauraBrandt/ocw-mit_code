# 6.00 Problem Set 9
#
# Intelligent Course Advisor


SUBJECT_FILENAME = "ps9_subjects.txt"
SHORT_SUBJECT_FILENAME = "ps9_shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """
    
    subjects = {}
    inputFile = open(filename)
    for line in inputFile:
        line = line.strip() # remove whitespace
        elements = line.split(",")
        subjects[elements[0]] = (float(elements[VALUE+1]), float(elements[WORK+1])) # subject -> (value, work)
    return subjects

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#


## Each of the 3 compare functions take in 2 tuples of (value, work)

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    if subInfo1[VALUE] > subInfo2[VALUE]:
        return True
    return False

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    if subInfo1[WORK] < subInfo2[WORK]:
        return True
    return False


def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    ratio1 = float(subInfo1[VALUE])/subInfo1[WORK]
    ratio2 = float(subInfo2[VALUE])/subInfo2[WORK]
    if ratio1 > ratio2:
        return True
    return False

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    subjects_copy = dict((k,v) for k,v in subjects.items())

    totalWork = 0
    chosenSubjects = {}
    finished = False

    while not finished:
        bestSubj = None
        bestInfo = None

        # Find the next best subject that meets the restriction
        for subj in subjects_copy:
            if totalWork+subjects_copy[subj][WORK] <= maxWork:
                if bestSubj == None:
                    bestSubj = subj
                    bestInfo = subjects_copy[subj]
                elif comparator(subjects_copy[subj],bestInfo):
                    bestSubj = subj
                    bestInfo = subjects_copy[subj]

        # No more subjects could fit - finished               
        if bestSubj == None:
            finished = True
            continue

        # Update variables
        chosenSubjects[bestSubj]= bestInfo
        totalWork += bestInfo[WORK]
        del subjects_copy[str(bestSubj)]

    return chosenSubjects
          

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    pset = genPset(subjects.keys())
    #print "pset generated"
    bestGroup = chooseBest(subjects, pset, maxWork)
    bestSubjects = {}
    for subj in bestGroup:
        bestSubjects[subj] = subjects[subj]
    return bestSubjects

def dToB(n, numDigits):
    """requires: n is a natural number less than 2**numDigits
    returns a binary string of length numDigits representing the
    the decimal number n."""
    assert type(n)==int and type(numDigits)==int and n >=0 and n <2**numDigits
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n//2
    while numDigits - len(bStr) > 0:
        bStr = '0' + bStr
    return bStr

def genPset(subject_keys):
    """Generate a list of lists representing the power set of Items"""
    numSubsets = 2**len(subject_keys)
    templates = []
    for i in range(numSubsets):
        templates.append(dToB(i, len(subject_keys)))
    #print numSubsets, "templates generated"
    pset = []
    for t in templates:
        elem = []
        for j in range(len(t)):
            if t[j] == '1':
                elem.append(subject_keys[j])
        pset.append(elem)
    return pset 

def chooseBest(subjects, pset, maxWork):
    """ subjects: a dictionary of subjectName -> (value, work)
        pset: a list of lists of all the possible combinations of
        subjects (keys from the dictionary "subjects")
        maxWork: a numerical constraint on the maximum number of hours
        
        Finds the set of items from pset that has the highest value
        while not exceeding maxWork

        Returns the list of a group of keys from the dictionary subjects
        that has the highest value
    """

    bestVal = 0
    bestGroup = None
    for group in pset:
        totalVal = 0
        totalWork = 0
        for subjectKey in group:
            (value, work) = subjects[subjectKey]
            totalVal += value
            totalWork += work
        if totalWork <= maxWork and totalVal > bestVal:
            bestVal = totalVal
            bestGroup = group
    return bestGroup


### Test:
subjects = loadSubjects(SHORT_SUBJECT_FILENAME)
###printSubjects(subjects)
##result = greedyAdvisor(subjects, 15, cmpRatio)
##printSubjects(result)
bruteForceAdvisor(subjects, 15)
