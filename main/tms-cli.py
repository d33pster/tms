#!/usr/bin/env python3

import sys, os, time, collections
from itertools import islice

def clean():
    os.system('cls') if 'nt' in os.name else os.system('clear')

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

# return string before index
def parse_before(rule, index):
    string = ''
    #use slicing later
    for i in range(index): 
        string = string + rule[i]
    
    return string

def parse_between(rule, start, end):
    string = ''
    
    # use slicing later
    for i in range(start, end):
        string = string + rule[i]
    
    return string

def parse_after(rule, index):
    string = rule[index:]
    #use slicing later
    # for i in range(index, len(rule)):
    #     string = string = rule[i]
    
    return string

# * checker - single
def up_checker(rule, string):
    string_len = len(string)

    # input
    to_check = input("Enter String: ")
    to_check_len = len(to_check) - 1
    
    #if string length < rule then ded
    if to_check_len<string_len:
        print("Language Not supported.")
        time.sleep(4)
        clean()
        sys.exit(0)
        
    #check the string first and then the last char
    for j in range(string_len):
        if string[j]==to_check[j]:
            continue
        else:
            print("Language Not Supported.")
            time.sleep(4)
            clean()
            sys.exit(0)
    
    repeat_var = rule[string_len]
    # print(repeat_var)
    for i in range(string_len, to_check_len+1):
        if to_check[i]==repeat_var:
            continue
        else:
            print("Language Not Supported.")
            time.sleep(4)
            clean()
            sys.exit(0)
    
    print("Language Supported.")

def multStar(rule, infinit):
    to_check = input("Enter String: ")
    to_check_len = len(to_check)
    
    check1 = 0
    state = 0
    
    for char in rule:
        for repeat in infinit:
            if char==repeat:
                state=1
                break
            
                
                

def case1_checker(rule, start, repeat, end):
    start_len = len(start)
    repeat_len = len(repeat)
    end_len = len(end)
    
    to_check = input("Enter String: ")
    
    if ( len(to_check) - 1 ) < start_len + repeat_len + end_len:
        print('Language Not Supported. 1')
        time.sleep(4)
        clean()
        sys.exit(0)

    # check the start part
    for i in range(start_len):
        if start[i] == to_check[i]:
            continue
        else:
            print("Language Not Supported. 2")
            time.sleep(4)
            clean()
            sys.exit(0)
    
    # check repeating part
    check_range = iter(range(start_len, len(to_check)-end_len-1))
    for i in check_range:
        temp = i
        for j in range(repeat_len):
            if repeat[j]==to_check[temp]:
                temp = temp + 1
                continue
            else:
                print('Language Not Supported 3')
                time.sleep(4)
                clean()
                sys.exit(0)
        consume(check_range, repeat_len-1) #consume length of repeat and run
    
    # check end
    j=0
    for k in range(len(to_check)-end_len, end_len):
        if to_check[k] == end[j]:
            j = j + 1
            continue
        else:
            print('Language Not Supported. 4')
            time.sleep(4)
            clean()
            sys.exit(0)
    
    print("Language Supported")


def tms(rule):
    
    #check for keywords first
    is_up = 0
    is_bracket = 0
    is_consecutive = 0
    
    for char in rule:
        if char == '(':
            for temp in rule:
                if temp == ')':
                    is_bracket = is_bracket + 1 # increment if found more
                    break # if match found break the 2nd loop
        elif char == '*':
            index_up = rule.find('*')
            index_bracket = rule.find(')')
            # if * comes before ()
            if index_up < index_bracket:
                print("Rule not Supported yet")
                sys.exit(0)
            elif index_up == index_bracket + 1:
                is_up = 1
                is_consecutive = 1
            elif index_up > index_bracket:
                is_up = 1
    
    # checking multiple *
    if is_up == 1:
        is_up = 0
        for char in rule:
            if char == "*":
                is_up = is_up + 1
                      
    #case 1 - consecutive abc(ef)*gh -> this works for abc(def)*, (def)*, (def)*gh
    if is_up == 1 and is_bracket == 1 and is_consecutive == 1:
        # code for both () and * in consecutive order
        for i in range(len(rule)):
            if rule[i] == '(':
                stringBeforeBracket = parse_before(rule, i)
                stringBetweenBracket = parse_between(rule, rule.find('(') + 1, rule.find(')'))
                stringAfterUp = parse_after(rule, rule.find('*') + 1)
                case1_checker(rule, stringBeforeBracket, stringBetweenBracket, stringAfterUp)
    elif is_up == 1 and is_bracket == 0:
        # code for checking just * -> simple abc*
        for i in range(len(rule)):
            if rule[i] == '*':
                string = parse_before(rule, i-1)
                up_checker(rule, string)
    elif is_up > 1:
        # for multiple *
        infinit = []
        for i in range(len(rule)):
            if rule[i] == "*":
                infinit.append(rule[i-1])


def main(rule):
    clean()
    tms(rule)

if __name__=='__main__':
    clean()
    print('Turing Machine Sim')
    rule = input("Enter rule: ")
    main(rule)