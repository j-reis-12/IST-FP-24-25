''' 
    Este programa em Python permite a um jogador humano jogar contra o computador num
    jogo do tipo m, n, k, com as estrategias 'facil', 'normal' e 'dificil'.

    Um jogo m, n, k e um jogo de tabuleiro abstrato em que dois jogadores colocam
    pedras de forma alternada nas posicoes livres de um tabuleiro de dimensao m x n.
    O jogador que obtiver primeiro k pedras seguidas da sua propria cor / simbolo,
    horizontalmente, verticalmente ou diagonalmente, e o vencedor.
'''

def eh_tabuleiro(arg):
    '''
    Devolve True se o seu argumento corresponde a um tabuleiro e False
    caso contrario.
    
    eh_tabuleiro: universal --> bool
    '''
    if not (isinstance(arg, tuple) and 2 <= len(arg) <= 100 \
        and isinstance(arg[0], tuple) and 2 <= len(arg[0]) <= 100):
        return False
    
    n_colunas = len(arg[0])
    # 'm' e 'n' serao usados em geral como contadores de linhas / colunas
    for m in arg:
        if not (isinstance(m, tuple) and len(m) == n_colunas):
            return False
        for n in m:
            if not (type(n) == int and n in (-1, 0, 1)):
                return False
    return True

def eh_posicao(arg):
    '''
    Devolve True se o seu argumento corresponde a uma posicao dum
    tabuleiro e False caso contrario.
    As posicoes no tabuleiro sao definidas por um inteiro positivo.
    
    eh_posicao: universal --> bool
    '''
    return type(arg) == int and 0 < arg <= 10000

def obtem_dimensao(tab):
    '''
    Devolve um tuplo formado pelo numero de linhas 'm' e colunas 'n' 
    do tabuleiro (tambem um tuplo) de jogo mnk.
    
    Parameters:
        tab (tuple): um tabuleiro

    Returns:
        (m, n) (tuple): dimensoes do tabuleiro, 'm' e 'n'
    
    obtem_dimensao: tuple --> tuple
    '''
    if eh_tabuleiro(tab):
        return len(tab), len(tab[0])

