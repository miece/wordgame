from collections import Counter

lines = open('words.txt').read().replace("'", "").splitlines()

def freq_count(letters):
    """ Given a string of letters, return a dictionary
        which associates a frequency count with each letter. """
    f_count = {}
    for char in letters:
        f_count.setdefault(char, 0)
        f_count[char] += 1
    return f_count

def contains(source_word, what):
    """ Returns True if the letters that make up "what" are 
        contained in the letters that make up "source_word", 
        otherwise False is returned. """
    sc = sorted(source_word.lower())
    wc = sorted(what.lower())
    
    if(len(wc) == 0):
        return "Blank Word", "!"
    elif(len(wc) < 3):
        return what + (" is less than three letters") , "!"
    elif(set(wc) == set(sc)):
        return what + (" is the Source Word"), "!"
    elif(set(wc) < set(sc)):
        return isDictWord(what)
    else:
        return "Not in the word" , "!"
    
    

def isDictWord(word):
        if word in lines:
            return "Yes", 1
        else:
            return "No", "!"

def checkDupe(wordlist):
        #return [k for k,v in Counter(wordlist).items() if v>1]
        #return [i for key in (key for key, count in Counter(wordlist).items() if count > 1) for i, x in enumerate(wordlist) if x == key]
        return "hh"

if __name__ == "__main__":
    # A few tests/assertions to make sure things behave as expected.
    assert contains("admission", "sin") == True
    assert contains("admission", "soon") == False
    assert contains("admission", "miss") == True
    assert contains("admission", "moon") == False
    assert contains("admission", "admin") == True
    assert contains("admission", "dismiss") == False
    assert contains("admission", "sins") == True
    assert contains("admission", "missing") == False
