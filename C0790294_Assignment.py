
# Part1 Encryption algorithm

print("\n Part1-Encryption algorithm\n")
def cypher_txt_encryption(text,shift):
    result= ""
    for char in range(len(text)):
        character = text[char]
        #Encrypt uppercase characters
        if (character.isupper()):
            result += chr((ord(character)+ shift - 65)% 26 + 65)
        #Encrypt lowercase characters
        elif (character.islower()):
            result += chr((ord(character)+ shift - 97)% 26 +97)
        else:
            result += character
    return result

text = "i love python because PYTHON IS EASY TO LEARN"
shift = 3
print("The given Text is :", text)
print("Number of shifts :", str(shift))
print("The Cipher Encryption of the text is:", cypher_txt_encryption(text, shift))


#part2 Binary Search Algorithm

print("\n  Part2-Binary Search Algorithm\n")

def binary_search(array, start, end, key):
    if end >= start:
        mid = (end + start)//2
        if array[mid] == key:
            print("Sucessful Search")
            return True
        elif array[mid] > key:
            return binary_search(array,start,mid-1,key)
        else:
            return binary_search(array,mid+1,end,key)
    else:
        print("Unsucessful Search")
        return False
array=[2,5,7,11,13,17,19,23,29]
key=19
print("The elements in array:",array)
print("The value to be searched:",key)

result= binary_search(array,0,len(array)-1,key)
print(str(result))


# Part3 Formula Implementation

print("\n Part3-Formula Implementation\n")

import math

def estimate_pi():
    result=0
    k=0
    expression = 2 * math.sqrt(2) / 9801
    while True:

        upper_exp = math.factorial(4 * k) * (1103 + 26390 * k)
        lower_exp = math.factorial(k) ** 4 * 396 ** (4 * k)
        equation=expression *upper_exp / lower_exp
        result = result + equation

        if abs(equation) < 1e-15:
            break
        k = k+1
    return 1/result

print("Estimate value of Pi is :",estimate_pi())