# auxiliar - devolve as cordenadas de uma posicao
def obtem_coordenadas(tab, pos):
    '''
    Devolve um tuplo formado pelas coordenadas (m, n) de uma posicao num tabuleiro.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao dum tabuleiro

    Returns:
        (m, n)  (tuple): valores correspondentes a linha e coluna da posicao
    
    obtem_coordenadas: tuple, int --> tuple
    '''
    m_tab, n_tab = obtem_dimensao(tab)[0], obtem_dimensao(tab)[1]
    if eh_tabuleiro(tab) and eh_posicao(pos) and pos <= m_tab * n_tab:
        if pos <= n_tab: # primeira linha
            return (0, pos - 1)
        elif pos % n_tab == 0: # ultima coluna duma linha, para evitar devolver -1
            return (pos // n_tab - 1, n_tab - 1)
        else:
            return (pos // n_tab, pos % n_tab - 1)

def obtem_valor(tab, pos):
    '''
    Devolve o valor contido numa posicao do tabuleiro.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro

    Returns:
        (int): valor da posicao do tabuleiro: -1 | 1 (jogador), 0 (livre)
    
    obtem_valor: tuple, int --> int
    '''
    return tab[obtem_coordenadas(tab, pos)[0]][obtem_coordenadas(tab, pos)[1]]

def obtem_coluna(tab, pos):
    '''
    Devolve um tuplo com todas as posicoes que formam a coluna em que esta
    contida a posicao, ordenadas de menor a maior.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro

    Returns:
        out (tuple): posicoes da coluna do tabuleiro
    
    obtem_coluna: tuple, int --> tuple
    '''
    n_tab, n_target = obtem_dimensao(tab)[1], obtem_coordenadas(tab, pos)[1]
    out, count_pos = (), n_target + 1
    for m in range(len(tab)):
        out += (count_pos,)
        count_pos += n_tab
    return out

def obtem_linha(tab, pos):
    '''
    Devolve um tuplo com todas as posicoes que formam a linha em que esta
    contida a posicao, ordenadas de menor a maior.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro

    Returns:
        out (tuple): posicoes da linha do tabuleiro
    
    obtem_linha: tuple, int --> tuple
    '''
    m_target, n_tab = obtem_coordenadas(tab, pos)[0], obtem_dimensao(tab)[1] 
    out, count_pos = (), (m_target * n_tab) + 1 # comeca na primeira posicao da linha
    for n in range(n_tab):
        out += (count_pos,)
        count_pos += 1
    return out

def obtem_posicao(tab, coord):
    '''
    Devolve um inteiro correspondente a posicao do tabuleiro (None caso contrario).
    Usada quando percorrer o tabuleiro apenas 1 vez for insuficiente.

    Parameters:
        tab (tuple): um tabuleiro
        coord (tuple): coordenadas (m, n) de uma posicao do tabuleiro

    Returns:
        count_pos (int): posicao do tabuleiro
    
    obtem_posicao: tuple, tuple --> int
    '''
    n_tab, count_pos = obtem_dimensao(tab)[1], 1
    for m in range(len(tab)):
        if m == coord[0]:
            for n in range(len(tab[m])):
                if n == coord[1]:
                    return count_pos
                count_pos += 1
        else:
            count_pos += n_tab

def obtem_diagonais(tab, pos):
    '''
    Devolve o tuplo formado por dois tuplos de posicoes correspondentes a diagonal
    (descendente da esquerda para a direita) e antidiagonal (ascendente da esquerda
    para a direita) que passam pela posicao, respetivamente.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro

    Returns:
        (tuple): posicoes da diagonal e antidiagonal que passam pela posicao
    
    obtem_diagonais: tuple, int --> tuple
    '''
    m_pos, n_pos = obtem_coordenadas(tab, pos)
    m_tab, n_tab = obtem_dimensao(tab)
    out_d, out_ad = (), ()

    # Procura a posicao mais a esquerda da diagonal, avancando depois
    # pela mesma, registando as posicoes
    # diagonal
    m_target, n_target = m_pos, n_pos
    while m_target > 0 and n_target > 0:
        m_target -= 1
        n_target -= 1
    while m_target < m_tab and n_target < n_tab:
        out_d += (obtem_posicao(tab, (m_target, n_target)),)
        m_target += 1
        n_target += 1

    # antidiagonal
    m_target, n_target = m_pos, n_pos
    while m_target < m_tab - 1 and n_target > 0:
        m_target += 1
        n_target -= 1
    while m_target >= 0 and n_target < n_tab:
        out_ad += (obtem_posicao(tab, (m_target, n_target)),)
        m_target -= 1
        n_target += 1
    return (out_d, out_ad)

def tabuleiro_para_str(tab):
    '''
    Devolve a cadeia de caracteres que representa o tabuleiro de jogo mnk.
    
    Parameters:
        tab (tuple): um tabuleiro

    Returns:
        tab_str (str): representacao do tabuleiro em string
    
    tabuleiro_para_str: tuple --> str
    '''
    simbolos = {-1: 'O', 0: '+', 1: 'X'}
    m_tab, n_tab = obtem_dimensao(tab)
    tab_str = ''

    for m in range(m_tab):
        for n in range(n_tab):
            tab_str += simbolos[tab[m][n]]
            if n < n_tab - 1:
                tab_str += '---'
        if m < m_tab - 1:
            tab_str += '\n'
            for i in range(n_tab - 1):
                tab_str += ('|   ')
            tab_str += '|\n'
    return tab_str

def eh_posicao_valida(tab, pos):
    '''
    Devolve True se a posicao corresponde a uma posicao do tabuleiro
    e False caso contrario.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro
    
    eh_posicao_valida: tuple, int --> bool
    '''
    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError('eh_posicao_valida: argumentos invalidos')
    
    m, n = obtem_dimensao(tab)
    return pos <= m * n

def eh_posicao_livre(tab, pos):
    '''
    Devolve True se a posicao corresponde a uma posicao livre (nao ocupada)
    e False caso contrario.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro
    
    eh_posicao_livre: tuple, int --> bool
    '''
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_posicao_valida(tab, pos)):
        raise ValueError('eh_posicao_livre: argumentos invalidos')
    return obtem_valor(tab, pos) == 0

def obtem_posicoes(tab, valor):
    '''
    Devolve o tuplo com todas as posicoes do tabuleiro com o valor indicado.
    
    Parameters:
        tab (tuple): um tabuleiro
        valor (int): valor das posicoes a procurar

    Returns:
        out (tuple): posicoes com o valor indicado
    
    obtem_posicoes: tuple, int --> tuple
    '''
    out, count_pos = (), 1
    for m in tab:
        for n in m:
            if n == valor:
                out += (count_pos,)
            count_pos += 1
    return out

def obtem_posicoes_livres(tab):
    '''
    Devolve o tuplo com todas as posicoes livres do tabuleiro, ordenadas de menor a maior.
    
    Parameters:
        tab (tuple): um tabuleiro

    Returns:
        (tuple): posicoes livres do tabuleiro
    
    obtem_posicoes_livres: tuple --> tuple
    '''
    if not eh_tabuleiro(tab):
        raise ValueError('obtem_posicoes_livres: argumento invalido')
    return obtem_posicoes(tab, 0)

def eh_jogador(jog):
    '''
    Devolve True se o jogador corresponde a um jogador valido (1 | -1)
    e False caso contrario.
    
    eh_jogador: int --> bool
    '''
    return type(jog) == int and jog in (-1, 1)

def obtem_posicoes_jogador(tab, jog):
    '''
    Devolve o tuplo com todas as posicoes do tabuleiro ocupadas pelo jogador,
    ordenadas de menor a maior.
    
    Parameters:
        tab (tuple): um tabuleiro
        jog (int): jogador (-1 | 1)

    Returns:
        (tuple): posicoes ocupadas pelo jogador
    
    obtem_posicoes_jogador: tuple, int --> tuple
    '''
    if not (eh_tabuleiro(tab) and eh_jogador(jog)):
        raise ValueError('obtem_posicoes_jogador: argumentos invalidos')
    return obtem_posicoes(tab, jog)

def obtem_posicoes_adjacentes(tab, pos):
    '''
    Devolve o tuplo formado pelas posicoes do tabuleiro adjacentes
    (horizontal, vertical e diagonal), ordenadas de menor a maior.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro

    Returns:
        out (tuple): tuplo das posicoes adjacentes
    
    obtem_posicoes_adjacentes: tuple, int --> tuple
    '''
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_posicao_valida(tab, pos)):
        raise ValueError('obtem_posicoes_adjacentes: argumentos invalidos')
    
    m_pos, n_pos = obtem_coordenadas(tab, pos)
    cantos = ((m_pos - 1, n_pos - 1), (m_pos - 1, n_pos + 1), \
              (m_pos + 1, n_pos - 1), (m_pos + 1, n_pos + 1))
    retas = ((m_pos, n_pos - 1), (m_pos, n_pos + 1), \
              (m_pos - 1, n_pos), (m_pos + 1, n_pos))
    out = ()
    for adj in cantos + retas:
        adj_posicao = obtem_posicao(tab, adj)
        if adj_posicao != None and eh_posicao_valida(tab, adj_posicao):
            out += (adj_posicao,)
    return tuple(sorted(out))

