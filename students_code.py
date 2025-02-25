class Node:
    def __init__(self, word, times=1):
        self.word = word
        self.times = times
    def __contains__(self, item):
        return item == self.word

class Hashtab:
    def __init__(self, depth=0, bucketsize = 100, otherSizeConstant = 5, change = 0):
        self.size = bucketsize
        self.bucket_size = bucketsize
        self.arrayThing = [None] * self.bucket_size
        self.collisions = 0
        self.depth = depth
        self.otherSizeConstant = otherSizeConstant
        self.tracker = 0
        self.change = change

    def convertSmart(self, word, sz):
        GOLDEN_RATIO = 0x9E3779B9
        key = 0
        for i in word:
            key = key*GOLDEN_RATIO+(ord(i)-self.change)
        # Golden ratio constant (2^32 * (sqrt(5) - 1) / 2)
        return key % sz

    def add_to_chicken(self, word, key=-1):
        word = word.lower()
        if key == -1:
            key = self.convertSmart(word, self.bucket_size)
        nd = Node(word)
        bucket = self.arrayThing[key]
        if bucket == None:
            self.arrayThing[key] = nd
            return
        elif self.depth>=1:
            bucket = self
        if type(bucket) == Node:
            if bucket.word == word:
                bucket.times += 1
                return
            chicken = Hashtab(self.depth + 1, self.otherSizeConstant, self.otherSizeConstant, self.change)
            chicken.tracker+=2
            self.size+=self.otherSizeConstant
            chicken.add_to_chicken(bucket.word,self.convertSmart(bucket.word,self.otherSizeConstant))
            chicken.add_to_chicken(word,self.convertSmart(word,self.otherSizeConstant))
            self.arrayThing[key]=chicken
            self.collisions+=1
        else:
            piggy = self.convertSmart(word,self.otherSizeConstant)
            thang = bucket.arrayThing[piggy]
            if type(thang) == Hashtab:
                thang.add_to_chicken(word,piggy)
            while thang != None:
                if thang.word == word:
                    thang.times += 1
                    return
                piggy-=1
                thang = bucket.arrayThing[piggy]
            bucket.tracker+=1
            self.collisions+=1
            bucket.arrayThing[piggy]=Node(word)

    def cull(self):
        while self.arrayThing[-1] is None:
            self.size-=1
            self.arrayThing.pop()
        for i in self.arrayThing:
            if type(i) == Hashtab:
                while i.arrayThing and i.arrayThing[-1] is None:
                    self.size-=1
                    i.arrayThing.pop()

    def search_for_chicken(self, word, key=-1):
        word = word.lower()
        if key == -1:
            key=self.convertSmart(word, self.bucket_size)

        bucket = self.arrayThing[key]
        lookUpTime = 1
        if type(bucket) == Hashtab:
            lookUpTime+=1
            key = self.convertSmart(word,self.otherSizeConstant)
            thang = bucket.arrayThing[key]
            while thang.word != word:
                lookUpTime+=1
                key-=1
                thang = bucket.arrayThing[key]
            return thang.times,lookUpTime
        else:
            return bucket.times,lookUpTime

    def __del__(self):
        self.arrayThing.clear()
        self.collisions = 0
        self.size = 0

def test(word_list,besT,t,x,change=0):
    try:
        hashBrown = Hashtab(0,t,x,change)

        for i in word_list:
            hashBrown.add_to_chicken(i)

        totallookUpTimeNew = 0
        hashBrown.cull()
        for i in word_list:
            rubish,sumd = hashBrown.search_for_chicken(i)
        totallookUpTimeNew+=sumd

        something = totallookUpTimeNew+hashBrown.size+hashBrown.collisions
        if besT[1] == 0:
            besT = (t,something,x,change)
        elif something < besT[1]:
            besT = (t,something,x,change)

        del hashBrown
        return besT

    except IndexError:
        return besT

def words_in(word_list):
    besT = (0,0,0,0)
    for x in range(3,5):
        for i in range(-10,10):
            for t in range(len(word_list)//2,len(word_list)):
                besT = test(word_list, besT, t, x, i)
    hashBrown = Hashtab(0,besT[0],besT[2],besT[3])

    for i in word_list:
        hashBrown.add_to_chicken(i)

    hashBrown.cull()

    sumed0 = 0
    sumed1 = 0
    for i in hashBrown.arrayThing:
        if i == None:
            sumed0+=1
        elif type(i) == Hashtab:
            for x in i.arrayThing:
                if x == None:
                    sumed1+=1
    return hashBrown.size, hashBrown.collisions, hashBrown

def lookup_word_count(word,hashTable):
    times,lookups = hashTable.search_for_chicken(word)
    return times,lookups
