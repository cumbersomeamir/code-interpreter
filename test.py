def print_primes_till_50():
    for num in range(2, 51):  # Numbers from 2 to 50
        prime = True
        for i in range(2, num):  # Check for factors of num
            if (num % i) == 0:
                prime = False
                break
        if prime:
            print(num)

# Execute the function to print prime numbers till 50
print_primes_till_50()
