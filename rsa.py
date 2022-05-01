from pyexpat.errors import messages
import random
class KeyGeneration:
    def __init__(self) -> None:
        self.p_number = 11
        self.q_number = 173
        self.second_part_of_the_key = self.p_number * self.q_number
        self.lambda_n = (self.p_number - 1)* (self.q_number - 1)
        self.e_number = 17
        self.d_number = self.inverse_mod(self.e_number, self.lambda_n)
    def gcd(self, a, b):
        if a % b == 0:
            return b
        return self.gcd(b, a % b)
    def inverse_mod(self, a, m):
        '''
        Finds modular multiplicative inverse of a under modulo m
        '''
        for x in range(1, m):
            if (((a%m) * (x%m)) % m == 1):
                return x
    def key_generation(self, p, q):
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
        bit_power_len = len(bin(power)) - 2
        terms_mod = []
        terms_mod.append(number % mod)
        for i in range(bit_power_len + 1):
            terms_mod.append(terms_mod[-1] ** 2 % mod)

        output = 1
        for i in range(bit_power_len):
            if (1 << i) & power:
                output *= terms_mod[i]
                output = output % mod

        return output
    def encrypt(self):
        blocks= []
        for i in range(len(message)):
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
            letter_index = self.fast_modular_power(int(number), self.private[0], self.private[1])
            output += chr(letter_index)
        return output


if __name__ == "__main__":
    p, q = KeyGeneration().p_number, KeyGeneration().q_number
    keys = KeyGeneration().key_generation(p, q)
    public, private = keys['public'], keys['private']
    message = 'dfadsjkfna'
    encrypted = Encryption(message, public).encrypt()
    decrypted = Decryption(encrypted, private).decrypt()
    print(encrypted)
    print(decrypted)
