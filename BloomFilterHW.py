from BitHash import BitHash 
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # See Slide 12 for the math needed to do this.    
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        phi = (1.0- (maxFalsePositive**(1.0/numHashes)))
        nBits = float(numHashes)/(1.0-(phi**(1.0/numKeys)))
        return int(nBits)     # make sure # of bits is a whole number
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed  
        self.__size = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bv = BitVector(size = self.__size)
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        self.__numBitsSet = 0
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        seed = 0
        #create number of hash values passed into the bloom filter
        for i in range(self.__numHashes):
            h = BitHash(key, seed)
            hv = h % self.__size
            #if location wasn't set, change the bit and increment bit counter
            if self.__bv[hv] == 0:
                self.__bv[hv] = 1
                self.__numBitsSet += 1
                
            #make old hash value new seed    
            seed = h
            
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        seed = 0
        #create number of hash values passed into the bloom filter
        for i in range(self.__numHashes):
            h = BitHash(key, seed)
            hv = h % self.__size
            
            #check for the key not inserted, return false
            if self.__bv[hv] == 0:
                return False
            
            #make old hash value new seed    
            seed = h
            
        #all bits were set   
        return True  
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # actually measuring the proportion of false positives that 
    # are actually encountered.
    def falsePositiveRate(self):
        projectedFPR = (float(self.__numBitsSet)/self.__size)**self.__numHashes
        return projectedFPR
    
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__numBitsSet

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = 0.05
    
    # create the Bloom Filter
    bf = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    
    fin = open("wordlist.txt")
    
    for i in range(numKeys):       
        line = fin.readline()       
        bf.insert(line)
        
    fin.close()

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    
    print("Projected false positive rate is:", bf.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    
    fin = open("wordlist.txt")
    
    countMissing = 0
    
    for i in range(numKeys):      
        line = fin.readline()          
        if not bf.find(line):
            countMissing += 1
    print("The number of missing keys from the bloom filter is", countMissing)
    

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    countFalseFinds = 0
    for i in range(numKeys):
        line = fin.readline()        
        if bf.find(line):
            countFalseFinds += 1
            
    print("The number of keys that were falsely found in the bloom filter is", countFalseFinds)      
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    
    actualFalsePositiveRate = countFalseFinds/numKeys

    print("Actual false positive rate is:", actualFalsePositiveRate)
    
    
if __name__ == '__main__':
    __main()       

