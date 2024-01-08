import math
import random



class Rock:
    """
    Represents a rock in the game.

    Attributes:
    - speed: Rock's speed
    - pos: Current position of the rock [x, y]
    - direction: Direction of the rock's movement [dx, dy]
    """

    def __init__(self, direction, pos):
        """
        Initializes a new Rock instance.

        Parameters:
        - direction: Initial direction of the rock's movement [dx, dy]
        - pos: Initial position of the rock [x, y] (default is [0, 0] if not provided)
        """
        self.speed = 0.1
        self.pos = pos if pos is not None else [0, 0]
        self.direction = direction

    def update_pos(self):
        """
        Updates the position of the rock based on its direction and speed.
        """
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

    def calculate_distance(self):
        """
        Calculates the distance traveled by the rock from the origin.

        Returns:
        - float: Distance traveled by the rock
        """
        return math.sqrt(self.pos[0]**2+self.pos[1]**2)

class Bullet:
    """
    Represents a bullet in the game.

    Attributes:
    - speed: Bullet's speed
    - pos: Current position of the bullet [x, y]
    - direction: Direction of the bullet's movement [dx, dy]
    """
    def __init__(self, direction, pos = None):
        """
        Initializes a new Bullet instance.

        Parameters:
        - direction: Initial direction of the bullet's movement [dx, dy]
        - pos: Initial position of the bullet [x, y] (default is [0, 0] if not provided)
        """
        self.speed = 1    
        self.pos = pos if pos is not None else [0, 0]
        self.direction = direction

    def update_pos(self):
        """
        Updates the position of the bullet based on its direction and speed.
        """
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

    def calculate_distance(self):
        """
        Calculates the distance traveled by the bullet from the origin.

        Returns:
        - float: Distance traveled by the bullet
        """
        return math.sqrt(self.pos[0]**2+self.pos[1]**2)
    
    def distance_to_rock(self, rock_position):
        """
        Calculates the distance between the bullet and a rock.

        Parameters:
        - rock_position: Position of the rock [x, y]

        Returns:
        - float: Distance between the bullet and the rock
        """
        return math.sqrt((self.pos[0]-rock_position[0])**2 + (self.pos[1]-rock_position[1])**2)
        


class GameArena:
    """
    Represents the game arena containing rocks and bullets.

    Attributes:
    - rocks: List of rocks in the arena
    - bullets: List of bullets in the arena
    - gameboard_width: Width of the game arena
    - gameboard_height: Height of the game arena
    """

    def __init__(self, width, height):
        """
        Initializes a new GameArena instance.

        Parameters:
        - width: Width of the game arena
        - height: Height of the game arena
        """
        self.rocks = []
        self.bullets = []
        self.gameboard_width = width
        self.gameboard_height = height


    def shoot(self, angle):
        """
        Creates a new bullet and adds it to the list of bullets.

        Parameters:
        - angle: Angle at which the bullet is shot (in degrees)
        """
        direction = [math.cos(angle*math.pi/180-math.pi/2), math.sin(angle*math.pi/180-math.pi/2)]
        self.bullets.append(Bullet(direction))

    def rock_attack(self):
        """
        Initiates a rock attack by creating a new rock with a random initial position and direction.
        """
        initial_pos = random.randrange(2*(self.gameboard_height+self.gameboard_width))
        angle = random.uniform(0, 2*math.pi)

        # Determine initial position and direction based on the random value
        if initial_pos < self.gameboard_width:
            initial_x = initial_pos
            initial_y = 0
            direction = [math.cos(angle), abs(math.sin(angle))]
        elif initial_pos < self.gameboard_height + self.gameboard_width:
            initial_x = self.gameboard_width
            initial_y = initial_pos-self.gameboard_width
            direction = [-abs(math.cos(angle)), abs(math.sin(angle))]
        elif initial_pos < 2*self.gameboard_width + self.gameboard_height:
            initial_x = initial_pos - (self.gameboard_height+self.gameboard_width)
            initial_y = self.gameboard_height
            direction = [math.cos(angle), -abs(math.sin(angle))]
        else:
            initial_x = 0
            initial_y = initial_pos -(2*self.gameboard_width+self.gameboard_height)
            direction = [abs(math.cos(angle)), math.sin(angle)]
        
        initial_x -= self.gameboard_width/2
        initial_y -= self.gameboard_height/2

        pos = [initial_x, initial_y]

        self.rocks.append(Rock(direction, pos))
    
    def check_death(self):
        """
        Checks if any rocks are close enough to the center to cause game over.

        Returns:
        - bool: True if the game should end, False otherwise
        """
        for rock in self.rocks:
            if math.sqrt(rock.pos[0]**2+rock.pos[1]**2) < 30:
                return True 
        else:
            return False

    def check_kill(self):
        """
        Checks for collisions between bullets and rocks. Removes bullets and rocks involved in collisions.
        """
        for i, bullet in reversed(list(enumerate(self.bullets))):
            for j, rock in reversed(list(enumerate(self.rocks))):
                if bullet.distance_to_rock(rock.pos) < 20:
                    self.bullets.pop(i)
                    self.rocks.pop(j)  

    def update_gameboard(self):
        """
        Updates the game arena by checking and handling collisions, and updating the positions of bullets and rocks.
        """
        self.check_kill()

        for i, bullet in reversed(list(enumerate(self.bullets))):

            if bullet.calculate_distance() > self.gameboard_width:
                self.bullets.pop(i)
            else:
                bullet.update_pos()
        
        for i, rock in reversed(list(enumerate(self.rocks))):
            if rock.calculate_distance() > 2*self.gameboard_width:
                self.rocks.pop(i)
            else:
                rock.update_pos()
        



        


       





