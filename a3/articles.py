class Attributes(object):
    # class variables
    # @ self.cnt : total count of attributes (words)
    def __init__(self):
        file = open("words.txt")
        self.cnt = 0

        while 1:
            line = file.readline()
            if not line:
                break
            self.cnt += 1

        file.close()
    
    def get_cnt(self):
        return self.cnt

# Used as Examples
class Article(object):
    # class variables
    # @ self.attr_vals      : array of all attributes values
    # @ self.classification : class
    def __init__(self, attr_cnt):
        # pre-allocate list
        self.attr_vals = [False for n in range(attr_cnt)]

    def set_attr(self, idx):
        if self.attr_vals[idx] == True:
            raise DoubleSetException()
        # Set corresponding attributes to True
        self.attr_vals[idx] = True
    
    def get_attr(self, idx):
        return self.attr_vals[idx]
    
    def set_class(self, cls):
        # 1 = False
        # 2 = True
        self.classification = cls == 2
    
    def get_class(self):
        return self.classification

class ArticleCollection(object):
    # class variables
    # @ self.attrs : array of all articles
    def __init__(self, attr_cnt):
        # pre-allocate list
        self.attrs = [Article(attr_cnt) for n in range(1061)]
        # read data
        file = open("trainData.txt")
        while 1:
            line = file.readline()
            if not line:
                break
            # get article index and attribute index
            tokens = line.split("\t")
            art_idx = int(tokens[0]) - 1
            attr_idx = int(tokens[1]) - 1
            # set attribute
            self.attrs[art_idx].set_attr(attr_idx)
        file.close()

        # read lable
        file = open("trainLabel.txt")
        art_idx = 0
        while 1:
            line = file.readline()
            if not line:
                break
            # get classification
            classification = int(line)
            # set attribute
            self.attrs[art_idx].set_class(classification)
            # move to next article
            art_idx += 1
        file.close()
    
    def get_art_cls(self, idx):
        return self.attrs[idx].get_class()

    def get_art_attr(self, art_idx, attr_idx):
        return self.attrs[art_idx].get_attr(attr_idx)

    def get_cnt(self):
        return len(self.attrs)

# # Test
# att = Attributes()
# print(att.get_cnt())
# art_col = ArticleCollection(att.get_cnt())
# print(art_col.get_art_attr(1060, 25))
# print(art_col.get_art_attr(1060, 26))
# print(art_col.get_art_attr(1060, 27))
# print(art_col.get_art_cls(479))
# print(art_col.get_art_cls(480))
# print(art_col.get_art_cls(1060))