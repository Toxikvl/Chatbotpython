import string, random

alphabet = string.ascii_letters + string.digits + string.punctuation


class GoodGenPassword:

    def __init__(self, length=10):
        self.length = length

    def generate(self):
        password = ''.join(random.choices(alphabet, k=self.length))
        return password


if __name__ == '__main__':
    gen = GoodGenPassword(10)
    print(gen.generate())
