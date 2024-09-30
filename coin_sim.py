""" Limbus Company Coin Simulator """

import math

def binomial_probability(n, k, p):
    """ 二項分布の確率を計算する関数
        n:試行回数  k:成功回数  p:試行1回の成功確率 """
        # リンバスにおいては
        # n:コイン枚数  k:表コイン枚数  p:表面が出る確率
    combination = math.factorial(n) / ( math.factorial(k) * math.factorial(n-k) )
    return combination * (p**k) * ( (1-p) ** (n-k) )


class skill:
    """ スキルの最終威力とそれが出る確率の組み合わせを計算 """
    def __init__(
        self,
        base_power  :int,
        coin_power  :int,
        coin_count  :int,
        mental      :int,
        paralyze    :int,
    ):

        self.bp  = base_power
        self.cp  = coin_power
        self.cc  = coin_count
        self.men = mental
        self.prz = paralyze

        self.results =[]
        self.cal_final_power_and_probability()

    def cal_final_power_and_probability(self):
        # コインが表になる確率
        coin_heads_prob = (self.men + 50) / 100

        self.results = []
        # 最終威力とそれが出る確率の組み合わせが全て格納されるリスト

        # 麻痺を考慮した補正コイン枚数を算出
        ccc = self.cc - self.prz
        # ccc: correction coin counts  補正コイン枚数
            # 麻痺は裏面固定と同義なので
            # コイン枚数を麻痺の数値分減らす事で組み合わせを計算できる

        if ccc > 0:
        # コイン枚数>麻痺の場合

            heads_counts = range(ccc + 1)
            # 表コインの枚数の組み合わせを生成 表0枚～n枚まで

            # 各組み合わせの最終威力と確率を計算
            for heads_count in heads_counts:

                final_power = self.bp + (heads_count * self.cp)
                # 最終威力計算  基礎威力+( 表の枚数 x コイン威力 )
                if final_power < 0:
                    final_power = 0     # 威力が0以下なら0として判定


                probability = binomial_probability(ccc, heads_count, coin_heads_prob)
                # 最終威力が出る確率

                self.results.append( (final_power, probability) )
                # 最終威力とその確率をタプル型でリザルトリストに追加

        else:
        # 麻痺>=コイン枚数の場合
            self.results.append( (self.bp, 1) )
            # 全てのコインが麻痺によって威力0になる
            # 100%の確率で基礎威力の値が最終威力になる


def cal_match(
        a_bp, a_cp, a_cc, a_men, a_prz,
        e_bp, e_cp, e_cc, e_men, e_prz,
    ):
    """ スキルマッチ1回分の勝率計算 """

    ally_skill = skill(a_bp, a_cp, a_cc, a_men, a_prz)
    enemy_skill= skill(e_bp, e_cp, e_cc, e_men, e_prz)

    # 勝率敗率引分率
    win_prob  = 0
    lose_prob = 0
    draw_prob = 0

    for (ally_fp, ally_prob) in ally_skill.results:
        for (enemy_fp, enemy_prob) in enemy_skill.results:

            # 確率
            probability = ally_prob * enemy_prob

            # 勝敗の比較
            if ally_fp > enemy_fp:          # 勝率
                win_prob += probability
            elif ally_fp < enemy_fp:        # 敗率
                lose_prob += probability
            else:
                pass

    # マッチ勝率
    if a_prz == 0 and e_prz == 0:
        # 麻痺が無ければ引き分けの可能性を消す
        # 永遠に引き分ける可能性を残すと
        # cal_win_probでの再帰計算が終わらないので引き分けの可能性をここで消す
        win_prob  = win_prob / ( win_prob + lose_prob )
        lose_prob = 1 - win_prob
    else:
        # 麻痺があれば次のマッチで麻痺が減る事で
        # 勝率が変わるので引き分けも含めて勝率を出す
        draw_prob = 1 - ( win_prob + lose_prob )


    return win_prob, lose_prob, draw_prob


