/*
 * fn_linear_conflicts.c                                                       #
 *                                                                             #
 * By - jacksonwb                                                              #
 * Created: Wednesday December 1969 4:00:00 pm                                 #
 * Modified: Monday Sep 2019 9:15:23 pm                                        #
 * Modified By: jacksonwb                                                      #
 */

#include <stdlib.h>

int find_number(const int * ar, int size, int num) {
	for (int i = 0; i < size * size; i++) {
		if (ar[i] == num)
			return i;
	}
	return -1;
}

int linearConflictDist(const int *st, const int *goal, int size){
    int total = 0;
    int n;
    int m;
    int n2;
    int m2;

    for (int i = 0; i < size * size; i++){
		n = find_number(goal, size, st[i]);
        total +=  (abs(i % size - n % size) + abs(i / size - n / size));
    }

    for (int i = 0; i < size; i++)
    	for (int j = 0; j < size - 1; j++)
    	{
			n = find_number(goal, size, st[i * size + j]);
			n2 = find_number(goal, size, st[j * size + i]);
    		for (int k = j + 1; k < size; k++)
    		{
    			if (n / size == i)
    			{
					m = find_number(goal, size, st[i * size + k]);
					if (m / size == i && n % size > m % size)
						total += 2;
				}
				if (n2 % size == i)
				{
					m2 = find_number(goal, size, st[k * size + i]);
					if (m2 % size == i && n2 / size > m2 / size)
						total += 2;
				}
    		}
    	}
    return total;
}