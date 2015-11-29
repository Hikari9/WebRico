from rico.backend.utils import *

'''
Transforms a list or string into an array of integers separated by negative numbers.
Complexity: O(n)
'''
def transform(text):
    transformed_text = []
    
    if isinstance(text, list):
        for i, subtext in enumerate(text):
            if not isstring(subtext):
                raise ValueError('text should be a string or a list of strings')
            transformed_text.extend(map(ord, subtext))
            transformed_text.append(~i)

    elif isstring(text):
        transformed_text.extend(map(ord, text))
        transformed_text.append(-1)
    
    else:
        raise ValueError('text should be a string or a list of strings')

    return transformed_text

class SuffixArray(list):
    
    def __init__(self, text, algo=u'radix sort'):
        
        # check if algorithm is valid
        
        algo = algo.lower()
        if algo not in SuffixArray.algorithms:
            raise ValueError(u"invalid argument: algo='%s' is not in %s" % (algo, str(SuffixArray.algorithms.keys())))
        
        self.text = text
        SuffixArray.algorithms[algo](self)
    
    def suffix(self, index):
        return u''.join(map(lambda num: u'$' if num < 0 else chr(num), self.string[self[index]:]))
    
    def counting_sort(self):
        
        string = transform(self.text)
        n = len(string)
        
        # create the initial list of indices
        list.__init__(self, range(n))
        position = string[:]
        value = [0] * n
        count = [0] * n
        
        # stable sort according to character index
        self.sort(cmp = lambda i, j: cmp(string[i], string[j]) if string[i] != string[j] else cmp(j, i))
        
        # commence counting sort
        gap = 1
        # resorting part
        while gap < (n << 1):
            value[self[0]] = 0
            for I in xrange(1, n):
                i, j = self[I - 1], self[I]
                value[j] = value[i] if position[i] == position[j] and i + gap < n and position[i + (gap >> 1)] == position[j + (gap >> 1)] else I
            for i in xrange(n):
                position[i] = value[i]
                value[i] = self[i]
                count[i] = i
            for i in xrange(n):
                index = value[i] - gap
                if index >= 0:
                    self[count[position[index]]] = index
                    count[position[index]] += 1
            gap <<= 1
        
        self.string = string
        self.position = position
        
        return self
    
    def radix_sort(self):
        
        # transform text into list of integers
        string = transform(self.text)
        n = len(string)
        
        # create the initial list of indices
        list.__init__(self, range(n))
        position = string[:]
        tmp = [0] * n
        gap = 1
        
        def compare(i, j):
            if position[i] != position[j]:
                return cmp(position[i], position[j])
            i += gap
            j += gap
            return cmp(position[i], position[j]) if i < n and j < n else cmp(j, i)
        
        while True:
            self.sort(cmp=compare)
            for i in xrange(1, n):
                tmp[i] = tmp[i - 1] + (1 if compare(self[i - 1], self[i]) < 0 else 0)
            for i in xrange(n):
                position[self[i]] = tmp[i]
            if tmp[n - 1] == n - 1:
                break
            gap <<= 1
        
        self.string = string
        self.position = position
        
        return self
    
    def dc3(self):
        
        # transform text into offsetted list of integers
        string = transform(self.text)
        n = len(string)
        
        # find offset to compress array
        origin = None
        for letter in string:
            if origin == None or (letter >= 0 and origin > letter):
                origin = letter
        
        if origin == None:
            list.__init__(self)
            self.position = []
            return self
        
        # compress array based on new origin
        mn, mx = origin + min(string), max(string)
        compressed_string = map(lambda x: x - mn + 1 if x >= 0 else origin + x - mn, string)
        compressed_string.extend([0, 0, 0])
        
        # import DC3 library
        from rico.backend.strings.DC3 import DC3algorithm
        
        # call DC3 algorithm
        list.__init__(self, [0] * n)
        DC3algorithm(compressed_string, self, n, mx - mn + 1)
        
        # position indices
        position = [0] * n
        for i in xrange(n):
            position[self[i]] = i
        
        self.string = string
        self.position = position
        
        return self
    
    algorithms = {
        u'counting sort': counting_sort,
        u'radix sort': radix_sort,
        u'dc3': dc3
    }