def obtem_distancia_centro(c_vetor, pos_vetor):
    '''
    Devolve a distancia, em posicoes, de uma dada posicao ao centro do tabuleiro.
    
    Parameters:
        c_vetor (tuple): coordenadas do centro do tabuleiro
        pos_vetor (int): coordenadas de uma posicao do tabuleiro

    Returns:
        (int): distancia ao centro do tabuleiro
        
    obtem_distancia_centro: tuple, tuple --> int
    '''
    return max(abs(c_vetor[0] - pos_vetor[0]), abs(c_vetor[1] - pos_vetor[1]))

def ordena_posicoes_tabuleiro(tab, tup):
    '''
    Devolve o tuplo com as posicoes em ordem ascendente de distancia a
    posicao central do tabuleiro.
    Posicoes com igual distancia ao centro sao ordenadas de menor a maior
    de acordo com a posicao que ocupam no tabuleiro.
    
    Parameters:
        tab (tuple): um tabuleiro
        tup (tuple): tuplo de posicoes do tabuleiro (potencialmente vazio)

    Returns:
        out_tup (tuple): tuplo das posicoes ordenadas
    
    ordena_posicoes_tabuleiro: tuple, tuple --> tuple
    '''
    if not (eh_tabuleiro(tab) and isinstance(tup, tuple)):
        raise ValueError('ordena_posicoes_tabuleiro: argumentos invalidos')
    for pos in tup:
        if not (eh_posicao(pos) and eh_posicao_valida(tab, pos)):
            raise ValueError('ordena_posicoes_tabuleiro: argumentos invalidos')

    m_tab, n_tab = obtem_dimensao(tab)
    c_tab = (m_tab // 2) * n_tab + n_tab // 2 + 1 # centro do tabuleiro
    c_vetor = obtem_coordenadas(tab, c_tab)
    
    # coloca em out_tup as posicoes da lista ordenada (de acordo com as distâncias)
    return tuple(pos for pos in sorted(tup, key=lambda \
                pos:(obtem_distancia_centro(c_vetor, obtem_coordenadas(tab, pos)), pos)))

def marca_posicao(tab, pos, jog):
    '''
    Devolve um novo tabuleiro com uma identificacao do jogador na posicao indicada.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro
        jog (int): jogador

    Returns:
        (tuple): tabuleiro com posicao ocupada
    
    marca_posicao: tuple, int, int --> tuple
    '''
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_jogador(jog) \
            and eh_posicao_valida(tab, pos)):
        raise ValueError('marca_posicao: argumentos invalidos')
    
    m_pos, n_pos = obtem_coordenadas(tab, pos)
    if not tab[m_pos][n_pos] == 0:
        raise ValueError('marca_posicao: argumentos invalidos')
    # slice do tabuleiro + slice do tuplo da posicao a marcar para colocar \
    # o inteiro do jogador
    return tab[:m_pos] + ((tab[m_pos][:n_pos] + (jog,) + tab[m_pos][n_pos + 1:]),) \
        + tab[m_pos + 1:]

