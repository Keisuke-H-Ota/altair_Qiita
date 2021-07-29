import datetime
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

st.title('Altair ギャラリー')
st.markdown('このサイトには[【Python】データ可視化ライブラリ Altair を使いこなす](https://qiita.com/keisuke-ota/items/aa93f45b3a9fc520541d)で作成した図を掲載する。それぞれの図にカーソルで触れて自由に動かしてみよう。')

# クロスセクションデータの作成

np.random.seed(1)## 乱数の固定

n = 300 ## 学生の人数
s = np.random.normal(55,10,n) ## 学生の学力（score）
c = np.random.randint(0,3,n) ## クラス
s = s * (1 + c * 0.015) ## クラスの学力差をつける
g = np.random.randint(0,2,n) ## 性別

## 得点データの生成
s1 = np.random.uniform(0.75,1.1,n) * s * (1 + g * 0.02)
s2 = np.random.uniform(0.9,1.1,n) * s * (1 - g * 0.05)
s3 = np.random.uniform(0.9,1.05,n) * s * (1 + g * 0.03)
s4 = np.random.uniform(0.9,1.2,n) * s * (1 - g * 0.02)
s5 = np.random.uniform(0.8,1.1,n) * s * (1 + g * 0.01)

sex = ['男','女'] ## 性別
cl = ['普通','理数','特進'] ## クラス
sub = ['国語','数学','理科','社会','英語'] ## 教科

df = pd.DataFrame()
df['学生番号'] = list(map(lambda x: 'ID'+str(x).zfill(3), range(1,1+n)))
df['国語'] = list(map(lambda x: round(x), s1))
df['数学'] = list(map(lambda x: round(x), s2))
df['理科'] = list(map(lambda x: round(x), s3))
df['社会'] = list(map(lambda x: round(x), s4))
df['英語'] = list(map(lambda x: round(x), s5))
df['合計'] = df['国語'] + df['数学'] + df['社会'] + df['理科'] + df['英語']
df['クラス'] = list(map(lambda x: cl[x], c))
df['性別'] = list(map(lambda x: sex[x], g))
print(df.head(10))

mdf = pd.melt(df.drop('合計',axis=1),id_vars=['学生番号','性別','クラス'],var_name="科目",value_name="得点")

st.markdown('# クロスセクションデータの可視化')

scatter = alt.Chart(df).mark_circle(
        size=30
        ).encode(
        x=alt.X('国語',
            scale=alt.Scale(
                domain=[0,100]
                ),
            axis=alt.Axis(
                labelFontSize=15, 
                ticks=True, 
                titleFontSize=18, 
                title='国語の得点')
            ),
        y=alt.Y('数学',
            scale=alt.Scale(
                domain=[0, 100]
                ),
            axis=alt.Axis(labelFontSize=15, 
                ticks=True, 
                titleFontSize=18, 
                title='数学の得点')
            ),
        column=alt.Column('クラス',
            header=alt.Header(
                labelFontSize=15, 
                titleFontSize=18), 
            sort = alt.Sort(
                cl
                ), 
            title='クラス'
            ),
        color=alt.Color('性別', 
            scale=alt.Scale(
                domain=sex,
                range=['blue', 'red']
                ),
            ),
        tooltip=['国語', '数学'],
    ).properties(
        width=300,
        height=300,
        title="国語と数学の得点分布"
    ).interactive()

st.markdown('## 散布図')
st.write(scatter)

scatter = alt.Chart(df).mark_point(
        filled=True, 
        size=200,
        opacity=0.7
    ).encode(
        x=alt.X(
            'mean(合計):Q',
            scale=alt.Scale(
                domain=[0,500]
                ),
            axis=alt.Axis(
                title='合計得点の平均'
                )
            ),
        y=alt.Y(
            'stdev(合計):Q',
            scale=alt.Scale(
                domain=[0,100]
                ),
            axis=alt.Axis(
                title='合計得点の標準偏差'
                )
            ),
        color=alt.Color('性別', 
            scale=alt.Scale(
                domain=sex,
                range=['blue', 'red']
                )
            )
    )

st.markdown('## 散布図（統計量の表示）')
st.write(scatter)

histgram = alt.Chart(df).mark_bar(opacity=0.5).encode(
    x=alt.X("合計", 
        bin=alt.Bin(
            step=10,
            extent=[0,500]
            ),
        axis=alt.Axis(
            labelFontSize=15, 
            ticks=True, 
            titleFontSize=18, 
            title='得点の分布'
            )
        ),
    y=alt.Y('count(合計)',
        axis=alt.Axis(
            labelFontSize=15, 
            ticks=True, 
            titleFontSize=18,
            title='人数'
            ),
        stack=None
        ),
    color=alt.Color('性別', 
            scale=alt.Scale(
                domain=sex,
                range=['blue','red']
                ),
            ),
    ).properties(
    width=600,
    height=500
    ).interactive()

