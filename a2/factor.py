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

    def print_table(self):
        # Use for printing probability
        curTuple = ()
        print(self.vars)
        self.out_prob_recurse(curTuple)

    def copy(self):
        fN = Factor([],[],[])
        fN.vars = list(self.vars)
        fN.idInfo = dict(self.idInfo)
        fN.pTable = self.pTable.copy()
        return fN

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

    @staticmethod
    def multiply(fl, fr):
        # Calculate common variables
        commonVars = [var for var in fl.vars if var in fr.vars]
        if len(commonVars) != 1:
            raise MoreThanOneCommonVarsException
        # Check alignment
        if (fl.vars[-1] != fr.vars[0]):
            # Not alignment
            if (len(commonVars) == 0):
                raise CommonVarNotAvailableException
            commonVar = commonVars[0] # Get 1 common Variable
            if (fl.vars[0] == commonVar and fr.vars[-1] == commonVar):
                # swap fl and fr
                fl, fr = fr, fl
            else:
                # Left factor is not aligned
                if (fl.vars[-1] != commonVar):
                    # Swap variable
                    cVarIdx = fl.vars.index(commonVar)
                    fl.vars[cVarIdx], fl.vars[-1] = fl.vars[-1], fl.vars[cVarIdx]
                    # Swap probability
                    fl.pTable = np.swapaxes(fl.pTable, cVarIdx, fl.pTable.ndim - 1)
               # Right factor is not aligned
                if (fr.vars[0] != commonVar):
                    # Swap variable
                    cVarIdx = fr.vars.index(commonVar)
                    fr.vars[cVarIdx], fr.vars[0] = fr.vars[0], fr.vars[cVarIdx]
                    # Swap probability
                    fr.pTable = np.swapaxes(fr.pTable, cVarIdx, 0)

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
        fN.vars = varsL + [varS] + varsR
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
    
    @staticmethod
    def normalize(f):
        # Create new factor object & copy
        fN = f.copy()
        # Normalize
        sum = fN.pTable.sum()
        fN.pTable = fN.pTable / sum

        return fN
    
    # fList: List of Factor objects
    # queryVars: query Variables
    # orderedHiddenVarsList: List of strings of Variable
    # evidenceList: Dict of Variable : Value
    @staticmethod
    def inference(fList, queryVars, orderedHiddenVarsList, evidenceList):
        # Restrict by evidence
        fListN = list()
        for e in evidenceList:
            for factor in fList:
                if (e in factor.vars):
                    fListN.append(Factor.restrict(factor, e, evidenceList[e]))
                else:
                    fListN.append(factor)
            # Update factor list
            fList = fListN
        fList[1].print_table()

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
            fProduct.print_table()
            # Summout
            fSumout = Factor.sumout(fProduct, hV)
            fSumout.print_table()
            # Update factor list
            fList = fListNM
            fList.append(fSumout)

        # The remaining factors only refer to query variable
        # Take product & normalize
        fProduct = reduce(Factor.multiply, fList)
        fResult = Factor.normalize(fProduct)

        return fResult

            