def cal_win_prob(
        a_bp, a_cp, a_cc, a_men, a_prz,
        e_bp, e_cp, e_cc, e_men, e_prz,
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
        # 今回のマッチ確率
        prob_A, prob_E, prob_d = cal_match(
            a_bp, a_cp, a_cc, a_men, a_prz,
            e_bp, e_cp, e_cc, e_men, e_prz
        )

        # 次のマッチの麻痺値の処理
        if a_prz > 0:
        # コインを振った分だけ麻痺値を減少
            a_prz = a_prz - a_cc
            if a_prz < 0:
            # 麻痺0未満になったら麻痺を0に
                a_prz = 0

        if e_prz > 0:
        # コインを振った分だけ麻痺値を減少
            e_prz = e_prz - e_cc
            if e_prz < 0:
            # 麻痺0未満になったら麻痺を0に
                e_prz = 0


        # マッチでAllyが勝つ場合
        prob_A_wins = (
            prob_A * cal_win_prob(
                        a_bp, a_cp, a_cc  , a_men, a_prz,
                        e_bp, e_cp, e_cc-1, e_men, e_prz,
            )
            # allyが勝つので次のマッチはenemyのコインが1枚減る
        )

        # マッチでEnemyが勝つ場合
        prob_E_wins = (
            prob_E * cal_win_prob(
                        a_bp, a_cp, a_cc-1, a_men, a_prz,
                        e_bp, e_cp, e_cc  , e_men, e_prz,
            )
            # enemyが勝つので次のマッチはallyのコインが1枚減る
        )

        # マッチで引き分ける場合
        if prob_d != 0:
            # 引き分ける時だけ計算する
            # cal_matchは麻痺が1以上の時だけ引き分けの確率を出す
            prob_draw = (
                prob_d * cal_win_prob(
                            a_bp, a_cp, a_cc, a_men, a_prz,
                            e_bp, e_cp, e_cc, e_men, e_prz,
                )
                # 引き分けるのでコインは減らない
            )
        else:
            prob_draw = prob_d


        # 最終的な勝率を計算して返す
        return prob_A_wins + prob_E_wins + prob_draw



def calcutate(ally_data, enemy_data):
    """ bp, cp, cc, men, prz """
    try:
        ally_base_power = int(ally_data[0])
        ally_coin_power = int(ally_data[1])
        ally_coin_count = int(ally_data[2])
        ally_mental     = int(ally_data[3])
        ally_paralyze   = int(ally_data[4])

        enemy_base_power = int(enemy_data[0])
        enemy_coin_power = int(enemy_data[1])
        enemy_coin_count = int(enemy_data[2])
        enemy_mental     = int(enemy_data[3])
        enemy_paralyze   = int(enemy_data[4])

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
    win_prob, lose_prob, draw_prob = cal_match(
        ally_base_power, ally_coin_power, ally_coin_count, ally_mental, ally_paralyze,
        enemy_base_power, enemy_coin_power, enemy_coin_count, enemy_mental, enemy_paralyze,
    )

    if draw_prob == 0:
        first_probability = win_prob
    else:
        # 引き分けの確率があるならそれを消して勝率を収束させる
        first_probability  = win_prob / ( win_prob + lose_prob )


    # 最終勝率
    final_probability = cal_win_prob(
        ally_base_power, ally_coin_power, ally_coin_count, ally_mental, ally_paralyze,
        enemy_base_power, enemy_coin_power, enemy_coin_count, enemy_mental, enemy_paralyze,
    )


    return first_probability, final_probability


# 動作テスト
if __name__ == '__main__':
    #       (基礎威力, コイン威力, コイン数, 精神力, 麻痺)
    ally  = ( 5, 1, 3, 0, 0 )
    enemy = ( 5, 1, 4, 0, 3 )

    result = calcutate(ally,enemy)
    print(
        f"初回勝率:{result[0]}\n"
        f"最終勝率:{result[1]}"
    )