st.markdown('## ヒストグラム')
st.write(histgram)

corr = df[sub].corr()
corr = pd.melt(corr.reset_index(),id_vars="index",var_name="科目",value_name="相関係数" )
heatmap = alt.Chart(corr).mark_rect().encode(
    x=alt.X(
        'index:O',
        sort=sub,
        axis=alt.Axis(
            labelFontSize=20, 
            ticks=True, 
            titleFontSize=20, 
            title='科目',
            labelAngle=0
            )
        ),
    y=alt.Y('科目:O',
        sort=sub, 
        axis=alt.Axis(
            labelFontSize=20, 
            ticks=True, 
            titleFontSize=20, 
            title='科目',
            labelAngle=0
            )
        ),
    color=alt.Color('相関係数:Q',
        scale=alt.Scale(
            domain=[0.8,1]
            )
        ),
    tooltip=['相関係数']
    ).properties(
    width=400,
    height=400
    ).interactive()

st.markdown('## ヒートマップ')
st.write(heatmap)

## 入力データは雑然データ df ではなく整然データ mdf であることに注意
violin = alt.Chart(mdf).transform_density('得点',
        as_=['得点', 'density'],
        extent=[0, 100],
        groupby=['科目']
    ).mark_area(orient='horizontal').encode(
        x=alt.X(
            'density:Q',
            stack='center',
            impute=None,
            title=None,
            axis=alt.Axis(
                labels=False, 
                values=[0],
                grid=False, 
                ticks=True
                )
            ),
        y='得点:Q',
        color='科目:N',
        column=alt.Column(
            '科目:N',
            header=alt.Header(
                titleOrient='bottom',
                labelOrient='bottom',
                labelPadding=0,
                labelFontSize=15, 
                titleFontSize=18
            ),
        )
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    ).properties(
        width=100,
        height=300
    ).interactive()

st.markdown('## ヴァイオリンプロット')
st.write(violin)

step = 50
overlap = 1

ridgeline = alt.Chart(mdf).transform_bin(
    as_ = 'ビン', field = '得点', bin=alt.Bin(step=5,extent=[0,100])
).transform_aggregate(
    y_axis='count()', groupby=['科目', 'ビン']
).transform_impute(
    impute='y_axis', groupby=['科目'], key='ビン', value=0, keyvals=[0,100]
).mark_area(
    interpolate="monotone", fillOpacity=0.6, stroke="lightgray", strokeWidth=0.5
).encode(
    alt.X('ビン:Q', title='得点',axis=alt.Axis(grid=False),scale=alt.Scale(domain=[0,100])),
    alt.Y('y_axis:Q',stack=None, title=None, axis=None,
        scale=alt.Scale(range=[step, - step * overlap])
        ),
    alt.Fill(
        "科目:N",
        legend=None
    ),
    alt.Row(
        "科目:N",
        title=None,
        header=alt.Header(labelAngle=0,labelAlign='left')
    )
).properties(
    bounds='flush',
    width=400, 
    height=int(step)
).configure_facet(
    spacing=0
).configure_view(
    stroke=None
).configure_title(
    anchor="end"
)

st.markdown('## リッジラインプロット')
st.write(ridgeline)

point = alt.Chart().mark_point().encode(
    x=alt.X('性別', 
        axis=alt.Axis(
            labelFontSize=20, 
            ticks=True, 
            titleFontSize=20, 
            grid=False,
            labelAngle=0
            ),
        sort=sex
        ),
    y=alt.Y('得点:Q', 
        aggregate='mean', 
        axis=alt.Axis(
            labelFontSize=20, 
            ticks=True, 
            titleFontSize=20, 
            grid=False,
            domain=True
            ),
        scale=alt.Scale(
            domain=[0, 100]
            ),
        ),
    color=alt.Color('性別', 
            scale=alt.Scale(
                domain=sex,
                range=['steelblue','darkorange']
                ),
            ),
    )

bar = alt.Chart().mark_errorbar(
    extent='stderr',
    ticks=True,
    orient='vertical'
    ).encode(
    x=alt.X('性別', 
        axis=alt.Axis(
            labelFontSize=20, 
            ticks=True, 
            titleFontSize=20, 
            grid=False,
            labelAngle=0
            ),
        sort=sex
        ),
    y=alt.Y('得点:Q', 
        axis=alt.Axis(
            labelFontSize=20, 
            ticks=True, 
            titleFontSize=20, 
            grid=False,
            domain=True
            ),
        scale=alt.Scale(
            domain=[0, 100]
            ),
        ),
    color=alt.Color('性別', 
            scale=alt.Scale(
                domain=sex,
                range=['steelblue','darkorange']
                ),
            ),
    )

