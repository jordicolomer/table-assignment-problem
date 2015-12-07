import math

def _get_table_suggestions(tables, num):
    '''
    The table assigment problem is the problem of assigning tables for a 
    number of people with the following desirable properties.
      - Avoid having unused seats in tables
      - If several tables are required, they should be near to each other
      - Select isolated tables
        (far from occupied tables, or big unoccupied tables)

    This greedy algorithm finds a solution in polinomial time O(n^3),
    where n is the number of tables.

    Intuitively, the algorithm tries to optimize the aggregate of utilities
    for each person.

    The utility of a person is defined based on the amount of sound that comes
    from seats who can be occupied by her friends (relevant elements) or not.
    We compute the precision (friends sound received over total sound received)
    and recall (friends sound received over total friends sound). The utility is
    the harmonic mean of the above quantities (F-measure). We consider that
    empty seats generate a fraction of the sound generated by an occupied seat,
    this favors choosing more isolated tables.

    The quantity of sound received from one person p1 sitting in table t1 by
    another person p2 sitting in table t2 depends on the distance between this
    two persons. The distance is computed as the Euclidean distance of t1 and t2
    The distance has constant values on the special cases
    (t1 equals t2,
    t1 and t2 belong in different rooms,
    t1 or t2 have no coordinates).

    - The algorithm iteratively selects tables until there is no more people
      to be seated.
    - At each step the table with highest score is selected.
    - The score is computed as the sum of the score of each seat if the table is
      selected.
    - The score of each seat in the table is computed as the F-measure if the
      seat is occupied. The seat takes a negative constant value if it is not occupied.
    '''
    # the utility of an empty seat in an occupied table
    empty_seat_utility = -0.5

    # fraction of noise that an empty seat generates
    # should aproximatelly the probability of the seat being occupied
    # in the near future
    empty_seat_noise_factor = 0.1

    # this simulates amplifying the sound of our friends
    # as we pay more attention to them
    friends_factor = 2

    # constants for special distances
    distance_same_table = 1
    distance_different_rooms = 100.
    distance_unassigned_table = 2.

    ret = []
    if num > sum([table.available for table in tables]):
        return None
    toseat = num
    while toseat > 0:
        maxtable = None
        maxutility = float('-inf')
        for table in tables:
            if table.available:
                friends_sound_received = 0
                total_sound_received = 0
                empty_seats = 0
                ppl1 = table.capacity
                if toseat < table.capacity:
                    ppl1 = toseat
                    empty_seats = table.capacity-toseat
                for table2 in tables:
                    if table.id == table2.id:
                        d = distance_same_table
                    elif table.roomid != table2.roomid:
                        d = distance_different_rooms
                    elif table.unassigned or table2.unassigned:
                        d = distance_unassigned_table
                    else:
                        d = math.sqrt(
                            math.pow(
                                table.table_location_horizontal -
                                table2.table_location_horizontal, 2) +
                            math.pow(table.table_location_vertical -
                                     table2.table_location_vertical, 2))
                    friends = False
                    if table.id == table2.id:
                        friends = True
                    else:
                        for r in ret:
                            if r.id == table2.id:
                                friends = True
                    ppl2 = table2.capacity
                    if table2.available:
                        ppl2 = table2.capacity*empty_seat_noise_factor
                    sound = ppl2/d
                    if friends:
                        sound = sound * friends_factor
                    total_sound_received += sound
                    if friends:
                        friends_sound_received += sound
                unseated_ppl = toseat - table.capacity
                if unseated_ppl < 0:
                    unseated_ppl = 0
                precision = friends_sound_received/total_sound_received
                recall = ppl1*friends_sound_received/num
                F = 2*precision*recall/(precision+recall)
                utility = ppl1*F + empty_seats*empty_seat_utility
                if utility > maxutility:
                    maxutility = utility
                    maxtable = table
        if maxtable:
            ret.append(maxtable)
            maxtable.available = 0
            toseat -= maxtable.capacity
    return ret
