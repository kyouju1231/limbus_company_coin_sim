""" Limbus Company Coin Simulator """

def binomial_probability(n, k, p):
    # 二項分布の確率を計算する関数
    # n:試行回数  k:成功回数  p:試行1回の成功確率
    return (factorial(n) / (factorial(k) * factorial(n - k))) * (p ** k) * ((1 - p) ** (n - k))

def factorial(n):
    # 階乗を計算する関数
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

class skill:
    def __init__(self, base_power:int, coin_power:int, coin_count:int, mental:int):
        self.base_power = base_power
        self.coin_power = coin_power
        self.coin_count = coin_count
        self.mental = mental
        self.results =[]
        self.calculate_power_and_probability()

    def calculate_power_and_probability(self):
        # コインが表になる確率
        coin_probability = (self.mental + 50) / 100

        # 表が出たコインの枚数の組み合わせを生成
        heads_counts = range(0, self.coin_count + 1)

        # 各組み合わせの最終威力と確率を計算
        self.results = []
        for heads_count in heads_counts:    # 表0枚から順番に計算していく
            # 最終威力計算  基礎威力+( 表の枚数 x コイン威力 )
            final_power = self.base_power + (heads_count * self.coin_power)

            # 最終威力が出る確率
            probability = binomial_probability(self.coin_count, heads_count, coin_probability)

            # 最終威力とその確率をタプル型でリザルトリストに追加
            self.results.append( (final_power, probability) )


def match_cal(ally_skill:skill, enemy_skill:skill):
    win_probability = 0
    draw_probability = 0

    for (ally_fp, ally_prblty) in ally_skill.results:
        for (enemy_fp, enemy_prblty) in enemy_skill.results:

            # 確率
            probability = ally_prblty*enemy_prblty

            # 勝敗の比較
            if ally_fp > enemy_fp:      # 勝率
                win_probability += probability
            elif ally_fp == enemy_fp:   # 引分率
                draw_probability += probability
            else:
                pass

    final_probability = win_probability / (1-draw_probability)
    return final_probability


def calculate_win_probability(a_bp, a_cp, a_cc, a_m, e_bp, e_cp, e_cc, e_m):
    # Aがコインを持っていない場合、Eの勝ち
    if a_cc == 0:
        return 0

    # Eがコインを持っていない場合、Aの勝ち
    elif e_cc == 0:
        return 1

    # それ以外の場合、再帰的に勝率を計算
    else:
        ally_skill = skill(a_bp, a_cp, a_cc, a_m)
        enemy_skill = skill(e_bp, e_cp, e_cc, e_m)

        # Allyが勝つ確率
        p_A = match_cal(ally_skill,enemy_skill)
        # Enemyが勝つ確率
        p_E = 1 - p_A

        # Aが勝つ場合
        prob_A_wins = p_A * calculate_win_probability(a_bp, a_cp, a_cc, a_m, e_bp, e_cp, e_cc-1, e_m)
        # Eが勝つ場合
        prob_B_wins = p_E * calculate_win_probability(a_bp, a_cp, a_cc-1, a_m, e_bp, e_cp, e_cc, e_m)
        # 最終的な勝率を計算して返す
        return prob_A_wins + prob_B_wins



def calcutate(ally_data, enemy_data):
    try:
        ally_base_power = int(ally_data[0])
        ally_coin_power = int(ally_data[1])
        ally_coin_count = int(ally_data[2])
        ally_mental     = int(ally_data[3])

        enemy_base_power = int(enemy_data[0])
        enemy_coin_power = int(enemy_data[1])
        enemy_coin_count = int(enemy_data[2])
        enemy_mental     = int(enemy_data[3])

    except ValueError:
        return -2,0


    # コインが0枚以下、精神力が-45~45の範囲外
    if (ally_coin_count < 1) or (enemy_coin_count < 1) or not(-45 <= ally_mental <= 45) or not(-45 <= enemy_mental <= 45):
        # エラー値を返す
        return -1,0


    # 初回マッチ勝率
    ally_skill = skill(ally_base_power, ally_coin_power, ally_coin_count, ally_mental)
    enemy_skill = skill(enemy_base_power, enemy_coin_power, enemy_coin_count, enemy_mental)
    result1 = match_cal(ally_skill,enemy_skill)

    # 最終勝率
    result2 = calculate_win_probability(
        ally_base_power, ally_coin_power, ally_coin_count, ally_mental,
        enemy_base_power, enemy_coin_power, enemy_coin_count, enemy_mental )



    return result1,result2