chart = alt.layer(point, bar, data=mdf
    ).properties(
        width=60,
        height=300
    ).facet(
    column=alt.Column('科目', 
        header=alt.Header(
            labelFontSize=20, 
            titleFontSize=20
            )
        ),
    row = alt.Row('クラス', 
        header=alt.Header(
            labelFontSize=20, 
            titleFontSize=20
            )
        )
    ).interactive()

st.markdown('## 図の重ね合わせ')
st.write(chart)

genre_dropdown = alt.binding_select(options=cl)
genre_select = alt.selection_single(fields=['クラス'], bind=genre_dropdown, name="class", init={'クラス': cl[0]})

chart = alt.layer(point, bar, data=mdf ## point と bar は layered.html のものと共通
    ).properties(
        width=60,
        height=300
    ).add_selection(
        genre_select
    ).transform_filter(
        genre_select
    ).facet(
    column=alt.Column('科目', 
        header=alt.Header(
            labelFontSize=20, 
            titleFontSize=20
            )
        )
    ).interactive()

st.markdown('## プルダウンによる図の切替')
st.write(chart)

mdf_mean = mdf.groupby(['科目','クラス']).mean().reset_index()
mdf_std = mdf.groupby(['科目','クラス']).std().reset_index()
mdf_agg = pd.merge(mdf_mean,mdf_std,on=['科目','クラス'],suffixes=('（平均）', '（標準偏差）'))

selector = alt.selection_single(empty='all', fields=['科目'])
color_scale = alt.Scale(domain=cl,
                        range=['#1FC3AA','#4682b4','#8624F5'])

points = alt.Chart(mdf_agg).mark_point(filled=True, size=200).encode(
    x=alt.X('得点（標準偏差）',
            scale=alt.Scale(
                domain=[5,15]
                )
            ),
    y=alt.Y('得点（平均）',
            scale=alt.Scale(
                domain=[40,70]
                )
            ),
    color=alt.condition(selector,
                        'クラス',
                        alt.value('lightgray'),
                        scale=color_scale),
    tooltip=['科目','クラス']
    ).add_selection(
    selector
    )

hists = alt.Chart(mdf).mark_bar(opacity=0.5, thickness=100).encode(
    x=alt.X('得点',
            bin=alt.Bin(step=5), ## step keeps bin size the same
            scale=alt.Scale(domain=[0,100])),
    y=alt.Y('count()',
            stack=None,
            scale=alt.Scale(domain=[0,120])),
    color=alt.Color('クラス',
                    scale=color_scale)
).transform_filter(
    selector
)

st.markdown('## プルダウンによる図の切替')
st.write(points|hists)

points = alt.Chart(mdf_agg).mark_point(filled=True, size=200).encode(
    x=alt.X('得点（標準偏差）',
            scale=alt.Scale(
                domain=[5,15]
                )
            ),
    y=alt.Y('得点（平均）',
            scale=alt.Scale(
                domain=[40,70]
                )
            ),
    color=alt.condition(selector,
                        'クラス',
                        alt.value('lightgray'),
                        scale=color_scale),
    tooltip=['科目','クラス']
    ).add_selection(
    selector
    )

stripplot = alt.Chart(mdf).mark_circle(size=8).encode(
    x=alt.X(
        'jitter:Q',
        title=None,
        axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
        scale=alt.Scale(),
    ),
    y=alt.Y('得点:Q'),
    color=alt.condition(selector,
                        'クラス',
                        alt.value('lightgray'),
                        scale=color_scale),
    column=alt.Column('クラス', 
        header=alt.Header(
            labelFontSize=20, 
            titleFontSize=20
            )
        )
    ).transform_filter(
        selector
    ).transform_calculate(
        ## Generate Gaussian jitter with a Box-Muller transform
        jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
    ).properties(
        width=50
    )

st.markdown('## ジッタープロット')
st.write(points|stripplot)

ID = df['学生番号'].values.tolist()

genre_dropdown = alt.binding_select(options=ID)
genre_select = alt.selection_single(fields=['学生番号'], bind=genre_dropdown, name="ID", init={'学生番号': ID[0]})

brush = alt.selection(type='interval', encodings=['x'])

bars = alt.Chart().mark_bar().encode(
        x = alt.X('科目:O'),
        y = alt.Y('得点:Q',scale=alt.Scale(domain=[0,100])),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7))
    ).add_selection(
        brush
    ).add_selection(
        genre_select
    ).transform_filter(
        genre_select
    )

line = alt.Chart().mark_rule(color='firebrick').encode(
    y = alt.Y('mean(得点):Q',scale=alt.Scale(domain=[0,100]),title='得点（赤線は各科目の平均）'),
    size=alt.SizeValue(3)
).transform_filter(
    genre_select
).transform_filter(
    brush
)

