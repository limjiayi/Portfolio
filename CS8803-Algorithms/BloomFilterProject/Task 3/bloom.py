# -*- coding: utf-8 -*-
#argparse allows the parsing of command line arguments
import argparse
#utility functions for the bloom filter project
import bfProjectUtils as util
#numpy numerical library - use for random values only
import numpy.random as random
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
#USAGE : 
#random.seed(x) : sets seed to x
#random.randint(a,b) : returns random integer in range [a,b) (inclusive beginning and exclusive ending values)
#DO NOT IMPORT NUMPY other than the function above


class HashType1(object):
    #Implement Hash Type 1
    
    def __init__(self, config, genHashes, c):
        """
        Args:
            config (dictionary) : contains configuration data for this hashing object 
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients 
                                    (Task 2 provides hash seeds/coefficients, 
                                    Tasks 1 and 3 require you to make them yourself) 
        """
        self.k = config['k']
        if config['task'] == 3:
            self.n = c * config['m']
        else:
            self.n = config['n']

        # set random seed to be generated seed at config load
        random.seed(config['genSeed'])

        # if generate new random hashes
        if genHashes:
            # build seed list self.seeds
            self.seeds = random.randint(low=0, high=(self.n/10000), size=self.k)
            print("Seeds: " + str(self.seeds))
            pass
        # if not gen (task 2), then use hashes that are in config dictionary
        else:
            self.seeds = config['seeds']
    
    def getHashList(self, x):
        """
        Return list of k hashes of the passed integer, using self.seeds[i]+x to 
        seed random number gen to give i'th hash value
        Args :
            x (int) : element to hash
        Returns list of k hashes of this element
        """
        results = list()
        for i in range(self.k):
            random.seed((self.seeds[i] + x))
            results.append(random.randint(low=0, high=self.n))
        
        # your code goes here
        return results


class HashType2(object):
    # Implement Hash Type 2

    def __init__(self, config, genHashes, c):
        """
        Args:
            config (dictionary):contains configuration data for this hashing object            
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients 
                                    (Task 2 provides hash seeds/coefficients, 
                                    Tasks 1 and 3 require you to make them yourself) 
        """
        self.k = config['k']
        self.N = config['N']
        self.P = util.findNextPrime(self.N)

        if config['task'] == 3:
            self.n = c * config['m']
        else:
            self.n = config['n']

        #generate new random hashes, or not if task2
        if genHashes:
            #set random seed to be generated seed at config load
            random.seed(config['genSeed'])
            #build lists of coefficients self.a and self.b
            self.a = random.randint(low=0, high=(self.n - 1), size=self.k)
            self.b = random.randint(low=0, high=(self.n - 1), size=self.k)

        #if not gen (task 2), then use hashes that are in config dictionary
        else:
            self.a = config['a']
            self.b = config['b']
            
    def getHashList(self, x):
        """
        Return list of k hashes of the passed integer, using 
        (self.a[i] * x + self.b[i] mod P) mod n 
        to give i'th hash value - remember P and n must be prime, and P >= N
        
        Args :
            x (int) : element to hash
        Returns list of k hashes of this element
        """
        results = []

        for i in range(self.k):
            results.append(((((self.a[i] * x)) + self.b[i]) % self.N) % self.n)

        #your code goes here
        return results
    
    


class BloomFilter(object):     
    #Implement a Bloom Filter data structure."""

    def __init__(self, config, c):
        """        
        Args:
            config (dictionary): Configuration of this bloom filter
            config['N'] (int) universe size
            config['m'] (int) number of elements to add to filter
            config['n'] (int) number of bits in bloom filter storage array
            config['k'] (int) number of hash functions to use
            config['task'] (int) the task this bloom filter is to perform (1,2,3)
            config['type'] (int) type of hash function (1, 2, -1==unknown type)
            if type 1 hash :
                config['seeds'] (list of k ints) : seed values for k hash functions for type 1 hash function
            if type 2 hash : 
                config['a'] (list of k ints) : a coefficients for k hash functions for type 2 hash function
                config['b'] (list of k ints) : b coefficients for k hash functions for type 2 hash function
            
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients 
                                    (Task 2 provides hash seeds/coefficients, 
                                    Tasks 1 and 3 require you to make them yourself) 
        """

        #task this boom filter is performing
        self.task = config['task']
        #task 1 and 3 reguire generated seeds for hashes, task 2 uses provided seeds/coefficients
        genHashes = (self.task != 2)
        #type of hash for this bloom filter
        self.type = config['type']
        if(self.type == 1):
            self.hashFunc = HashType1(config,genHashes,c)
        elif(self.type == 2):
            print("Hash Function 2")
            self.hashFunc = HashType2(config,genHashes,c)
        #elif(self.type == 3): #add your own hashes
        else:
            print('BloomFilter for task ' + str(self.task) + ' ctor : Unknown Hash type : ' + str(self.type))
            
        
        #your code goes here
        self.members = list()

        self.N = config['N']
        self.m = config['m']
        self.k = config['k']
        self.n = config['n']

        self.hashtable = [0] * self.n

    def add(self, x):
        """Adds x to the data structure, using self.hashFunc     
        Args:
            x (int): The integer to add to the bloom filter
        """
        self.members.append(x)
        bits = self.hashFunc.getHashList(x)

        for bit in bits:
            self.hashtable[bit] = 1

        return


    def contains(self, x):
        """Indicates whether data structure contains x, using self.hashFunc, with the possibility of false positives

        Args:
            x (int): The integer to test.
        Returns:
            True or False whether structure contains x or not
        """
        bits = self.hashFunc.getHashList(x)

        for bit in bits:
            if self.hashtable[bit] == 0:
                return False
        
        return True




