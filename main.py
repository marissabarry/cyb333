#!/usr/bin/env python3
#Password Generation Utility
#CYB333 Final Project
#Marissa Barry, Sariah Kilroy, Shantel Jackson, and BriAna Siliga.

#Generates a user-inputted number of passwords of user-inputted length utilizing a selection of random ASCII characters
#Provides the option to save passwords to a file; produces an encrypted file, a plain-text version (for ease of administration),
#and a keyfile containing the encryption key.

#Imports; using string for easy access to lists of ASCII characters and random for the randomization
import random, string, cryptography
from cryptography.fernet import Fernet

#Defining some global variables
inputSamples = 0
inputLength = 0
cont = False
genPass = []

#Function definitions
#Polls user for input, returns boolean; used in a loop for input handling
#Uses inputSamples as a global for simplicity
def getSamplesNum():
    try:
        global inputSamples
        inputSamples = int(input('Generate how many passwords? '))
        return True
    except ValueError:
        print('Invalid input, please try again.')
        return False

#Same idea as getSamplesNum but for length
def getSamplesLength():
    try:
        global inputLength
        inputLength = int(input('Desired password length (min 8 recommended): '))
        return True
    except ValueError:
        print('Invalid input, please try again.')
        return False

#Returns a randomly generated password of the desired length
def passGen():
    pword = ''
    for j in range(inputLength):
        pword += random.choice(asciiAll)
    return pword

#Gets called after generation to parse user input for writing to a file
def userYN():
    check = str(input('Save output to a file? (Y/N): ')).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid entry')
            return userYN()
    except Exception as error:
        print('Enter a valid input')
        print(error)
        return userYN()

#Main menu: prompt user to select choice
print('CYB333 Password Generator')

#Get number of samples to generate using earlier functions
#Use of global variables earlier makes this far simpler
while cont is False:
    cont = getSamplesNum()
#Get length of samples to generate
cont = False
while cont is False:
    cont = getSamplesLength()

#Now we know how many passwords to generate and how long they should be, let's get to it
print('\nGenerating',inputSamples,'passwords with',inputLength,'characters...')
#Establish a base character set to pull from 
asciiLow = string.ascii_lowercase
asciiUp = string.ascii_uppercase
asciiNum = string.digits
asciiSym = string.punctuation
asciiAll = asciiLow + asciiUp + asciiNum + asciiSym

#Loop to iterate through the length of the password
#Adds each newely generated password to the list defined at the beginning

for i in range(inputSamples):
    pword = passGen()
    #for j in range(inputLength):
    #    pword += random.choice(asciiAll)
    if pword in genPass:
        print('Generated a duplicate, regenerating!')
        pword = passGen()

    genPass.insert(i,pword)

#Printing newly generated passwords
print('\nGenerated',inputSamples,'passwords:\n')
for i in genPass:
    print(i)
print('\n')

#Bad passwords are EVERYWHERE so let's make sure that none of the generated ones are bad
#Using the top 10000 most common passwords from the OWASP SecList Project in a text file, one per line
#Using the passwords.txt file to read the list into a list 
#Create list of common passwords from file
bank = open('passwords.txt', 'r')
parse = []

for i in bank:
    words = i.split()
    for a in words:
        parse.append(a)

#Check generated passwords against list, once again using a boolean/for setup
#Testing this is tricky because the generator is too random and hasn't turned up any duplicates yet.
#Even on massive test sets (500K,1M) it doesn't find a match but just in case
print('Checking generated passwords against list of common passwords...')
present = False
for i in genPass:
    if i in parse:
        print(genpass[i],'is on the list of commonly used passwords, recommend not using and regenerating as needed.')
        present = True
if present is False:
    print('No matches found!')

#Close the wordbank file since we're done with it
bank.close()
#Prompts the user if they want to save the list of passwords to a file
#If so, creates the file output.txt and dumps the passwords into it, one per line
if userYN() is True:
    print('\nWriting passwords to output.txt')
    
    output = open('output.txt','w')
    for i in genPass:
        fOut = i + '\n'
        output.write(fOut)
    output.close()
    print('Successfully wrote',inputSamples,'passwords to output.txt')
    #Implement cryptography for outputted file
    #Generate a key
    print('Generating encryption key to encrypt output file...')
    key = Fernet.generate_key()
    cypher = Fernet(key)
    with open('output.txt','rb') as file:
        plaintxt = file.read()

    #Encryption time
    crypt = cypher.encrypt(plaintxt)
    with open('encryptedoutput.txt','wb') as encrypted_out:
        encrypted_out.write(crypt)
    #Save encryption key to a file
    with open('key.key','wb') as keyout:
        keyout.write(key)
    print('Passwords successfully encrypted using the following key (saved as key.txt):\n',key,'\n\nNote: Safeguard this key file to avoid potential data compromise.')
    print('Caution: output.txt is not encrypted and is for ease of initial administration, encryptedoutput.txt is the encrypted version that may be safely retained.')

