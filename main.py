from dataclasses import dataclass
# 歩   10
# 香車 20
# 桂馬 30
# 銀  40
# 金  50
# 角  60
# 飛車70
# 王  80

board = [[ 20,  30,  40,  50,  80,  50,  40,  30,  20],
         [  0,  70,   0,   0,   0,   0,   0,  60,   0],
         [ 10,  10,  10,  10,  10,  10,  10,  10,  10], 
         [  0,   0,   0,   0,   0,   0,   0,   0,   0], 
         [  0,   0,   0,   0,   0,   0,   0,   0,   0], 
         [  0,   0,   0,   0,   0,   0,   0,   0,   0],
         [-10, -10, -10, -10, -10, -10, -10, -10, -10],
         [  0, -70,   0,   0,   0,   0,   0, -60,   0],
         [-20, -30, -40, -50, -80, -50, -40, -30, -20]]

capture_piece = [[],[]]

def print_board(board):                                                                      
    for i in range(9):                                                                       
        print()                                                                              
        for j in range(9):
            print(f"{board[i][j]:4d}", end="")
    print()

    print("capture_piece :")
    print("+", capture_piece[0])
    print("-", capture_piece[-1])

def check_range(li) -> bool:
    for i in li:
        if not (0 < i < 8): return True
    return False

def get_playerhand() -> list:
    while(True):
        print_board(board)
        #csa形式で受け取る
        hand = list(input())

        piece_x = int(hand[1]) - 1
        piece_y = int(hand[2]) - 1
        move_x = int(hand[3]) - 1
        move_y = int(hand[4]) - 1

        if check_range([piece_x, piece_y, move_x, move_y]) : continue
        piece = board[piece_y][piece_x]
        move = board[move_y][move_x]

        return [[[piece, [piece_x, piece_y]], [move, [move_x, move_y]]]]

    
def main():

    print_board(board)
    #csa形式で受け取る
    hand = list(input())

    piece = board[int(hand[2]) - 1][int(hand[1]) - 1]
    move = board[int(hand[4]) - 1][int(hand[3]) - 1]

    # 移動先に何の駒も無ければ、移動を承認する
    if move is 0  :
        board[int(hand[4]) - 1][int(hand[3]) - 1] = piece
        board[int(hand[2]) - 1][int(hand[1]) - 1] = 0


    #移動先の駒が自分と逆の符号なら、移動を承認し持ち駒にその駒を加える
    if move > 0:
        flag_a = piece > 0
        flag_b = move  > 0

        xor = flag_a ^ flag_b

        if xor:
            if flag_a:
                capture_piece[0].append(-move)
                board[int(hand[4]) - 1][int(hand[3]) - 1] = piece
                board[int(hand[2]) - 1][int(hand[1]) - 1] = 0
            else:
                capture_piece[-1].append(-move)
                board[int(hand[4]) - 1][int(hand[3]) - 1] = piece
                board[int(hand[2]) - 1][int(hand[1]) - 1] = 0

    print(piece)
    print(move)

    print_board(board)




