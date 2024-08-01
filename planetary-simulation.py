import pygame, math
pygame.init()


# Set up the display
WIDTH, HEIGHT = 1500, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
BRIGHT_BLUE = (0, 255, 255)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
FONT = pygame.font.SysFont("comicsans", 20)


class Planet:
    # Constants
    AU = 149.6e6 * 1000 # 1 Astronomical Unit (AU) is the average distance from the Earth to the Sun
    G = 6.67430e-11 # Gravitational constant
    SCALE = 250 / AU # Scale for the simulation, 1AU = 100 pixels
    # the smaller the scale, the bigger the planets and the closer they are to each other.
    TIMESTEP = 60 * 60 * 12 # half a day
    
    
    def __init__(self, name, x, y, radius, color1, color2, mass):
        # x, y: position of the planet
        self.x = x
        self.y = y
        self.name = name
        self.orbit = [] # list of points that the planet has orbited
        
        self.radius = radius
        self.color1 = color1
        self.color2 = color2
        self.mass = mass
        
        self.x_vel = 0
        self.y_vel = 0
        self.sun = False
        self.distance_to_sun = 0 # distance from the sun


    def draw(self, win):
        # 0 0 : top left
        # 800 0 : top right
           
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2:
            update_points = []
            for i, point in enumerate(self.orbit):
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                update_points.append((x, y))

            # draw the full orbit line
            
            # rainbow color
            for i in range(len(update_points) - 1):
                color = pygame.Color(0)
                color_duration = 500 # longer value for longer duration of each color.
                color.hsva = ((i * 360 / color_duration) % 360, 100, 100, 100)
                pygame.draw.line(win, color, update_points[i], update_points[i + 1], 1)       
        
            # normal color                                                
            # pygame.draw.lines(win, self.color1, False, update_points, 3)
            # pygame.draw.lines(win, self.color2, False, update_points, 1)

        # draw the planet        
        pygame.draw.circle(win, BLACK, (x, y), self.radius + 20)        
        pygame.draw.circle(win, self.color1, (x, y), self.radius)
        pygame.draw.circle(win, self.color2, (x, y), self.radius * 0.5)
        # display planet's name
        win.blit(FONT.render(self.name, 1, WHITE), (x + 20, y))
        win.blit(FONT.render(f'TIMESTEP : {str(self.TIMESTEP)} (12 hours)', 1, WHITE), (100, 100))


    def attraction(self, other):
        other_x, other_y = other.x, other.y
        # Calculate the distance between the two planets
        distance = math.sqrt((other_x - self.x) ** 2 + (other_y - self.y) ** 2)
        
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        # Calculate the angle of the force
        theta = math.atan2(other_y - self.y, other_x - self.x)
        # Calculate the force components in the x and y directions
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y


    def move(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet:
                continue
            force_x, force_y = self.attraction(planet)
            total_force_x += force_x
            total_force_y += force_y

        # Calculate the acceleration
        self.x_vel += total_force_x / self.mass * self.TIMESTEP
        self.y_vel += total_force_y / self.mass * self.TIMESTEP
        # Calculate the new position
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



def main():
    run = True
    clock = pygame.time.Clock()
    
    # planet sizes here are not correct because this is a fun, simple simulation.
    sun = Planet('Sun', 0, 0, 696340 * Planet.SCALE * 20000, YELLOW, YELLOW, 1.989e30)
    sun.sun = True
    earth = Planet('Earth', -1 * Planet.AU, 0, 6371 * Planet.SCALE * 1500000, BLUE, GREEN, 5.972e24)
    earth.y_vel = 29.783 * 1000
    mercury = Planet('Mercury', 0.39 * Planet.AU, 0, 2439 * Planet.SCALE * 1500000, BLUE, YELLOW, 3.285e23)
    mercury.y_vel = -47.87 * 1000
    mars = Planet('Mars', -1.524 * Planet.AU, 0, 3389 * Planet.SCALE * 1500000, ORANGE, YELLOW, 6.39e23)
    mars.y_vel = 24.077 * 1000
    venus = Planet('Venus', 0.72 * Planet.AU, 0, 6051 * Planet.SCALE * 1500000, RED, ORANGE, 4.867e24)
    venus.y_vel = -35.02 * 1000
    
    
    planets = [sun, earth, mercury, mars, venus]
    

    while run:
        clock.tick(60)
        win.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False    
        for planet in planets:
            planet.move(planets)
            planet.draw(win)
        pygame.display.update()            
                     
    pygame.quit()
    


main()
