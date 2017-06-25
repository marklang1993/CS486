import math
from articles import Attributes, Article, ArticleCollection

class DTL(object):
    # class variables
    # @ self.zero_val : zero value threshold
    # @ self.att_cnt  : count of all attributes
    # @ self.art_col  : the collection of all train articles
    def __init__(self):
        # initialize all data
        self.zero_val = 0.00000001
        att = Attributes()
        self.att_cnt = att.get_cnt()
        self.art_col = ArticleCollection(self.att_cnt)
    
    @staticmethod
    def log2(anti_log):
        return math.log(anti_log) / math.log(2.0)

    # split list of articles to 2 lists of articles based on an attribute
    # @ idx_list : list of all examples' index
    # @ attr_idx : attribute index
    # RETURN     : tup
    def split(self, idx_list, attr_idx):
        pos_len = 0
        neg_len = 0
        # pre-scan
        for art_idx in idx_list:
            if True == self.art_col.get_art_attr(art_idx, attr_idx):
                pos_len += 1
            else:
                neg_len += 1
        # pre-allocate memory
        pos_list = [-1 for n in range(pos_len)]
        neg_list = [-1 for n in range(neg_len)]
        # scan again to split
        pos_pos = 0
        neg_pos = 0
        for art_idx in idx_list:
            if True == self.art_col.get_art_attr(art_idx, attr_idx):
                pos_list[pos_pos] = art_idx
                pos_pos += 1
            else:
                neg_list[neg_pos] = art_idx
                neg_pos += 1
                
        return (pos_list, neg_list, pos_len, neg_len)

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
    # calculate information gain based on an attribute
    # @ idx_list : list of all examples' index
    # @ attr_idx : attribute index
    def ig(self, idx_list, attr_idx):
        # split and calculate ig
        (pos_list, neg_list, pos_len, neg_len) = self.split(idx_list, attr_idx)
        tol_len = pos_len + neg_len
        assert(tol_len == len(idx_list))
        # calculate ig
        if 0 == pos_len or 0 == neg_len:
            # any sub list = 0, IG = 0
            ig = 0.0
        else:
            epy_base = self.entropy(idx_list)
            # calculate remainder
            epy_pos = self.entropy(pos_list)
            epy_neg = self.entropy(neg_list)
            nor_epy_pos = float(pos_len)/float(tol_len) * float(epy_pos)
            nor_epy_neg = float(neg_len)/float(tol_len) * float(epy_neg)
            remainder = nor_epy_pos + nor_epy_neg
            ig = epy_base - remainder

        return ig

print "Loading..."
dtl = DTL()
print dtl.entropy(range(0, 960))
print dtl.split(range(0, 1060), 0)
print "IG:"
print dtl.ig(range(0, 1060), 0)
print dtl.ig(range(0, 1060), 1)
print dtl.ig(range(0, 1060), 20)