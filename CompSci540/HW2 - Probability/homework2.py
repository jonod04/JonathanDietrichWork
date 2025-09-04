import sys
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    X = {chr(i): 0 for i in range(ord('A'), ord('Z')+1)}
    
    with open(filename, encoding='utf-8') as f:
        text = f.read()
        for letter in text:
            letter = letter.upper()
            if letter in X:
                X[letter] += 1
    
    return X

def print_q1(X):
    print("Q1")
    for letter in range(ord('A'), ord('Z')+1):
        print(f"{chr(letter)} {X[chr(letter)]}")

def calculate_q2(X, e, s):
    x1 = X['A']
    q2_english = x1 * math.log(e[0]) if x1 > 0 and e[0] > 0 else 0
    q2_spanish = x1 * math.log(s[0]) if x1 > 0 and s[0] > 0 else 0
    
    print("Q2")
    print(f"{q2_english:.4f}")
    print(f"{q2_spanish:.4f}")

def calculate_F(X, p, prior):
    log_sum = 0
    for i, letter in enumerate(range(ord('A'), ord('Z')+1)):
        count = X[chr(letter)]
        if count > 0 and p[i] > 0:
            log_sum += count * math.log(p[i])
    
    return math.log(prior) + log_sum

def print_q3(F_english, F_spanish):
    print("Q3")
    print(f"{F_english:.4f}")
    print(f"{F_spanish:.4f}")

def calculate_p_english(F_english, F_spanish):
    diff = F_spanish - F_english
    
    if diff >= 100:
        return 0
    elif diff <= -100:
        return 1
    else:
        return 1 / (1 + math.exp(diff))

def print_q4(p_english):
    print("Q4")
    print(f"{p_english:.4f}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 hw2.py [letter file] [english prior] [spanish prior]")
        sys.exit(1)
        
    filename = sys.argv[1]
    english_prior = float(sys.argv[2])
    spanish_prior = float(sys.argv[3])
    
    e, s = get_parameter_vectors()
    
    X = shred(filename)
    
    print_q1(X)
    
    calculate_q2(X, e, s)
    
    F_english = calculate_F(X, e, english_prior)
    F_spanish = calculate_F(X, s, spanish_prior)
    print_q3(F_english, F_spanish)
    
    p_english = calculate_p_english(F_english, F_spanish)
    print_q4(p_english)

if __name__ == "__main__":
    main()