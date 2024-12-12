import pygame, sys, random  # Nhập các thư viện cần thiết: pygame, sys (quản lý hệ thống), random (tạo số ngẫu nhiên)

# KHOI TẠO CÁC HÀM
def draw_floor():  # Hàm vẽ 2 sân chạy
    screen.blit(floor, (floor_x_pos, 650))  # Vẽ sân đầu tiên
    screen.blit(floor, (floor_x_pos + 432, 650))  # Vẽ sân thứ hai để tạo hiệu ứng liên tục

def create_column():  # Hàm tạo cột ngẫu nhiên
    random_column_pos = random.choice(column_height)  # Chọn vị trí cột ngẫu nhiên từ danh sách
    bot_column = column_surface.get_rect(midtop=(500, random_column_pos))  # Cột dưới
    top_column = column_surface.get_rect(midtop=(500, random_column_pos - 750))  # Cột trên
    return bot_column, top_column  # Trả về cột dưới và cột trên

def draw_column(columns):  # Hàm vẽ cột
    for column in columns:  # Duyệt qua tất cả các cột
        if column.bottom >= 600:  # Nếu cột ở dưới màn hình
            screen.blit(column_surface, column)  # Vẽ cột bình thường
        else:  # Nếu cột ở trên màn hình
            flip_column = pygame.transform.flip(column_surface, False, True)  # Lật cột
            screen.blit(flip_column, column)  # Vẽ cột đã lật

def move_column(columns):  # Hàm di chuyển cột
    for column in columns:  # Duyệt qua tất cả các cột
        column.centerx -= 2  # Di chuyển cột sang trái
    return columns  # Trả về danh sách cột sau khi di chuyển

def check_collision(columns):  # Hàm kiểm tra va chạm
    for column in columns:  # Duyệt qua tất cả các cột
        if bird_rect.colliderect(column):  # Kiểm tra xem chim có va chạm với cột không
            hit_sound.play()  # Phát âm thanh va chạm
            return False  # Nếu có va chạm, trả về False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:  # Nếu chim ra khỏi màn hình
        hit_sound.play()  # Phát âm thanh va chạm
        return False  # Trả về False khi chim ra ngoài
    return True  # Nếu không có va chạm, trả về True

def rotate_bird(bird1):  # Hàm quay chim theo hướng rơi
    new_bird = pygame.transform.rotozoom(bird1, -brid_movement * 3, 1)  # Quay chim theo hướng rơi
    return new_bird  # Trả về chim đã quay

def bird_animation():  # Hàm thay đổi hình ảnh chim (đập cánh)
    new_bird = bird_list[bird_index]  # Lấy hình ảnh chim hiện tại
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))  # Đặt vị trí chim
    return new_bird, new_bird_rect  # Trả về hình ảnh chim và vị trí mới

def score_display(game_state):  # Hàm hiển thị điểm
    if game_state == 'main_game':  # Nếu đang chơi
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))  # Tạo bề mặt điểm
        score_rect = score_surface.get_rect(center=(100, 50))  # Đặt vị trí điểm
        screen.blit(score_surface, score_rect)  # Vẽ điểm lên màn hình
    if game_state == 'game_over':  # Nếu game over
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))  # Tạo bề mặt điểm
        score_rect = score_surface.get_rect(center=(216, 50))  # Đặt vị trí điểm
        screen.blit(score_surface, score_rect)  # Vẽ điểm lên màn hình

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))  # Tạo bề mặt điểm kỷ lục
        high_score_rect = high_score_surface.get_rect(center=(216, 90))  # Đặt vị trí điểm kỷ lục
        screen.blit(high_score_surface, high_score_rect)  # Vẽ điểm kỷ lục lên màn hình

