import sys
import functools

class Vector(tuple):
    def __new__(cls, x, y, z):
        return super().__new__(cls, (x, y, z))

    @functools.cached_property
    def x(self):
        return self[0]

    @functools.cached_property
    def y(self):
        return self[1]

    @functools.cached_property
    def z(self):
        return self[2]
    
    def dot(self, other):
        x = other.x * self.x
        y = other.y * self.y
        z = other.z * self.z
        return x + y + z
        
    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def __mul__(self, other):
        x = other * self.x
        y = other * self.y
        z = other * self.z
        return Vector(x, y, z)

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __floordiv__(self, other):
        x = self.x // other
        y = self.y // other
        z = self.z // other
        return Vector(x, y, z)
    
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

class Stone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
    
    def at(self, time):
        return self.position + self.velocity * time
    
    def __str__(self):
        return str((self.position, self.velocity))

if __name__ == "__main__":
    stones = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            position, velocity = line.rstrip().split(" @ ")
            position = Vector(*(int(n) for n in position.split(", ")))
            velocity = Vector(*(int(n) for n in velocity.split(", ")))
            stones.append(Stone(position, velocity))

    reference = stones[0]
    line = stones[1]
    x = line.position - reference.position
    v = line.velocity - reference.velocity
    normal = x.cross(v)
    #print(normal)

    collisions = []
    for stone in stones[2:4]:
        x = stone.position - reference.position
        v = stone.velocity - reference.velocity
        t = -normal.dot(x) // normal.dot(v)
        collisions.append((stone.at(t), t))
    
    v = (collisions[1][0] - collisions[0][0]) // (collisions[1][1] - collisions[0][1])
    x = collisions[0][0] - collisions[0][1] * v
    print(sum(x))
