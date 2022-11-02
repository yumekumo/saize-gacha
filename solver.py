import pandas as pd
import pulp

df = pd.read_csv('menu.csv')

# 最適化に用いる定数
name = df.set_index('id')['name'].to_dict()
price = df.set_index('id')['price'].to_dict()
calorie = df.set_index('id')['calorie'].to_dict()
salt = df.set_index('id')['salt'].to_dict()

total_price = 1000
max_order = 10

prob = pulp.LpProblem("Saize", pulp.LpMaximize)

# 変数 x : 商品の選択数
x = pulp.LpVariable.dicts('x', df['id'], lowBound = 0, cat='Integer')

# 目的関数
prob += pulp.lpSum([x[i] * calorie[i] for i in x.keys()])

# 制約
prob += pulp.lpSum([x[i] * price[i] for i in x.keys()]) <= total_price

for i in x.keys():
    prob += x[i] <= max_order

sol = prob.solve()
# 解けているかの確認
print('Status', pulp.LpStatus[sol])
# 最適解を確認
print(pulp.value(prob.objective))

for i in x.keys():
    if x[i].value() > 0:
        print(name[i], int(x[i].value()))

