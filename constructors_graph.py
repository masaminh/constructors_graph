"""コンストラクターのグラフを作る."""
from graphviz import Digraph
from constructors_data import constructor_ranking, constructor_connect


def main():
    """メイン関数."""
    g = Digraph('G', filename='constructors.gv')

    # クラスタ内のノードに対してランク付けさせるのに必要
    g.attr('graph', newrank='true')

    # クラスタ間でエッジ接続させるのに必要
    g.attr('graph', compound='true')

    # ノードのデフォルトはbox
    g.attr('node', shape='box')

    # 年をラベルとして表示
    for year, _ in constructor_ranking:
        g.node(str(year), label=str(year), shape='none')

    # 処理しやすいように一旦フラットな構造にする
    flat_data = [
        (year, name, rank)
        for year, rankings in constructor_ranking
        for rank, name in rankings
    ]

    # チームごとに(年,順位)のタプルのリストを作る
    teams = {name: [] for _, name, _ in flat_data}

    for year, name, rank in flat_data:
        teams[name].append((year, rank))

    # チームごとにノードとエッジを作る
    for name, rankings in teams.items():
        # cluster_チーム名という形でチームごとの枠を作る
        with g.subgraph(name=f'cluster_{name}') as c:
            # 枠の名前はチーム名にしておく
            c.attr(label=name)
            node_names = []

            # 年ごとのノードを作る
            for year, rank in rankings:
                node_name = f'{name}_{year}'
                c.node(node_name, label=f'{rank}位' if rank > 0 else '-')
                node_names.append(node_name)

            # 1つずらすことでノード間のエッジを作る
            c.edges(zip(node_names[:-1], node_names[1:]))

    # 年単位で位置を揃える
    for year, rankings in constructor_ranking:
        nodes = ', '.join([f'"{name}_{year}"' for _, name in rankings])
        g.body.append('{rank=same; ' + f'"{year}", {nodes}' + '}')

    # クラスタ間でエッジをつなげる
    for tail, head in constructor_connect:
        g.edge(f'{tail[0]}_{tail[1]}', f'{head[0]}_{head[1]}',
               lhead=f'cluster_{head[0]}', ltail=f'cluster_{tail[0]}')

    # 描画
    g.view()


if __name__ == '__main__':
    main()
