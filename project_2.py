'''
    Este programa em Python permite a um utilizador jogar a uma adaptacao do jogo Orbito, tanto
contra o computador, com as estrat'egias "fácil" e "normal", ou contra outro jogador.

    O "Orbito-n" e um jogo de tabuleiro abstrato para dois jogadores. Trata-se dum caso particular de
jogo m, n, k, onde as posicoes formam n orbitas. Os jogadores, em turnos alternados, colocam uma
pedra propria numa posicao livre.
    No fim de cada turno, todas as pedras rodam uma posicao em sentido anti-horario nas suas orbitas.
    O primeiro jogador que obtiver no fim de um turno 2 * n pedras seguidas da sua cor,
horizontalmente, verticalmente ou diagonalmente, e o vencedor.
'''

from math import sqrt

# ----- TAD posicao -----
'''
O TAD imutavel posicao e usado para representar uma posicao do tabuleiro de Orbito-n.
A representacao interna adotada para este TAD foi o tuplo.

Operações básicas:
    Construtores:
        cria_posicao(str, int) -> posicao
    
    Seletores:
        obtem_pos_col(posicao) -> string
        obtem_pos_lin(posicao) -> integer
    
    Reconhecedores:
        eh_posicao(universal) -> boolean
    
    Testes:
        posicoes_iguais(posicao, posicao) -> boolean
    
    Transformadores:
        posicao_para_str(posicao) -> string
        str_para_posicao(str) -> tuple

Funcoes de alto nivel:
    eh_posicao_valida(posicao, int) -> boolean
    obtem_posicoes_adjacentes(posicao, int, bool) -> tuple
    ordena_posicoes(tuple, int) -> tuple
        AUX: obtem_dados_pos(posicao) -> tuple
'''

def cria_posicao(col, lin):
    '''
    cria_posicao(str, int) -> tuple

    Devolve a posicao correspondente.

    Parameters:
        col (str) : coluna da posicao
        lin (int) : linha da posicao
    '''
    if not (type(col) == str and len(col) == 1 and col in ('abcdefghij') and type(lin) == int \
        and lin in range(1, 11)):
        raise ValueError('cria_posicao: argumentos invalidos')
    return col, lin

def obtem_pos_col(p):
    '''
    obtem_pos_col(posicao) -> string
    
    Devolve a coluna col da posicao 'p'.
    '''
    return p[0]

def obtem_pos_lin(p):
    '''
    obtem_pos_lin(posicao) -> integer
    
    Devolve a linha lin da posicao 'p'.
    '''
    return p[1]

def eh_posicao(arg):
    '''
    eh_posicao(universal) -> boolean

    Devolve True caso o seu argumento seja um TAD posicao e False caso contrario.
    '''
    return type(arg) == tuple and len(arg) == 2 and type(arg[0]) == str and len(arg[0]) == 1 \
        and type(arg[1]) == int and arg[1] in range(1, 11)

def posicoes_iguais(p1, p2):
    '''
    posicoes_iguais(posicao, posicao) -> boolean

    Devolve True se 'p1' e 'p2' sao posicoes e sao iguais e False caso contrario.
    '''
    return p1 == p2

def posicao_para_str(p):
    '''
    posicao_para_str(posicao) -> string

    Devolve a cadeia de caracteres que representa o seu argumento.
    '''
    return p[0] + str(p[1])

def str_para_posicao(s):
    '''
    str_para_posicao(str) -> posicao
    
    Devolve a posicao representada pelo seu argumento.
    '''
    return s[0], int(s[1:])

def eh_posicao_valida(p, n):
    '''
    eh_posicao_valida(posicao, int) -> boolean
    
    Devolve True se 'p' e uma posicao valida dentro do tabuleiro e False caso contrario.

    Parameters:
        p (posicao) : posicao do tabuleiro
        n (int) : numero de orbitas do tabuleiro
    '''
    return eh_posicao(p) and 'a' <= obtem_pos_col(p) < chr(ord('a') + 2 * n) \
        and 1 <= obtem_pos_lin(p) <= 2 * n

