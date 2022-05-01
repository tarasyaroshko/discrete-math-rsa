from random import randint

class KeyGeneration:

    with open('prime_numbers.txt') as file:
        files_content = file.read().split('\n')
    prime_numbers = files_content[:-1]
        
    def __init__(self):

        self.primes = self.get_two_random_primes()
        self.first_half = self.calculate_first_half()
        self.e_number = self.calculate_second_half()
        self.secret_key = self.extended_eucledian()


    def get_two_random_primes(self):

        ind1, ind2 = randint(10000, 664575), randint(10000, 664575)
        return int(KeyGeneration.prime_numbers[ind1]), int(KeyGeneration.prime_numbers[ind2])


    def calculate_first_half(self):
        first_half = self.primes[0] * self.primes[1]
        self.first_half = first_half
        return first_half

    def calculate_gcd(self, num1, num2):
        while(num2):
            num1, num2 = num2, num1%num2
        return num1

    def calculate_second_half(self):
        num = (self.primes[0]-1)*(self.primes[1]-1)
        for e in range(11, 1000, 2):
            gcd = self.calculate_gcd(num, e)
            if gcd == 1:
                return e
                break

    def extended_eucledian(self):
        x = self.e_number
        y = (self.primes[0]-1)*(self.primes[1]-1)
        y_old = y
        secret_key = 1
        olds = 0
        oldoldt = 0
        oldt = 1
        while y != 0:
            q = x//y
            r = x%y
            x = y
            y = r
            s = secret_key - (q*olds)
            t = oldoldt - (q*oldt)
            secret_key = olds
            oldoldt = oldt
            olds = s
            oldt = t
        if secret_key < 0:
            secret_key = secret_key + y_old
        return secret_key
