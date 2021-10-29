import matplotlib.pyplot as plt
import numpy as np

class party:
    def __init__(self, name, r_0, r_1):
        self.name = name
        self.r_0 = r_0 # reserve of t_0
        self.r_1 = r_1 # reserve of t_1
        
    def show(self):
        print(self.name + "   [" + f(self.r_0) + ":t_0," + f(self.r_1) + ":t_1], v = " + f(self.get_v()) + " $")
    
    def get_v(self):
        return self.r_0*v_t_0 + self.r_1*v_t_1
    
class amm:
    def __init__(self, r_0, r_1, parties):
        self.r_0 = r_0 # reserve of t_0
        self.r_1 = r_1 # reserve of t_1
        self.c = r_0*r_1 # x*y = r_0*r_1 = c
        self.parties = parties
        
    # P swaps v of t_0 for at least w of t_1 (swap left)
    def sl(self,P,v,w):
        self.plot_before_swap(P.name + ":SL(" + str(v) + ":t_0," + str(w) + ":t_1)")
        
        # r_0 * r_1 = (r_0 + v) * (r_1 - w_prime) where w_prime >= w
        w_prime = - self.r_0 * self.r_1 / (self.r_0 + v) + self.r_1
        print("w-prime-w = " + f(w_prime-w) + " >= 0?")
        #assert(w_prime >= w)
        
        # Update P reserves
        P.r_0 -= v
        P.r_1 += w_prime
        
        # Update AMM reserves
        self.r_0 += v
        self.r_1 -= w_prime
        
        # Print swap, parties and amm info
        print(P.name + ":SL(" + f(v) + ":t_0," + f(w) + ":t_1)")
        self.show()
        
        self.plot_after_swap()
        
    # P swaps w of t_1 for at least v of t_0 (swap right)
    def sr(self,P,v,w):
        self.plot_before_swap(P.name + ":SR(" + str(v) + ":t_0," + str(w) + ":t_1)")
        
        # r_0 * r_1 = (r_0 - v_prime) * (r_1 + w) where v_prime >= v
        v_prime = - self.r_0 * self.r_1 / (self.r_1 + w) + self.r_0
        print("v-prime-v = " + f(v_prime-v) + " >= 0?")
        #assert(v_prime >= v)
        
        # Update P reserves
        P.r_0 += v_prime
        P.r_1 -= w
        
        # Update AMM reserves
        self.r_0 -= v_prime
        self.r_1 += w
        
        # Print swap, parties and amm info
        print(P.name + ":SR(" + f(v) + ":t_0," + f(w) + ":t_1)")
        self.show()
        
        self.plot_after_swap()
    
    def show(self):
        for P in self.parties:
            P.show()
        print("AMM [" + f(self.r_0) + ":t_0," + f(self.r_1) + ":t_1], v = " + f(self.get_v()) + " $\n")
    
    def get_v(self):
        return self.r_0*v_t_0 + self.r_1*v_t_1
    
    def plot_before_swap(self,title):        
        X_MAX = 150
        x = [i for i in np.arange(1,X_MAX)]
        y = [self.c/j for j in x]
        plt.title(title)        
        plt.plot(x, y)        
        plt.plot(self.r_0,self.r_1, "go")
        plt.annotate("(" + str(round(self.r_0,1)) + "," + str(round(self.r_1,1)) + ")", (self.r_0,self.r_1))      

    def plot_after_swap(self):        
        plt.plot(self.r_0,self.r_1, "ro")
        plt.annotate("(" + str(round(self.r_0,1)) + "," + str(round(self.r_1,1)) + ")", (self.r_0,self.r_1))                  
        plt.show()    

        # plt.plot([x_1, y_1], [x_2, y_2])  draw line          
        
# Format utility
def f(v):
    return '{0: <10}'.format(round(v,3))

# Values of t_0 and t_1 in $ (for simplicity both equal to 1)
v_t_0 = 1
v_t_1 = 1

# Init parties
M = party("M",5.9,15)
A = party("A",20,0)

# Init AMM
AMM = amm(100,100,[M,A])
AMM.show()

# Value of attacker tokens before attack
v_M_pre = M.get_v()

# Transactions
print("\n# Front-run\n")
AMM.sl(M,5.9,5.6)

print("\n# Victim swap\n")
AMM.sl(A,20,15)

print("\n# Back-run\n")
AMM.sr(M,25.9,20.6)

# Compute and print profit of the attacker M
print("Profit of M = " + f(M.get_v() - v_M_pre) + "$")