def obtem_posicoes_adjacentes(p, n, d):
    '''
    obtem_posicoes_adjacentes(posicao, int, bool) -> tuple

    Devolve um tuplo com as posicoes do tabuleiro adjacentes a posicao 'p' se 'd' for True, ou
    apenas as posicoes adjacentes ortogonais se for False.
    As posicoes do tuplo sao ordenadas em sentido horario comecando pela posicao acima de 'p'.

    Parameters:
        p (posicao) : posicao do tabuleiro
        n (int) : numero de orbitas do tabuleiro
        d (bool) : True para todas as posicoes adjacentes a 'p', False para apenas as ortogonais
    '''
    col_p, lin_p = obtem_pos_col(p), obtem_pos_lin(p)
    out = ()
    # cria o conjunto dos movimentos para obter cada posicao adjacente de acordo com o valor de 'd'
    if d:
        p_adj_possiveis = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    else:
        p_adj_possiveis = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    for move in p_adj_possiveis:
            col, lin = chr(ord(col_p) + move[0]), lin_p + move[1]
            # apenas adiciona a posicao se existe para 'n' orbitais
            if ord(col) in range(ord('a'), ord('a') + n * 2) and lin in range(1, n * 2 + 1): 
                out += (cria_posicao(col, lin),)
    return out

def obtem_pos_orbita(p, n):
    '''
    obtem_pos_orbita(posicao, int) -> int

    Devolve um a orbita de uma posicao do tabuleiro.

    Parameters:
        p (posicao) : posicao do tabuleiro
        n (int) : numero de orbitas do tabuleiro
    '''
    col_p, lin_p = ord(obtem_pos_col(p)) - ord ('a'), obtem_pos_lin(p) - 1
    centro_t = n - 0.5
    # calculo da orbita usando a formula de distancia entre dois pontos
    # usando indice comecado em 0
    orbita = sqrt((col_p - centro_t) ** 2 + (lin_p - centro_t) ** 2)
    return n if orbita > n else int(orbita) + 1 if orbita % 1 >= 0.5 else int(orbita)

def ordena_posicoes(t, n):
    '''
    ordena_posicoes(tuple, int) -> tuple

    Devolve um tuplo de posicoes com as mesmas posicoes de 't' ordenadas de acordo com a ordem de
    leitura do tabuleiro.

    Parameters:
        t (tuple) : tuplo de posicoes do tabuleiro
        n (int) : numero de orbitas do tabuleiro
    '''
    return tuple(sorted(t, key= lambda p: (obtem_pos_orbita(p, n), obtem_pos_lin(p), \
        obtem_pos_col(p))))

# ----- TAD pedra -----
'''
O TAD imutavel pedra e usado para representar as peras do jogo. As pedras podem pertencer ao
jogador branco ('O'), ao jogador preto ('X'), ou ser neutras (nao pertencem a nenhum jogador).
A representacao interna adotada para este TAD foi o inteiro.

Operações básicas:
    Construtores:
        cria_pedra_branca() -> int
        cria_pedra_preta() -> int
        cria_pedra_neutra() -> int
    
    Reconhecedores:
        eh_pedra(arg) -> boolean
        eh_pedra_branca(pedra) -> boolean
        eh_pedra_preta(pedra) -> boolean
    
    Testes:
        pedras_iguais(universal, universal) -> boolean
    
    Transformadores:
        pedra_para_str(pedra) -> string

Funcoes de alto nivel:
    eh_pedra_jogador(pedra) -> boolean
    pedra_para_int(pedra) -> integer
'''

def cria_pedra_branca():
    '''
    cria_pedra_branca() -> int

    Devolve uma pedra pertencente ao jogador branco ('O', -1).
    '''
    return -1

def cria_pedra_preta():
    '''
    cria_pedra_preta() -> int

    Devolve uma pedra pertencente ao jogador preto ('X', 1).
    Por convencao, o jogador preto e representado por 1, visto que joga sempre primeiro.
    '''
    return 1

def cria_pedra_neutra():
    '''
    cria_pedra_neutra() -> int

    Devolve uma pedra neutra (' ', 0).
    '''
    return 0

def eh_pedra(arg):
    '''
    eh_pedra(universal) -> boolean

    Devolve True caso o seu argumento seja um TAD pedra e False caso contr ́ario.
    '''
    return type(arg) == int and arg in (-1, 0, 1)

def eh_pedra_branca(p):
    '''
    eh_pedra_branca(pedra) -> boolean

    Devolve True caso a pedra p seja do jogador branco e False caso contr ́ario.
    '''
    return eh_pedra(p) and p == -1

def eh_pedra_preta(p):
    '''
    eh_pedra_preta(pedra) -> boolean

    Devolve True caso a pedra p seja do jogador preto e False caso contr ́ario.
    '''
    return eh_pedra(p) and p == 1

