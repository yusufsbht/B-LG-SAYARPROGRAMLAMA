import pygame
import random
import sys
from pygame.locals import *

# pygame i başlat
pygame.init()

# renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# tetris renkleri
COLORS = [
    (0, 0, 0),       # Empty space
    (0, 255, 255),   # I - Cyan
    (0, 0, 255),     # J - Blue
    (255, 165, 0),   # L - Orange
    (255, 255, 0),   # O - Yellow
    (0, 255, 0),     # S - Green
    (128, 0, 128),   # T - Purple
    (255, 0, 0)      # Z - Red
]

# Tetris şekilleri (0 = boş, 1-7 = şekiller)
SHAPES = [
    # I
    [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]
    ],
    
    # J
    [
        [[2, 0, 0],
         [2, 2, 2],
         [0, 0, 0]],
        
        [[0, 2, 2],
         [0, 2, 0],
         [0, 2, 0]],
        
        [[0, 0, 0],
         [2, 2, 2],
         [0, 0, 2]],
        
        [[0, 2, 0],
         [0, 2, 0],
         [2, 2, 0]]
    ],
    
    # L
    [
        [[0, 0, 3],
         [3, 3, 3],
         [0, 0, 0]],
        
        [[0, 3, 0],
         [0, 3, 0],
         [0, 3, 3]],
        
        [[0, 0, 0],
         [3, 3, 3],
         [3, 0, 0]],
        
        [[3, 3, 0],
         [0, 3, 0],
         [0, 3, 0]]
    ],
    
    # O
    [
        [[0, 4, 4, 0],
         [0, 4, 4, 0],
         [0, 0, 0, 0]],
        
        [[0, 4, 4, 0],
         [0, 4, 4, 0],
         [0, 0, 0, 0]],
        
        [[0, 4, 4, 0],
         [0, 4, 4, 0],
         [0, 0, 0, 0]],
        
        [[0, 4, 4, 0],
         [0, 4, 4, 0],
         [0, 0, 0, 0]]
    ],
    
    # S
    [
        [[0, 5, 5],
         [5, 5, 0],
         [0, 0, 0]],
        
        [[0, 5, 0],
         [0, 5, 5],
         [0, 0, 5]],
        
        [[0, 0, 0],
         [0, 5, 5],
         [5, 5, 0]],
        
        [[5, 0, 0],
         [5, 5, 0],
         [0, 5, 0]]
    ],
    
    # T
    [
        [[0, 6, 0],
         [6, 6, 6],
         [0, 0, 0]],
        
        [[0, 6, 0],
         [0, 6, 6],
         [0, 6, 0]],
        
        [[0, 0, 0],
         [6, 6, 6],
         [0, 6, 0]],
        
        [[0, 6, 0],
         [6, 6, 0],
         [0, 6, 0]]
    ],
    
    # Z
    [
        [[7, 7, 0],
         [0, 7, 7],
         [0, 0, 0]],
        
        [[0, 0, 7],
         [0, 7, 7],
         [0, 7, 0]],
        
        [[0, 0, 0],
         [7, 7, 0],
         [0, 7, 7]],
        
        [[0, 7, 0],
         [7, 7, 0],
         [7, 0, 0]]
    ]
]

# oyun boyutları
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_BORDER_WIDTH = 4
PREVIEW_SIZE = 4

SCREEN_WIDTH = CELL_SIZE * (GRID_WIDTH + 8)  # ızgara + kenar çubuğu
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
GRID_OFFSET_X = CELL_SIZE * 2

# oyun hızı (ızgara hücresi başına düşen kare sayısı)
SPEEDS = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2]

# Ekranı başlat
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Font yükle
font_small = pygame.font.SysFont('arial', 18)
font_medium = pygame.font.SysFont('arial', 24)
font_large = pygame.font.SysFont('arial', 36)

