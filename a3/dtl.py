import math
from articles import Attributes, Article, ArticleCollection

# NOTE: convention for classification
# class 1 -> negative
# class 2 -> positive

class DTNode(object):
    # class variables
    # @ self.pos      : branch of positive value
    # @ self.neg      : branch of negative value
    # @ self.attr_idx : attribute index (only valid on internal node)
    # @ self.ig       : information gain
    # @ self.cls      : classification (only valid on leaf node)
    # @ self.depth    : the depth of this node
    def __init__(self, depth):
        self.pos = None
        self.neg = None
        self.cls = False
        self.attr_idx = -1
        self.ig = -1.0
        self.depth = depth

class DTL(object):
    # class variables
    # @ self.zero_val : zero value threshold
    # @ self.attr     : attribute collection
    # @ self.att_cnt  : count of all attributes
    # @ self.art_col  : the collection of all training articles
    # @ self.root     : root of decision tree
    def __init__(self):
        # initialize all data
        self.zero_val = 0.0000000000000001
        self.attr = Attributes()
        self.att_cnt = self.attr.get_cnt()
        self.art_col = ArticleCollection(1061, "trainData.txt", "trainLabel.txt", self.att_cnt)
    
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
            epy = float(-1) * p_pos * math.log(p_pos, 2.0) \
            - p_neg * math.log(p_neg, 2.0)

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
            nor_epy_pos = float(pos_len) / float(tol_len) * float(epy_pos)
            nor_epy_neg = float(neg_len) / float(tol_len) * float(epy_neg)
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
        return pos_len >= neg_len
    
    # determine is the classification same among all examples
    def is_same_cls(self, idx_list):
        pos_len = 0
        neg_len = 0
        for art_idx in idx_list:
            if True == self.art_col.get_art_cls(art_idx):
                pos_len += 1
            else:
                neg_len += 1
        return pos_len == 0 or neg_len == 0


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

        return best_attr_idx, best_attr_ig
    
    # DTL recurse function
    # @ cur_depth   : current depth of decision tree
    # @ idx_list    : list of all current examples' index
    # @ attr_list   : list of all current attribute index
    # @ default_cls : default classification
    def learn_recurse(self, max_depth, cur_depth, idx_list, attr_list, default_cls):
        self.node_cnt += 1
        # print "current node count: ", self.node_cnt, "/", self.att_cnt
        if cur_depth == max_depth:
            # reach max_depth
            node = DTNode(cur_depth)
            node.cls = self.mode(idx_list)
            return node
        elif len(idx_list) == 0:
            # empty example list
            node = DTNode(cur_depth)
            node.cls = default_cls
            return node
        elif self.is_same_cls(idx_list):
            # all examples have same classification
            node = DTNode(cur_depth)
            node.cls = self.mode(idx_list)
            return node
        elif len(attr_list) == 0:
            # empty attribute list
            node = DTNode(cur_depth)
            node.cls = self.mode(idx_list)
            return node
        else:
            # duplicate attr_list
            dup_attr_list = list(attr_list)
            # calculate best attribute
            (best_attr, best_ig) = self.choose_attr(idx_list, dup_attr_list)
            # split
            (pos_list, neg_list, pos_len, neg_len) = self.split(idx_list, best_attr)
            # recurse procedure start here
            new_default_cls = self.mode(idx_list)
            new_depth = cur_depth + 1
            # print "current depth: ", cur_depth
            node = DTNode(cur_depth)
            # best_attr => True
            node.pos = self.learn_recurse(max_depth, new_depth, pos_list, \
                    dup_attr_list, new_default_cls)
            # best_attr => False
            node.neg = self.learn_recurse(max_depth, new_depth, neg_list, \
                    dup_attr_list, new_default_cls)
            # add branch label
            node.attr_idx = best_attr
            node.ig = best_ig
            return node

    # perfrom a DTL
    # @ max_depth : maximum depth of decision tree
    def learn(self, max_depth):
        # init.
        idx_list = range(0, self.art_col.get_cnt())
        attr_list = range(0, self.att_cnt)
        default_cls = self.mode(idx_list) # get default cls by mode
        self.node_cnt = 0
        # start to learn
        self.root = self.learn_recurse(max_depth, 0, idx_list, attr_list, default_cls)

    # print decision recurse procedure
    def print_tree_recurse(self, dt_node):
        if dt_node.pos == None and dt_node.neg == None:
            print "Class",
            if dt_node.cls == False:
                print "1"
            else:
                print "2"
        else:
            print "Label", dt_node.attr_idx + 1, "(", dt_node.ig, ")",
            print "-", self.attr.get_name(dt_node.attr_idx),
            # negative branch
            for n in xrange(0, dt_node.depth):
                print "  ",
            print "False:",
            self.print_tree_recurse(dt_node.neg)
            # positive branch
            for n in xrange(0, dt_node.depth):
                print "  ",
            print "True:",
            self.print_tree_recurse(dt_node.pos)

    # print decision tree
    def print_tree(self):
        self.print_tree_recurse(self.root)

    # test recurse procedure
    # @ test_art_col : test article collection
    # @ test_art_idx : test article index
    # @ dt : decision tree node
    def test_recurse(self, test_art_col, test_art_idx, dt_node):
        assert(dt_node != None)
        if dt_node.pos == None and dt_node.neg == None:
            # reach a leaf node
            return dt_node.cls
        else:
            # need to determine which node
            art_attr_val = test_art_col.get_art_attr(test_art_idx, dt_node.attr_idx)
            # print "article: ", test_art_idx, ", attribute index: ", dt_node.attr_idx
            # go to corresponding node
            if True == art_attr_val:
                return self.test_recurse(test_art_col, test_art_idx, dt_node.pos)
            else:
                return self.test_recurse(test_art_col, test_art_idx, dt_node.neg)

    # perform a test
    # @ art_cnt    : count of all articles
    # @ data_file  : test data file name
    # @ label_file : test label file name
    def test(self, art_cnt, data_file, label_file):
        # read all test data
        test_art_col = ArticleCollection(art_cnt, data_file, label_file, self.att_cnt)
        # pre-allocate memory for result
        result = [False for n in range(test_art_col.get_cnt())]
        # init. other variables
        pass_cnt = 0
        fail_cnt = 0
        # run test for all
        for test_art_idx in xrange(0, test_art_col.get_cnt()):
            test_result = self.test_recurse(test_art_col, test_art_idx, self.root)
            if test_result == test_art_col.get_art_cls(test_art_idx):
                pass_cnt += 1
            else:
                fail_cnt += 1
        
        print "Test result:"
        print "Pass / Fail : ", pass_cnt, "/", fail_cnt
        # calculate accuracy
        tol_cnt = test_art_col.get_cnt()
        accuracy = float(pass_cnt) / float(tol_cnt) * 100.0
        print "Accuracy: ", accuracy