def pedras_iguais(p1, p2):
    '''
    pedras_iguais(universal, universal) -> boolean

    Devolve True apenas se p1 e p2 sao pedras e sao iguais, e False caso contrario.
    '''
    return eh_pedra(p1) and eh_pedra(p2) and p1 == p2

def pedra_para_str(p):
    '''
    pedra_para_str(pedra) -> string
    
    Devolve a cadeia de caracteres que representa o jogador dono da pedra, isto ́e, 'O', 'X' ou
    ' ' para pedras do jogador branco, preto ou neutra respetivamente.
    '''
    if eh_pedra_branca(p):
        return 'O'
    if eh_pedra_preta(p):
        return 'X'
    return ' '

def eh_pedra_jogador(p):
    '''
    eh_pedra_jogador(pedra) -> boolean
    
    Devolve True caso a pedra p seja de um jogador e False caso contrario.
    '''
    return eh_pedra_branca(p) or eh_pedra_preta(p)

def pedra_para_int(p):
    '''
    pedra_para_int(pedra) -> integer
    
    Devolve um inteiro valor 1, -1 ou 0, dependendo se a pedra e do jogador preto, branco ou
    neutra, respetivamente.
    '''
    if eh_pedra_branca(p):
        return -1
    if eh_pedra_preta(p):
        return 1
    return 0

# ----- TAD tabuleiro -----
'''
O TAD tabuleiro e usado para representar um tabuleiro do jogo Orbito-n e as pedras dos jogadores
que nele sao colocadas.
A representacao interna adotada para este TAD foi a lista.

Operações básicas:
    Construtores:
        cria_tabuleiro_vazio(int) -> tabuleiro
        cria_tabuleiro(int, tuple, tuple) -> tabuleiro
            AUX: preenche_tabuleiro(int, tuple, pedra) -> tabuleiro
        cria_copia_tabuleiro(tabuleiro) -> tabuleiro
    
    Seletores:
        obtem_numero_orbitas(tabuleiro) -> int
        obtem_pedra(tabuleiro, posicao) -> pedra
        obtem_linha_horizontal(tabuleiro, posicao) -> tuple
        obtem_linha_vertical(tabuleiro, posicao) -> tuple
        obtem_linhas_diagonais(tabuleiro, posicao) -> tuple, tuple
            AUX: obtem_linha_diagonal(int, int, int, int, bool) -> tuple
        obtem_posicoes_pedra(tabuleiro, pedra) -> tuple
    
    Modificadores:
        coloca_pedra(tabuleiro, posicao, pedra) -> tabuleiro
        remove_pedra(tabuleiro, posicao) -> tabuleiro
    
    Reconhecedores:
        eh_tabuleiro(universal) -> boolean
    
    Testes:
        tabuleiros_iguais(universal, universal) -> boolean
    
    Transformadores:
        tabuleiro_para_str(tabuleiro) -> string

Funcoes de alto nivel:
    move_pedra(tabuleiro, posicao, posicao) -> tabuleiro
    obtem_posicao_seguinte(tabuleiro, posicao, bool) -> posicao
    roda_tabuleiro(tabuleiro) -> tabuleiro
    verifica_linha_pedras(tabuleiro, posicao, pedra, int) -> boolean
        AUX: verifica_linha(tuple, pedra, int, posicao) -> boolean
'''

def cria_tabuleiro_vazio(n):
    '''
    cria_tabuleiro_vazio(int) -> tabuleiro

    Devolve um tabuleiro com 'n' orbitas, sem posicoes ocupadas. O numero minimo de orbitas de um
    tabuleiro de Orbito e 2 e o maximo e 5.

    Parameters:
        n (int) : numero de orbitas do tabuleiro
    '''
    if not (type(n) == int and 2 <= n <= 5):
        raise ValueError('cria_tabuleiro_vazio: argumento invalido')
    return [[cria_pedra_neutra() for _ in range(n * 2)] for _ in range(n * 2)]