def eh_k_valido(k):
    '''
    Devolve True se o valor indicado de k e valido (inteiro positivo)
    e False caso contrario.
    
    eh_k_valido: universal --> bool
    '''
    return type(k) == int and 0 < k <= 100

def verifica_linha(tab, linha, jog, k, pos_i):
    '''
    Devolve True se existem k ou mais posicoes consecutivas do jogador indicado
    (incluindo a posicao indicada) na linha indicada e False caso contrario.
    
    Parameters:
        tab (tuple): um tabuleiro
        linha (tuple): linha do tabuleiro a verificar
        jog (int): jogador
        k (int): valor de k do jogo
        pos_i (int): posicao da linha a verificar

    Returns:
        (bool): True se existem k ou mais posicoes consecutivas do jogador indicado
    
    verifica_linha: tuple, int, int, int --> bool
    '''
    count_k , contem_pos_i = 0, False
    for pos_l in linha:
        if obtem_valor(tab, pos_l) == jog:
            count_k += 1
            if pos_l == pos_i:
                contem_pos_i = True
        else: # reset caso as posicoes nao sejam consecutivas
            if contem_pos_i == True: # se ja tinha passado pela posicao inicial, ignora o resto
                return False 
            count_k = 0
        if count_k == k and contem_pos_i == True:
            return True
    return False