def update_score(score, high_score):  # Hàm cập nhật điểm kỷ lục
    if score > high_score:  # Nếu điểm hiện tại cao hơn điểm kỷ lục
        high_score = score  # Cập nhật điểm kỷ lục
    return high_score  # Trả về điểm kỷ lục mới

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)  # Khởi tạo mixer âm thanh
pygame.init()  # Khởi tạo pygame
screen = pygame.display.set_mode((432, 768))  # Tạo cửa sổ game với kích thước 432x768
clock = pygame.time.Clock()  # Khởi tạo đồng hồ game
game_font = pygame.font.Font(r'F:\code_game\FlappyBird\sound&font\04B_19.TTF', 40)  # Tạo font hiển thị điểm

# KHOI TẠO CÁC BIẾN
gravity = 0.18  # Khai báo trọng lực
brid_movement = 0  # Khai báo chuyển động chim
game_active = False  # Trạng thái game không hoạt động
start_game = True  # Trạng thái màn hình bắt đầu
score = 0  # Khởi tạo điểm ban đầu
high_score = 0  # Khởi tạo điểm kỷ lục

# Khai báo background
bg = pygame.image.load('F:\code_game\FlappyBird\image\Background.png').convert()  # Tải hình nền
bg = pygame.transform.scale(bg, (432, 668))  # Thay đổi kích thước hình nền
bg_x_pos = 0  # Khởi tạo vị trí x cho background

# Khai báo sân
floor = pygame.image.load('F:\code_game\FlappyBird\image\Floor.png').convert()  # Tải hình sân
floor = pygame.transform.scale(floor, (432, 168))  # Thay đổi kích thước sân
floor_x_pos = 0  # Khởi tạo vị trí x cho sân

# Khai báo chim
bird_downn = pygame.image.load('F:\code_game\FlappyBird\image\Bird_down.png').convert_alpha()  # Chim khi rơi
bird_mid = pygame.image.load('F:\code_game\FlappyBird\image\Bird_mid.png').convert_alpha()  # Chim ở giữa
bird_up = pygame.image.load('F:\code_game\FlappyBird\image\Bird_up.png').convert_alpha()  # Chim khi bay lên
bird_list = [bird_downn, bird_mid, bird_up]  # Danh sách các hình ảnh chim
bird_index = 0  # Chim bắt đầu ở trạng thái đứng
bird = bird_list[bird_index]  # Chim hiện tại
bird_rect = bird.get_rect(center=(40, 30))  # Vị trí của chim

# Khai báo timer cho chim
bird_flap = pygame.USEREVENT + 1  # Sự kiện đập cánh của chim
pygame.time.set_timer(bird_flap, 200)  # Đặt timer cho chim đập cánh mỗi 500ms

# Khai báo cột
column_surface = pygame.image.load('F:\code_game\FlappyBird\image\Column.png').convert()  # Tải hình cột
column_surface = pygame.transform.scale(column_surface, (50, 600))  # Thay đổi kích thước cột
column_list = []  # Danh sách cột

# Khai báo timer cho cột
spawncolumn = pygame.USEREVENT  # Sự kiện sinh cột
pygame.time.set_timer(spawncolumn, 1500)  # Đặt timer sinh cột mỗi 1500ms
column_height = [600, 550, 500, 450, 400, 350, 300]  # Các chiều cao có thể của cột

# Khai báo màn hình vào game
new_game = pygame.image.load('F:\code_game\FlappyBird\image\message.png').convert_alpha()  # Màn hình bắt đầu
new_game_rect = new_game.get_rect(center=(216, 384))  # Vị trí của màn hình bắt đầu

# Khai báo màn hình game over
game_over = pygame.image.load('F:\code_game\FlappyBird\image\gameover.png').convert_alpha()  # Màn hình game over
game_over_rect = game_over.get_rect(center=(216, 384))  # Vị trí của màn hình game over

# Khai báo âm thanh
flap_sound = pygame.mixer.Sound('F:\code_game\FlappyBird\sound&font\sfx_wing.wav')  # Âm thanh đập cánh
hit_sound = pygame.mixer.Sound('F:\code_game\FlappyBird\sound&font\sfx_hit.wav')  # Âm thanh va chạm