chart = alt.layer(bars,line,data=mdf).properties(
        width=200,
        height=400
    )

st.markdown('## 棒グラフ')
st.write(chart)

brush = alt.selection(type='interval')

select_scatter = alt.Chart(df).mark_circle(
        size=30
        ).encode(
        x=alt.X('国語',
            scale=alt.Scale(domain=[0,100]),
            axis=alt.Axis( title='国語の得点')
            ),
        y=alt.Y('数学',
            scale=alt.Scale(domain=[0, 100]),
            axis=alt.Axis( title='数学の得点')
            ),
        color=alt.Color('性別', 
            scale=alt.Scale(
                domain=sex,
                range=['blue', 'red']
                ),
            ),
        tooltip=['国語', '数学'],
    ).properties(
        width=300,
        height=300,
        title="国語と数学の得点分布"
    ).add_selection(
        brush
    ).properties(
        width=350,
        height=300
    )

selected_bars = alt.Chart(df).mark_bar().encode(
    y='クラス:N',
    color=alt.Color('性別', 
            scale=alt.Scale(
                domain=sex,
                range=['blue', 'red']
                ),
            ),
    x=alt.X('count(クラス):Q',title='人数',scale=alt.Scale(domain=[0, 110]))
    ).transform_filter(
        brush
    ).properties(
        width=350,
        height=50
    )

chart = alt.vconcat(select_scatter, selected_bars, data=df)

st.markdown('## 散布図と棒グラフの連携')
st.write(chart)

# 時系列データの作成

np.random.seed(1) # 乱数の固定

goods_list = ['商品A','商品B','商品C'] # 調査対象の商品
sex_list = ['男','女']

t = [] # 時刻リスト
g = [] # 商品リスト
a = [] # 年齢リスト
s = [] # 性別リスト

# 2000 年の元日からの 1 年間でシミュレーションを行う。
time = datetime.datetime(2000, 1, 1, 0)

while time.year == 2000:
    # 顧客の来店をガンマ分布でシミュレーション
    # 冬に来客数が増えるように調整
    gamma = 0.5 * (12-abs(time.month-6)) 
    time += datetime.timedelta(
        hours = np.round(np.random.gamma(gamma)
            )
        )
    ## 営業時間を 9:00 ~ 21:00 とする。
    ## それ以外に来客した場合、来客時間を 12 時間先送りにする。
    if 21 < time.hour or time.hour < 9:
        time += datetime.timedelta(hours = 12)
    t.append(time)

    # 顧客がどの商品を選ぶのかをランダムで決める
    goods = np.random.choice(goods_list, p=[0.6,0.3,0.1])
    g.append(goods)

    # 商品購入者の年齢をシミュレーション
    if goods == '商品A':
        age = np.round(np.random.normal(35,15))
    elif goods == '商品B':
        age = np.round(np.random.normal(50,20))
    else :
        age = np.round(np.random.normal(65,10))
    a.append(age)

    # 商品購入者の性別をシミュレーション
    if goods == '商品A':
        sex = np.random.choice(sex_list, p=[0.75,0.25])
    elif goods == '商品B':
        sex = np.random.choice(sex_list, p=[0.4,0.6])
    else :
        sex = np.random.choice(sex_list, p=[0.2,0.8])
    s.append(sex)

    # 2001 年になったらシミュレーションを終了する。
    if time.year == 2001:
        break

df = pd.DataFrame()
df['来客時間'] = t
df['購入商品'] = g
df['年齢'] = a
df['性別'] = s
df = df[:-1]

st.markdown('# 時系列データの可視化')

line = alt.Chart(df).mark_line().encode(
    x=alt.X('month:O',
        timeUnit='month',
        title='来客月'
        ),
    y=alt.Y('count(購入商品)',
        title='購入数'
        ),
    color='購入商品'
    ).transform_timeunit(
    month='month(来客時間)'
    )

st.markdown('## 折れ線グラフ')
st.write(line)

line = alt.Chart().mark_line().encode(
    x=alt.X('month:O',
        timeUnit='month',
        title='来客月'
        ),
    y=alt.Y('mean(年齢)',
        title='年齢'
        ),
    color='購入商品'
).transform_timeunit(
    month='month(来客時間)'
)

band = alt.Chart().mark_errorband(extent='ci').encode(
    x=alt.X('month:O',
        timeUnit='month',
        title='来客月'
        ),
    y=alt.Y('年齢', 
        title='年齢'
        ),
    color='購入商品'
).transform_timeunit(
    month='month(来客時間)'
)

chart = alt.layer(line,band, data=df)

st.markdown('## 折れ線グラフ（エラーバンドあり）')
st.write(chart)