def cria_tabuleiro(n, tp, tb):
    '''
    cria_tabuleiro(int, tuple, tuple) -> tabuleiro

    Devolve um tabuleiro com 'n' ́orbitas, com as posicoes do tuplo 'tp' ocupadas por pedras
    pretas e as posicoes do tuplo 'tb' ocupadas por pedras brancas. O numero minimo de orbitas de
    um tabuleiro de Orbito e 2 e o maximo e 5.

    Parameters:
        n (int) : numero de orbitas do tabuleiro
        tp (tuple) : posicoes ocupadas por pedras pretas
        tb (tuple) : posicoes ocupadas por pedras brancas
    '''
    if not (type(n) == int and 2 <= n <= 5 and type(tp) == tuple and type(tb) == tuple \
            and len(set(tp + tb)) == len(tp) + len(tb)):
        raise ValueError('cria_tabuleiro: argumentos invalidos')
    
    def preenche_tabuleiro(t, n, tup, j):
        '''
        preenche_tabuleiro(int, tuple, pedra) -> tabuleiro

        Devolve o tabuleiro 't' com as posicoes do tuplo 'tup' ocupadas pela pedra especificada.

        Parameters:
            t (tabuleiro) : tabuleiro de Orbito-n
            n (int) : numero de orbitas do tabuleiro
            tup (tuple) : tuplo de posicoes do tabuleiro
            j (pedra) : pedra do jogador
        '''
        for p in tup:
            if not eh_posicao_valida(p, n):
                raise ValueError('cria_tabuleiro: argumentos invalidos')
            t[obtem_pos_lin(p) - 1][ord(obtem_pos_col(p)) - ord('a')] = j
        return t
    
    t = preenche_tabuleiro(cria_tabuleiro_vazio(n), n, tp, cria_pedra_preta())
    t = preenche_tabuleiro(t, n, tb, cria_pedra_branca())
    return t

def cria_copia_tabuleiro(t):
    '''
    cria_copia_tabuleiro(tabuleiro) -> tabuleiro

    Devolve uma copia do tabuleiro 't'.
    '''
    return [[col for col in lin] for lin in t]

def obtem_numero_orbitas(t):
    '''
    obtem_numero_orbitas(tabuleiro) -> int
    
    Devolve o numero de orbitas do tabuleiro 't'.
    '''
    # n = 2
    # for orbita in range(4, 11, 2): # aumento de acordo com o numero de orbitas
    #     # ve a posicao no canto inferiror direito de cada orbita
    #     if not eh_posicao_valida(cria_posicao(chr(ord('a') + orbita), orbita + 1)):
    #         return n - 1
    #     n += 1^
    return len(t) // 2

def obtem_pedra(t, p):
    '''
    obtem_pedra(tabuleiro, posicao) -> pedra

    Devolve a pedra na posicao 'p' do tabuleiro 't'. Se a posicao nao estiver ocupada, devolve uma
    pedra neutra.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro 't'
    '''
    pedra = t[obtem_pos_lin(p) - 1][ord(obtem_pos_col(p)) - ord('a')]
    if eh_pedra_jogador(pedra):
        return pedra
    return cria_pedra_neutra()

def obtem_linha_horizontal(t, p):
    '''
    obtem_linha_horizontal(tabuleiro, posicao) -> tuple

    Devolve o tuplo formado por tuplos de dois elementos correspondentes a posicao e o valor de
    todas as posicoes da linha horizontal que passa pela posicao 'p', ordenadas da esquerda para a
    direita.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro 't'
    '''
    p_lin, n, out, out_p = obtem_pos_lin(p), obtem_numero_orbitas(t), (), ()
    for col in range(n * 2):
        out_p = cria_posicao(chr(ord('a') + col), p_lin)
        out += ((out_p, obtem_pedra(t, out_p)),)
    return out

def obtem_linha_vertical(t, p):
    '''
    obtem_linha_vertical(tabuleiro, posicao) -> tuple

    Devolve o tuplo formado por tuplos de dois elementos correspondentes a posicao e o valor de
    todas as posicoes da linha vertical que passa pela posicao 'p', ordenadas da esquerda para a
    direita.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro 't'
    '''
    p_col, out, out_p = obtem_pos_col(p), (), ()
    for lin in range(len(t)):
        out_p = cria_posicao(p_col, lin + 1)
        out += ((out_p, obtem_pedra(t, out_p)),)
    return out