class Tetris:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = SPEEDS[0]
        self.fall_counter = 0
        self.fast_drop = False

    def new_piece(self):
        # Returns a dictionary with piece information
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': shape_idx,
            'rotation': 0,
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0][0]) // 2,
            'y': 0
        }

    def get_piece_coords(self, piece=None):
        #Parça bloklarının koordinatlarını al
        if piece is None:
            piece = self.current_piece
        
        shape_matrix = SHAPES[piece['shape']][piece['rotation']]
        coords = []
        
        for y, row in enumerate(shape_matrix):
            for x, cell in enumerate(row):
                if cell:
                    coords.append((piece['x'] + x, piece['y'] + y))
        
        return coords

    def is_valid_position(self, piece=None):
        # Parçanın geçerli bir konumda olup olmadığını kontrol edin
        coords = self.get_piece_coords(piece)
        
        for x, y in coords:
            # Sınırların dışında olup olmadığını kontrol edin
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            
            # Mevcut bloklarla örtüşüp örtüşmediğini kontrol edin
            if y >= 0 and self.grid[y][x]:
                return False
        
        return True

    def rotate(self):
        # Parçayı döndür
        old_rotation = self.current_piece['rotation']
        self.current_piece['rotation'] = (self.current_piece['rotation'] + 1) % 4
        
        if not self.is_valid_position():
            # Duvar tekmelerini deneyin (döndürme çatışmaya neden olursa sola/sağa hareket edin)
            for offset in [1, -1, 2, -2]:
                self.current_piece['x'] += offset
                if self.is_valid_position():
                    return
                self.current_piece['x'] -= offset
            
            # Geçerli bir pozisyon bulunamazsa, rotasyonu geri alın
            self.current_piece['rotation'] = old_rotation

    def move_left(self):
        # Parçayı sola taşı
        self.current_piece['x'] -= 1
        if not self.is_valid_position():
            self.current_piece['x'] += 1

    def move_right(self):
        # Parçayı sağa taşı
        self.current_piece['x'] += 1
        if not self.is_valid_position():
            self.current_piece['x'] -= 1

    def move_down(self):
        # Parçayı aşağı taşı
        self.current_piece['y'] += 1
        
        if not self.is_valid_position():
            self.current_piece['y'] -= 1
            self.lock_piece()
            return False
        
        return True

    def drop(self):
        # Parçayı aşağıya bırak
        while self.move_down():
            pass
        
        # Sert düşüş için ödül puanları
        self.score += 2

    def lock_piece(self):
        #Mevcut parçayı yerinde kilitleyin
        for x, y in self.get_piece_coords():
            if y >= 0:  # Yalnızca şebekenin içindeyse kilitle
                self.grid[y][x] = self.current_piece['shape'] + 1
        
        # Tamamlanan satırları kontrol edin
        self.clear_lines()
        
        # Yeni parça al
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # Oyunun bitip bitmediğini kontrol edin
        if not self.is_valid_position():
            self.game_over = True

    def clear_lines(self):
        # Tamamlanmış satırları kontrol edin ve temizleyin
        lines_to_clear = []
        
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        # Puan, aynı anda temizlenen hat sayısına göre belirlenir
        num_lines = len(lines_to_clear)
        if num_lines > 0:
            # Puanlama: 1 satır için 100, 2 satır için 300, 3 satır için 500, 4 satır için 800 (Tetris)
            line_scores = [100, 300, 500, 800]
            self.score += line_scores[min(num_lines - 1, 3)] * self.level
            
            # Güncellenen satırlar temizlendi ve seviyelendirildi
            self.lines_cleared += num_lines
            self.level = min(self.lines_cleared // 10 + 1, 20)
            self.fall_speed = SPEEDS[min(self.level - 1, len(SPEEDS) - 1)]
            
            # Tamamlanan satırları kaldır
            for y in lines_to_clear:
                self.grid.pop(y)
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

    def update(self):
        # Oyunun durumunu güncelle
        if self.game_over:
            return
        
        # Düşen kolu
        self.fall_counter += 1
        fall_speed = 2 if self.fast_drop else self.fall_speed
        
        if self.fall_counter >= fall_speed:
            self.move_down()
            self.fall_counter = 0

    def draw_grid(self):
        # Arka planı ve ızgarayı çizin
        screen.fill(BLACK)
        
        # Izgara kenarlığını çiz
        border_rect = pygame.Rect(
            GRID_OFFSET_X - GRID_BORDER_WIDTH,
            0 - GRID_BORDER_WIDTH,
            GRID_WIDTH * CELL_SIZE + GRID_BORDER_WIDTH * 2,
            GRID_HEIGHT * CELL_SIZE + GRID_BORDER_WIDTH * 2
        )
        pygame.draw.rect(screen, WHITE, border_rect, GRID_BORDER_WIDTH)
        
        # Izgara hücrelerini çiz
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_value = self.grid[y][x]
                if cell_value:
                    pygame.draw.rect(
                        screen,
                        COLORS[cell_value],
                        (GRID_OFFSET_X + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                    pygame.draw.rect(
                        screen,
                        WHITE,
                        (GRID_OFFSET_X + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        1
                    )
                else:
                    #Boş hücreler için kılavuz çizgileri çizin
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        (GRID_OFFSET_X + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        1
                    )
        
        # Geçerli parçayı çiz
        if not self.game_over:
            for x, y in self.get_piece_coords():
                if y >= 0:  # Sadece ızgaranın içindeyse çiz
                    pygame.draw.rect(
                        screen,
                        COLORS[self.current_piece['shape'] + 1],
                        (GRID_OFFSET_X + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                    pygame.draw.rect(
                        screen,
                        WHITE,
                        (GRID_OFFSET_X + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        1
                    )
        
        #Parçanın nereye düşeceğinin önizlemesini çizin
        if not self.game_over:
            ghost_piece = self.current_piece.copy()
            while True:
                ghost_piece['y'] += 1
                if not self.is_valid_position(ghost_piece):
                    ghost_piece['y'] -= 1
                    break
            
            for x, y in self.get_piece_coords(ghost_piece):
                if y >= 0 and (x, y) not in self.get_piece_coords():  # Sadece ızgaranın içindeyse ve mevcut parçayla örtüşmüyorsa hayalet çiz
                    pygame.draw.rect(
                        screen,
                        (100, 100, 100),  # Hayalet parçası için daha koyu gölge
                        (GRID_OFFSET_X + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2  # Taslak olarak çiz
                    )

    def draw_sidebar(self):
        # Bir sonraki parçanın önizlemesi ve puanı ile kenar çubuğunu çizin
        sidebar_x = GRID_OFFSET_X + GRID_WIDTH * CELL_SIZE + 20
        
        # Sonraki parça kutusu
        pygame.draw.rect(screen, WHITE, (sidebar_x, 30, PREVIEW_SIZE * CELL_SIZE + 10, PREVIEW_SIZE * CELL_SIZE + 10), 2)
        
        #Sonraki parça etiketi
        next_text = font_medium.render("SIRADAKİ", True, WHITE)
        screen.blit(next_text, (sidebar_x + (PREVIEW_SIZE * CELL_SIZE - next_text.get_width()) // 2 + 5, 5))
        
        # Sonraki parçayı çiz
        shape_matrix = SHAPES[self.next_piece['shape']][self.next_piece['rotation']]
        for y, row in enumerate(shape_matrix):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        COLORS[self.next_piece['shape'] + 1],
                        (sidebar_x + 5 + x * CELL_SIZE, 35 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                    pygame.draw.rect(
                        screen,
                        WHITE,
                        (sidebar_x + 5 + x * CELL_SIZE, 35 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        1
                    )
        
        #puan
        score_y = 160
        score_text = font_medium.render("PUAN", True, WHITE)
        screen.blit(score_text, (sidebar_x, score_y))
        
        score_value = font_medium.render(str(self.score), True, WHITE)
        screen.blit(score_value, (sidebar_x, score_y + 30))
        
        # seviye
        level_y = 230
        level_text = font_medium.render("SEVİYE", True, WHITE)
        screen.blit(level_text, (sidebar_x, level_y))
        
        level_value = font_medium.render(str(self.level), True, WHITE)
        screen.blit(level_value, (sidebar_x, level_y + 30))
        
        # çizgiler
        lines_y = 300
        lines_text = font_medium.render("ÇİZGİLER", True, WHITE)
        screen.blit(lines_text, (sidebar_x, lines_y))
        
        lines_value = font_medium.render(str(self.lines_cleared), True, WHITE)
        screen.blit(lines_value, (sidebar_x, lines_y + 30))
        
        # kontroller
        controls_y = 380
        controls = [
            "KONTROLLER:",
            "← → : YÖNLER",
            "↑ : ÇEVİR",
            "↓ : YAVAŞ İNDİR",
            "SPACE : HIZLI BIRAK",
            "P : DURDUR",
            "R : TEKRAR BAŞLAT"
        ]
        
        for i, control in enumerate(controls):
            control_text = font_small.render(control, True, WHITE)
            screen.blit(control_text, (sidebar_x, controls_y + i * 25))

    def draw_game_over(self):
        # Oyunu ekranın üzerine çiz
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("KAYBETTİN", True, WHITE)
            screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 50))
            
            score_text = font_medium.render(f"OYUN PUANI: {self.score}", True, WHITE)
            screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, SCREEN_HEIGHT // 2))
            
            restart_text = font_medium.render("TEKRAR BAŞLAMAK İÇİN R YE BAS", True, WHITE)
            screen.blit(restart_text, ((SCREEN_WIDTH - restart_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 40))

    def draw(self):
        # Oyunu çiz
        self.draw_grid()
        self.draw_sidebar()
        self.draw_game_over()
        pygame.display.flip()

def main():
    # Ana oyun döngüsü
    game = Tetris()
    clock = pygame.time.Clock()
    paused = False
    
    # Anahtar tekrarlarını (hareket) işlemek için
    pygame.key.set_repeat(200, 100)  # Gecikme, milisaniye cinsinden aralık
    
    while True:
        #Olay yönetimi
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if game.game_over and event.key == K_r:
                    game.reset()
                elif not game.game_over and not paused:
                    if event.key == K_LEFT:
                        game.move_left()
                    elif event.key == K_RIGHT:
                        game.move_right()
                    elif event.key == K_UP:
                        game.rotate()
                    elif event.key == K_DOWN:
                        game.fast_drop = True
                    elif event.key == K_SPACE:
                        game.drop()
                
                if event.key == K_p:
                    paused = not paused
                elif event.key == K_r:
                    game.reset()
                    paused = False
            
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    game.fast_drop = False
        
        # Oyun mantığı
        if not paused and not game.game_over:
            game.update()
        
        # Çizim
        game.draw()
        
        # Duraklatma mesajını göster
        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            pause_text = font_large.render("OYUN DURDU", True, WHITE)
            screen.blit(pause_text, ((SCREEN_WIDTH - pause_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 20))
            
            pygame.display.flip()
        
        # Kare hızını sınırlayın
        clock.tick(60)

if __name__ == "__main__":
    main()