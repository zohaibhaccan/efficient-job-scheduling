import sys
import heapq
import time
import random

def generate_large_test_file(filename, num_jobs):
    with open(filename, 'w') as f:
        f.write(f"{num_jobs}\n")
        current_time = 0
        for _ in range(num_jobs):
            release_time = current_time
            processing_time = random.randint(1, 100)  # Adjust as needed
            f.write(f"{release_time} {processing_time}\n")
            current_time += random.randint(0, 10)

# Generate a test file with 1,000,000 jobs
generate_large_test_file('large_input.txt', 1000000)

def main():
    start_time = time.time()  # Start timing

    # Read and parse the input from standard input.
    try:
        data = sys.stdin.read().split()
        if not data:
            print("0")
            return

        n = int(data[0])
        if n <= 0:
            print("0")
            return
    except Exception as e:
        print("Invalid input format")
        return

    # Parse job data: each job is a tuple (release_time, processing_time)
    jobs = []
    index = 1
    for _ in range(n):
        try:
            r = int(data[index])
            p = int(data[index + 1])
        except Exception as e:
            print("Invalid input format")
            return
        jobs.append((r, p))
        index += 2

    # Sort jobs by their release times
    jobs.sort(key=lambda x: x[0])

    current_time = 0
    total_completion_time = 0
    heap = []
    i = 0  # pointer to jobs list

    # Process jobs until all are handled and the heap is empty
    while i < n or heap:
        # If no job is available to process, jump to the next job's release time.
        if not heap:
            current_time = max(current_time, jobs[i][0])
            while i < n and jobs[i][0] <= current_time:
                # Push tuple (remaining_processing_time, release_time) for comparison
                heapq.heappush(heap, (jobs[i][1], jobs[i][0]))
                i += 1

        # Get the job with the smallest remaining processing time
        proc_time, release_time = heapq.heappop(heap)

        # Check if a new job will arrive before finishing the current job
        if i < n and current_time + proc_time > jobs[i][0]:
            # Process partially until the next job arrives
            time_slice = jobs[i][0] - current_time
            proc_time -= time_slice
            current_time += time_slice
            # Put the partially processed job back if it still has remaining time
            heapq.heappush(heap, (proc_time, release_time))
            # Add all jobs that have now been released
            while i < n and jobs[i][0] <= current_time:
                heapq.heappush(heap, (jobs[i][1], jobs[i][0]))
                i += 1
        else:
            # Finish the job completely
            current_time += proc_time
            total_completion_time += current_time
            # Add any new jobs that have been released by now
            while i < n and jobs[i][0] <= current_time:
                heapq.heappush(heap, (jobs[i][1], jobs[i][0]))
                i += 1

    # Output the total completion time
    print(f"The total execution time is:", total_completion_time, "units" )

    end_time = time.time()  # End timing
    print(f"Execution time: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()