while True:  # Vòng lặp game chính
    # Tạo cửa sổ game
    for event in pygame.event.get():  # Duyệt qua các sự kiện
        # Tạo nút thoát game
        if event.type == pygame.QUIT:  # Nếu người dùng thoát game
            pygame.quit()  # Thoát pygame
            sys.exit()  # Thoát chương trình
        # Tạo hiệu ứng chim bay lên khi nhấn space
        if event.type == pygame.KEYDOWN:  # Nếu người dùng nhấn phím
            if event.key == pygame.K_SPACE and start_game:  # Nếu phím là space và game bắt đầu
                start_game = False  # Chuyển sang trạng thái game đang chơi
                game_active = True  # Bắt đầu game
                column_list.clear()  # Xóa cột
                bird_rect.center = (100, 384)  # Đặt lại vị trí chim
                brid_movement = 0  # Reset chuyển động chim
                score = 0  # Reset điểm
            elif event.key == pygame.K_SPACE and game_active:  # Khi space và game đang chơi
                brid_movement = 0  # Reset chuyển động chim
                brid_movement = -5  # Chim bay lên
                flap_sound.play()  # Phát âm thanh đập cánh
            elif event.key == pygame.K_SPACE and not game_active:  # Khi space và game kết thúc
                game_active = True  # Bắt đầu game lại
                column_list.clear()  # Xóa cột
                bird_rect.center = (100, 384)  # Đặt lại vị trí chim
                brid_movement = 0  # Reset chuyển động chim
                score = 0  # Reset điểm
        # Tạo hiệu ứng spawn cột
        if event.type == spawncolumn:  # Khi timer sinh cột hết giờ
            column_list.extend(create_column())  # Thêm cột vào danh sách
        # Tạo hiệu ứng đập cánh
        if event.type == bird_flap:  # Khi timer đập cánh hết giờ
            if bird_index < 2:  # Nếu chưa đến cuối danh sách
                bird_index += 1  # Chuyển sang ảnh chim tiếp theo
            else:  # Nếu đến ảnh cuối
                bird_index = 0  # Quay lại ảnh đầu tiên
            bird, bird_rect = bird_animation()  # Cập nhật hình ảnh chim và vị trí

    # Hiển thị màn hình bắt đầu
    if start_game:  # Nếu game chưa bắt đầu
        screen.blit(bg, (0, 0))  # Vẽ background
        screen.blit(new_game, new_game_rect)  # Vẽ màn hình bắt đầu
    else:  # Nếu game đã bắt đầu
        # Cho background vào màn hình        
        screen.blit(bg, (0, 0))  # Vẽ background
        # Cho game active vào
        if game_active:  # Nếu game đang chơi
            brid_movement += gravity  # Thêm trọng lực vào chuyển động chim
            rotated_bird = rotate_bird(bird)  # Quay chim theo chuyển động
            bird_rect.centery += brid_movement  # Di chuyển chim theo trọng lực
            column_list = move_column(column_list)  # Di chuyển các cột
            draw_column(column_list)  # Vẽ các cột
            screen.blit(rotated_bird, bird_rect)  # Vẽ chim lên màn hình
            game_active = check_collision(column_list)  # Kiểm tra va chạm
            score += 0.5  # Cập nhật điểm
            score_display('main_game')  # Hiển thị điểm 
        else:
            screen.blit(game_over, game_over_rect)  # Vẽ màn hình game over
            high_score = update_score(score, high_score)  # Cập nhật điểm kỷ lục
            score_display('game_over')  # Hiển thị điểm khi game over

    # Cho sân vào màn hình
    floor_x_pos -= 1  # Di chuyển sân sang trái
    draw_floor()  # Vẽ sân
    if floor_x_pos <= -432:  # Nếu sân ra ngoài màn hình
       floor_x_pos = 0  # Đặt lại vị trí sân
    pygame.display.update()  # Cập nhật màn hình, vẽ lại mọi thay đổi (ví dụ: chim, cột, điểm) lên cửa sổ game.
    clock.tick(80)  # Điều khiển tốc độ của vòng lặp game, giới hạn tốc độ tối đa của vòng lặp là 80 FPS (frames per second).