def obtem_linhas_diagonais(t, p):
    '''
    obtem_linhas_diagonais(tabuleiro, posicao) -> tuple, tuple

    Devolve dois tuplos formados cada um deles por tuplos de dois elementos correspondentes a
    posicao e o valor de todas as posicoes que formam a diagonal (descendente da esquerda para a
    direita) e antidiagonal (ascendente da esquerda para a direita) que passam pela posicao 'p',
    respetivamente.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro 't'
        '''
    
    max_lin_col, out = obtem_numero_orbitas(t) * 2, ()
    for sign in (+1, -1): # +1 para diagonal, -1 para antidiagonal
        diag = ()
        lin, col = obtem_pos_lin(p) - 1, ord(obtem_pos_col(p)) - ord('a')
        offset = min(lin, col) if sign == 1 else min(max_lin_col - 1 - lin, col) 
        lin, col = lin - sign * offset, col - offset
        for d in range(max_lin_col):
            if 0 <= lin + sign * d < max_lin_col and 0 <= col + d < max_lin_col:
                pos = cria_posicao(chr(col + d + ord('a')), lin + sign * d + 1)
                diag += ((pos, obtem_pedra(t, pos)),)
        out += (diag,)
    return out

def obtem_posicoes_pedra(t, j):
    '''
    obtem_posicoes_pedra(tabuleiro, pedra) -> tuple

    Devolve o tuplo formado por todas as posicoes do tabuleiro ocupadas por pedras 'j',
    ordenadas em ordem de leitura do tabuleiro.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        j (pedra) : pedra do jogador
    '''
    out = ()
    for lin in range(len(t)):
        for col in range(len(t[lin])):
            if t[lin][col] == j:
                out += (cria_posicao(chr(ord('a') + col), lin + 1),)
    return ordena_posicoes(out, obtem_numero_orbitas(t))

def coloca_pedra(t, p, j):
    '''
    coloca_pedra(tabuleiro, posicao, pedra) -> tabuleiro

    Modifica destrutivamente o tabuleiro 't' colocando a pedra 'j' na posicao 'p' e devolve o
    proprio tabuleiro.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro 't'
        j (pedra) : pedra do jogador
    '''
    t[obtem_pos_lin(p) - 1][ord(obtem_pos_col(p)) - ord('a')] = j
    return t

def remove_pedra(t, p):
    '''
    remove_pedra(tabuleiro, posicao) -> tabuleiro

    Modifica destrutivamente o tabuleiro 't' removendo a pedra da posicao 'p' e devolve o proprio
    tabuleiro.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro 't'
    '''
    t[obtem_pos_lin(p) - 1][ord(obtem_pos_col(p)) - ord('a')] = cria_pedra_neutra()
    return t

def eh_tabuleiro(arg):
    '''
    eh_tabuleiro(universal) -> boolean

    Devolve True caso o seu argumento seja um TAD tabuleiro e False caso contrario.
    '''
    if not (type(arg) == list and 2 <= obtem_numero_orbitas(arg) <= 5):
        return False
    n_lin, pedras = len(arg), (cria_pedra_branca(), cria_pedra_preta(), cria_pedra_neutra())
    for lin in arg:
        if not len(lin) == n_lin:
            return False
        for col in lin:
            if not (eh_pedra(col) and col in pedras):
                return False
    return True

def tabuleiros_iguais(t1, t2):
    '''
    tabuleiros_iguais(universal, universal) -> boolean

    Devolve True apenas se t1 e t2 forem tabuleiros e forem iguais.
    '''
    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1 == t2

def tabuleiro_para_str(t):
    '''
    tabuleiro_para_str(tabuleiro) -> string

    Devolve a cadeia de caracteres que representa o tabuleiro.
    '''
    n_lin_col = obtem_numero_orbitas(t) * 2
    out = ' '
    # escreve as letras das colunas
    for col in range(n_lin_col):
        out += '   ' + chr(ord('a') + col)
    out += ('\n')

    # escreve as linhas do tabuleiro com os separadores
    for lin in range(1, n_lin_col + 1):
        string = ('0' if lin < 10 else '') + str(lin) + ' '
        for col in range(n_lin_col):
            string += f'[{pedra_para_str(t[lin - 1][col])}]'
            if col < n_lin_col - 1:
                string += '-'
        out += string
        if lin < n_lin_col:
            out += '\n' + ' ' + '   |' * n_lin_col + '\n'
    return out

def move_pedra(t, p1, p2):
    '''
    move_pedra(tabuleiro, posicao, posicao) -> tabuleiro

    Modifica destrutivamente o tabuleiro 't' movendo a pedra da posicao 'p1' para a posicao 'p2',
    e devolve o proprio tabuleiro.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p1 (posicao) : posicao de origem do tabuleiro 't'
        p1 (posicao) : posicao de destino do tabuleiro 't'
    '''
    j = obtem_pedra(t, p1)
    return coloca_pedra(remove_pedra(t, p1), p2, j)

