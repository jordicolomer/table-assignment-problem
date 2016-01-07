import random
import time
from table_assign import _get_table_suggestions

class Table:
    id = 0
    table_location_horizontal = 0
    table_location_vertical = 0
    capacity = 0
    available = 0
    roomid = 0
    unassigned = False
    
    def _print(self):
        print self.table_location_horizontal, self.table_location_vertical, self.capacity, self.available, self.roomid, self.unassigned


def str2tables(s):
    tables = []
    id = 0
    if s[0] == '\n':
        s = s[1:]
    if s[-1] == '\n':
        s = s[:-1]
    rooms = s.split('\n\n')
    for roomid in range(len(rooms)):
        rows = rooms[roomid].split('\n')
        for y in range(len(rows)):
            row = rows[y]
            row = row.replace('*', ' *')
            row = row.strip()
            cells = row.split(' ')
            unassigned = False
            if cells[0] == 'u':
                unassigned = True
                cells = cells[1:]
            for x in range(len(cells)):
                cell = cells[x]
                if cell[0] == '*':
                    available = 0
                    capacity = int(cell[1:])
                else:
                    available = int(cell)
                    capacity = int(cell)
                if capacity > 0:
                    table = Table()
                    table.table_location_horizontal = x+1
                    table.table_location_vertical = y+1
                    table.capacity = capacity
                    table.available = available
                    table.roomid = roomid
                    table.unassigned = unassigned
                    table.id = id
                    id+=1
                    tables.append(table)
                    
    return tables


def tables2str(tables, selected=None):
    ret = '\n'
    maxroom = max([table.roomid for table in tables])
    for roomid in range(maxroom+1):
        #print 'roomid',roomid
        roomtables = []
        for table in tables:
            if table.roomid == roomid:
                roomtables.append(table)
        maxx = max([table.table_location_horizontal for table in roomtables if not table.unassigned])
        maxy = max([table.table_location_vertical for table in roomtables if not table.unassigned])
        for j in range(1, maxy+1):
            row = ''
            for i in range(1, maxx+1):
                tableij = None
                for table in roomtables:
                    if table.table_location_horizontal == i and table.table_location_vertical == j and not table.unassigned:
                        tableij = table
                if tableij:
                    #print i,j
                    #tableij._print()
                    #print tableij.id
                    bselected = False
                    for sel in selected:
                        if tableij.id == sel.id:
                            bselected = True
                    if bselected:
                        row += '+'+str(tableij.capacity)
                    elif tableij.available == 0:
                        row += '*'+str(tableij.capacity)
                    else:
                        row += ' '+str(tableij.capacity)
                else:
                    row += ' 0'
            #print row
            ret += row+'\n'
        row = 'u'
        for table in roomtables:
            if table.unassigned:
                bselected = False
                for sel in selected:
                    if table.id == sel.id:
                        bselected = True
                if bselected:
                    row += '+'+str(table.capacity)
                elif table.available == 0:
                    row += '*'+str(table.capacity)
                else:
                    row += ' '+str(table.capacity)
        if len(row)>1:
            #print row
            ret += row+'\n'
        #print ''
        ret += '\n'
    return ret[:-1]
                

def random_tables():
    nrooms = random.randint(1, 3) #[a,b]
    s='\n'
    for room in range(nrooms):
        x = random.randint(1, 5)
        y = random.randint(1, 5)
        for j in range(y):
            for i in range(x):
                capacity = random.randint(0, 9)
                s += ' '+str(capacity)
            s += '\n'
        unassigned = 0
        if random.randint(1, 4) == 1:
            unassigned = random.randint(1, 5)
            s += 'u'
            for i in range(unassigned):
                capacity = random.randint(0, 9)
                s += ' '+str(capacity)
            s += '\n'
        s += '\n'
    return s[:-1]


def random_tests():
    random.seed(0)
    for n in range(10):
        print 'Facility',n
        s = random_tables()
        print '['+s+']'
        tables = str2tables(s)
        for n in range(10):
            print 'ite',n
            num = random.randint(1, 5) #[a,b]
            print 'num:',num
            selected = _get_table_suggestions(tables, num)
            if selected is None:
                print "doesn't fit"
                print tables2str(tables, [])
            else:
                print tables2str(tables, selected)

random_tests()


def assert_output(s1, num, s2=None):
    tables = str2tables(s1)
    selected = _get_table_suggestions(tables, num)
    if selected:
        sres = tables2str(tables, selected)
        if s2:
            print s2 == sres
            if s2 != sres:
                print sres
        else:
            print sres

s1='''
 2
 1
 1
'''
num = 3
s2='''
+2
+1
 1
'''
assert_output(s1, num, s2)

s1='''
 1 1 1
 1 1 1
 1 1 2
'''
num = 1
s2='''
+1 1 1
 1 1 1
 1 1 2
'''
assert_output(s1, num, s2)

s1='''
*1 1 1
 1 1 1
 1 1 1
'''
num = 1
s2='''
*1 1 1
 1 1 1
 1 1+1
'''
assert_output(s1, num, s2)

s1='''
*1 1 1

 1 1 1
'''
num = 3
s2='''
*1 1 1

+1+1+1
'''
assert_output(s1, num, s2)

s1='''
 1 2 1

 1 1 2
'''
num = 1
s2='''
 1 2 1

+1 1 2
'''
assert_output(s1, num, s2)

s1='''
 1 2
'''
num = 2
s2='''
 1+2
'''
num = 2
assert_output(s1, num, s2)


s1='''
 2 8

 2
'''
num = 4
s2='''
 2+8

 2
'''
assert_output(s1, num, s2)


s1='''
 2 3

 2 2 2
'''
num = 6
s2='''
 2 3

+2+2+2
'''
assert_output(s1, num, s2)


s1='''
 1 1 1 1 1 5

 1 1 1 1 1 5
'''
num = 10
s2='''
+1+1+1+1+1+5

 1 1 1 1 1 5
'''
assert_output(s1, num, s2)
