import random

class KeyGeneration:
    def __init__(self) -> None:
        self.p_number, self.q_number = self.generate_p_and_q()
        self.second_part_of_the_key = self.p_number * self.q_number
        self.lambda_n = (self.p_number - 1)* (self.q_number - 1)
        self.e_number = self.calculate_second_half()
        self.d_number = self.extended_eucledian(self.e_number, self.lambda_n)
    def calculate_gcd(self, num1, num2):
        while(num2):
            num1, num2 = num2, num1%num2
        return num1
    def calculate_second_half(self):
        for e in range(11, 1000, 2):
            gcd = self.calculate_gcd(self.lambda_n, e)
            if gcd == 1:
                return e
    def generate_p_and_q(self):
        with open('prime_numbers.txt', 'r') as file:
            lines = file.read().split("\n")
            p = int(random.choice(lines))
            q = int(random.choice(lines))
            if p == q:
                q = int(random.choice(lines))
            return p,q
    def gcd(self, a, b):
        if a % b == 0:
            return b
        return self.gcd(b, a % b)
    def extended_eucledian(self, x, y):
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
            if secret_key < 0:
                secret_key = secret_key + y_old
        return secret_key
    def key_generation(self):
        if self.d_number < 0:
            self.d_number += self.lambda_n
        return {'private': (self.d_number, self.second_part_of_the_key), 'public': (self.e_number, self.second_part_of_the_key)}
    def fast_modular_power(self, number, power, mod):
        r = 1
        if 1 & power:
            r = number
        while power:
            power >>= 1
            number = (number * number) % mod
            if power & 1: r = (r * number) % mod
        return r





class Encryption:
    def __init__(self, message, public) -> None:
        self.message = message
        self.public = public
    def fast_modular_power(self, number, power, mod):
        r = 1
        if 1 & power:
            r = number
        while power:
            power >>= 1
            number = (number * number) % mod
            if power & 1: r = (r * number) % mod
        return r
    def encrypt(self):
        blocks = []
        for i in range(len(self.message)):
            number = self.fast_modular_power(ord(self.message[i]), self.public[0], self.public[1])
            blocks.append(str(number))
        return " ".join(blocks)





class Decryption:
    def __init__(self, message, private) -> None:
        self.message = message
        self.private = private
    def fast_modular_power(self, number, power, mod):
        r = 1
        if 1 & power:
            r = number
        while power:
            power >>= 1
            number = (number * number) % mod
            if power & 1: r = (r * number) % mod
        return r
    def decrypt(self):
        message = self.message.split(' ')
        output = ""
        for number in message:
            index = self.fast_modular_power(int(number), self.private[0], self.private[1])
            output += chr(index)
        return output


if __name__ == "__main__":
    p, q = KeyGeneration().p_number, KeyGeneration().q_number
    keys = KeyGeneration().key_generation()
    public, private = keys['public'], keys['private']
    message = 'прфпрфд fiwughiuebiu^&$@(*@'
    encrypted = Encryption(message, public).encrypt()
    decrypted = Decryption(encrypted, private).decrypt()
    print(encrypted)
    print(decrypted)
