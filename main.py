import pygame
pygame.init()

WIDTH, HEIGHT = 700,500 #by making the variables capital, I can make the variables constant.
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #This displays the window
pygame.display.set_caption("Pong game") #This sets the name of the window

WHITE = (255,255,255)
BLACK = (0,0,0)

FPS =60

PADDLE_WIDTH, PADDLE_HEIGHT = 20,100

BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WINNING_SCORE = 10

class Paddle:
    COLOR = WHITE
    VEL =4

    def __init__(self,x,y,width,height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self,win): #draws the paddle
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True): #movement of the paddle
        if up:
            self.y -= self.VEL  # when y goes down, the paddle moves up
        else:
            self.y += self.VEL # when y goes up, the paddle moves down

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self,x,y,radius) :
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel =0

    def draw(self,win): #draws the ball
        pygame.draw.circle(win,self.COLOR, (self.x,self.y),self.radius)

    def move(self): #moves the ball
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel =0
        self.x_vel *= -1

        

def draw(win,paddles, ball, left_score, right_score): #this draws the paddles,ball, scores
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text,(WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text,(WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20): #This draws the white dashes in the middle of the window. //20 means 20 dashes.
        if i % 2 == 1: #if i is an even number it skips the number. Otherwise, it draws the rectangular dash.
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 -5, i, 10, HEIGHT//20)) 

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:  #This if statement handles the collisions with the ceilings.
        ball.y_vel *= -1
    elif ball.y - ball.radius <=0:
        ball.y_vel *= -1

    if ball.x_vel <0: #This handles the collisions of the left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height: 
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2)/ ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    
def handle_paddle_movement(keys,left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y-left_paddle.VEL >=0: #If we press the 'w' key, it moves the paddle up.
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y+ left_paddle.VEL + left_paddle.height <= HEIGHT: #If we press the 's' key, it moves the paddle down
        # when moving down we need to add the y-coordinate and the height so that the paddle doesn't go all the way down.
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y-right_paddle.VEL >=0: #If we press the 'UP' key, it moves the paddle up
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y+ right_paddle.VEL + right_paddle.height <= HEIGHT: #If we press the 'DOWN' key, it moves the paddle down
        right_paddle.move(up=False)



def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH,PADDLE_HEIGHT)

    ball = Ball(WIDTH //2, HEIGHT //2, BALL_RADIUS)

    left_score = 0
    right_score =0

    while run:
        clock.tick(FPS) #This makes sure that the while loop runs 60 times per min

        draw(WIN, [left_paddle,right_paddle], ball, left_score, right_score) #draw the two paddles and also the ball

        for event in pygame.event.get(): #This loops through all the events occuring on your keyboard, like clicking the mouse, pressing up,etc
            if event.type ==pygame.QUIT: #This checks if we are quitting the game
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move() # this calls the move functions which moves the ball
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x<0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()


        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text,1,WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ =="__main__":
    main()