import numpy as np

class Factor(object):
    # class variables
    # self.vars : list of variables in order
    # self.idInfo : dict of vars and vals
    # self.pTable : probability table

    def __init__(self):
        pass

    # vars: list of variables
    # vals: 2d list of values of variables
    # p: 2d list of probability of values
    def __init__(self, vars, vals, p):
        if len(vars) == 0:
            return

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

    @staticmethod
    def restrict(f, variable, value):
        # Find index of variable
        idxVar = f.vars.index(variable)
        # Construct sliceObjTuple
        sliceObjTuple = ()
        for i in xrange(0, idxVar):
            vals = f.idInfo[f.vars[i]]
            sliceObjTuple += slice(None),
        # Process target variable's value
        vals = f.idInfo[f.vars[idxVar]]
        idxVal = vals.index(value)
        sliceObjTuple += slice(idxVal, idxVal + 1),

        # 1. Slice vars
        var = f.vars[idxVar]
        del f.vars[idxVar]

        # 2. Slice vals
        del f.idInfo[var]

        # 3. Slice pTable
        f.pTable = f.pTable[sliceObjTuple]
        rankTable = ()
        for i in xrange(0, len(f.vars)):
            vals = f.idInfo[f.vars[i]]
            curTuple = (len(vals),)
            rankTable = rankTable + curTuple         
        f.pTable = f.pTable.reshape(rankTable)

    @staticmethod
    def multiply(fl, fr):
        # Check alignment
        if (fl.vars[-1] != fr.vars[0]):
            raise NotAlignmentException

        # Create new factor object
        fN = Factor([],[],[])

        # Creat new variables & values dict
        varS = fl.vars[-1] # shared variable
        idInfoN = dict() # new idInfo dict 

        varsL = fl.vars[:len(fl.vars) - 1]
        cntVarsL = len(varsL)
        for var in varsL:
            idInfoN[var] = fl.idInfo[var]
        
        idInfoN[varS] = fl.idInfo[varS]

        varsR = fr.vars[1:len(fr.vars)]
        cntVarsR = len(varsR)
        for var in varsR:
            idInfoN[var] = fr.idInfo[var]
        # Update new Factor object
        fN.vars = varsL + list(varS) + varsR
        fN.idInfo = idInfoN

        # Reshape fl
        rankTable = fl.pTable.shape
        for i in xrange(0, cntVarsR):
            rankTable += (1,)
        pTableL = fl.pTable.reshape(rankTable)
        # Reshape fr
        rankTable = ()
        for i in xrange(0, cntVarsL):
            rankTable += (1,)
        rankTable += fr.pTable.shape
        pTableR = fr.pTable.reshape(rankTable)
        # Create new pTable
        fN.pTable = pTableL * pTableR

        return fN
