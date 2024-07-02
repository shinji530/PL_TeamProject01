import sys
# 정수 변수 next_token, 문자열 변수 token_string, 함수 lexical() 포함
charClass = 0
lexeme = []
nextChar = ''
lexLex = 0
next_token = 0
token_string = ''

numID = 0       # IDENT 개수
numCONST = 0    # CONST 개수
numOP = 0       # OP 개수

# 문자 유형(charClass)
LETTER = 0
DIGIT = 1
UNKNOWN = 99
EOF = -1

# 토큰 코드
CONST = 10
IDENT = 11
ASSIGNMENT_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
SEMI_COLON = 27

# IDENT값 저장
symbolTable = {}

# 문장 읽어서 오류 있다면 복구하여 저장하는 list
read_list = []
error_list = []
error_check = True # error 발생 시 False

# nextChar lexeme에 추가하는 함수
def addChar():
    global lexLex
    if lexLex <= 98:
        lexeme.append(nextChar)
        lexLex += 1
    else:
        error_check = False
        error_list.append('Error - lexeme is too long')

# 파일 읽어서 문자 유형 저장
def getChar():
    global nextChar, charClass
    global file
    nextChar = file.read(1)

    if nextChar != '':
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        else :
            charClass = UNKNOWN
    else:
        charClass = EOF

# 공백 문자가 아닐 때 getChar() 호출
def getNonBlanck():
    while nextChar.isspace():
        getChar()


def lookup(ch):
    global next_token, numOP, error_check
    if ch == '(':
        addChar()       # nextChar lexeme 추가
        next_token = LEFT_PAREN

    elif ch == ')':
        addChar()
        next_token = RIGHT_PAREN

    elif ch == '+':
        addChar()
        next_token = ADD_OP
        numOP += 1      # OP 개수 증가

    elif ch == '-':
        addChar()
        next_token = SUB_OP
        numOP += 1

    elif ch == '*':
        addChar()
        next_token = MULT_OP
        numOP += 1

    elif ch == '/':
        addChar()
        next_token = DIV_OP
        numOP += 1

    elif ch == ';':
        addChar()
        next_token = SEMI_COLON
        read_list.append(';')

    # 한 글자씩 읽으므로 : 이후 = 가 나오는지 검사 후 read_list에 := 추가 
    elif nextChar == ':':
        addChar()
        getChar()
        if nextChar == '=':
            addChar()
            next_token = ASSIGNMENT_OP
            read_list.append(':=')

    else:
        addChar()
        next_token = EOF

    return next_token

# 입력 값 분석 후 lexeme을 찾아내서 토큰 유형을 next_token에 저장하고, lexeme 문자열을 token_string에 저장
def lexical():
    # 필요한 전역 변수 호출
    global charClass, lexLex, next_token, lexeme
    global numID, numCONST, numOP
    global token_string, error_check
    # lexme, lexLen 초기화
    lexeme.clear()
    lexLex = 0
    getNonBlanck()

    # 식별자 파싱
    if charClass == LETTER:
        addChar()
        getChar()
        while charClass == LETTER or charClass == DIGIT:
            addChar()
            getChar()
        next_token = IDENT
        numID += 1
        # 입력 받은 lexeme을 token_string에 추가
        token_string = ''.join(lexeme)
        # read_list에 token_string(lexeme) 추가
        read_list.append(token_string)

    # 정수 리터럴 파싱
    elif charClass == DIGIT:
        addChar()
        getChar()
        while charClass == DIGIT:
            addChar()
            getChar()
        numCONST += 1
        next_token = CONST
        token_string = ''.join(lexeme)
        read_list.append(token_string)
        
    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()

    elif charClass == EOF:
        next_token = EOF

    token_string = ''.join(lexeme)
    
    # 한 문장 씩 파싱하므로 \n 만날 시 read_list 출력, 에러 발생 시 error_list 출력
    if nextChar == '' or nextChar == '\n':
        if read_list:
            read_string = ''.join(read_list)
            print(read_string)
            print('ID: ', numID, '; CONST: ', numCONST, '; OP: ', numOP, ';')
            if error_check == True:
                print('(OK)', end='')
            else:
                for error in error_list:
                    print(error)
                error_list.clear()
            print('\n')
            # IDNET, CONST, OP 개수 초기화
            numID = 0   
            numCONST = 0
            numOP = 0
            # read_list 초기화
            read_list.clear()
            error_check = True

# Recursive Descent Parsing ==> 파싱 트리 자동 생성
# <program> → <statements>
def program():
    statements()

# <statements> → <statement> | <statement><semi_colon><statements>
def statements():
    global error_check
    statement()
    while next_token == SEMI_COLON:
        lexical()
        statements()

# <statement> → <ident><assignment_op><expression>
def statement():
    global error_list
    if next_token == IDENT:
        # <ident>를 symboleTable key값으로 추가 (우선 Unknown으로 초기화)
        symbolTable[token_string] = 'Unknown'
        # <ident>에 <expr> 값 저장하기 위한 임시 변수
        temp_IDstring = token_string
        lexical()

        if next_token == ASSIGNMENT_OP:
            lexical()
            expression = expr()
            # <expr> 결과 값 <ident>에 대입
            symbolTable[temp_IDstring] = expression


