import math
from articles import Attributes, Article, ArticleCollection

# NOTE: convention for classification
# class 1 -> negative
# class 2 -> positive

class factor(object):
    # class variables
    # @ self.att_idx        : attribute index
    # @ self.classification : classification
    # NOTE: p(att | classification)
    def __init__(self):
        self.att_idx = -1
        self.classification = False
        self.p_pos = 0.0

    # set parameter of this factor
    # @ att_idx        : represented attribute index
    # @ classification : represented classification
    # @ p_pos          : possibility of when attribute is True
    def set_param(self, att_idx, classification, p_pos):
        self.att_idx = att_idx
        self.classification = classification
        self.p_pos = p_pos

    # get possibility of when attribute is True
    def get_p_pos(self):
        return self.p_pos

    # get possibility of when attribute is False
    def get_p_neg(self):
        return 1.0 - self.p_pos


class NBM(object):
    # class variables
    # @ self.attr        : attribute collection
    # @ self.att_cnt     : count of all attributes
    # @ self.art_col     : the collection of all training articles
    # @ self.factors_neg : the list of all factors of classification 1
    # @ self.factors_pos : the list of all factors of classification 2
    # @ self.prior_neg   : prior possibility of classification 1
    # @ self.prior_pos   : prior possibility of classification 2
    def __init__(self):
    # initialize all data
        self.attr = Attributes()
        self.att_cnt = self.attr.get_cnt()
        self.art_col = ArticleCollection(1061, "trainData.txt", "trainLabel.txt", self.att_cnt)
        self.factors_neg = None
        self.factors_pos = None
        self.prior_neg = -1.0
        self.prior_pos = -1.0

    # train the model by using trainData
    def learn(self):
        # init.
        idx_list = range(0, self.art_col.get_cnt())
        # split articles by classification
        (pos_list, neg_list) = self.split_cls(idx_list)
        # calculate prior possibility
        self.prior_pos = float(len(pos_list) + 1) / float(len(idx_list) + 2)
        self.prior_neg = float(len(neg_list) + 1) / float(len(idx_list) + 2)
        # print "Prior (neg, pos): ", self.prior_neg, self.prior_pos
        # calculate all factors
        self.factors_neg = [factor() for n in range(self.att_cnt)]
        self.factors_pos = [factor() for n in range(self.att_cnt)]
        for i in xrange(0, self.att_cnt):
            # calculate and assign
            p_pos = self.cal_pos_attr(pos_list, i)
            p_neg = self.cal_pos_attr(neg_list, i)
            self.factors_neg[i].set_param(i, False, p_neg)
            self.factors_pos[i].set_param(i, True, p_pos)
            # print "P -", i, "(neg, pos): ", p_neg, p_pos
    
    # test an article by using trained model
    # @ test_art_col : collection of all articles
    # @ art_idx      : article index
    def test_art(self, test_art_col, art_idx):
        # calculate posterior possibility of classification 1
        sum_neg = math.log(self.prior_neg)
        for i in xrange(0, self.att_cnt):
            if test_art_col.get_art_attr(art_idx, i) == True:
                # attribute == True
                sum_neg += math.log(self.factors_neg[i].get_p_pos())
            else:
                # attribute == False
                sum_neg += math.log(self.factors_neg[i].get_p_neg())
        
        # calculate posterior possibility of classification 2
        sum_pos = math.log(self.prior_pos)
        for i in xrange(0, self.att_cnt):
            if test_art_col.get_art_attr(art_idx, i) == True:
                # attribute == True
                sum_pos += math.log(self.factors_pos[i].get_p_pos())
            else:
                # attribute == False
                sum_pos += math.log(self.factors_pos[i].get_p_neg())
        
        # return result
        # print "pos, neg: ", sum_pos, ",", sum_neg
        if sum_pos > sum_neg:
            return True
        else:
            return False
    
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
            test_result = self.test_art(test_art_col, test_art_idx)
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

    # calculate the possibility of a True attribute within a list of articles
    # @ idx_list : list of articles' index
    # @ attr_idx : attribute index
    def cal_pos_attr(self, idx_list, attr_idx):
        pos_cnt = 0
        for art_idx in idx_list:
            if self.art_col.get_art_attr(art_idx, attr_idx) == True:
                pos_cnt += 1
        return float(pos_cnt + 1) / float(len(idx_list) + 2)

    # split list of articles into articles of class 2 and class 1
    # @ idx_list : list of articles' index
    def split_cls(self, idx_list):
        pos_cnt = 0
        neg_cnt = 0
        # calculate pos_cnt & neg_cnt
        for art_idx in idx_list:
            if self.art_col.get_art_cls(art_idx) == True:
                pos_cnt += 1
            else:
                neg_cnt += 1
        # pre-allocate memory
        pos_list = [-1 for n in range(pos_cnt)]
        neg_list = [-1 for n in range(neg_cnt)]
        # split
        pos_pos = 0
        neg_pos = 0
        for art_idx in idx_list:
            if self.art_col.get_art_cls(art_idx) == True:
                pos_list[pos_pos] = art_idx
                pos_pos += 1
            else:
                neg_list[neg_pos] = art_idx
                neg_pos += 1
        return (pos_list, neg_list)
    
    # sort index and value based on value
    def sort_idxval(self, idx, vals):
       for i in xrange(0, len(vals) - 1):
           for j in xrange(0, len(vals) - 1 - i):
               if (vals[j] <= vals[j + 1]):
                   # swap vals
                   (vals[j], vals[j + 1]) = (vals[j + 1], vals[j])
                   # swap index
                   (idx[j], idx[j + 1]) = (idx[j + 1], idx[j])

    # list top 10 discriminative words
    def list_top10(self):
        # pre-allocate memory
        result_idx = range(0, self.att_cnt)
        result_val = [-1.0 for n in range(self.att_cnt)]
        # calculate
        for attr_idx in result_idx:
            result_val[attr_idx] = abs(\
            math.log(self.factors_pos[attr_idx].get_p_pos(), 2) -\
            math.log(self.factors_neg[attr_idx].get_p_pos(), 2))
        # sort
        self.sort_idxval(result_idx, result_val)
        # print
        for i in xrange(0, 10):
            print "No.", i, ":", result_idx[i] + 1, ",", result_val[i], 
            print ",", self.attr.get_name(result_idx[i]),

# run
nbm = NBM()
nbm.learn()

nbm.list_top10()
nbm.test(707, "testData.txt", "testLabel.txt")
nbm.test(1061, "trainData.txt", "trainLabel.txt")