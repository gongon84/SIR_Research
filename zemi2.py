
#インポート
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation
import random
import time


# プログラムの実行時間を測る
def get_h_m_s(td):
    m, s = divmod(td, 60)
    h, m = divmod(m, 60)
    return h, m, s


# 関数
def SIR():

    # 定義
    times = 100  # 観測時間
    N = 50  # 人の数(≥ 1)
    I0 = 10  # t=0の感染者数
    R0 = 0  # t=0の回復者数
    recover_time = 20  # 感染してから回復までにかかる時間(≥ 1)
    infection_rate = 0.8  #感染率
    recovery_rate = 0.05  #回復率
    max = 12  # グラフの幅
    min = -12
    speed = 50  #アニメーションの速さ（小さい方が早い）
    wall_is = False  # 壁をつけるかどうか(True or False)
    ims = []  # アニメーションの画像を追加する
    flag_legend = True  # ラベル表示の際に使用
    t_list = [i for i in range(0, times+1)]
    inum_list = [I0]  # ２つ目のグラフ用
    recover_list = [0]
    s_list = [N-I0]

    # 密度
    mitudo = N / (max**2)
    print('密度', mitudo)

    # 人の初期位置（ランダム）
    person_x = [random.randint(min,max) for i in range(N)]
    person_y = [random.randint(min,max) for i in range(N)]

    # 初期の感染者
    # 「方法」ランダムな数字(rand)を取ってきて、rand番目の人を感染させる
    inum = []
    while len(inum) < I0:
        rand = random.randint(0,N-1)
        if not rand in inum:
            inum.append(rand)

    # 回復者
    infect_period = [0]*N  # 感染してからの時間を計測
    remove_list = []  # 回復者をinumから削除する
    recover_num = []

    # 壁
    if wall_is:
        wallx = [-8,-7,-6,-5,-4,-3,-2,-1, 0, 0, 0, 0]
        wally = [-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-4,-5]

    # 初期位置　グラフ表示
    fig = plt.figure(figsize=(9,8))  # グラフを表示する場所を設定
    plt.subplots_adjust(right=0.85, hspace=0.3)  # 右側に余白を追加（ラベル配置のため）
    ax1 = fig.add_subplot(211)  # figの上にax1を設定
    ax1.set_aspect('equal')  # グラフの比を１：１に
    img = ax1.plot(person_x, person_y, marker='.', markersize=20, linestyle='None', color='blue')
    for k in inum:
        img += ax1.plot(person_x[k], person_y[k], marker='.', markersize=20, linestyle='None', color='red')
    for k in recover_num:
        img += ax1.plot(person_x[k], person_y[k], marker='.', markersize=20, linestyle='None', color='green')
    if wall_is:
        img += ax1.plot(wallx, wally, color='green')
    img += [ax1.text(1.2*max, 0.6*min, 't=' + str(0), fontsize='16')]
    img += [ax1.text(1.2*max, 0.2*min, 'N=' + str(N), fontsize='16')]
    img += [ax1.text(1.2*max, 0.8*min, 'S(t)=' + str(N - len(inum)), fontsize='16')]
    img += [ax1.text(1.2*max, min, 'I(t)=' + str(len(inum)), fontsize='16')]
    ims.append(img)  #プロット画像を追加

    # 実行時間の計測
    start = time.time()

    # 観測スタート
    for t in range(times):
        # 表示までの時間をカウント
        if t == times / 2:
            print('{} 残り半分'.format(times - t))
        elif t == times * 3 / 4:
            print('{} 残り４分の１'.format(times - t))
        elif t % 10 == 0:
            print(times - t)

        # 回復者
        # 時間で回復する場合
        # for num in inum:  # 回復してからの時間を記録
        #     infect_period[num] += 1
        #     if infect_period[num] == recover_time:
        #         infect_period[num] = 0
        #         remove_list.append(num)

        # 回復率を設定する場合
        for num in inum:
            rand = random.random()  # 0以上1未満のランダムな数
            if rand <= recovery_rate:
                remove_list.append(num)

        if remove_list:  # 回復者をinumから削除してrecover_listに追加
            for num in remove_list:
                recover_num.append(num)
                inum.remove(num)
            remove_list.clear()

        # 人を順番に動かしていく
        for i in range(N):
            # ランダムウォーク
            ran = random.randint(1,4)
            if ran == 1:
                person_y[i] = person_y[i] + 1
            elif ran == 2:
                person_x[i] = person_x[i] + 1
            elif ran == 3:
                person_y[i] = person_y[i] - 1
            elif ran == 4:
                person_x[i] = person_x[i] - 1

            # 人が端に行ったら折り返す
            if person_x[i] >= max:
                person_x[i] -= 1
            elif person_y[i] >= max:
                person_y[i] -= 1
            elif person_x[i] <= min:
                person_x[i] += 1
            elif person_y[i] <= min:
                person_y[i] += 1

            # 壁にぶつかったときに戻る
            if wall_is:
                # 外から
                if ran == 4 and person_x[i] == 0 and -5 <= person_y[i] <= -2:
                    person_x[i] += 1
                elif ran == 3 and person_y[i] == -2 and person_x[i] <= 0:
                    person_y[i] += 1
                # 内から
                elif ran == 2 and person_x[i] == 0 and -5 <= person_y[i] <= -2:
                    person_x[i] -= 1
                elif ran == 1 and person_y[i] == -2 and person_x[i] <= 0:
                    person_y[i] -= 1

            # 未感染者が感染者と重なったとき感染率に従って感染する
            if not i in inum and not i in recover_num:
                rand = random.random()  # 0以上1未満のランダムな数
                if rand <= infection_rate:
                    for k in inum:
                            if person_x[i] == person_x[k] and person_y[i] == person_y[k] and i != k:
                                inum.append(i)

        # グラフのプロット「未感染者、感染者、壁」
        # 未感染者
        img = ax1.plot(person_x, person_y, marker='.', markersize=18, linestyle='None', color='blue', label='Susceptible')
        # 感染者
        for k in inum:
            img += ax1.plot(person_x[k], person_y[k], marker='.', markersize=18, linestyle='None', color='red', label='Infected')
            # ラベルを１回だけ表示（for文での繰り返しを防ぐ）
            if flag_legend:
                if wall_is:
                    img += ax1.plot(wallx, wally, color='grey', label='Wall')
                # Recoverdのラベルを表示するため
                img += ax1.plot(10+max, 10+max, marker='.', markersize=18, linestyle='None', color='green', label='Recovered')
                ax1.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
                flag_legend = False
        # 回復者
        for k in recover_num:
            img += ax1.plot(person_x[k], person_y[k], marker='.', markersize=18, linestyle='None', color='green')
        # 壁
        if wall_is:
            img += ax1.plot(wallx, wally, color='grey', label='wall')
        # ラベル
        img += [ax1.text(1.3*max, 0.1*min, 't     =' + str(t+1), fontsize='16')]
        img += [ax1.text(1.3*max, 0.4*min, 'N    =' + str(N), fontsize='16')]
        img += [ax1.text(1.3*max, 0.6*min, 'S(t) =' + str(N - len(inum) - len(recover_num)), fontsize='16')]
        img += [ax1.text(1.3*max, 0.8*min, 'I(t)  ='+str(len(inum)), fontsize='16')]
        img += [ax1.text(1.3*max, min, 'R(t)  =' + str(len(recover_num)), fontsize='16')]

        # タイトル、軸
        ax1.set_title("SIR Model  --Random Walk--", size=14)
        ax1.set_xticks(np.arange(min, max+1))
        ax1.set_yticks(np.arange(min, max+1))
        ax1.set_xlim(min, max+1)
        ax1.set_ylim(min, max+1)
        # 目盛りなし
        ax1.xaxis.set_major_locator(mpl.ticker.NullLocator())
        ax1.yaxis.set_major_locator(mpl.ticker.NullLocator())

        # アニメーション使用する画像を追加
        ims.append(img)

        # グラフ２つ目用
        inum_list.append(len(inum))
        recover_list.append(len(recover_num))
        s_list.append(N - len(inum) - len(recover_num))

    # ２つ目のグラフ
    ax2 = fig.add_subplot(212)
    ax2.plot(t_list, s_list, color='blue')  # 未感染者
    ax2.plot(t_list, inum_list, color='red')  # 感染者
    ax2.plot(t_list, recover_list, color='green')  # 回復者
    ax2.set_title('Changes in Number of Infected People', size=14)
    ax2.set_ylim(0, N)

    # 実行時間の計測
    end = time.time()
    h, m, s = get_h_m_s(int(end - start))
    print('実行時間:{}h{}m{}s'.format(h,m,s))

    # アニメーション開始
    ani = animation.ArtistAnimation(fig, ims, interval=speed, repeat=False)
    plt.show()


if __name__ == '__main__':

    SIR()