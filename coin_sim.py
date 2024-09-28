""" Limbus Company Coin Simulator """

import math

def binomial_probability(n, k, p):
    """ 二項分布の確率を計算する関数
        n:試行回数  k:成功回数  p:試行1回の成功確率 """
    # リンバスにおいては
    # n:コイン枚数  k:表コイン枚数  p:表面が出る確率
    combination = math.factorial(n) / ( math.factorial(k) * math.factorial(n-k) )
    return combination * (p**k) * ( (1-p) ** (n-k))


class skill:
    """ スキルの最終威力とそれが出る確率の組み合わせを計算 """
    def __init__(
        self,
        base_power  :int,
        coin_power  :int,
        coin_count  :int,
        mental      :int,
    ):

        self.bp = base_power
        self.cp = coin_power
        self.cc = coin_count
        self.men = mental
        self.results =[]
        self.cal_final_power_and_probability()

    def cal_final_power_and_probability(self):
        # コインが表になる確率
        coin_heads_prob = (self.men + 50) / 100

        # 表コインの枚数の組み合わせを生成 表0枚～n枚まで
        heads_counts = range(self.cc + 1)

        # 各組み合わせの最終威力と確率を計算
        self.results = []
        for heads_count in heads_counts:
            # 表0枚の時の最終威力とその確率から表n枚までを計算

            final_power = self.bp + (heads_count * self.cp)
            # 最終威力計算  基礎威力+( 表の枚数 x コイン威力 )

            probability = binomial_probability(self.cc, heads_count, coin_heads_prob)
            # 最終威力が出る確率

            self.results.append( (final_power, probability) )
            # 最終威力とその確率をタプル型でリザルトリストに追加
            # 最終威力とそれが出る確率の組み合わせが全て格納される


def cal_match(ally_skill:skill, enemy_skill:skill):
    """ スキルマッチ1回分の勝率計算 """
    # どちらのコインが破壊されるかの確率
    win_prob = 0
    lose_prob = 0

    for (ally_fp, ally_prob) in ally_skill.results:
        for (enemy_fp, enemy_prob) in enemy_skill.results:

            # 確率
            probability = ally_prob*enemy_prob

            # 勝敗の比較
            if ally_fp > enemy_fp:      # 勝率
                win_prob += probability
            elif ally_fp < enemy_fp:   # 敗率
                lose_prob += probability
            else:
                pass

    # マッチ勝率
    final_probability = win_prob / ( win_prob+lose_prob )

    return final_probability


def cal_win_prob(
        a_bp, a_cp, a_cc, a_m,
        e_bp, e_cp, e_cc, e_m
    ):
    """ 最終勝率計算 """
    if a_cc == 0:
    # Aがコインを持っていない場合、Eの勝ち
        return 0

    elif e_cc == 0:
    # Eがコインを持っていない場合、Aの勝ち
        return 1

    else:
    # それ以外の場合、再帰的に勝率を計算
        ally_skill = skill(a_bp, a_cp, a_cc, a_m)
        enemy_skill = skill(e_bp, e_cp, e_cc, e_m)

        # Allyが勝つ確率
        prob_A = cal_match(ally_skill,enemy_skill)
        # Enemyが勝つ確率
        prob_E = 1 - prob_A

        # Aが勝つ場合
        prob_A_wins = (
            prob_A * cal_win_prob(
                        a_bp, a_cp, a_cc, a_m,
                        e_bp, e_cp, e_cc-1, e_m
            )
        )

        # Eが勝つ場合
        prob_B_wins = (
            prob_E * cal_win_prob(
                        a_bp, a_cp, a_cc-1, a_m,
                        e_bp, e_cp, e_cc, e_m
            )
        )

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
    if (
        (ally_coin_count < 1)  or
        (enemy_coin_count < 1) or
        not(-45 <= ally_mental <= 45) or
        not(-45 <= enemy_mental <= 45)
    ):
        # エラー値を返す
        return -1,0


    # 初回マッチ勝率
    ally_skill = skill(
        ally_base_power,
        ally_coin_power,
        ally_coin_count,
        ally_mental
    )
    enemy_skill = skill(
        enemy_base_power,
        enemy_coin_power,
        enemy_coin_count,
        enemy_mental
    )
    result1 = cal_match(ally_skill,enemy_skill)

    # 最終勝率
    result2 = cal_win_prob(
        ally_base_power, ally_coin_power, ally_coin_count, ally_mental,
        enemy_base_power, enemy_coin_power, enemy_coin_count, enemy_mental
    )




    return result1,result2
