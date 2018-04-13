from typing import List
from scipy.sparse.csgraph import shortest_path as sp
import numpy as np

class WagnerWhitin:
    '''
    A Wagner-Whitin problem.

    H.M. Wagner and T. Whitin, "Dynamic version of the economic lot size model," Management Science, Vol. 5, pp. 89–96, 1958
    '''

    def __init__(self, K: float, h: float, d: List[float]):
        '''
        Create an instance of a Wagner-Whitin problem.
        K: the fixed ordering cost;
        h: the per unit holding cost;
        d: the demand in each period.
        '''
        self.K = K #The fixed ordering cost
        self.h = h #The per unit holding cost
        self.d = d #The demand in each period
    
    def cycle_cost(self, i: int, j: int) -> float:
        '''
        Compute the cost of a replenishment cycle covering periods i,...,j
        '''
        return self.K + self.h*sum([(k-i)*self.d[k] for k in range(i,j+1)]) if i<=j else 0

    def cycle_cost_matrix(self):
        '''
        Compute a matrix with the cost of every possible replenishment cycle
        '''
        T = len(self.d)
        return [[self.cycle_cost(i,j) for j in range(0,T)] for i in range(0,T)]

    def optimal_cost(self):
        '''
        Compute the cost of an optimal solution to the Wagner-Whitin problem
        '''
        m = sp(np.array(self.cycle_cost_matrix()))
        pred = sp(np.array(self.cycle_cost_matrix()),return_predecessors=True)[1][0,:]
        T = len(self.d)
        s, p, cost = T, pred[T-1], 0
        while p > 0: 
            cost += m[p][s-1]
            s, p = p, pred[p]
        return cost + m[p][s-1]

    def order_quantities(self):
        '''
        Compute optimal Wagner-Whitin order quantities
        '''
        pred = sp(np.array(self.cycle_cost_matrix()),return_predecessors=True)[1][0,:]
        T = len(self.d)
        s, p = T, pred[T-1]
        qty = [0 for k in range(0,T)]
        while p > 0: 
            qty[p] = sum([self.d[k] for k in range(p,s)])
            s, p = p, pred[p]
        qty[0] = sum([self.d[k] for k in range(0,s)])
        return qty

if __name__ == '__main__':
    instance = {"K": 30, "h": 1, "d":[10,20,30,40]}
    ww = WagnerWhitin(**instance)
    print("Cost of an optimal plan: ", ww.optimal_cost())
    print("Optimal order quantities: ", ww.order_quantities())