def verifica_k_linhas(tab, pos, jog, k):
    '''
    Devolve True se existe pelo menos uma linha (horizontal, vertical ou diagonal)
    que contenha k ou mais posicoes consecutivas do jogador indicado
    (incluindo a posicao indicada) e False caso contrario.
    
    Parameters:
        tab (tuple): um tabuleiro
        pos (int): posicao do tabuleiro
        jog (int): jogador
        k (int): valor de k do jogo

    Returns:
        (bool): True se existem k ou mais posicoes consecutivas do jogador indicado
    
    verifica_k_linhas: tuple, int, int, int --> bool
    '''
    if not (eh_tabuleiro(tab) and eh_posicao(pos) and eh_posicao_valida(tab, pos) \
            and (eh_jogador(jog) or jog == 0) and eh_k_valido(k)):
        raise ValueError('verifica_k_linhas: argumentos invalidos')
    if not obtem_valor(tab, pos) == jog:
        return False

    for linha in [obtem_linha(tab, pos), obtem_coluna(tab, pos), \
                  *obtem_diagonais(tab, pos)]:
        if len(linha) >= k and verifica_linha(tab, linha, jog, k, pos):
            return True
    return False

def eh_fim_jogo(tab, k):
    '''
    Devolve um booleano a indicar se o jogo terminou (True) ou nao (False).
    Um jogo pode terminar caso um dos jogadores tenha k posicoes consecutivas,
    ou caso ja nao existam mais posicoes livres para marcar.
    
    Parameters:
        tab (tuple): um tabuleiro
        k (int): valor de k do jogo

    Returns:
        (bool): True se um jogador venceu ou nao existem mais posicoes livres
    
    eh_fim_jogo: tuple, int --> bool
    '''
    if not (eh_tabuleiro(tab) and eh_k_valido(k)):
        raise ValueError('eh_fim_jogo: argumentos invalidos')
    
    for jog in (-1, 1):
        for pos in obtem_posicoes_jogador(tab, jog):
            if verifica_k_linhas(tab, pos, jog, k):
                return True
    return obtem_posicoes_livres(tab) == ()

def escolhe_posicao_manual(tab):
    '''
    Devolve uma posicao introduzida manualmente pelo jogador.
    O jogador deve introduzir uma posicao livre do tabuleiro.
    
    Parameters:
        tab (tuple): um tabuleiro

    Returns:
        pos (int): True se a posicao introduzida e livre
    
    escolhe_posicao_manual: tuple --> int
    '''
    if not eh_tabuleiro(tab):
        raise ValueError('escolhe_posicao_manual: argumento invalido')
    
    pos = 0
    while True:
        pos = input('Turno do jogador. Escolha uma posicao livre: ')
        if pos.isnumeric():
            pos = int(pos)
        if eh_posicao(pos) and eh_posicao_valida(tab, pos) and eh_posicao_livre(tab, pos):
            return pos


def determina_maior_l(tab, jog, k, pos_livres):
    '''
    Devolve o maior valor de L ≤ k tal que o proprio ou o adversario obteem L posicoes
    consecutivas na proxima jogada e a posicao do tabuleiro que permite obter esse valor.
    
    Parameters:
        tab (tuple): um tabuleiro
        jog (int): jogador
        k (int): valor de k do jogo
        pos_livres (tuple): posicoes livres do tabuleiro

    Returns:
        (tuple): maior valor de L posicoes consecutivas possivel e a posicao para esse valor
    
    determina_maior_l: tuple, int, int, tuple --> tuple
    '''
    l_max, pos_l_max = 0, ()
    # para cada l (a partir de 1), verifica se e possivel obter l posicoes consecutivas
    # se houver mais de uma posicao com l maximo, ordena depois
    for l in range(1, k + 1):
        for pos in pos_livres:
            if verifica_k_linhas(marca_posicao(tab, pos, jog), pos, jog, l) and l > l_max:
                l_max, pos_l_max = l, pos
    return l_max, pos_l_max

