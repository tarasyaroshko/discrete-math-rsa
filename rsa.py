import random


class KeyGeneration:
    """
    Generating public and private key
    """

    def __init__(self) -> None:
        self.p_number, self.q_number = self.generate_p_and_q()
        self.second_part_of_the_key = self.p_number * self.q_number
        self.lambda_n = (self.p_number - 1) * (self.q_number - 1)
        self.e_number = self.calculate_second_half()
        self.d_number = self.extended_eucledian(self.e_number, self.lambda_n)

    def calculate_gcd(self, num1, num2):
        """
        Calculate gcd of two numbers
        """
        while num2:
            num1, num2 = num2, num1 % num2
        return num1

    def calculate_second_half(self):
        """
        Generate e_number for keys generation
        """
        for e in range(11, 1000, 2):
            gcd = self.calculate_gcd(self.lambda_n, e)
            if gcd == 1:
                return e

    def generate_p_and_q(self):
        """
        Generate p and q(prime numbers) from the txt file
        """
        with open("prime_numbers.txt", "r") as file:
            lines = file.read().split("\n")
            p = int(random.choice(lines))
            q = int(random.choice(lines))
            if p == q:
                q = int(random.choice(lines))
            return p, q

    def extended_eucledian(self, x, y):
        """
        Extended Euclidian algorithm for finding d_number
        """
        y_old = y
        secret_key = 1
        olds = 0
        oldoldt = 0
        oldt = 1
        while y != 0:
            q = x // y
            r = x % y
            x = y
            y = r
            s = secret_key - (q * olds)
            t = oldoldt - (q * oldt)
            secret_key = olds
            oldoldt = oldt
            olds = s
            if secret_key < 0:
                secret_key = secret_key + y_old
        return secret_key

    def key_generation(self):
        """
        Return dict with public and private keys
        """
        if self.d_number < 0:
            self.d_number += self.lambda_n
        return {
            "private": (self.d_number, self.second_part_of_the_key),
            "public": (self.e_number, self.second_part_of_the_key),
        }


class Encryption:
    """
    Class for message encryption
    """

    def __init__(self, message, public) -> None:
        self.message = message
        self.public = public

    def fast_modular_power(self, number, power, mod):
        """
        Efficiently getting the modular power of the number
        """
        r = 1
        if 1 & power:
            r = number
        while power:
            power >>= 1
            number = (number * number) % mod
            if power & 1:
                r = (r * number) % mod
        return r

    def encrypt(self):
        """
        Encrypting the message with blocks of numbers separated by space
        """
        blocks = []
        for i in range(len(self.message)):
            number = self.fast_modular_power(
                ord(self.message[i]), self.public[0], self.public[1]
            )
            blocks.append(str(number))
        return " ".join(blocks)


class Decryption:
    """
    Class for message decryption
    """

    def __init__(self, message, private) -> None:
        self.message = message
        self.private = private

    def fast_modular_power(self, number, power, mod):
        """
        Efficiently getting the modular power of the number
        """
        r = 1
        if 1 & power:
            r = number
        while power:
            power >>= 1
            number = (number * number) % mod
            if power & 1:
                r = (r * number) % mod
        return r

    def decrypt(self):
        """
        Decrypting the string of numbers separated by space
        """
        message = self.message.split(" ")
        output = ""
        for number in message:
            index = self.fast_modular_power(
                int(number), self.private[0], self.private[1]
            )
            output += chr(index)
        return output


if __name__ == "__main__":
    p, q = KeyGeneration().p_number, KeyGeneration().q_number
    keys = KeyGeneration().key_generation()
    public, private = keys["public"], keys["private"]
    message = "прфпрфд fiwughiuebiu^&$@(*@"
    encrypted = Encryption(message, public).encrypt()
    decrypted = Decryption(encrypted, private).decrypt()
    print(encrypted)
    print(decrypted)