def obtem_posicao_seguinte(t, p, s):
    '''
    obtem_posicao_seguinte(tabuleiro, posicao, bool) -> posicao

    Devolve a posicao da mesma orbita que 'p' que se encontra a seguir no tabuleiro 't' em sentido
    horario se 's' for True ou anti-horario se for False.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro
        s (bool) : True para o sentido horario, False para o sentido contrario
    '''
    n = obtem_numero_orbitas(t)
    p_orbit, p_col, p_lin = obtem_pos_orbita(p, n), obtem_pos_col(p), obtem_pos_lin(p)
    p_adjacentes = obtem_posicoes_adjacentes(p, n, False)
    # filtra as posicoes adjacentes da mesma orbita de 'p'
    p_seg_possiveis = [pos for pos in p_adjacentes if obtem_pos_orbita(pos, n) == p_orbit]
    # verifica se a posicao se encontra na borda esquerda de cima da orbita no tabuleiro
    borda_top_lef_n = (p_col == chr(ord('a') + n - p_orbit) \
        and p_lin in range(1 + n - p_orbit, n + p_orbit + 1)) or (p_lin == 1 + n - p_orbit \
        and ord(p_col) in range(ord('a') + n - p_orbit, ord('a') + n + p_orbit))
    # inverte a ordem das adjacentes de acordo com o sentido escolhido e a posicao
    if not borda_top_lef_n:
        if s:
            p_seg_possiveis = p_seg_possiveis[::-1]
    elif not s:
        p_seg_possiveis = p_seg_possiveis[::-1]
    return p_seg_possiveis[0]

def roda_tabuleiro(t):
    '''
    roda_tabuleiro(tabuleiro) -> tabuleiro

    Modifica destrutivamente o tabuleiro 't' rodando todas as pedras uma posicao em sentido
    anti-horario e devolve o proprio tabuleiro.
    '''
    p_jogadores, p_seguintes = obtem_posicoes_pedra(t, cria_pedra_branca()) + \
        obtem_posicoes_pedra(t, cria_pedra_preta()), ()
     
    for p in p_jogadores:
        p_seguintes += ((obtem_posicao_seguinte(t, p, False), obtem_pedra(t, p)),)
        _ = remove_pedra(t, p)
    for p_seg, pedra in p_seguintes:
        _ = coloca_pedra(t, p_seg, pedra)
    return t

def verifica_linha(linha, j, k, pos_i):
    '''
    verifica_linha(tuple, pedra, int, posicao) -> boolean

    Devolve True se existem k ou mais posicoes consecutivas do jogador indicado
    (incluindo a posicao indicada) na linha indicada e False caso contrario.
    
    Parameters:
        linha (tuple): linha do tabuleiro a verificar
        j (pedra): pedra do jogador
        k (int) : numero de pedras consecutivas a verificar
        pos_i (int): posicao da linha a verificar
    '''
    count_k , contem_pos_i = 0, False
    for pos_l, pedra_l in linha:
        if pedra_l == j:
            count_k += 1
            if posicoes_iguais(pos_l, pos_i):
                contem_pos_i = True
        else: # reset caso as posicoes nao sejam consecutivas
            if contem_pos_i == True: # se ja tinha passado pela posicao inicial, ignora o resto
                return False 
            count_k = 0
        if count_k == k and contem_pos_i == True:
            return True
    return False

def verifica_linha_pedras(t, p, j, k):
    '''
    verifica_linha_pedras(tabuleiro, posicao, pedra, int) -> boolean

    Devolve True se existe pelo menos uma linha (horizontal, vertical ou diagonal) que contenha a
    posicao 'p' com 'k' ou mais pedras consecutivas do jogador com pedras 'j', e False caso
    contrario.

    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        p (posicao) : posicao do tabuleiro
        j (pedra) : pedra do jogador
        k (int) : numero de pedras consecutivas a verificar
    '''
    if not obtem_pedra(t, p) == j:
        return False
    
    for l in [obtem_linha_horizontal(t, p), obtem_linha_vertical(t, p), \
              *obtem_linhas_diagonais(t, p)]:
        if len(l) >= k and verifica_linha(l, j, k, p):
            return True
    return False

# ----- Funcoes adicionais -----
def eh_vencedor(t, j):
    '''
    eh_vencedor(tabuleiro, pedra) -> boolean

    Devolve True se existe uma linha completa do tabuleiro de pedras do jogador ou False caso
    contrario.
    
    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        j (pedra) : pedra do jogador
    '''
    n, posicoes = obtem_numero_orbitas(t), obtem_posicoes_pedra(t, j)
    for p in posicoes:
        if verifica_linha_pedras(t, p, j, n * 2):
            return True
    return False