"""
function will take data list, insert first m elements into bloom filter, and check all elements in datalist for membership, returning a list of results of check
    Args : 
        data (list) : list of integer data to add 
        bf (object) : bloom filter object
        m (int) : number of elements to add to bloom filter from data (first m elements)
    Returns : 
        list of results of checking 
    
"""
def testBF(data, bf, m):
    #add first m elements
    for i in range(0,m):
        bf.add(data[i]) 
    print('Finished adding '+ str(m) +' integers to bloom filter')
    resList =[]
    #test membership of all elements
    for i in range(0,len(data)):
        resList.append(str(bf.contains(data[i])))
    return resList

def testBF_3(data, bf, m):
    falsePositives = 0
    falseNegatives = 0

    # data = [x/1000 for x in data]

    #add first m elements
    for i in range(0,m):
        bf.add(data[i])
    print('Finished adding '+ str(m) +' integers to bloom filter')
    resList =[]
    #test membership of all elements
    for i in range(m,len(data)):
        result = bf.contains(data[i])
        resList.append(str(result))
        if result:
            falsePositives += 1

            for member in bf.members:
                if data[i] == member:
                    falsePositives -= 1
                    break
    print("For k = " + str(bf.k))
    print("False Positives: " + str(falsePositives))
    return resList

"""
function will support required test for Task 2.  DO NOT MODIFY.
    configData : dictionary of configuration data required to build and test bloom filter
"""
def task2(configData):        
    #instantiate bloom filter object    
    bf = BloomFilter(configData)    

    #bfInputData holds a list of integers.  Using these values you must :
    #   insert the first configData['m'] of them into the bloom filter
    #   test all of them for membership in the bloom filter
    bfInputData = util.readIntFileDat(configData['inFileName'])
    if(len(bfInputData) == 0):
        print('No Data to add to bloom filter')
        return
    else :
        print('bfInputData has '+str(len(bfInputData)) +' elements')
    #testBF will insert elements and test membership
    outputResList = testBF(bfInputData, bf, configData['m'])            
    #write results to output file
    util.writeFileDat(configData['outFileName'],outputResList)
    #load appropriate validation data list for this hash function and compare to results    
    util.compareResults(outputResList,configData)    
    print('Task 2 complete')    

"""     
these two functions are added for your convenience, if you choose to use this code to perform tasks 1 and 3
"""     
def task1(configData, inputFile):
    # if you wish to use this code to perform task 1, you may do so
    # NOTE : task 1 does not require you to instantiate a bloom filter

    hash1 = HashType1(configData, True)
    hash2 = HashType2(configData, True)
    file = open(inputFile, "r")

    try:
        byte = file.readline()
        while byte != '':
            if byte != '\n':
                hash1.getHashList(2 * int(byte))
            byte = file.readline()

    except ValueError:
        print("Reached End of File")

    finally:
        file.close()

    plotHistData(hash1.hashtables, hash1.n)
    #plotScatterData(hash2.hashtables, hash2.values)
"""
    for i in range(10):
        print("Hashes for h" + str(i))

        for j in range(10):
            print(hash1.hashtables[i][j])
"""

