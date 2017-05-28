import numpy as np

class Factor(object):
    # class variables
    # self.vars : list of variables in order
    # self.idInfo : dict of vars and vals
    # self.pTable : probability table

    # vars: list of variables
    # vals: 2d list of values of variables
    # p: 2d list of probability of values
    def __init__(self, vars, vals, p):
        # Set variables
        self.vars = vars

        # Get count of variables
        cntVars = len(vars)
        # Generate identity information
        self.idInfo = dict()
        for i in xrange(0, cntVars):
            self.idInfo[vars[i]] = vals[i]

        # Generate np array
        self.pTable = np.array(p)
        rankTable = ()
        for i in xrange(0, cntVars):
            curTuple = (len(vals[i]),)
            rankTable = rankTable + curTuple
        # Reshape
        self.pTable = self.pTable.reshape(rankTable)

    def out(self):
        # Use for debugging
        print(self.pTable)

    def out_prob_recurse(self, curTuple):
        # Print probability recursively
        lenCurTuple = len(curTuple)
        if (len(self.vars) == lenCurTuple):
            # Base: Print
            for i in xrange(0, len(self.vars)):
                vals = self.idInfo[self.vars[i]]
                print vals[curTuple[i]],
                print(','),
            print(': '),
            print self.pTable.item(curTuple)
        else:
            # Next variable
            vals = self.idInfo[self.vars[lenCurTuple]]
            for i in xrange(0, len(vals)):
                nextTuple = (i, )
                self.out_prob_recurse(curTuple + nextTuple)

    def out_prob(self):
        # Use for printing probability
        curTuple = ()
        print(self.vars)
        self.out_prob_recurse(curTuple)

    def restrict(self, variable, value):
        # Find index of variable
        idxVar = self.vars.index(variable)
        # Construct sliceObjTuple
        sliceObjTuple = ()
        for i in xrange(0, idxVar):
            vals = self.idInfo[self.vars[i]]
            sliceObjTuple += slice(0, len(vals)),
        # Process target variable's value
        vals = self.idInfo[self.vars[idxVar]]
        idxVal = vals.index(value)
        sliceObjTuple += slice(idxVal, idxVal + 1),

        # 1. Slice vars
        var = self.vars[idxVar]
        del self.vars[idxVar]

        # 2. Slice vals
        del self.idInfo[var]

        # 3. Slice pTable
        self.pTable = self.pTable[sliceObjTuple]
        rankTable = ()
        for i in xrange(0, len(self.vars)):
            vals = self.idInfo[self.vars[i]]
            curTuple = (len(vals),)
            rankTable = rankTable + curTuple         
        self.pTable = self.pTable.reshape(rankTable)




