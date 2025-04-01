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