class Shogi():
    class Board:
        board : list = [[ 20,  30,  40,  50,  80,  50,  40,  30,  20],
                        [  0,  70,   0,   0,   0,   0,   0,  60,   0],
                        [ 10,  10,  10,  10,  10,  10,  10,  10,  10], 
                        [  0,   0,   0,   0,   0,   0,   0,   0,   0], 
                        [  0,   0,   0,   0,   0,   0,   0,   0,   0], 
                        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                        [-10, -10, -10, -10, -10, -10, -10, -10, -10],
                        [  0, -70,   0,   0,   0,   0,   0, -60,   0],
                        [-20, -30, -40, -50, -80, -50, -40, -30, -20]]

        def update_board(self, shogi) -> bool:
            self.board[shogi.move.y][shogi.move.x] = self.board[shogi.piece.y][shogi.piece.x]
            self.board[shogi.piece.y][shogi.piece.x] = 0

            return True
        
        def get_piece(self, shogi) -> int:
            return self.board[shogi.piece.y][shogi.piece.x]
        
        def get_move(self, shogi) -> int:
            return self.board[shogi.move.y][shogi.move.x]

        def print_board(self, shogi):
            for i in range(9):
                print()
                for j in range(9):
                    print(f"{self.board[i][j]:4d}", end="")
            print()

            print("capture_piece :")
            print("+", shogi.capture_piece[0])
            print("-", shogi.capture_piece[-1])

    class Piece:
        x : int = 0
        y : int = 0

        def check_range(self, num : int) -> bool:
            if not (0 <= num <= 8) :  return False

            return True
        
        def set_position(self, position : list) -> bool:
            if not self.check_range(position[0]) : return False
            if not self.check_range(position[1]) : return False

            self.x = position[0]
            self.y = position[1]

            return True

    def __init__(self):
        self.board = Shogi.Board()
        self.capture_piece = [[], []]
        self.turn = 0

        self.piece = Shogi.Piece()
        self.move = Shogi.Piece()

    def make_hand(self, csa : str) -> bool:
        hand = list(csa)
        self.piece.x = int(hand[1]) - 1
        self.piece.y = int(hand[2]) - 1
        self.move.x = int(hand[3]) - 1
        self.move.y = int(hand[4]) - 1

        return False
    
    def get_dx(self) -> int:
        dx : int = self.move.x - self.piece.x

        return dx
    
    def get_dy(self) -> int:
        dy : int = self.move.y - self.piece.y

        return dy

    def get_side(self) -> int:
        return self.turn % 2 == 1
    
    def eliminate_choose_zero(self) -> bool:
        flag : bool = self.board.get_piece(self) == 0

        return True if flag else False
    
    def eliminate_same_owner(self) -> bool:
        if self.board.get_piece(self) > 0:
            if self.board.get_move(self) > 0:
                return True
        elif self.board.get_piece(self) < 0:
            if self.board.get_move(self) < 0:
                return True
        return False

    def eliminate_choose_wrong_piece(self) -> bool:
        piece_val = self.board.get_piece(self)
        if self.turn % 2 == 0:
            return piece_val <= 0
        else :
            return piece_val >= 0
    
    def movement_verification_fu(self) -> bool:
        if self.get_dx == 0 : return True
        if self.get_side():
            if self.get_dy() != 1 : return True
        else:
            if self.get_dy() != -1 : return True

        return False
    
    def movement_verification_kyosha(self) -> bool:
        return
    
    def movement_verifivation_keima(self) -> bool:
        return
    
    def movement_verification_gin(self) -> bool:
        return 
    
    def movement_verification_kin(self) -> bool:
        return 
    
    def movement_verification_kaku(self) -> bool:
        return
    
    def movement_verification_hisha(self) -> bool:
        return

    def movement_verification_ryu(self) -> bool:
        return

    def movement_verification_ma(self) -> bool:
        return 
    
    def movement_verification_ou(self) -> bool:
        return
    
    def movement_verification(self) -> bool:
        type_of_piece = abs(self.board.get_piece(self))
        match type_of_piece:
            case 10:
                self.movement_verification_fu()
            case 20:
                self.movement_verification_kyosha()
            case 30:
                self.movement_verifivation_keima()
            case 40:
                self.movement_verification_gin()
            case 11 | 21 | 31 | 41 | 50:
                self.movement_verification_kin()
            case 60:
                self.movement_verification_kaku()
            case 61:
                self.movement_verification_ma()
            case 70:
                self.movement_verification_hisha()
            case 71:
                self.movement_verification_ryu()
            case 80:
                self.movement_verification_ou()

    def get_playerhand(self):
        while(True):
            csa = list(input("your hand : "))
            if self.make_hand(csa) : continue
            if self.eliminate_choose_zero() : continue
            if self.eliminate_choose_wrong_piece() : continue
            if self.eliminate_same_owner() : continue

            break

    def main(self):
        while(True):
            print("turn : ", self.turn + 1)
            self.board.print_board(self)
            self.get_playerhand()
            self.board.update_board(self)
            self.turn += 1

if __name__ == "__main__":
    shogi = Shogi()
    shogi.main()