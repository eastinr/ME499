#!/usr/bin/env python

import itertools


class CapacitorSet:
    stringlist = []

    def __init__(self, caplist, parent=None, cap1=None, cap2=None):
        self.parent = parent
        self.caplist = caplist
        self.depth = len(caplist)
        self.child1 = cap1
        self.child2 = cap2
        self.ans = None

        if self.parent == None:
            try:
                self.str = str(self.caplist[0])
            except:
                self.str = "C"
            self.func = self.caplist[0]
            self.name = "root"
        else:
            self.str = self.parent.str

    def series(self):
        self.name = "Series".format(self.depth)
        self.func = self.calcSeries([self.parent.func, self.caplist[0]])
        if self.parent.name == self.name:
            newstr = self.parent.str
            if newstr[0] == '(' and newstr[-1] == ')':
                newstr = newstr[1:-1]
            self.str = "{0} + {1}".format(newstr, self.caplist[0])

        else:
            self.str = "({0} + {1})".format(self, self.caplist[0])
        self.stringlist.append((self.str, self.func))

    def parallel(self):
        self.name = "Parallel".format(self.depth)
        self.func = self.calcParallel([self.parent.func, self.caplist[0]])
        if self.parent.name == self.name:
            newstr = self.parent.str
            if newstr[0] == '(' and newstr[-1] == ')':
                newstr = newstr[1:-1]
            self.str = "{0} || {1}".format(newstr, self.caplist[0])

        else:
            self.str = "({0} || {1})".format(self, self.caplist[0])
        self.stringlist.append((self.str, self.func))

    def __str__(self):
        return self.str

    def __repr__(self):
        return self.str

    def getcombo(self):
        if self.depth == 1:
            return
        else:
            c1 = CapacitorSet(self.caplist[1:], self)
            c2 = CapacitorSet(self.caplist[1:], self)
            c1.series()
            c2.parallel()
            self.setchild(c1, c2)
            self.child1.getcombo()
            self.child2.getcombo()

    def setchild(self, child1, child2):
        self.child1 = child1
        self.child2 = child2


    def calcParallel(self, args):
        if len(args) == 2:
            return 1 / (1 / float(args[0]) + 1 / float(args[1]))
        else:
            ans = 1 / (1 / float(self.func) + 1 / float(args[0]))
            return ans

    def calcSeries(self, args):
        if len(args) == 2:
            return args[0] + args[1]
        else:
            ans = self.func() + args[1]
            return ans

def findCapacitor(target, max_number, caplist):
    newlist = itertools.product(caplist, repeat=max_number)
    dataset = set([])
    for lst in newlist:
        cap = CapacitorSet(lst)
        cap.getcombo()
        dataset |= set(cap.stringlist)
    datalist = list(dataset)
    datalist.sort(key=lambda data: -abs(target - data[1]))
    for datum in datalist:
        print "{0:.3f} = {1}".format(datum[1], datum[0])


if __name__ == '__main__':
    cap_list = [1, 10000, 10, 330, 100000, 1000, 3300, 2200]
    target = 26.53
    findCapacitor(target, 4, cap_list)

    #for index, func in enumerate(cap.funclist):
    #    print "{0}\t=\t{1}".format(cap.stringlist[index], func)
