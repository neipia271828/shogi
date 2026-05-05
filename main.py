from dataclasses import dataclass
import math

# 歩   10 FU
# と   11 TO
# 香車 20 KY
# 成香 21 NY
# 桂馬 30 KE
# 成佳 31 NK
# 銀  40 GI
# 成銀41 NG
# 金  50
# 角  60
# 馬  61 UM
# 飛車70 HI
# 竜  71 RY
# 王  80 OU
class Shogi():
    class Board:
        board : list = [[ 20,  30,  40,  50,  80,  50,  40,  30,  20],
                        [  0,  70,   0,   0,   0,   0,   0,  60,   0],
                        [ 10,  10,  10,  10,  10,  10,  10,  10,  10], 
                        [  0,   0,   0,   0,   0,   0,   0,   0,   0], 
                        [  0,   0,   0,   0,   0,   0,   0,   0,   0], 
                        [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                        [-10, -10, -10, -10, -10, -10, -10, -10, -10],
                        [  0, -60,   0,   0,   0,   0,   0, -70,   0],
                        [-20, -30, -40, -50, -80, -50, -40, -30, -20]]

        def update_board(self, shogi : Shogi) -> bool:
            self.board[shogi.destination_cell.y][shogi.destination_cell.x] = self.board[shogi.start_cell.y][shogi.start_cell.x]
            self.board[shogi.start_cell.y][shogi.start_cell.x] = 0

            return True
        
        def get_piece_from_start_cell(self, shogi : Shogi) -> int:
            return self.board[shogi.start_cell.y][shogi.start_cell.x]
        
        def get_piece_from_destination_cell(self, shogi) -> int:
            return self.board[shogi.destination_cell.y][shogi.destination_cell.x]

        def get_piece_from_any_cell(self, x : int, y : int) -> int:
            return self.board[y][x]

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
        symbol : int = 0

        def check_range(self, num : int) -> bool:
            if not (0 <= num <= 8) :  return False

            return True
        
        def set_position(self, position : list) -> bool:
            if not self.check_range(position[0]) : return False
            if not self.check_range(position[1]) : return False

            self.x = position[0]
            self.y = position[1]
            self.symbol = position[2]

            return True

    class MoveVerificator():
        def __init__(self, 
                     need_slide_move_verification : bool,
                     need_straight_move_verification : bool,
                     need_L_move_verification : bool,
                     slide_list : list, 
                     straight_list : list):
            self.slide = slide_list
            self.straight = straight_list

            self.verificator = []
            if need_straight_move_verification : self.verificator.append(self.verification_straight_move) 
            if need_slide_move_verification    : self.verificator.append(self.verification_slide_move) 
            if need_L_move_verification        : self.verificator.append(self.verification_L_move) 

        def get_effective_slide(self, shogi) -> list:                                          
            if shogi.get_side():  # 先手                                                       
                return self.slide[::-1]  # 行を逆順に
            return self.slide                                                        
        
        def get_effective_straight(self, shogi) -> list:                                       
            if shogi.get_side():
                return self.straight[::-1]                                                     
            return self.straight
        
        def verification_slide_move(self, shogi : Shogi) -> bool:
            slide = self.get_effective_slide(shogi)
            x = 1 + shogi.get_dx_as_3bit()
            y = 1 + shogi.get_dy_as_3bit()
            
            if not slide[y][x]: return True

            return False
        
        def verification_straight(self, shogi : Shogi) -> bool:
            x_step = shogi.get_dx_as_3bit()
            y_step = shogi.get_dy_as_3bit()
            x_start = shogi.start_cell.x
            y_start = shogi.start_cell.y

            for _ in range(shogi.get_displacement() - 1):
                x_start += x_step
                y_start += y_step

                piece = shogi.board.get_piece_from_any_cell(x_start, y_start)

                if piece != 0 : return True

            return False
        
        def verification_straight_move(self, shogi : Shogi) -> bool:
            straight = self.get_effective_straight(shogi)
            x = 1 + shogi.get_dx_as_3bit()
            y = 1 + shogi.get_dy_as_3bit()
            
            if not straight[y][x]: return True

            return self.verification_straight(shogi)
        
        def verification_L_move(self, shogi : Shogi) -> bool:
            if abs(shogi.get_dx()) != 1: return True
            if shogi.get_side():
                if shogi.get_dy() != 2: return True
            else:
                if shogi.get_dy() != -2: return True

            return False
        
        def verification(self, shogi) -> bool:
            _ = []
            for f in self.verificator:
                _.append(f(shogi))
            return any(_)

    class Verificator():
        def __init__(self):
            self.fu     = Shogi.MoveVerificator(True,  False, False, [[0, 1, 0], [0, 0, 0], [0, 0, 0]], None).verification
            self.kyosha = Shogi.MoveVerificator(True,  True,  False, [[0, 1, 0], [0, 0, 0], [0, 0, 0]], [[0, 1, 0], [0, 0, 0], [0, 0, 0]]).verification
            self.keima  = Shogi.MoveVerificator(False, False, True,  None, None).verification
            self.gin    = Shogi.MoveVerificator(True,  False, False, [[1, 1, 1], [0, 0, 0], [1, 0, 1]], None).verification
            self.kin    = Shogi.MoveVerificator(True,  False, False, [[1, 1, 1], [1, 0, 1], [0, 1, 0]], None).verification
            self.kaku   = Shogi.MoveVerificator(True,  True,  False, [[1, 0, 1], [0, 0, 0], [1, 0, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]).verification
            self.hisha  = Shogi.MoveVerificator(True,  True,  False, [[0, 1, 0], [1, 0, 1], [0, 1, 0]], [[0, 1, 0], [1, 0, 1], [0, 1, 0]]).verification
            self.ma     = Shogi.MoveVerificator(True,  True,  False, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]).verification
            self.ryu    = Shogi.MoveVerificator(True,  True,  False, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[0, 1, 0], [1, 0, 1], [0, 1, 0]]).verification
            self.ou     = Shogi.MoveVerificator(True,  False, False, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], None).verification

    class BiDict:
        def __init__(self, li : list):
            self.forward : dict = {}
            for d in li:
                self.forward[d[0]] = d[1]
            
            self.reverse : dict = {}
            for d in li:
                self.reverse[d[1]] = d[0]
        
        def get_by_value(self, key):
            return self.reverse[key]
        
        def get_by_key(self, key):
            return self.forward[key]
        
    def __init__(self):
        self.board = Shogi.Board()
        self.capture_pieces = [[], []]
        self.turn = 1

        self.start_cell = Shogi.Piece()
        self.destination_cell = Shogi.Piece()

        self.verificator = Shogi.Verificator()

        self.symbol_dict = Shogi.BiDict([
                                            ("FU", 10),
                                            ("TO", 11),
                                            ("KY", 20),
                                            ("NY", 21),
                                            ("KE", 30),
                                            ("NK", 31),
                                            ("GI", 40),
                                            ("NG", 41),
                                            ("KI", 50),
                                            ("KA", 60),
                                            ("UM", 61),
                                            ("HI", 70),
                                            ("RY", 71),
                                            ("OU", 80),
                                        ])

    def make_hand(self) -> bool:
        csa = list(input("your hand : "))
        hand = csa
        self.start_cell.x = int(hand[1]) - 1
        self.start_cell.y = int(hand[2]) - 1

        self.start_cell.symbol = self.symbol_dict(hand[5] + hand[6])

        self.destination_cell.x = int(hand[3]) - 1
        self.destination_cell.y = int(hand[4]) - 1

        return False
    
    def get_dx(self) -> int:
        dx : int = self.destination_cell.x - self.start_cell.x

        return dx
    
    def get_dy(self) -> int:
        dy : int = self.destination_cell.y - self.start_cell.y

        return dy

    def get_displacement(self) -> int:
        return max(abs(self.get_dx()), abs(self.get_dy()))
    
    def get_dx_as_3bit(self) -> int:
        return 1 if self.get_dx() > 0 else (-1 if self.get_dx() < 0 else 0)
    
    def get_dy_as_3bit(self) -> int:
        return 1 if self.get_dy() > 0 else (-1 if self.get_dy() < 0 else 0)
    
    # True  -> first hand
    # False -> second hand
    def get_side(self) -> bool:
        return self.turn % 2 == 1
    
    def eliminate_choose_zero(self) -> bool:
        if self.start_cell.x == -1 and self.start_cell.y == -1:
            if self.start_cell.symbol in self.capture_pieces:
                return True
        else:
            x = self.start_cell.x
            y = self.start_cell.y
            if self.board.get_piece_from_any_cell(x, y) == 0: return True

        return False
    
    # 自分の駒を取ろうとしてしまう。
    def eliminate_capture_own_piece(self) -> bool:
        if self.board.get_piece_from_start_cell(self) > 0:
            if self.board.get_piece_from_destination_cell(self) > 0:
                return True
        elif self.board.get_piece_from_start_cell(self) < 0:
            if self.board.get_piece_from_destination_cell(self) < 0:
                return True
        return False

    # 自分が所有していない駒を選択してしまう。
    def eliminate_choose_wrong_owner_piece(self) -> bool:
        piece_val = self.board.get_piece_from_start_cell(self)
        if self.get_side():
            return piece_val <= 0
        else :
            return piece_val >= 0
    
    def movement_verification(self) -> bool:
        type_of_piece = abs(self.board.get_piece_from_start_cell(self))
        match type_of_piece:
            case 10:
                return self.verificator.fu(self)
            case 20:
                return self.verificator.kyosha(self)
            case 30:
                return self.verificator.keima(self)
            case 40:
                return self.verificator.gin(self)
            case 11 | 21 | 31 | 41 | 50:
                return self.verificator.kin(self)
            case 60:
                return self.verificator.kaku(self)
            case 61:
                return self.verificator.ma(self)
            case 70:
                return self.verificator.hisha(self)
            case 71:
                return self.verificator.ryu(self)
            case 80:
                return self.verificator.ou(self)

    def apply_capture(self):
        capture_piece = self.board.get_piece_from_destination_cell(self)
        if capture_piece != 0:
            if self.get_side():
                self.capture_pieces[0].append(int(math.copysign(
                                                                (capture_piece + 1 if abs(capture_piece) % 10 == 1 else capture_piece),
                                                                1
                                                                )))
            else:
                self.capture_pieces[-1].append(int(math.copysign(
                                                                (capture_piece - 1 if abs(capture_piece) % 10 == 1 else capture_piece),
                                                                -1
                                                                )))

    def get_playerhand(self):
        while(True):
            if self.make_hand() : continue
            if self.eliminate_choose_zero() : continue
            if self.eliminate_choose_wrong_owner_piece() : continue
            if self.eliminate_capture_own_piece() : continue
            if self.movement_verification() : continue

            break

    def main(self):
        while(True):
            print("turn : ", self.turn)
            self.board.print_board(self)
            self.get_playerhand()
            self.apply_capture()
            self.board.update_board(self)
            self.turn += 1

if __name__ == "__main__":
    shogi = Shogi()
    shogi.main()