def escolhe_posicao_auto(tab, jog, k, lvl):
    '''
    Devolve a posicao escolhida automaticamente de acordo com a estrategia selecionada.
    Sempre que houver mais do que uma posicao que cumpra um dos criterios definidos,
    devolve a posicao mais proxima do centro do tabuleiro.

    Estrategia facil:
        Procura pelo menos uma posicao livre e adjacente a uma posicao propria.
        Se nao, devolve numa posicao livre.
    
    Estrategia normal:
        Procura uma posicao que permita obter uma linha que contenha essa posicao com L
        posicoes consecutivas proprias.
        Se nao, devolve uma posicao que impossibilite o adversario de obter L posicoes
        consecutivas.

    Estrategia dificil:
        Procura uma posicao que permita obter uma linha propria com k posicoes
        consecutivas e ganhar o jogo.
        Se nao, procura uma posicao que impossibilite ao adversario de ganhar o jogo.
        Se nao, para cada posicao livre, simula um jogo ate ao fim assumindo que
        os dois jogadores alternadamente jogam seguindo uma estrategia de jogo normal:
            Regista o resultado de cada simulacao e devolve a posicao que leva ao melhor
            resultado possivel: ganhar o jogo, empatar o jogo, ou uma posicao livre,
            respetivamente.
    
    Parameters:
        tab (tuple): um tabuleiro
        jog (int): jogador
        k (int): valor de k do jogo
        lvl (str): estrategia de jogo

    Returns:
        (int): Posicao mais proxima do centro do tabuleiro que cumpre os criterios da
        estrategia selecionada
    
    escolhe_posicao_auto: tuple, int, int, str --> int
    '''
    if not (eh_tabuleiro(tab) and eh_jogador(jog) and eh_k_valido(k) \
            and lvl in ('facil', 'normal', 'dificil') and not eh_fim_jogo(tab, k)):
        raise ValueError('escolhe_posicao_auto: argumentos invalidos')
    
    pos_livres = obtem_posicoes_livres(tab)
    if not pos_livres:
        raise ValueError('escolhe_posicao_auto: argumentos invalidos')
    # trabalha com as posicoes ja ordenadas por distancia ao centro para poupar tempo
    pos_livres = ordena_posicoes_tabuleiro(tab, pos_livres)

    if lvl == 'facil':
        pos_possiveis = ()
        for pos in pos_livres:
            pos_adjacentes = obtem_posicoes_adjacentes(tab, pos)
            for pos_adj in pos_adjacentes:
                if obtem_valor(tab, pos_adj) == jog:
                    pos_possiveis += (pos,)
        if pos_possiveis:
            return ordena_posicoes_tabuleiro(tab, pos_possiveis)[0]
        return pos_livres[0]
    
    elif lvl == 'normal':
        l_max_cpu, pos_l_max_cpu = determina_maior_l(tab, jog, k, pos_livres)
        if l_max_cpu == k:
            return pos_l_max_cpu
        l_max_adv, pos_l_max_adv = determina_maior_l(tab, -jog, k, pos_livres)
        if l_max_cpu >= l_max_adv:
            return pos_l_max_cpu
        return pos_l_max_adv
    
    else:
        # verificacao inicial: vencer ou impedir adversario de vencer
        pos_empate = 0
        for pos in pos_livres:
            if verifica_k_linhas(marca_posicao(tab, pos, jog), pos, jog, k):
                return pos
            elif pos_empate == 0 and verifica_k_linhas(marca_posicao(tab, pos, -jog), \
                                                       pos, -jog, k):
                pos_empate = pos
        if pos_empate != 0:
            return pos_empate
        
        # simulacoes para cada posicao livre
        tab_sim, jog_sim, pos_empate = (), 0, 0
        # expressão de depth com base em testes para melhor desempenho nos tabuleiros
        max_depth = abs(10 - max(obtem_dimensao(tab))) 

        for pos_liv in pos_livres:
            tab_sim, jog_sim, depth = marca_posicao(tab, pos_liv, jog), -jog, 0
            while depth < max_depth:
                if eh_fim_jogo(tab_sim, k):
                    break
                tab_sim = marca_posicao(tab_sim, escolhe_posicao_auto(tab_sim, jog_sim, k, \
                                                                      'normal'), jog_sim)
                jog_sim = -jog_sim
                depth += 1
            
            nao_vence_adv = True
            for pos in obtem_posicoes_jogador(tab_sim, jog):
                if verifica_k_linhas(tab_sim, pos, jog, k):
                    return pos_liv
            if pos_empate == 0:
                for pos in obtem_posicoes_jogador(tab_sim, -jog):
                    if verifica_k_linhas(tab_sim, pos, -jog, k):
                        nao_vence_adv = False
                        break
                if nao_vence_adv:
                    pos_empate = pos_liv
        
        if pos_empate != 0:
            return pos_empate
        return pos_livres[0]

