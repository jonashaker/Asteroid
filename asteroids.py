import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QStatusBar, QTextEdit, QFileDialog,
                             QLabel, QWidget, QHBoxLayout, QPushButton, QLineEdit,
                             QRadioButton, QGridLayout, QFormLayout, QAction, QVBoxLayout)
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QKeyEvent, QPalette, QColor, QPainter, QPolygonF, QTransform
import math
import gameboard

class Asteroids(QWidget):
    """
    Main class representing the Asteroids game window.

    Attributes:
    - frame_height: Height of the game window
    - frame_width: Width of the game window
    - game_running: Flag indicating whether the game is currently running
    - triangle_pos: Position of the player's triangle [x, y]
    - triangle_size: Size of the player's triangle
    - rotation_angle: Current rotation angle of the player's triangle
    - bullet_radius: Radius of bullets
    - rock_radius: Radius of rocks
    - gameboard: Instance of the Gameboard class for managing game entities
    - timer: QTimer for updating the game
    - create_rock_timer: QTimer for creating rocks at regular intervals
    - start_button: QPushButton to start or restart the game
    - game_over_label: QLabel for displaying "Game Over" message
    """
    def __init__(self):
        """
        Initializes a new instance of the Asteroids class.
        """
        super().__init__()

        # Define constants for frame dimensions
        self.frame_height = 600
        self.frame_width = 1000

        # Flag to track whether game is running
        self.game_running = False

        # Initialize UI components
        self.init_ui()


    def init_ui(self):
        """
        Initializes the user interface components.
        """

        # Set window dimensions, title and background color of the window.
        self.setGeometry(750-int(self.frame_width/2), 450-int(self.frame_height/2), self.frame_width, self.frame_height)
        self.setWindowTitle("Asteroid")
        self.setBackgroundColor(QColor(100, 200, 200))

        # Create start button and game over label
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_game)

        self.game_over_label = QLabel("Game Over", self)
        self.game_over_label.setStyleSheet("QLabel { font-size: 24px; color: red; }")
        self.game_over_label.hide()
        
        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.game_over_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        layout.addWidget(self)

        self.setLayout(layout)


    def start_game(self):
        """
        Starts or restarts the game.
        """


        # Hide start button and game over label
        self.start_button.hide()
        self.game_over_label.hide()


        # Initialize game variables
        self.triangle_pos = [self.frame_width/2, self.frame_height/2]
        self.triangle_size = 20
        self.rotation_angle = 0.0
        self.bullet_radius = 5
        self.rock_radius = 20
        self.rock_release_interval = 500

        # Initialize gameboard instance
        self.gameboard = gameboard.GameArena(self.frame_width, self.frame_height)

        # Set game running flag to True
        self.game_running = True

        # Start timers for game update and rock creation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
    
        self.create_rock_timer = QTimer(self)
        self.create_rock_timer.timeout.connect(self.rock_attack)

        self.timer.start()
        self.create_rock_timer.start(self.rock_release_interval)
        
    def end_game(self):
        """
        Ends the game and shows the game over message.
        """

        # Show start button and game over label, stop timers.
        self.start_button.show()
        self.game_over_label.show()

        self.timer.stop()
        self.create_rock_timer.stop()
    
    def rock_attack(self):
        """
        Initiates a rock attack.
        """
        self.gameboard.rock_attack()

    def update_game(self):
        """
        Updates the game state and triggers repaint.
        """
        if self.gameboard.check_death():
            self.game_running = False
            self.end_game()

        self.gameboard.update_gameboard()
        self.update()

    def draw_rocks(self, painter):
        """
        Draws rocks on the screen.

        Parameters:
        - painter: QPainter object for drawing
        """
        painter.setBrush(QColor(0, 0, 200))  # Blue color

        for rock in self.gameboard.rocks:
            
            rock_circle = QRectF(QPointF(rock.pos[0]-self.rock_radius, rock.pos[1]-self.rock_radius), 
                                    QPointF(rock.pos[0]+self.rock_radius, rock.pos[1]+self.rock_radius))
            rock_circle.translate(self.triangle_pos[0], self.triangle_pos[1])
            painter.drawEllipse(rock_circle)

    def draw_shooter(self, painter):
        """
        Draws the player's triangle (shooter) on the screen.

        Parameters:
        - painter: QPainter object for drawing
        """
        triangle = QPolygonF([
            QPointF(0, -self.triangle_size),
            QPointF(self.triangle_size/1.5*math.cos(7*math.pi/6), -self.triangle_size/1.5*math.sin(7*math.pi/6)),
            QPointF(self.triangle_size/1.5*math.cos(11*math.pi/6), -self.triangle_size/1.5*math.sin(11*math.pi/6))
        ])
        # Draw the triangle 
        rotation_matrix = QTransform()
        rotation_matrix.translate(self.triangle_pos[0], self.triangle_pos[1])

        rotation_matrix.rotate(self.rotation_angle)

        rotated_triangle = rotation_matrix.map(triangle)
        
        painter.setBrush(QColor(255, 0, 0))  # Red color
        painter.drawPolygon(rotated_triangle)

    def draw_bullets(self, painter):
        """
        Draws bullets on the screen.

        Parameters:
        - painter: QPainter object for drawing
        """
    
        painter.setBrush(QColor(0, 0, 255))  # Blue color
        
        for bullet in self.gameboard.bullets:
            
            bullet_circle = QRectF(QPointF(bullet.pos[0]-self.bullet_radius, bullet.pos[1]-self.bullet_radius), 
                                    QPointF(bullet.pos[0]+self.bullet_radius, bullet.pos[1]+self.bullet_radius))
            
            bullet_circle.translate(self.triangle_pos[0], self.triangle_pos[1])
            
            painter.drawEllipse(bullet_circle)

    def setBackgroundColor(self, color):
        """
        Sets the background color of the game window.

        Parameters:
        - color: QColor object representing the background color
        """
        palette = self.palette()
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)


    def paintEvent(self, event):
        """
        Paint event handler. Called whenever the window needs to be repainted 
        """
        if self.game_running is True:
            painter = QPainter(self)
            self.draw_shooter(painter)
            self.draw_bullets(painter)
            self.draw_rocks(painter)
        
    def keyPressEvent(self, event):
        """
        Handle key presses for movement and shooting
        """
        turn = 10

        if event.key() == Qt.Key_Left:
            self.rotation_angle -= turn
        elif event.key() == Qt.Key_Right:
            self.rotation_angle += turn
        elif event.key() == Qt.Key_Space:
            self.gameboard.shoot(self.rotation_angle)
        
        self.rotation_angle % 360

        self.update()



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    asteroid = Asteroids()

    asteroid.show()

    sys.exit(app.exec_())

