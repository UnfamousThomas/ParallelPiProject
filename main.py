import multiprocessing
import math
import time


def leibniz_term(start, end):
    # Calculates the term from start to end
    # Uses the leibiniz formula for partial sum
    # Meaning that basically it first checks if it should be a negative or positive using (-1) to the power of index, meaning the sign is alternated
    # Then it creates the appropriate denominator, by doubling the index and adding 1. For example:
    # i= 0 then (-1)**0 = 1 2*0+1 = 1 1/1=1
    # i = 1 then (-1)**1 = -1 2*1+1=2+1 = 3 so the total is 1/3
    # It then adds up all of them to the partial sum, which the process eventually returns
    partial_sum = 0.0
    for i in range(start, end):
        term = (-1) ** i / (2 * i + 1)
        partial_sum += term
    return partial_sum


def calculate_pi(terms, processes):
    # This method handles calling the processes. It first divides them into chunks. Meaning how many terms per process
    # It then pools the processes
    chunk_size = math.ceil(terms / processes)
    pool = multiprocessing.Pool(processes=processes)

    #Here the logic for creation of the tasks is made. Each task contains of a starting index and ending index.
    tasks = []
    for i in range(processes):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, terms)
        tasks.append((start, end))

    # Then a results object is created, which is an array of integers eventually
    # Starmap is a pool method for functions that take multiple arguments, in our case start and end
    # Simply put, we tell the pool to create the amount of processes equal to amount of tasks
    # Where each process runs the leibniz_term with the arguments given to it
    results = pool.starmap(leibniz_term, tasks)
    # Denotes that no more tasks will be joining the pool
    pool.close()
    # Wait for all processes to finish in the pool
    pool.join()

    # Approximation is pi/4, so times it with 4 and sum the results
    pi_approximation = 4 * sum(results)

    # Return the approximate
    return pi_approximation

if __name__ == "__main__":
    # How many terms to calculate
    num_terms = int(input("Enter number of terms to calculate: "))
    # How many processes to use, this could probably be improved a lot, but a basic decision on how many processes to use:
    # Basically tries to allocate 1000 term calculations to each process, if more than 100, caps there.
    num_processes = min(math.ceil(num_terms / 1000), 100)
    start_time = time.time()  # Record the start time
    pi_value = calculate_pi(num_terms, num_processes)
    end_time = time.time()  # Record the end time

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Pi approximation took {elapsed_time:.6f} seconds to complete using {num_processes} processes.")
    print(f"Approximation of π using {num_terms} terms: {pi_value}")
