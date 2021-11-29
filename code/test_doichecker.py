from doichecker import doichecker
import timeit

test_n = 3000

def test_1():


    start = timeit.default_timer()
    doi_prefix = 'doi:'
    dchecker = doichecker()


    for i in range(test_n):
        doi_str = doi_prefix + str(i)
        print(doi_str, 'is a duplicate is', dchecker.duplicate(doi_str))

    print('pass #2')
    for i in range(test_n):
        doi_str = doi_prefix + str(i)
        print(doi_str, 'is a duplicate is', dchecker.duplicate(doi_str))

    stop = timeit.default_timer()
    print('Time: ', stop - start)

test_1()