def eh_fim_jogo(t):
    '''
    eh_vencedor(tabuleiro) -> boolean

    Devolve True se o jogo ja terminou ou False caso contrario.
    '''
    return eh_vencedor(t, cria_pedra_preta()) or eh_vencedor(t, cria_pedra_branca()) or \
        not obtem_posicoes_pedra(t, cria_pedra_neutra())

def escolhe_movimento_manual(t):
    '''
    escolhe_movimento_manual(tabuleiro) -> posicao

    Permite escolher uma posicao livre do tabuleiro onde colocar uma pedra.
    '''
    n = obtem_numero_orbitas(t)
    while True:
        s = input('Escolha uma posicao livre:')
        if (len(s) == 2 and ord(s[0]) in range(ord('a'), ord('a') + n * 2) and s[1].isdigit() \
            and int(s[1]) in range(1, n * 2 + 1)) or (len(s) == 3 and n == 5 \
            and ord(s[0]) in range(ord('a'), ord('a') + n * 2) and s[1].isdigit() \
            and s[2].isdigit() and int(s[1:]) == 10):
            p = str_para_posicao(s)
            j = obtem_pedra(t, p)
            if j == cria_pedra_neutra():
                break
    return p

def determina_maior_l(t, j, k, p_livres, adv):
    '''
    determina_maior_ l(tabuleiro, pedra, int) -> tuple

    Devolve o maior valor de L ≤ k tal que o jogador obtem L posicoes consecutivas no fim do
    turno e a posicao do tabuleiro que permite obter esse valor.
    
    Parameters:
        t (tabuleiro) : tabuleiro de Orbito-n
        j (pedra) : pedra do jogador
        k (int) : numero maximo de posicoes consecutivas
        p_livres (tuple) : tuplo de posicoes livres
        adv (bool) : True se e a jogada do adversario; o tabuleiro roda duas vezes
    '''
    for l in range(k, 1, -1):
        for p in p_livres:
            t_copy = cria_copia_tabuleiro(t)
            _ = roda_tabuleiro(coloca_pedra(t_copy, p, j))
            p_seguinte = obtem_posicao_seguinte(t, p, False)
            if adv:
                _ = roda_tabuleiro(t_copy)
                p_seguinte = obtem_posicao_seguinte(t, p_seguinte, False)
            if verifica_linha_pedras(t_copy, p_seguinte, j, l):
                return l, p
    return 1, p_livres[0]

def escolhe_movimento_auto(t, j, lvl):
    '''
    escolhe_movimento_auto(tabuleiro, pedra, str) -> posicao

    Devolve a posicao escolhida automaticamente de acordo com a estrategia selecionada para
    o jogador com pedras j.
    As posicoes sao calculadas pela ordem de leitura do tabuleiro.

    Estrategia facil:
        Procura uma posicao livre que, no fim do turno, seja adjacente a uma posicao propria.
        Se nao, devolve numa posicao livre.
    
    Estrategia normal:
        Procura uma posicao que, no fim do turno, permita obter uma linha que contenha essa
        posicao com mais L <= k posicoes consecutivas proprias.
        Se nao, devolve uma posicao que impossibilite o adversario de obter mais L posicoes
        consecutivas no fim do turno.
    
    Parameters:
        tab (tabuleiro) : tabuleiro de Orbito-n
        jog (pedra) : pedra do jogador
        lvl (str) : estrategia de jogo
    '''
    # if not (eh_tabuleiro(t) and eh_pedra_jogador(j)a nd lvl in ('facil', 'normal') and not eh_fim_jogo(t)):
    #     raise ValueError('escolhe_posicao_auto: argumentos invalidos')
    
    n = obtem_numero_orbitas(t)
    p_livres = obtem_posicoes_pedra(t, cria_pedra_neutra())
    if j == cria_pedra_preta():
        j_adv = cria_pedra_branca()
    else:
        j_adv = cria_pedra_preta()

    if lvl == 'facil':
        for p in p_livres:
            t_copy = roda_tabuleiro(coloca_pedra(cria_copia_tabuleiro(t), p, j))
            p_adjacentes = obtem_posicoes_adjacentes(obtem_posicao_seguinte(t, p, False), n, True)
            for p_adj in p_adjacentes:
                if obtem_pedra(t_copy, p_adj) == j:
                    return p
        return p_livres[0]
    
    else:
        k = n * 2
        l_max_cpu, p_l_max_cpu = determina_maior_l(t, j, k, p_livres, False)
        if l_max_cpu > 1:
            return p_l_max_cpu
        return determina_maior_l(t, j_adv, k, p_livres, True)[1]

