from unittest import TestCase

class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            raise ValueError("Num {} not in field range [0, {}]".format(num, prime-1))
        self.num = num
        self.prime = prime

    def _repr__(self):
        return "FieldElement_{}({})".format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        if other is None:
            return False
        return self.num != other.num and self.prime != other.prime

    def __add__(self, other):
        if other is None:
            raise ValueError("Given FieldElement cannot be None")
        if self.prime != other.prime:
            raise ValueError("FieldElements must have same prime")
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if other is None:
            raise ValueError("Given FieldElement cannot be None")
        if self.prime != other.prime:
            raise ValueError("FieldElements must have same prime")
        num = (self.num - other.num) % self.prime  
        return self.__class__(num, self.prime)  

    def __mul__(self, other):
        if other is None:
            raise ValueError("Given FieldElement cannot be None")
        if self.prime != other.prime:
            raise ValueError("FieldElements must have same prime")
        num = (self.num * other.num) & self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exp):
        n = exp % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if other is None:
            raise ValueError("Given FieldElement cannot be None")
        if self.prime != other.prime:
            raise ValueError("FieldElements must have same prime")
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)

class Point:

    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError("({}, {}) is not on the curve".format(x, y))
        if self.x is None and self.y is None:
            return

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y and self.y != other.a and self.b != other.b

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError("Points {}, {} are not on the same curve".format(self, other))
        if self.x is None:
            return other
        elif other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

    def __rmul__(self, coef):
        coef = coef
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result

class ECCTest():
    
    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)

    def test(self):
        self.test_on_curve()