def plotHistData(data, limit):

    plt.interactive(False)
    plt.title('Occurrences of Hashed Values for Hash Function 1\n(Ordered Data)')
    plt.xlabel('Hashed Value\n(Histogram w/ Bucket Size: 99)')
    plt.ylabel('Occurrences')

    #fig = plt.figure()

    num_bins = 99
    #y, x, _ = plt.hist(data, num_bins, facecolor='blue', alpha=0.5)
    y, x, _ = plt.hist(data, num_bins)

    ax = plt.gca()

    ymax = y.max()
    ymin = y.min()

    counter = 0

    for i in y:
        if i == 0.0:
            print("Zero Location: " + str(x[counter]))
        counter += 1

    print("Min: " + str(ymin) + " Max: " + str(ymax))

    _, ylimmax = ax.get_ylim()
    _, xlimmax = ax.get_xlim()

    plt.annotate('Max Occurrences: ' + str(ymax) + '\nMinimum Occurrences: ' + str(ymin), xy=(xlimmax/4, 1), xytext=(xlimmax/4, 1))

    plt.show()

def plotScatterData(data, values):

    plt.interactive(False)
    plt.rcParams['agg.path.chunksize'] = 10000
    plt.title('Scatter Plot of Data vs. The Hashed Value\n(Ordered Data)')
    plt.xlabel('Original Value')
    plt.ylabel('Hashed Value')
    x = values
    y = data

    # x[:] = [i / 1000 for i in x]

    plt.plot(x, y, 'o', color='black', markersize=1)

    plt.show()

def task3(configData):
    #if you wish to use this code to perform task 3, you may do so
    #NOTE task 3 will require you to remake your bloom filter multiple times to perform the appropriate trials
    #this will necessitate either making a new bloom filter constructor or changing the config dictionary to 
    #hold the appropriate values for k and n (filter size) based on c value, derived as in the notes
    #REMEMBER for type 2 hashes n must be prime.  util.findNextPrime(n) is provided for you to use to find the next largest
    #prime value of some integer.
    c = 15
    configData['n'] = configData['m'] * c
    configData['type'] = 2

    # instantiate bloom filter object
    bf = BloomFilter(configData, c)

    # bfInputData holds a list of integers.  Using these values you must :
    #   insert the first configData['m'] of them into the bloom filter
    #   test all of them for membership in the bloom filter
    bfInputData = util.readIntFileDat(configData['inFileName'])
    if (len(bfInputData) == 0):
        print('No Data to add to bloom filter')
        return
    else:
        print('bfInputData has ' + str(len(bfInputData)) + ' elements')
    # testBF will insert elements and test membership
    outputResList = testBF_3(bfInputData, bf, configData['m'])
    # write results to output file
    # util.writeFileDat(configData['outFileName'], outputResList)
    # load appropriate validation data list for this hash function and compare to results
    # util.compareResults(outputResList, configData)


    print('Task 3 complete')
    

"""     
main
"""     
def main():	
    #DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    parser = argparse.ArgumentParser(description='BloomFilter Project')
    parser.add_argument('-c', '--configfile',  help='File holding configuration of Bloom Filter', default='testConfigHashType2.txt', dest='configFileName')
    parser.add_argument('-i', '--infile',  help='Input file of data to add to Bloom Filter', default='testInput.txt', dest='inFileName')
    parser.add_argument('-o', '--outfile',  help='Output file holding Bloom Filter results', default='testOutput.txt', dest='outFileName')	
    #you may use this argument to distinguish between tasks - default is task 2 - do not change
    #you are not required to use this code template for tasks 1 and 3.
    parser.add_argument('-t', '--task',  help='Which task to perform (1,2,3)', type=int, choices=[1, 2, 3], default=3, dest='taskToDo')
    parser.add_argument('-v', '--valfile',  help='Validation file holding Bloom Filter expected results', default='validResHashType2.txt', dest='valFileName')	
    
    #args for autograder, do not modify
    parser.add_argument('-n', '--sName',  help='Student name, used by autograder', default='GT', dest='studentName')	
    parser.add_argument('-x', '--autograde',  help='Autograder-called (2) or not (1=default)', type=int, choices=[1, 2], default=1, dest='autograde')
    args = parser.parse_args()
        
    #configData is a dictionary that holds the important info needed to build your bloom filter
    #this includes the hash functon coefficients for the hash calculation for Task 2 (do not use these for Tasks 1 and 3)
    #buildBFConfigStruct prints out to the console all the elements in configData
    configData = util.buildBFConfigStruct(args) 
    
    #perform appropriate task - 2 is default and the task2 code execution will be tested for your grade    
    if configData['task'] == 2 :
        task2(configData)
    elif configData['task'] == 1 :
        #you are not required to use this code template for tasks 1 and 3.
        task1(configData, args.inFileName)
    elif configData['task'] == 3 :
        #you are not required to use this code template for tasks 1 and 3.
        for i in range(5,16):
            configData['k'] = i
            task3(configData)
    else :
        print ('Unknown Task : ' + str(configData['task']))  



if __name__ == '__main__':
    main()
    