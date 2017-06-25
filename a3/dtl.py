import math
from articles import Attributes, Article, ArticleCollection

class DTL(object):
    # class variables
    # @ self.zero_val : zero value threshold
    # @ self.att      : all attributes
    # @ self.art_col  : the collection of all train articles
    def __init__(self):
        # initialize all data
        self.zero_val = 0.00000001
        self.att = Attributes()
        self.art_col = ArticleCollection(self.att.get_cnt())
    
    @staticmethod
    def log2(anti_log):
        return math.log(anti_log) / math.log(2.0)

    # calculate entropy of a set of examples
    # @ idx_list : list of all examples' index
    def entropy(self, idx_list):
        # initialize count
        cnt_pos = 0
        cnt_neg = 0
        cnt_tol = 0
        # iterate
        for art_idx in idx_list:
            if True == self.art_col.get_art_cls(art_idx):
                cnt_pos += 1
            else:
                cnt_neg += 1
            cnt_tol += 1

        # calculate
        p_pos = float(cnt_pos) / float(cnt_tol)
        p_neg = float(cnt_neg) / float(cnt_tol)
        if p_pos < self.zero_val:
            # consider possibility of positive articles is 0
            epy = 0.0

        elif p_neg < self.zero_val:
            # consider possibility of negative articles is 0
            epy = 0.0
        else:
            # nothing has possibility of 0
            epy = float(-1) * p_pos * DTL.log2(p_pos) - p_neg * DTL.log2(p_neg)

        return epy


print "Loading..."
dtl = DTL()
print dtl.entropy(range(0, 960))