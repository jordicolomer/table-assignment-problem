# Table assigment problem
    The table assigment problem is the problem of assigning tables for a 
    number of people with the following desirable properties.
      - Avoid having unused seats in tables
      - If several tables are required, they should be near to each other
      - Select isolated tables
        (far from occupied tables, or big unoccupied tables)

    This greedy algorithm finds a solution in polynomial time O(n^3),
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
    t1 and t2 belong to different rooms,
    t1 or t2 have no coordinates).

    - The algorithm iteratively selects tables until there is no more people
      to be seated.
    - At each step the table with highest score is selected.
    - The score is computed as the sum of the score of each seat if the table is
      selected.
    - The score of each seat in the table is computed as the F-measure if the
      seat is occupied. The seat takes a negative constant value if it is not occupied.
