class FileWithPrimes:

    def __init__(self):
        self.files_content = self.gen_file_with_primes(10000000)

    def gen_file_with_primes(self, end):
        with open('prime_numbers.txt', 'w') as file:
            prime = [True for i in range(end + 1)]
            p = 2
            while p*p <= end:
                if prime[p] is True:
                    for i in range(p ** 2, end + 1, p):
                        prime[i] = False
                p += 1
            prime[0] = False
            prime[1] = False
            for p in range(end + 1):
                if prime[p]:
                    file.write(str(p)+'\n')
    
    def list_with_primes(self):
        with open('prime_numbers.txt', 'r') as file:
            files_content = file.read().split('\n')
        return files_content[:-1]
        