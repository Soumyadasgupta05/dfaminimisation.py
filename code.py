import xlrd
import os

class Minimization:



    

    def __init__(self):
        self.location='' #file location of the excel file

        self.Q =[] #['a','b','c','d','e','f'] list of states in the DFA
        self.Sigma =[] #['0','1'] # alphabet set in the DFA
        self.q_0 = '' #'a'  # starting state of DFA
        self.F = [] # ['b','c','e']  # final states of DFA
        self.M =[] #[['d','b'],['c','f'],['c','f'],['a','e'],['c','f'],['f','f']]
        self.P_0=[] # for storing the initial partition
        self.q_1=''
        self.q_2=''
        self.P_new=[] # list for storing the states of the newly formed minimized DFA
        self.q_0_new=[] # list for storing the initial state of the newly formed minimized DFA
        self.F_new=[] # accepting states of the newly formed minimized DFA
        self.delta_new=[] # matrix for storing the new transition values(states) of the new states after being acted upon by the given alphabets 

        #self.S_L=[]

    def file_loc(self):
        self.location =input('give the location of the excel file'+ " :")

        #location of the excel file containing information of the DFA





    def states(self):  # function for storing the states of the DFA

        workbook=xlrd.open_workbook(self.location)
        sheet=workbook.sheet_by_index(0)  #sheet in which the states of the DFA are present in the first row, in the form of single characters i.e the first sheet

        self.Q=sheet.row_values(0)
        print(self.Q)



    def alphabet(self):  # function for storing the alphabets(symbols) of the DFA
        workbook = xlrd.open_workbook(self.location)
        sheet = workbook.sheet_by_index(0)  # sheet in which the alphabets of the DFA are present in the second row, in the form of single characters i.e the first sheet
        self.Sigma= sheet.row_values(1)
        print(self.Sigma)

    def ini_state(self):
        workbook = xlrd.open_workbook(self.location)
        sheet = workbook.sheet_by_index(0)  # sheet in which the first shell of the 3rd row is occupied by the initial state of the DFA i.e the first sheet
        self.q_0= sheet.row_values(2)
        print(self.q_0)

    def delta_function_matrix(self):
        workbook = xlrd.open_workbook(self.location)
        sheet = workbook.sheet_by_index(1)# this is the second sheet in which the delta matrix is given
        self.M = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
        print(self.M)



    def final_states_ofDFA(self):  # function for storing the final states
        workbook = xlrd.open_workbook(self.location)
        sheet = workbook.sheet_by_index(0)  # sheet in which the final states of the DFA are present in the 4th row i.e the first sheet
        self.F = sheet.row_values(3)
        print(self.F)

    def base_partition(self):
        W=[]

        for i in range(0,len(self.Q)):
            if self.Q[i] not in self.F:
                W.append(self.Q[i])  # W is the list of all states that are not accepting

        self.P_0=[W,self.F] #zero level partition formed
        print(self.P_0)




    def partition(self,P):

        P1=[]
        S=[]
        U=[]

        for i in range(0,len(P)):
            S=self.partition_1(P[i],P) #partition of P[i]
            U=U+S
            #print(U) #new partition
            
            
        ctr=0
        for i in range(0,len(U)):
            
            if U[i] in P:
                ctr=ctr+1
        if ctr==len(U):
            
            print(P)
            self.P_new=P
            return P
                        #base case
                                #P contains lists, each of which can be thought of as the states of the new minimized DFA
        else:
            self.partition(U)  # i.e if new partitions are created, iterate the function once more


    def partition_1(self, P_i, P):
        L=[]
        t=0
        list=[]
        j=0
        i=0

        for i in range(0, len(P_i)):
            #print(len(P_i))
            list=[P_i[i]]
            #print(list)

            for j in range(0,len(P_i)):
                ctr=0

                if j!=i:
                    
                    for k in range(0, len(self.Sigma)):

                        self.q_1= self.transition(P_i[i],self.Sigma[k])
                        self.q_2= self.transition(P_i[j],self.Sigma[k])
                        #print(self.Sigma[k])
                        #print(P_i[i]+" "+P_i[j])
                        #print( self.q_1 +" "+self.q_2 )

                        flag=0

                        for l in range(0,len(P)):

                            if self.q_1 in P[l] and self.q_2 in P[l]: #checking whether q1 and q2 are present in some partition of P
                            
                                flag=1  #indicating q1 & q2 belongs to Sigma where Sigma is an element in the list P

                    

                        if flag==1:
                        
                            ctr=ctr+1

                    if ctr== len(self.Sigma):
                        #print(ctr)
                        list.append(P_i[j])
                        #print(list)

            if L==[]:
                #print(len(L))
                L.append(list)
                #print(L)
            else:

                for i in range(0,len(L)):
                    #print(len(L))
                    #print(L)
                    if set(list)!=set(L[i]):
                        t=t+1
                        #print(t)
                if t==len(L):
                    L.append(list)
                    #print(L)

        #print(L)
        return L #returning the collection of all the partitions of P_i where P_i is an element of P

    def transition(self, q, s):
        state_index= self.Q.index(q)
        
        
        alphabet_index=self.Sigma.index(s)
        
        #print(self.M[state_index][alphabet_index])

        return self.M[state_index][alphabet_index]  #returning the state at which 'q' will reach after acting upon the alphabet 's'
    
    def final_states_new(self):
        for i in range(0,len(self.P_new)):
            if self.subset(self.P_new[i],self.F):
                self.F_new.append(self.P_new[i])
        print(" She accepting states of the newly formed minimized DFA---->"+ str(self.F_new))

    def subset(self,L_1,L_2):
        ctr=0
        for i in range(0,len(L_1)):
            if L_1[i] in L_2:
                ctr=ctr+1
        if ctr==len(L_1):
            return True
        else:
            return False

    def new_initial_state(self):
        for i in range(0,len(self.P_new)):
            if self.q_0[0] in self.P_new[i]:
                self.q_0_new=self.P_new[i]
        print("The initial state of the modified DFA---->"+str(self.q_0_new))

    def transit_value_storing(self):
        for i in range(0,len(self.P_new)):
            self.delta_new.append(self.new_transition(self.P_new[i]))
    
    def new_transition(self,L):
        list=[]
        trans=[]

        for i in range(0,len(self.Sigma)):
            list=self.new_transition_func(L,self.Sigma[i])
            
            trans.append(list)
            print("delta( " + str(L)+" , "+str(self.Sigma[i])+" )--->"+str(list))
        
        #print(trans)
        return trans
    
    def new_transition_func(self, L, c):
        state_0=L[0]
        state_S=self.M[self.Q.index(state_0)][self.Sigma.index(c)]
        #print(state_S)

        for i in range(0,len(self.P_new)):
            if state_S in self.P_new[i]:
                #print(i)
                break
        #print(self.P_new[i])
        return self.P_new[i]









M= Minimization()
M.file_loc()
M.states()
M.alphabet()
M.ini_state()
M.delta_function_matrix()
M.final_states_ofDFA()

M.base_partition()

#M.partition_1()
#M.transition()
M.partition(M.P_0)
M.final_states_new()
M.new_initial_state()
M.transit_value_storing()
#M.new_transition_func(['a','d'],M.Sigma[1])
#M.new_transition(['a','d'])