#<expression> → <term><term_tail>
def expr():
    term_return = 0
    expr_ = 0

    term_return = term()
    if term_return != 'Unknown':
        # term_tail의 + / - 연산 결과
        expr_ = term_tail(term_return)
    else :
        # 정의 되지 않은 연산자
        expr_ = 'Unknown'
        term_tail(term_return)

    return expr_

#<term> → <factor> <factor_tail>
def term():
    factorReturn = 0
    factorReturn = factor()
    term_ = 0
    if factorReturn != 'Unknown':
        # factor_tail의 */ / 연산 수행 결과
        term_ = factor_tail(factorReturn)
    else:
        term_ = 'Unknown'
        factor_tail(factorReturn)
    return term_

#<term_tail> → <add_op><term><term_tail> | ε
def term_tail(t_t):
    global numOP, error_check, error_list
    t_tail = t_t
    term_return = 0

    # 중복 연산자 오류 검사
    if next_token == ADD_OP:
        read_list.append(token_string)
        lexical()

        if next_token == ADD_OP:
            error_list.append('(Warning) 중복 연산자(+) 제거')
            error_check = False
            numOP -= 1
            lexical()

        term_return = term()
        term_tail(term_return)

        # 연산 수행
        if term_return != 'Unknown' and t_t != 'Unknown':
            t_tail = term_return + t_t
        else:
            return 'Unknown'
        
    elif next_token == SUB_OP:
        read_list.append(token_string)
        lexical()

        if next_token == SUB_OP:
            error_list.append('(Warning) 중복 연산자(-) 제거')
            numOP -= 1
            error_check = False
            lexical()

        term_return = term()
        term_tail(term_return)
        if term_return != 'Unknown' and t_t != 'Unknown':
            t_tail = term_return - t_t
    
    # 연산 결과 return
    return t_tail

#<factor> → <left_paren><expression><right_paren> | <ident> | <const>
def factor():
    global error_check
    factor_ = 0

    # next_token이 <left_paren>
    # 왼쪽 괄호일 경우, lexical() 호출하여 괄호 전달 후 <expr> 호출 후 괄호 검사
    if next_token == LEFT_PAREN:
        read_list.append(token_string)
        lexical()
        factor_ = expr()
        if next_token == RIGHT_PAREN:
            read_list.append(token_string)
            lexical()
        else:
            # 왼쪽 괄호가 나왔는데 오른쪽 괄호가 없을 시 괄호 검사 실패
            error_check = False
            error_list.append('(Warning) 괄호 검사 실패')

    # next_token이 <ident>
    # symbolTable 검사 후 정의 되지 않은 식별자라면 오류 출력
    elif next_token == IDENT:
        # symbolTable에 존재하면 factor()함수의 반환값으로 줌
        if token_string in symbolTable:
            factor_ = symbolTable[token_string]
        else:
            er_string = (f"(Error) 정의되지 않은 변수 ({token_string})가 참조됨")
            error_list.append(er_string)
            error_check = False

            # 정의되지 않은 식별자는 'Unknown'으로 추가
            symbolTable[token_string] = 'Unknown'
            factor_ = 'Unknown'
        lexical()

   # next_token이 <const>
    elif next_token == CONST:
        # int로 형변환하여 factor() 결과로 저장
        factor_ = int(token_string)
        lexical()

    # <left_paren><expression><right_paren> | <ident> | <const>
    # 위에 포함되지 않는 문자가 나온다면 오류 처리
    else:
        error_list.append('(Error) 상수 혹은 피연산자 필요')
        error_check = False

    return factor_

#<factor_tail> → <mult_op><factor><factor_tail> | ε
def factor_tail(f_t):
    global numOP, error_list, error_check
    f_tail = f_t
    if next_token == MULT_OP:
        read_list.append(token_string)
        lexical()

        # 중복 연산자 발생 시 오류 제거
        if next_token == MULT_OP:
            error_check = False
            print("(Warning) 중복 연산자(*) 제거")
            numOP -= 1
            lexical()
        # 오류 제거 후 or 오류 미발생 시 factor() 리턴값으로 저장
        factor_return = factor()
        factor_tail(factor_return)

        # 연산 실행
        if factor_return != 'Unknown' and f_t != 'Unknown':
            f_tail = factor_return * f_t

    elif next_token == DIV_OP:
        read_list.append(token_string)
        lexical()

        if next_token == DIV_OP:
            error_check = False
            print("(Warning) 중복 연산자(/) 제거")
            numOP -= 1
            lexical()

        factor_return = factor()
        factor_tail(factor_return)

        if factor_return != 'Unknown' and f_t != 'Unknown':
            f_tail = factor_return / f_t
    
    return f_tail



# 입력 데이터 파일 내용 처리
args = sys.argv[1:]
file_name = ""
for i in args:
    file_name += i
file = open(file_name, 'r')
# file_name = input('파일명을 입력하세요      ex) eval1.txt\n')
# file = open(file_name, 'r')

getChar()

while next_token != EOF:
    lexical()
    program()

# 파일 내용 연산 총 결과 출력
print('Result ==> ', end='')
for k, v in symbolTable.items():
    print(f"{k} : {v};" , end='')
print("\n")
file.close()