print "Loading..."
dtl = DTL()
# print dtl.entropy(range(0, 960))
# print dtl.split(range(0, 1060), 0)

# print dtl.mode(range(0, 1060))
# print dtl.mode(range(0, 960))
# print dtl.mode(range(0, 959))
# print dtl.mode(range(1, 959))

# print "IG:"
# print 0, dtl.ig(range(0, 1060), 0)
# print 1, dtl.ig(range(0, 1060), 1)
# print 20, dtl.ig(range(0, 1060), 20)
# print 40, dtl.ig(range(0, 1060), 40)

# print "Choose Attribute:"
# attr_list = [0, 1, 20, 40]
# print attr_list
# print dtl.choose_attr(range(0, 1060), attr_list)
# print attr_list

# 1. Calculate the accuracy under each max_depth
for max_depth in xrange(0, 26):
    print "Max Depth:", max_depth
    print "Learning..."
    dtl.learn(max_depth)
    print "Test trainData: "
    dtl.test(1061, "trainData.txt", "trainLabel.txt")
    print "Test testData: "
    dtl.test(707, "testData.txt", "testLabel.txt")

# 2. Output tree when maximum accuracy is reached
dtl.learn(4)
dtl.print_tree()
dtl.test(707, "testData.txt", "testLabel.txt")
