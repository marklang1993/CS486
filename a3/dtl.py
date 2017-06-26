import math
from articles import Attributes, Article, ArticleCollection

# NOTE: convention for classification
# class 1 -> negative
# class 2 -> positive

class DTNode(object):
    # class variables
    # @ self.pos   : branch of positive value
    # @ self.neg   : branch of negative value
    # @ self.cls   : only valid on leaf node
    # @ self.depth : the depth of this node
    def __init__(self, depth):
        self.pos = None
        self.neg = None
        self.cls = False
        self.depth = depth

class DTL(object):
    # class variables
    # @ self.zero_val : zero value threshold
    # @ self.att_cnt  : count of all attributes
    # @ self.art_col  : the collection of all training articles
    # @ self.root     : root of decision tree
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

    # calculate mode classification
    # @ idx_list : list of all examples' index
    def mode(self, idx_list):
        pos_len = 0
        neg_len = 0
        for art_idx in idx_list:
            if True == self.art_col.get_art_cls(art_idx):
                pos_len += 1
            else:
                neg_len += 1
        print pos_len, neg_len
        return pos_len >= neg_len
    
    # generate an attribute list of all available attribute index
    def attr_list_gen(self):
        return range(0, self.att_cnt)

    # choose best attribute based on IG
    # @ idx_list  : list of all examples' index
    # @ attr_list : list of all attribute index
    def choose_attr(self, idx_list, attr_list):
        # determine the attr_list is empty
        if len(attr_list) == 0:
            return -1
        # init.
        best_attr_ig = -1.0 # IG of corresponding attribute (NOTE: larger is better)
        best_attr_idx = -1  # attribute index
        best_attr_idx_in_list = -1 # index of attrbute index in attr_list
        # calculat best
        for i in xrange(0, len(attr_list)):
            attr_idx = attr_list[i]
            # calculate IG
            attr_ig = self.ig(idx_list, attr_idx)
            # determine is this attribute is better?
            if attr_ig > best_attr_ig:
                best_attr_ig = attr_ig
                best_attr_idx = attr_idx
                best_attr_idx_in_list = i
        # remove that attribute
        del attr_list[best_attr_idx_in_list]

        return best_attr_idx
    
    # DTL recurse function
    # @ cur_depth   : current depth of decision tree
    # @ idx_list    : list of all current examples' index
    # @ attr_list   : list of all current attribute index
    # @ default_cls : default classification
    def learn_recurse(self, cur_depth, idx_list, attr_list, default_cls):
        if len(idx_list) == 0:
            node = DTNode(cur_depth)
            return default_cls

    # perfrom a DTL
    # @ max_depth : maximum depth of decision tree
    def learn(self, max_depth):
        # init.
        idx_list = range(0, 1060)
        attr_list = range(0, self.att_cnt)
        default_cls = self.mode(idx_list) # get default cls by mode
        # start to learn
        self.root = self.learn_recurse(0, idx_list, attr_list, default_cls)


print "Loading..."
dtl = DTL()
# print dtl.entropy(range(0, 960))
# print dtl.split(range(0, 1060), 0)
print "IG:"
print 0, dtl.ig(range(0, 1060), 0)
print 1, dtl.ig(range(0, 1060), 1)
print 20, dtl.ig(range(0, 1060), 20)
print 40, dtl.ig(range(0, 1060), 40)
# print dtl.mode(range(0, 1060))
# print dtl.mode(range(0, 960))
# print dtl.mode(range(0, 959))
# print dtl.mode(range(1, 959))
print "Choose Attribute:"
attr_list = [0, 1, 20, 40]
print attr_list
print dtl.choose_attr(range(0, 1060), attr_list)
print attr_list

