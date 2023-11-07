#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from itertools import islice
import socket, collections

class tms(Tk):
    def __init__(self):
        super().__init__()
        self.title(f'Turing Machine Sim - running on {socket.gethostname()}')
        self.init()
    
    def init(self):
        self.configure(bg="#ADD8E6") 
        
        # Frame 1
        self.Frame1 = ttk.Frame(self)
        self.Frame1.pack(fill=BOTH)
        self.Label1 = ttk.Label(self.Frame1, text='Rule:', font=('Verdana', 16), background="#ADD8E6", width=10)
        self.Label1.pack(side=LEFT)
        self.Entry1 = ttk.Entry(self.Frame1, width=30)
        self.Entry1.pack(side=RIGHT)
        
        # Frame 2
        self.Frame2 = ttk.Frame(self)
        self.Frame2.pack(fill=BOTH)
        self.Button1 = ttk.Button(self.Frame2, text='[Next]', command=self.enterString)
        self.Button1.pack()
    
    def enterString(self):
        # Lock Entry
        self.rule = self.Entry1.get()
        self.Entry1.forget()
        self.Label2 = ttk.Label(self.Frame1, text=self.rule, font=('ComicSans', 16), background='#ADD8E6', width=30)
        self.Label2.pack(side=RIGHT)
        
        # forget Frame 2
        self.Frame2.forget()
        
        # Frame temp
        self.FrameTemp = ttk.Frame(self)
        self.FrameTemp.pack(fill=BOTH)
        self.LabelTemp = ttk.Label(self.FrameTemp, text='Checking...', font=('Verdana', 12), background='#ADD8E6')
        self.LabelTemp.pack(side=LEFT)
        self.LabelTemp.after(1000, self.checkRule)
    
    # check Rule
    def checkRule(self):
        rule = self.rule
        self.case1 = 0
        self.up = 0
        self.is_up = 0
        self.is_bracket = 0
        self.is_consecutive = 0
        
        for char in rule:
            if char == '(':
                for temp in rule:
                    if temp == ')':
                        self.is_bracket = 1
                        continue
            elif char == '*':
                index_up = rule.find('*')
                index_bracket = rule.find(')')
            
                if index_up < index_bracket:
                    messagebox.askretrycancel('Invalid Rule', f'{rule} is not yet supported!')
                    self.handleRuleError()
                elif index_up == index_bracket + 1:
                    self.is_up = 1
                    self.is_consecutive = 1
                elif index_up > index_bracket:
                    self.is_up = 1
        
        # handle no rule error
        if self.is_up==0 and self.is_bracket==0:
            messagebox.askretrycancel('Invalid Rule', f'\'{rule}\' has Syntax Error!')
            self.handleRuleError()
        
        #case 1 - consecutive abc(ef)*gh
        if self.is_up == 1 and self.is_bracket == 1 and self.is_consecutive == 1:
            # code for both () and * in consecutive order
            for i in range(len(rule)):
                if rule[i] == '(':
                    self.stringBeforeBracket = self.parse_before(rule, i)
                    self.stringBetweenBracket = self.parse_between(rule, rule.find('(') + 1, rule.find(')'))
                    self.stringAfterUp = self.parse_after(rule, rule.find('*') + 1)
                    # case1_checker(rule, stringBeforeBracket, stringBetweenBracket, stringAfterUp)
                    self.case1 = 1
                    self.checkEntryPassed()
        elif self.is_up == 1 and self.is_bracket == 0:
            # code for checking just *
            
            self.up = 1
            self.checkEntryPassed()
            # string = self.parse_before(rule, i-1)
            # self.up_checker(rule, string) 
    
    def parse_before(self, rule, i):
        string = rule[0:i]
        return string
    
    def parse_between(self, rule, start, end):
        string = rule[start:end]
        return string
    
    def parse_after(self, rule, index):
        string = rule[index:]
        return string
    
    def handleRuleError(self):
        # handle Invalid Rule Error
        self.FrameTemp.destroy()
        self.Frame1.destroy()
        self.Frame2.destroy()
        self.init()
        
    def checkEntryPassed(self):
        # forget Frame Temp
        self.FrameTemp.forget()
        # Frame 3
        self.Frame3 = ttk.Frame(self)
        self.Frame3.pack(fill=BOTH)
        self.Label3 = ttk.Label(self.Frame3, text='String:', font=('Verdana', 16), background='#ADD8E6', width=10)
        self.Label3.pack(side=LEFT)
        self.Entry2 = ttk.Entry(self.Frame3, width=30)
        self.Entry2.pack(side=RIGHT)
        
        # Frame 4
        self.Frame4 = ttk.Frame(self)
        self.Frame4.pack(fill=BOTH)
        self.Button2 = ttk.Button(self.Frame4, text='[Back]', command=self.goBack)
        self.Button2.pack(side=LEFT)
        self.Button3 = ttk.Button(self.Frame4, text='[Check]', command=self.check)
        self.Button3.pack(side=RIGHT)
    
    def goBack(self):
        self.Frame3.forget()
        self.Frame4.forget()
        self.Frame1.forget()
        self.init()
    
    def check(self):
        # lock entry of string
        self.string = self.Entry2.get()
        self.Entry2.forget()
        self.Label4 = ttk.Label(self.Frame3, width=30, text=self.string, font=('ComicSans', 16), background='#ADD8E6')
        self.Label4.pack(side=RIGHT)
        
        # Forget Frame 4
        self.Frame4.forget()
        
        # Frame 5
        self.Frame5 = ttk.Frame(self)
        self.Frame5.pack(fill=BOTH)
        self.Label5 = ttk.Label(self.Frame5, text='Checking...', font=('Verdana', 12), background='#ADD8E6')
        self.Label5.pack(side=LEFT)
        self.Label1.after(1000, self.checkString)
        
    def checkString(self):
        rule = self.rule
        string = self.string
        
        if self.up==1 and self.case1==0:
            for i in range(len(rule)):
                if rule[i]=='*':
                    temp = self.parse_before(rule, i-1)
                    self.up_checker(rule, temp, string)
        elif self.up==0 and self.case1==1:
            self.case1_checker()
        else:
            pass
    
    def case1_checker(self):
        start = self.stringBeforeBracket
        repeat = self.stringBetweenBracket
        end = self.stringAfterUp
        rule = self.rule
        to_check = self.string
        error = 0
        
        start_len = len(start)
        repeat_len = len(repeat)
        end_len = len(end)
        
        if ( len(to_check) - 1 ) < start_len + repeat_len + end_len:
            messagebox.askretrycancel('String Not Accepted', f'string \'{to_check}\' not accepted!')
            error=1
            self.handleStringNotAcceptedError()

        # check the start part
        for i in range(start_len):
            if start[i] == to_check[i]:
                continue
            else:
                messagebox.askretrycancel('String Not Accepted', f'string \'{to_check}\' not accepted!')
                error=1
                self.handleStringNotAcceptedError()
        
        # check repeating part
        check_range = iter(range(start_len, len(to_check)-end_len-1))
        for i in check_range:
            temp = i
            for j in range(repeat_len):
                if repeat[j]==to_check[temp]:
                    temp = temp + 1
                    continue
                else:
                    messagebox.askretrycancel('String Not Accepted', f'string \'{to_check}\' not accepted!')
                    error=1
                    self.handleStringNotAcceptedError()
            self.consume(check_range, repeat_len-1) #consume length of repeat and run
        
        # check end
        j=0
        for k in range(len(to_check)-end_len, end_len):
            if to_check[k] == end[j]:
                j = j + 1
                continue
            else:
                messagebox.askretrycancel('String Not Accepted', f'string \'{to_check}\' not accepted!')
                error=1
                self.handleStringNotAcceptedError()
        
        if error == 0:
            self.handleStringAccept()

    def consume(self, iterator, n):
        # "Advance the iterator n-steps ahead. If n is none, consume entirely."
        # Use functions that consume iterators at C speed.
        if n is None:
            # feed the entire iterator into a zero-length deque
            collections.deque(iterator, maxlen=0)
        else:
            # advance to the empty slice starting at position n
            next(islice(iterator, n, n), None)
    
    def up_checker(self, rule, string, string2):
        string_len = len(string)

        error = 0
        
        # input
        to_check = string2
        to_check_len = len(to_check) - 1
        
        #if string length < rule then ded
        if to_check_len<string_len:
            messagebox.askretrycancel('String Not Accepted', f'string \'{to_check}\' not accepted!')
            error=1
            self.handleStringNotAcceptedError()
            
        #check the string first and then the last char
        for j in range(string_len):
            if string[j]==to_check[j]:
                continue
            else:
                messagebox.askretrycancel('String Not Accepted', f'string \'{to_check}\' not accepted!')
                error=1
                self.handleStringNotAcceptedError()
        
        repeat_var = rule[string_len]
        
        for i in range(string_len, to_check_len+1):
            if to_check[i]==repeat_var:
                continue
            else:
                messagebox.askretrycancel('String Not Accepted', f'string \'{to_check}\' not accepted!')
                error=1
                self.handleStringNotAcceptedError()
        
        if error == 0:
            self.handleStringAccept()
    
    def handleStringNotAcceptedError(self):
        # forget Frame 5
        self.Frame5.forget()
        
        # destroy label 4
        self.Label4.destroy()
        
        # destroy entry 2
        self.Entry2.destroy()
        
        # create Entry 2
        self.Entry2 = ttk.Entry(self.Frame3, width=30)
        self.Entry2.pack(side=RIGHT)
        
        # bring back Frame 4
        self.Frame4.pack(fill=BOTH)
    
    def handleStringAccept(self):
        # forget frame 5
        self.Frame5.forget()
        
        # Frame 6
        self.Frame6 = ttk.Frame(self)
        self.Frame6.pack(fill=BOTH)
        self.Label6 = ttk.Label(self.Frame6, text='String Accepted!', background='#ADD8E6', font=('Verdana', 12))
        self.Label6.pack()
        
        # Frame 7
        self.Frame7 = ttk.Frame(self)
        self.Frame7.pack(fill=BOTH)
        self.Button4 = ttk.Button(self.Frame7, text='[Check Another String]', command=self.checkAnother)
        self.Button4.pack(side=LEFT)
        self.Button5 = ttk.Button(self.Frame7, text='[Reset]', command=self.reset)
        self.Button5.pack(side=RIGHT)
        
    def reset(self):
        self.string=''
        self.rule=''
        self.Frame1.destroy()
        self.Frame2.destroy()
        self.Frame3.destroy()
        self.Frame4.destroy()
        self.Frame5.destroy()
        self.Frame6.destroy()
        self.Frame7.destroy()
        self.FrameTemp.destroy()
        self.init()
    
    def checkAnother(self):
        # Forget Frame 7
        self.Frame7.pack_forget()
        # Forget Frame 6
        self.Frame6.pack_forget()
        # destroy Label 4
        self.Label4.destroy()
        # destroy Entry 2
        self.Entry2.destroy()
        # Create Entry 2
        self.Entry2 = ttk.Entry(self.Frame3, width=30)
        self.Entry2.pack(side=RIGHT)
        # bring back Frame 4
        self.Frame4.pack(fill=BOTH)

def main():
    app = tms()
    app.mainloop()

if __name__=='__main__':main()