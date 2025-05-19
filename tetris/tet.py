import pygame
import random
import os # Import os module for file path handling
import time # Import time module for getting real time for timer

# Define some colors using RGB tuples
colors = [
    (0, 0, 0),         # Black (Used for background, though screen is filled with WHITE)
    (120, 37, 179),    # Purple
    (100, 179, 179),   # Teal
    (80, 34, 22),      # Dark Brown
    (80, 134, 22),     # Olive Green
    (180, 34, 22),     # Red
    (180, 34, 122),    # Pink/Maroon
    (128, 128, 128)    # Gray (Added for grid outline - used in drawing)
]

# Define the path for the high score file
HIGH_SCORE_FILE = 'highscore.txt'

class Figure:
    """Đại diện cho một khối Tetris (Tetrimino)."""
    x = 0
    y = 0

    # Định nghĩa các hình dạng và trạng thái xoay của 7 khối Tetris.
    # Mỗi hình dạng được biểu diễn bằng danh sách các chỉ số trong lưới 4x4 (0-15).
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Hình chữ I
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Hình chữ Z
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # Hình chữ S
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # Hình chữ L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],# Hình chữ J
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # Hình chữ T
        [[1, 2, 5, 6]], # Hình chữ O
    ]

    def __init__(self, x, y):
        """
        Khởi tạo một đối tượng Figure mới.

        Args:
            x (int): Tọa độ x ban đầu (cột) của khối trên lưới trò chơi.
            y (int): Tọa độ y ban đầu (hàng) của khối trên lưới trò chơi.
        """
        self.x = x
        self.y = y
        # Chọn ngẫu nhiên một loại hình dạng khối
        self.type = random.randint(0, len(self.figures) - 1)
        # Chọn ngẫu nhiên một màu sắc (trừ chỉ số màu 0, là màu đen/nền)
        self.color = random.randint(1, len(colors) - 1)
        # Bắt đầu với trạng thái xoay đầu tiên
        self.rotation = 0

    def image(self):
        """
        Trả về hình dạng hiện tại (danh sách các chỉ số) của khối dựa trên trạng thái xoay.

        Returns:
            list: Danh sách các số nguyên biểu thị các ô được điền trong lưới 4x4
                  cho hình dạng và trạng thái xoay hiện tại.
        """
        return self.figures[self.type][self.rotation]

    def rotate(self):
        """
        Chuyển đổi trạng thái xoay của khối hiện tại.
        """
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    """Đại diện cho trạng thái và logic chính của trò chơi Tetris."""

    def __init__(self, height, width):
        """
        Khởi tạo bảng trò chơi Tetris và trạng thái ban đầu.

        Args:
            height (int): Số hàng của lưới trò chơi.
            width (int): Số cột của lưới trò chơi.
        """
        # Thông số bảng chơi
        self.height = height
        self.width = width
        self.field = [] # Danh sách 2 chiều biểu thị lưới trò chơi
        # Khởi tạo lưới với các ô trống (0)
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0) # 0 biểu thị ô trống
            self.field.append(new_line)

        # Thông số trạng thái trò chơi
        self.score = 0
        self.high_score = 0 # Biến lưu điểm cao nhất
        self.load_high_score() # Tải điểm cao nhất từ tệp khi khởi tạo
        self.state = "start" # Trạng thái trò chơi hiện tại (ví dụ: "start", "gameover")
        self.figure = None # Khối đang rơi hiện tại

        # Thông số bộ đếm thời gian (sử dụng mô-đun time để tính giây)
        self.start_time = time.time() # Ghi lại thời điểm bắt đầu trò chơi
        self.elapsed_time = 0 # Thời gian đã trôi qua kể từ khi bắt đầu

        # Thông số tốc độ
        # Tần suất rơi biểu thị số khung hình trôi qua giữa các lần rơi
        self.initial_drop_freq = 25 # Ví dụ: rơi mỗi 25 khung hình tại 25 fps = rơi mỗi giây
        self.min_drop_freq = 5     # Ví dụ: rơi mỗi 5 khung hình = rơi mỗi 0.2 giây (tốc độ tối đa)
        self.freq_decrease_rate = 1 # Giảm tần suất 1 khung hình mỗi khoảng
        self.speed_increase_interval_sec = 30 # Tăng tốc mỗi 30 giây
        self.current_drop_freq = self.initial_drop_freq # Tần suất rơi hiện tại

        # Thông số hiển thị
        self.x = 100  # Tọa độ x của góc trên bên trái lưới trên màn hình
        self.y = 60   # Tọa độ y của góc trên bên trái lưới trên màn hình
        self.zoom = 20 # Kích thước mỗi ô lưới tính bằng pixel

    def load_high_score(self):
        """Tải điểm cao nhất từ tệp."""
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as f:
                    content = f.read().strip()
                    if content.isdigit(): # Kiểm tra nếu nội dung là số hợp lệ
                        self.high_score = int(content)
                    else:
                         self.high_score = 0 # Mặc định là 0 nếu nội dung tệp không hợp lệ
            except IOError:
                self.high_score = 0 # Mặc định là 0 nếu không thể đọc tệp
        else:
            self.high_score = 0 # Mặc định là 0 nếu tệp không tồn tại

    def save_high_score(self):
        """Lưu điểm cao nhất hiện tại vào tệp."""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            print("Lỗi khi lưu điểm cao nhất.") # Tùy chọn: in thông báo lỗi

    def new_figure(self):
        """Tạo một khối mới ngẫu nhiên và đặt nó ở vị trí bắt đầu."""
        self.figure = Figure(self.width // 2 - 2, 0) # Bắt đầu gần giữa phía trên

    def intersects(self):
        """
        Kiểm tra xem khối hiện tại có va chạm với biên lưới hoặc các khối đã cố định.

        Returns:
            bool: True nếu có va chạm, False nếu không.
        """
        intersection = False
        # Duyệt qua lưới 4x4 của hình dạng khối hiện tại
        for i in range(4):
            for j in range(4):
                # Kiểm tra nếu ô (i, j) là một phần của hình dạng khối
                if i * 4 + j in self.figure.image():
                    # Tính tọa độ tuyệt đối trên lưới trò chơi
                    grid_y = i + self.figure.y
                    grid_x = j + self.figure.x

                    # Kiểm tra va chạm với biên (dưới, phải, trái)
                    # Cũng kiểm tra nếu grid_y âm (khối bắt đầu phía trên bảng)
                    if grid_y > self.height - 1 or grid_x > self.width - 1 or grid_x < 0 or grid_y < 0:
                        intersection = True
                        break # Không cần kiểm tra thêm nếu có va chạm biên

                    # Kiểm tra va chạm với các khối đã cố định trong lưới
                    # Đảm bảo grid_y trong phạm vi trước khi truy cập self.field
                    if grid_y >= 0 and self.field[grid_y][grid_x] > 0:
                         intersection = True
                         break # Không cần kiểm tra thêm nếu có va chạm khối

            if intersection:
                break # Không cần kiểm tra các hàng tiếp theo nếu đã có va chạm

        return intersection

    def break_lines(self):
        """
        Kiểm tra các hàng đầy, xóa chúng và cập nhật điểm số.
        """
        lines = 0 # Đếm số hàng được xóa trong bước này
        # Duyệt qua lưới từ dưới lên trên
        for i in range(self.height - 1, -1, -1):
            zeros = 0 # Đếm số ô trống trong hàng hiện tại
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            # Nếu hàng không có ô trống (đầy)
            if zeros == 0:
                lines += 1
                # Dịch tất cả các hàng phía trên xuống một hàng
                for i1 in range(i, 0, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
                # Xóa hàng trên cùng (đã được sao chép xuống)
                for j in range(self.width):
                     self.field[0][j] = 0

        # Cập nhật điểm số dựa trên số hàng xóa (lines^2)
        self.score += lines ** 2

    def go_space(self):
        """
        Thả khối hiện tại rơi thẳng xuống cho đến khi va chạm.
        """
        if self.state != "start": return # Chỉ cho phép hành động nếu trò chơi đã bắt đầu

        # Tiếp tục di chuyển khối xuống từng bước
        while not self.intersects():
            self.figure.y += 1
        # Khi va chạm, di chuyển khối lên lại một bước (vì bước cuối gây va chạm)
        self.figure.y -= 1
        # Cố định khối ở vị trí cuối cùng
        self.freeze()

    def go_down(self):
        """
        Di chuyển khối hiện tại xuống một hàng. Nếu va chạm sau khi di chuyển,
        di chuyển lại lên và cố định khối.
        """
        if self.state != "start": return # Chỉ cho phép hành động nếu trò chơi đã bắt đầu

        self.figure.y += 1
        # Kiểm tra va chạm sau khi di chuyển xuống
        if self.intersects():
            # Nếu va chạm, di chuyển lại lên
            self.figure.y -= 1
            # Cố định khối
            self.freeze()

    def freeze(self):
        """
        Cố định các ô của khối hiện tại vào lưới trò chơi,
        xóa các hàng đầy, tạo khối mới, và kiểm tra game over.
        """
        # Duyệt qua lưới 4x4 của hình dạng khối
        for i in range(4):
            for j in range(4):
                # Nếu ô (i, j) là một phần của hình dạng khối
                if i * 4 + j in self.figure.image():
                     # Đảm bảo tọa độ trong phạm vi lưới trước khi gán
                     grid_y = i + self.figure.y
                     grid_x = j + self.figure.x
                     if 0 <= grid_y < self.height and 0 <= grid_x < self.width:
                         self.field[grid_y][grid_x] = self.figure.color

        # Kiểm tra và xóa các hàng đầy
        self.break_lines()
        # Tạo khối mới
        self.new_figure()
        # Ngay sau khi tạo khối mới, kiểm tra xem nó có va chạm không
        # Điều này xác định xem trò chơi kết thúc (khối mới xuất hiện trong các khối hiện có)
        if self.intersects():
            self.state = "gameover"
            # Kiểm tra và lưu điểm cao nhất khi trò chơi kết thúc
            if self.score > self.high_score:
                 self.high_score = self.score
                 self.save_high_score()

    def go_side(self, dx):
        """
        Di chuyển khối hiện tại theo chiều ngang theo số cột dx.

        Args:
            dx (int): Số cột di chuyển (-1 sang trái, 1 sang phải).
        """
        if self.state != "start": return # Chỉ cho phép hành động nếu trò chơi đã bắt đầu

        old_x = self.figure.x # Lưu vị trí x ban đầu
        self.figure.x += dx   # Di chuyển khối theo chiều ngang
        # Kiểm tra xem di chuyển có dẫn đến va chạm không
        if self.intersects():
            self.figure.x = old_x # Nếu va chạm, quay lại vị trí cũ

    def rotate(self):
        """
        Cố gắng xoay khối hiện tại. Nếu xoay dẫn đến va chạm,
        trạng thái xoay sẽ được khôi phục.
        """
        if self.state != "start": return # Chỉ cho phép hành động nếu trò chơi đã bắt đầu

        old_rotation = self.figure.rotation # Lưu trạng thái xoay ban đầu
        self.figure.rotate()                # Thực hiện xoay
        # Kiểm tra xem xoay có dẫn đến va chạm không
        if self.intersects():
            self.figure.rotation = old_rotation # Nếu va chạm, quay lại trạng thái cũ

    def reset_game(self):
        """Đặt lại trạng thái trò chơi để bắt đầu trò chơi mới."""
        # Tạo đối tượng Tetris mới
        # Điều này khởi tạo lại mọi thứ bao gồm bảng, điểm số, trạng thái, bộ đếm thời gian, v.v.
        # Điểm cao nhất được tải lại trong __init__, nên nó được giữ nguyên.
        return Tetris(self.height, self.width)


# Initialize the game engine
pygame.init()

# Define some colors (already defined in colors list above, but keeping these standard ones too)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set the screen size
size = (400, 500)
screen = pygame.display.set_mode(size)

# Set the window title
pygame.display.set_caption("Tetris")

# --- Game Loop ---
done = False # Flag to control the game loop
clock = pygame.time.Clock() # Clock object to control frame rate
fps = 25 # Frames per second
game = Tetris(20, 10) # Create a Tetris game instance (20 rows, 10 columns)
counter = 0 # Counter for timing automatic descent (based on frames)

pressing_down = False # Flag to indicate if the down key is being held for soft drop

# Timer and speed update variables (using real time)
last_speed_update_time = time.time()


# The main game loop
while not done:
    # If there is no current falling figure, create a new one
    if game.figure is None:
        game.new_figure()

    # --- Game State Updates ---
    if game.state == "start":
        # Update counter (used for frame-based events like auto-drop)
        counter += 1
        if counter > 100000: # Prevent counter overflow
            counter = 0

        # Update elapsed time
        current_time = time.time()
        game.elapsed_time = current_time - game.start_time

        # Update speed based on elapsed time
        # Check if it's time to potentially decrease the drop frequency (increase speed)
        # The condition checks how many speed intervals have passed and ensures
        # we decrease the frequency by the rate for each full interval.
        # Using // for integer division to count full intervals passed
        intervals_passed = int(game.elapsed_time // game.speed_increase_interval_sec)
        target_freq_decrease = intervals_passed * game.freq_decrease_rate
        new_drop_freq = game.initial_drop_freq - target_freq_decrease
        game.current_drop_freq = max(game.min_drop_freq, new_drop_freq)


        # Handle automatic descent based on current drop frequency
        # Drop occurs when the frame counter is a multiple of the current drop frequency
        if counter % game.current_drop_freq == 0 or pressing_down:
             game.go_down()


    # --- Event Handling Loop ---
    for event in pygame.event.get():
        # Handle closing the window
        if event.type == pygame.QUIT:
            done = True
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            # Controls are only active if the game is in the "start" state
            if game.state == "start":
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True # Start soft drop
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space() # Hard drop
            # Handle ESC key to restart the game, regardless of state
            if event.key == pygame.K_ESCAPE:
                 # Reset the game by creating a new Tetris object
                 game = game.reset_game()
                 counter = 0 # Reset counter for the new game
                 pressing_down = False # Reset pressing_down flag


        # Handle key releases
        if event.type == pygame.KEYUP:
             if event.key == pygame.K_DOWN:
                 pressing_down = False # Stop soft drop

    # --- Drawing ---
    # Fill the background
    screen.fill(WHITE)

    # Draw the game grid and the fixed blocks
    for i in range(game.height):
        for j in range(game.width):
            # Draw the outline of each grid cell using GRAY
            pygame.draw.rect(screen, GRAY,
                             [game.x + game.zoom * j, game.y + game.zoom * i,
                              game.zoom, game.zoom], 1) # 1 is the line thickness

            # If a cell in the field is not empty (contains a block color)
            if game.field[i][j] > 0:
                # Draw the filled block (slightly smaller than the cell to create a border effect)
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1,
                                  game.zoom - 2, game.zoom - 2])


    # Draw the current falling figure if it exists
    if game.figure is not None:
        # Iterate through the 4x4 grid of the figure's image
        for i in range(4):
            for j in range(4):
                p = i * 4 + j # Calculate the index in the 4x4 grid
                # If the cell 'p' is part of the figure's current shape
                if p in game.figure.image():
                    # Calculate the absolute position on the screen
                    screen_x = game.x + game.zoom * (j + game.figure.x)
                    screen_y = game.y + game.zoom * (i + game.figure.y)

                    # Ensure we only draw if the figure block is within the visible grid area
                    if screen_y >= game.y:
                         # Draw the figure's block at the calculated screen position
                         pygame.draw.rect(screen, colors[game.figure.color],
                                          [screen_x + 1, screen_y + 1,
                                           game.zoom - 2, game.zoom - 2])

    # --- Drawing Text (Score, High Score, Timer, Game Over) ---
    # Initialize fonts (can be done once outside the loop for efficiency)
    # Using default system font 'Calibri'
    font = pygame.font.SysFont('Calibri', 25, True, False)
    font_large = pygame.font.SysFont('Calibri', 65, True, False)

    # Render Score text
    text_score = font.render("Score: " + str(game.score), True, BLACK)
    screen.blit(text_score, [0, 0]) # Position Score at top left

    # Render High Score text
    text_high_score = font.render("High Score: " + str(game.high_score), True, BLACK)
    screen.blit(text_high_score, [0, 30]) # Position High Score below Score

    # Render Timer text
    # Convert elapsed time from seconds float to MM:SS format
    minutes = int(game.elapsed_time // 60)
    seconds = int(game.elapsed_time % 60)
    timer_string = f"{minutes:02}:{seconds:02}"
    text_timer = font.render("Time: " + timer_string, True, BLACK)
    screen.blit(text_timer, [0, 60]) # Position Timer below High Score


    # If the game state is "gameover", draw the game over messages
    if game.state == "gameover":
        text_game_over = font_large.render("Game Over", True, (255, 125, 0)) # Orange color
        text_game_over1 = font_large.render("Press ESC", True, (255, 215, 0)) # Gold color
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    # --- Update Display ---
    pygame.display.flip() # Update the full screen to show what was drawn

    # --- Frame Rate Control ---
    clock.tick(fps) # Limit the game to the specified frames per second

# --- Quit Pygame ---
pygame.quit()