def obtem_vencedor(t):
    '''
    obtem_vencedor(tabuleiro) -> str, int

    Devolve o valor correspondente ao vencedor ('X' para preto, 'O' para branco e 0 para empate).
    '''
    preto_vence, branco_vence = False, False
    if eh_vencedor(t, cria_pedra_preta()):
        preto_vence = True
    if eh_vencedor(t, cria_pedra_branca()):
        branco_vence = True
    if preto_vence:
        if branco_vence:
            return 0
        return pedra_para_str(cria_pedra_preta())
    if branco_vence:
        return pedra_para_str(cria_pedra_branca())
    return 0

def orbito(n, modo, jog):
    '''
    orbito(int, str, str) -> int

    Funcao principal que permite jogar um jogo completo de Orbito-n contra o comuptador ou de
    dois jogadores:

        O jogo comeca sempre com o jogador com pedras pretas e termina se nao existem posicoes
        livres no tabuleiro ou, se ao finalizar o turno de um dos jogadores, existe uma linha com
        k pedras seguidas iguais.

        Se os dois jogadores tem k pedras seguidas ou se nenhum jogador as tem, o jogo termina em
        empate.

    No fim do jogo, mostra o resultado ('VITORIA', 'DERROTA' ou 'EMPATE').

    Devolve o inteiro correspondente ao vencedor (1 para preto, -1 para branco e 0 para empate).

    Parameters:
        n (int): numero de ́orbitas do tabuleiro
        modo (str) : modo de jogo
        jog (str) : representacao externa da pedra do jogador
    '''
    if not(type(n) == int and 2 <= n <= 5 and modo in ('facil', 'normal', '2jogadores') \
           and jog in ('X', 'O')):
        raise ValueError('orbito: argumentos invalidos')
    
    print(f'Bem-vindo ao ORBITO-{n}.')
    if modo == '2jogadores':
        jog, jog_primeiro = 'X', True
        print('Jogo para dois jogadores.')
    else:
        print(f'Jogo contra o computador ({modo}).')
        print(f"O jogador joga com '{jog}'.")
    
    if jog == 'X': # se o jogador for 'O', apenas comeca no segundo turno
        jog_primeiro = True
        adv = 'O'
        pedra_jog, pedra_adv = cria_pedra_preta(), cria_pedra_branca()
    else:
        jog_primeiro = False
        adv = 'X'
        pedra_jog, pedra_adv = cria_pedra_branca(), cria_pedra_preta()
    
    resultados = {'X': 1, 'O': -1, 0: 0}
    t, k = cria_tabuleiro_vazio(n), n * 2
    print(tabuleiro_para_str(t))
    while True:
        if jog_primeiro:
            if modo == '2jogadores':
                print(f"Turno do jogador '{jog}'.")
            else:
                print('Turno do jogador.')
            p_jog = escolhe_movimento_manual(t)
            _ = roda_tabuleiro(coloca_pedra(t, p_jog, pedra_jog))
            print(tabuleiro_para_str(t))
            if eh_fim_jogo(t):
                vencedor = obtem_vencedor(t)
                if modo == '2jogadores' and vencedor != 0:
                    print(f"VITORIA DO JOGADOR '{vencedor}'")
                elif vencedor == jog:
                    print('VITORIA')
                elif vencedor != 0:
                    print('DERROTA')
                else:
                    print('EMPATE')
                return resultados[vencedor]
            if modo == '2jogadores':
                jog, adv = adv, jog
                pedra_jog, pedra_adv = pedra_adv, pedra_jog
        
        jog_primeiro = True
        if modo != '2jogadores':
            print(f'Turno do computador ({modo}):')
            p_cpu = escolhe_movimento_auto(t, pedra_adv, modo)
            _ = roda_tabuleiro(coloca_pedra(t, p_cpu, pedra_adv))
            print(tabuleiro_para_str(t))
            if eh_fim_jogo(t):
                vencedor = obtem_vencedor(t)
                if vencedor == jog:
                    print('VITORIA')
                elif vencedor != 0:
                    print('DERROTA')
                else:
                    print('EMPATE')
                return resultados[vencedor]
