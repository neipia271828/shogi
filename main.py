from dataclasses import dataclass
import math
import inspect

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

# 検証 -> verificate
#

with open("kifu/original/example.txt", "r", encoding="utf-8") as f:
    kifu = f.readlines()
class Debug():
    need_print_debugmessage : bool = True
    
    @classmethod
    def print_debugmessage(cls, input_data : list, 
                           exception_message : Exception = None,
                           exception_type : type = None,
                           message : str = "violation has been detected",
                           additional_message : str = None):
        frame = inspect.currentframe()
        caller = inspect.getframeinfo(frame.f_back)

        if cls.need_print_debugmessage:
            print(f"{"from : ":30s}", caller.function)
            print(f"{"expection_type : ":30s}", exception_type)
            print(f"{"expection_message : ":30s}", exception_message)
            print(f"{"message : ":30s}", message)
            print(f"{"additional_message : ":30s}", additional_message)
            print("input_data : ")
            for d in input_data:
                print(d, type(d))

class Shogi():
    class Board:
        # board はクラス変数のため Board インスタンスを複数作ると盤面が共有される。現状は Shogi 1つに Board 1つなので問題ないが、意図的な設計ではない。
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
            if shogi.hand.start_cell.x == -1 and shogi.hand.start_cell.y == -1:
                side = 0 if shogi.get_side() else -1
                shogi.capture_pieces[side].remove(shogi.hand.captured_piece_symbol.get_piece_symbol_as_int())
                
            self.board[shogi.hand.destination_cell.y][shogi.hand.destination_cell.x] = self.board[shogi.hand.start_cell.y][shogi.hand.start_cell.x]
            self.board[shogi.hand.start_cell.y][shogi.hand.start_cell.x] = 0

            return True

        # Reviewed 5/7
        def get_piece_using_xy(self, x : int, y : int) -> int:
            return self.board[y][x]
        
        # Reviewed 5/7
        def get_piece_using_pieceposition_object(self, object : Shogi.PiecePosition) -> int:
            x = object.x
            y = object.y

            return self.board[y][x]
        
        # Reviewed 5/7
        def print_board(self, shogi : Shogi):
            for i in range(9):
                print()
                for j in range(9):
                    print(f"{self.board[i][j]:4d}", end="")
            print()

            print("capture_piece :")
            print("+", shogi.capture_pieces[0])
            print("-", shogi.capture_pieces[-1])

    # Reviewed 5/7
    class PiecePosition:
        x : int = 0
        y : int = 0

    # Reviewed 5/7
    class PieceSymbol:
        piece_symbol_as_int : int = 0
        
        # Reviewed 5/7
        def __init__(self, dic : Shogi.BiDict):
            self.piece_symbol_dict = dic

        # Reviewed 5/7
        def set_piece_symbol_using_int(self, shogi : Shogi, symbol_as_int : int):
            if shogi.symbol_dict.included_value(symbol_as_int):
                self.piece_symbol_as_int = symbol_as_int
        
        # Reviewed 5/7
        def set_piece_symbol_using_str(self, shogi : Shogi, symbol_as_str : str):
            if shogi.symbol_dict.included_key(symbol_as_str):
                self.piece_symbol_as_int = shogi.symbol_dict.get_by_key(symbol_as_str)

        # Reviewed 5/7
        def get_piece_symbol_as_int(self):
            return self.piece_symbol_as_int
        
        # Reviewed 5/7
        def get_piece_symbol_as_str(self, shogi : Shogi):
            return self.piece_symbol_dict.get_by_value(self.piece_symbol_as_int)

    class Hand:
        def __init__(self, dict : Shogi.BiDict):

            # クラス変数
            self.start_cell = Shogi.PiecePosition()
            self.destination_cell = Shogi.PiecePosition()
            self.placed_piece_symbol = Shogi.PieceSymbol(dict)
            self.captured_piece_symbol = Shogi.PieceSymbol(dict)
            self.placed_from_captured_pieces : bool = False
            self.userinput_as_list : list = ""
            self.side : bool = None

            # 検証メソッド
            self.move_verificator = Shogi.MoveVerificator()
        def make_hand_with_kifu(self, shogi : Shogi, kifu : str) -> bool:
            self.get_handcontent_via_direct(kifu)
            self.make_handobject_contents(shogi)
            self.verificate_handobject(shogi)

        def make_hand_with_cli(self, shogi : Shogi) -> bool:
            while(True):
                self.get_handcontent_via_shell()
                if self.make_handobject_contents(shogi): continue
                if self.verificate_handobject(shogi): continue
                break
            return False
        
        def get_handcontent_via_shell(self) -> list:
            self.userinput_as_list = list(input("your hand : "))
        
        def get_handcontent_via_direct(self, kifu : str) -> list:
            self.userinput_as_list = list(kifu)
        
        # Reviewed 5/7
        # Debug Message Added
        def make_handobject_contents(self, shogi : Shogi) -> bool:
            csa = self.userinput_as_list
            if csa[0] == "+":
                side = True
            elif csa[0] == "-":
                side = False
            else:
                Debug.print_debugmessage(input_data = [csa[0]],
                                         exception_type = "ValueError",
                                         exception_message = "Unexpected input")
                return True
            
            try:
                start_x = int(csa[1])
                start_y = int(csa[2])
                destination_x = int(csa[3])
                destination_y = int(csa[4])
            except Exception as e:
                Debug.print_debugmessage(input_data = [csa[1], csa[2], csa[3], csa[4]],
                                         exception_type=type(e),
                                         exception_message=e)
                return True
            
            start_cell_position_as_zerobase = [start_x - 1, start_y - 1]
            destination_cell_position_as_zerobase = [destination_x - 1, destination_y - 1]
            
            try:
                piece_symbol_as_str = csa[5] + csa[6]
            except Exception as e:
                Debug.print_debugmessage(input_data = [csa[5], csa[6]],
                                         exception_type=type(e),
                                         exception_message=e)
                return True
            
            try:
                piece_symbol_as_num = shogi.symbol_dict.get_by_key(piece_symbol_as_str)
            except Exception as e:
                Debug.print_debugmessage(input_data=[shogi.symbol_dict.get_by_key(piece_symbol_as_num)],
                                         exception_type=type(e),
                                         exception_message=e)
                return True
            
            try:
                self.make_handobject(
                            shogi,
                            side,
                            start_cell_position_as_zerobase,
                            destination_cell_position_as_zerobase,
                            piece_symbol_as_num
                            )
            except Exception as e:
                Debug.print_debugmessage(input_data=[shogi,
                                                     side,
                                                     start_cell_position_as_zerobase,
                                                     destination_cell_position_as_zerobase, 
                                                     piece_symbol_as_num],
                                         exception_type=type(e),
                                         exception_message=e)
                return True
            return False
            
        # Reviewed 5/7
        # inputer guarant consistantency
        def make_handobject(self,
                     shogi : Shogi,
                     side : bool,
                     start_cell_position_as_zerobase : list, 
                     destination_cell_position_as_zerobase : list, 
                     placed_piece_symbol_as_int : int):
            if start_cell_position_as_zerobase[0] == -1 and start_cell_position_as_zerobase[1] == -1:
                self.start_cell.x = None
                self.start_cell.y = None
                self.from_captured = True
            else:
                self.start_cell.x = start_cell_position_as_zerobase[0]
                self.start_cell.y = start_cell_position_as_zerobase[1]
            
            self.destination_cell.x = destination_cell_position_as_zerobase[0]
            self.destination_cell.y = destination_cell_position_as_zerobase[1]

            self.side = side
            self.placed_piece_symbol.set_piece_symbol_using_int(shogi, placed_piece_symbol_as_int)

            captured_piece_symbol = shogi.board.get_piece_using_pieceposition_object(self.destination_cell)
            self.captured_piece_symbol.set_piece_symbol_using_int(shogi, captured_piece_symbol)

        # Reviewed 5/7
        # method have debug message
        def verificate_handobject(self, shogi : Shogi) -> bool:
            if self.verificate_choose_zero(shogi):return True
            if self.verificate_actual_and_input_difference(shogi): return True
            if self.verificate_capture_own_piece(): return True
            if self.verificate_choose_wrong_owner_piece(): return True
            if self.move_verificator.verificate_move(shogi): return True
            return False
        
        # Reviewed 5/7
        # Debug Message Added
        # 自分自身の駒を取ろうとしてしまう
        def verificate_capture_own_piece(self) -> bool:
            if self.placed_piece_symbol.get_piece_symbol_as_int() > 0:
                if self.captured_piece_symbol.get_piece_symbol_as_int() > 0:
                    Debug.print_debugmessage(input_data=[self.placed_piece_symbol.get_piece_symbol_as_int(),
                                                         self.captured_piece_symbol.get_piece_symbol_as_int()])
                    return True
            elif self.placed_piece_symbol.get_piece_symbol_as_int() < 0:
                if self.captured_piece_symbol.get_piece_symbol_as_int() < 0:
                    Debug.print_debugmessage(input_data=[self.placed_piece_symbol.get_piece_symbol_as_int(),
                                                         self.captured_piece_symbol.get_piece_symbol_as_int()])
                    return True
            return False
        
        # Reviewed 5/7
        # Debug Message Added
        # 自分が所有していない駒を選択してしまう。
        def verificate_choose_wrong_owner_piece(self) -> bool:
            piece_val = self.placed_piece_symbol.get_piece_symbol_as_int()
            if self.side:
                if piece_val <= 0:
                    Debug.print_debugmessage(input_data=[self.side, piece_val])
                    return True
                else:
                    return False
            else :
                if piece_val >= 0:
                    Debug.print_debugmessage(input_data=[self.side, piece_val])
                    return True
                else:
                    return False
        
        # Reviewed 5/7
        # Debug Message Added
        # 何も無いところを選択しない
        def verificate_choose_zero(self, shogi : Shogi) -> bool:
            side = 1 if self.side else -1
            # 手持ちを指している時
            if self.start_cell.x == -1 and self.start_cell.y == -1:
                if self.placed_piece_symbol.get_piece_symbol_as_int() not in shogi.capture_pieces[side]:
                    Debug.print_debugmessage(input_data=[self.start_cell.x,
                                                         self.start_cell.y,
                                                         self.placed_piece_symbol.get_piece_symbol_as_int(),
                                                         shogi.capture_pieces[side]])
                    return True
            else:
                x = self.start_cell.x
                y = self.start_cell.y
                if shogi.board.get_piece_using_pieceposition_object(self.start_cell) == 0:
                    Debug.print_debugmessage(input_data=[self.start_cell.x,
                                                         self.start_cell.y,
                                                         shogi.board.get_piece_using_pieceposition_object(self.start_cell)])
                    return True

            return False
        

        # Reviewed 5/7
        # Debug Message Added
        def verificate_actual_and_input_difference(self, shogi : Shogi) -> bool:
            input_symbol = self.placed_piece_symbol.get_piece_symbol_as_int()
            actual_symbol = shogi.board.get_piece_using_pieceposition_object(self.start_cell)

            if input_symbol != actual_symbol:
                Debug.print_debugmessage(input_data=[input_symbol, actual_symbol])
                return True
            
            input_side = self.side
            actual_side = shogi.get_side()

            if input_side != actual_side:
                Debug.print_debugmessage(input_data=[input_side, actual_side])
                return True
            
            return False
        
        # Reviewed 5/7
        def get_dx(self) -> int:
            dx : int = self.destination_cell.x - self.start_cell.x

            return dx
        
        # Reviewed 5/7
        def get_dy(self) -> int:
            dy : int = self.destination_cell.y - self.start_cell.y

            return dy
    class MoveVerificationPatternGenerator():
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

        # Reviewed 5/7
        def get_effective_slide(self, shogi) -> list:                                          
            if shogi.get_side():  # 先手                                                       
                return self.slide[::-1]  # 行を逆順に
            return self.slide
        
        # Reviewed 5/7
        def get_effective_straight(self, shogi) -> list:
            if shogi.get_side():
                return self.straight[::-1]                                                     
            return self.straight
        
        # Reviewed 5/7
        # Debug Message Added
        def verification_slide_move(self, shogi : Shogi) -> bool:
            slide = self.get_effective_slide(shogi)
            x = 1 + shogi.get_dx_as_3bit()
            y = 1 + shogi.get_dy_as_3bit()
            
            if not slide[y][x]:
                Debug.print_debugmessage(input_data=[slide, x, y])
                return True

            return False
        
        # Reviewed 5/7
        # Dubug Message Added
        def verification_straight(self, shogi : Shogi) -> bool:
            x_step = shogi.get_dx_as_3bit()
            y_step = shogi.get_dy_as_3bit()
            x_start = shogi.hand.start_cell.x
            y_start = shogi.hand.start_cell.y

            for _ in range(shogi.get_displacement() - 1):
                x_start += x_step
                y_start += y_step

                piece = shogi.board.get_piece_from_any_cell(x_start, y_start)

                if piece != 0 : 
                    Debug.print_debugmessage(input_data=[piece, x_start, y_start])
                    return True

            return False
        
        # Reviewed 5/7
        # Debug Message Added
        def verification_straight_move(self, shogi : Shogi) -> bool:
            straight = self.get_effective_straight(shogi)
            x = 1 + shogi.get_dx_as_3bit()
            y = 1 + shogi.get_dy_as_3bit()
            
            if not straight[y][x]:
                Debug.print_debugmessage(input_data=[x, y, straight])
                return True

            return self.verification_straight(shogi)
        
        # Reviewed 5/7
        # Debug Message Added
        def verification_L_move(self, shogi : Shogi) -> bool:
            if abs(shogi.hand.get_dx()) != 1:
                Debug.print_debugmessage(input_data=[shogi.hand.get_dx()])
                return True
            if shogi.get_side():
                if shogi.hand.get_dy() != 2:
                    Debug.print_debugmessage(input_data=[shogi.get_side(), shogi.hand.get_dy()])
                    return True
            else:
                if shogi.hand.get_dy() != -2:
                    Debug.print_debugmessage(input_data=[shogi.get_side(), shogi.hand.get_dy()])
                    return True

            return False
        
        # Reviewed 5/7
        # Debug Message Added
        def verification(self, shogi) -> bool:
            _ = []
            for f in self.verificator:
                _.append(f(shogi))
            if any(_):
                Debug.print_debugmessage(input_data=[_])
                return True
            else:
                return False

    class MoveVerificator():
        def __init__(self):
            self.fu     = Shogi.MoveVerificationPatternGenerator(True,  False, False, [[0, 1, 0], [0, 0, 0], [0, 0, 0]], None).verification
            self.kyosha = Shogi.MoveVerificationPatternGenerator(True,  True,  False, [[0, 1, 0], [0, 0, 0], [0, 0, 0]], [[0, 1, 0], [0, 0, 0], [0, 0, 0]]).verification
            self.keima  = Shogi.MoveVerificationPatternGenerator(False, False, True,  None, None).verification
            self.gin    = Shogi.MoveVerificationPatternGenerator(True,  False, False, [[1, 1, 1], [0, 0, 0], [1, 0, 1]], None).verification
            self.kin    = Shogi.MoveVerificationPatternGenerator(True,  False, False, [[1, 1, 1], [1, 0, 1], [0, 1, 0]], None).verification
            self.kaku   = Shogi.MoveVerificationPatternGenerator(True,  True,  False, [[1, 0, 1], [0, 0, 0], [1, 0, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]).verification
            self.hisha  = Shogi.MoveVerificationPatternGenerator(True,  True,  False, [[0, 1, 0], [1, 0, 1], [0, 1, 0]], [[0, 1, 0], [1, 0, 1], [0, 1, 0]]).verification
            self.ma     = Shogi.MoveVerificationPatternGenerator(True,  True,  False, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]).verification
            self.ryu    = Shogi.MoveVerificationPatternGenerator(True,  True,  False, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[0, 1, 0], [1, 0, 1], [0, 1, 0]]).verification
            self.ou     = Shogi.MoveVerificationPatternGenerator(True,  False, False, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], None).verification

        def verificate_move(self, shogi : Shogi) -> bool:
            type_of_piece = abs(shogi.hand.placed_piece_symbol.get_piece_symbol_as_int())
            match type_of_piece:
                case 10:
                    return self.fu(shogi)
                case 20:
                    return self.kyosha(shogi)
                case 30:
                    return self.keima(shogi)
                case 40:
                    return self.gin(shogi)
                case 11 | 21 | 31 | 41 | 50:
                    return self.kin(shogi)
                case 60:
                    return self.kaku(shogi)
                case 61:
                    return self.ma(shogi)
                case 70:
                    return self.hisha(shogi)
                case 71:
                    return self.ryu(shogi)
                case 80:
                    return self.ou(shogi)

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
        
        def included_key(self, key : str) -> bool:
            return key in self.forward
        
        def included_value(self, value : str) -> bool:
            return value in self.reverse
    

    def __init__(self):
        self.board = Shogi.Board()
        self.capture_pieces = [[], []]
        self.turn = 1

        self.verificator = Shogi.MoveVerificator()

        self.symbol_dict = Shogi.BiDict([
                                            ("NA", 00),
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
        
        self.hand : Shogi.Hand = Shogi.Hand(self.symbol_dict)
    


    def get_displacement(self) -> int:
        return max(abs(self.hand.get_dx()), abs(self.hand.get_dy()))
    
    def get_dx_as_3bit(self) -> int:
        return 1 if self.hand.get_dx() > 0 else (-1 if self.hand.get_dx() < 0 else 0)
    
    def get_dy_as_3bit(self) -> int:
        return 1 if self.hand.get_dy() > 0 else (-1 if self.hand.get_dy() < 0 else 0)
    
    # True  -> first hand
    # False -> second hand
    def get_side(self) -> bool:
        return self.turn % 2 == 1

    def apply_capture(self):
        capture_piece = self.hand.captured_piece_symbol.get_piece_symbol_as_int()
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

    def processing_kifu(self, kifu : list):
        for csa in kifu:
            self.hand.make_hand_with_kifu(self, csa.strip())
            self.apply_capture()
            self.board.update_board(self)
            self.turn += 1
        
    def main(self, kifu = None):
        if kifu is not None : self.processing_kifu(kifu)
        while(True):
            print("turn : ", self.turn)
            self.board.print_board(self)
            self.hand.make_hand_with_cli(self)
            self.apply_capture()
            self.board.update_board(self)
            self.turn += 1

if __name__ == "__main__":
    shogi = Shogi()
    shogi.main(kifu)