def eh_cfg_valida(cfg):
    '''
    Devolve True se o tuplo indicado corresponde a uma configuracao valida (m, n, k) de um
    jogo e False caso contrario.
    
    eh_cfg_valida: universal --> bool
    '''
    return isinstance(cfg, tuple) and len(cfg) == 3 and isinstance(cfg[0], int) \
        and 2 <= cfg[0] <= 100 and isinstance(cfg[1], int) and 2 <= cfg[1] <= 100 \
        and isinstance(cfg[2], int) and cfg[2] > 0

def jogo_mnk(cfg, jog, lvl):
    '''
    Funcao principal que permite jogar um jogo mnk completo de um jogador contra o computador:
        O jogo comeca com o jogador 'X' (1) a marcar uma posicao livre e termina quando um dos
        jogadores vence ou se nao existirem posicoes livres no tabuleiro.
    Mostra o resultado do jogo (VITORIA, DERROTA ou EMPATE) e devolve um inteiro identificando
    o vencedor (1, -1 ou 0 em caso de empate).

    Parameters:
        cfg (tuple): configuracao do jogo (m, n, k)
        jog (int): jogador
        lvl (str): estrategia de jogo

    Returns:
        (tuple): maior valor de L posicoes consecutivas possivel e a posicao para esse valor
    
    determina_maior_l: tuple, int, int, tuple --> tuple
    '''
    if not(eh_cfg_valida(cfg) and eh_jogador(jog) and lvl in ('facil', 'normal', 'dificil')):
        raise ValueError('jogo_mnk: argumentos invalidos')
    
    m_tab, n_tab, k = cfg
    tab = (((0,) * n_tab),) * m_tab
    simbolos = {-1: 'O', 1: 'X'}

    jog_primeiro = True
    if not jog == 1: # se o jogador for O (-1), apenas comeca no segundo turno
        jog_primeiro = False

    print('Bem-vindo ao JOGO MNK.')
    print(f"O jogador joga com '{simbolos[jog]}'.")
    print(tabuleiro_para_str(tab))
    while True:
        if jog_primeiro:
            pos_jog = escolhe_posicao_manual(tab)
            tab = marca_posicao(tab, pos_jog, jog)
            print(tabuleiro_para_str(tab))
            if verifica_k_linhas(tab, pos_jog, jog, k):
                print('VITORIA')
                return jog
            if not obtem_posicoes_livres(tab):
                print('EMPATE')
                return 0
        
        jog_primeiro = True
        print(f'Turno do computador ({lvl}):')
        pos_cpu = escolhe_posicao_auto(tab, -jog, k, lvl)
        tab = marca_posicao(tab, pos_cpu, -jog)
        print(tabuleiro_para_str(tab))
        if verifica_k_linhas(tab, pos_cpu, -jog, k):
            print('DERROTA')
            return -jog
        if not obtem_posicoes_livres(tab):
            print('EMPATE')
            return 0
