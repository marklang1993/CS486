import numpy as np

class Factor(object):
    # class variables
    # self.vars : list of variables in order
    # self.idInfo : dict of vars and vals
    # self.pTable : probability table

    # __init__()
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

    # print_table_recurse(): print_table() helper function
    def print_table_recurse(self, curTuple):
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
                self.print_table_recurse(curTuple + nextTuple)

    # print_table(): Print current factor in a neat form
    def print_table(self):
        # Use for printing probability
        curTuple = ()
        print(self.vars)
        self.print_table_recurse(curTuple)

    # copy(): Duplicate current factor
    def copy(self):
        fN = Factor([],[],[])
        fN.vars = list(self.vars)
        fN.idInfo = dict(self.idInfo)
        fN.pTable = self.pTable.copy()
        return fN

    # sort_factor(): Sort variables in this factor
    def sort_factor(self):
       for i in xrange(0, len(self.vars) - 1):
           for j in xrange(0, len(self.vars) - 1 - i):
               if (self.vars[i] > self.vars[i + 1]):
                   # swap variables
                   tmp = self.vars[i]
                   self.vars[i] = self.vars[i + 1]
                   self.vars[i + 1] = tmp
                   # swap axes
                   self.pTable = np.swapaxes(self.pTable, i, i + 1)

    # restrict()
    # f: Factor object
    # variable: Restricted variable
    # value: Variable's value
    @staticmethod
    def restrict(f, variable, value):
        # Create new factor object & copy
        fN = f.copy()
        # Find index of variable
        idxVar = fN.vars.index(variable)
        # Construct sliceObjTuple
        sliceObjTuple = ()
        for i in xrange(0, idxVar):
            vals = fN.idInfo[fN.vars[i]]
            sliceObjTuple += slice(None),
        # Process target variable's value
        vals = fN.idInfo[fN.vars[idxVar]]
        idxVal = vals.index(value)
        sliceObjTuple += slice(idxVal, idxVal + 1),
        # 1. Slice vars
        var = fN.vars[idxVar]
        del fN.vars[idxVar]
        # 2. Slice vals
        del fN.idInfo[var]
        # 3. Slice pTable
        fN.pTable = fN.pTable[sliceObjTuple]
        rankTable = ()
        for i in xrange(0, len(fN.vars)):
            vals = fN.idInfo[fN.vars[i]]
            curTuple = (len(vals),)
            rankTable = rankTable + curTuple         
        fN.pTable = fN.pTable.reshape(rankTable)
        return fN

    # multiply()
    # fl: Left Factor object
    # fr: Right Factor object
    @staticmethod
    def multiply(fl, fr):
        # Sort each factor
        fl.sort_factor()
        fr.sort_factor()
        # Calculate common variables
        commonVars = list()
        for var in fl.vars:
            if var in fr.vars:
                commonVars.append(var)
        for var in fr.vars:
            if var in fl.vars:
                if not(var in commonVars):
                    commonVars.append(var)
        # Calculate union variables
        unionVars = list(fl.vars)
        for var in fr.vars:
            if not (var in commonVars):
                unionVars.append(var)
        # Sort both lists
        commonVars.sort()
        unionVars.sort()

        # Check each variable
        flTuple = ()
        frTuple = ()
        for var in unionVars:
            if var in fl.vars:
                flTuple += (len(fl.idInfo[var]), )
            else:
                flTuple += (1, )
            if var in fr.vars:
                frTuple += (len(fr.idInfo[var]), )
            else:
                frTuple += (1, )
        # Reshape
        pTableL = fl.pTable.reshape(flTuple)
        pTableR = fr.pTable.reshape(frTuple)

        # Create new factor object
        fN = Factor([],[],[])
        fN.pTable = pTableL * pTableR
        fN.vars = unionVars
        fN.idInfo = dict()
        for var in unionVars:
            if var in fl.idInfo:
                fN.idInfo[var] = list(fl.idInfo[var])
            if var in fr.idInfo:
                fN.idInfo[var] = list(fr.idInfo[var])
        return fN

    # sumout()
    # f: Factor object
    # variable: Summout variable
    @staticmethod
    def sumout(f, variable):
        # Create new factor object & copy
        fN = f.copy()
        # Get var index & update variables list
        varIdx = fN.vars.index(variable)
        del fN.vars[varIdx]
        # Update idInfo
        del fN.idInfo[variable]
        # Update pTable
        fN.pTable = fN.pTable.sum(axis = varIdx)
        return fN

    # normalize()
    # f: Factor object
    @staticmethod
    def normalize(f):
        # Create new factor object & copy
        fN = f.copy()
        # Normalize
        sum = fN.pTable.sum()
        fN.pTable = fN.pTable / sum
        return fN
    
    # inference()
    # fList: List of Factor objects
    # queryVars: query Variables
    # orderedHiddenVarsList: List of strings of Variable
    # evidenceList: Dict of Variable : Value
    @staticmethod
    def inference(fList, queryVars, orderedHiddenVarsList, evidenceList):
        # Restrict by evidence
        for e in evidenceList:
            fListN = list()
            for factor in fList:
                if (e in factor.vars):
                    fRestrict = Factor.restrict(factor, e, evidenceList[e])
                    print 'Restrict:',
                    print e
                    fRestrict.print_table()
                    fListN.append(fRestrict)
                else:
                    fListN.append(factor)
            # Update factor list
            fList = fListN

        # Elimination
        for hV in orderedHiddenVarsList:
            fListM = list() # list of factors needed to be multiplied
            fListNM = list() # list of factors not needed to be multiplied
            # Split
            for factor in fList:
                if (hV in factor.vars):
                    fListM.append(factor)
                else:
                    fListNM.append(factor)
            
            # Multiply all
            fProduct = reduce(Factor.multiply, fListM)
            print 'Multiply:',
            print hV
            fProduct.print_table()
            # Sumout
            fSumout = Factor.sumout(fProduct, hV)
            print 'Sumout:',
            print hV
            fSumout.print_table()
            # Update factor list
            fList = fListNM
            fList.append(fSumout)

        # The remaining factors only refer to query variable
        # Take product & normalize
        fProduct = reduce(Factor.multiply, fList)
        print 'Last Multiply:'
        fProduct.print_table()
        print 'Normalize'
        fResult = Factor.normalize(fProduct)
        return fResult

            
