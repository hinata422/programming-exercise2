import pytest


@pytest.fixture
def pre(capsys):
    from week10_2 import GraphWalk
    fi = open('kyotocitybus_line.dat', 'r', encoding = 'utf-8')
    bus_network = GraphWalk()
    lines = fi.readlines()
    for line in lines:
        line = line.rstrip()
        items = line.split(' ')  # 1行を半角スペースで区切ってitemsリストに代入
        bus_network.add_undirected_edge(items[0], items[1], items[3])  # 無向エッジを追加
    fi.close()
    yield bus_network, capsys


def test_week10_2_walk(pre):
    pre[0].walk_without_loop('ED01_1914', 5)
    captured = pre[1].readouterr()
    assert captured.out == '''ED01_1914 --[快速202号系統]--> ED01_1936 --[快速202号系統]--> ED01_1927 --[快速202号系統]--> ED01_1883 --[10号系統]--> ED01_1882 --[10号系統]--> ED01_1881
''', '標準出力が異なる'


def test_week10_2_walk_invalid_start(pre):
    pre[0].walk_without_loop('ED01_0000', 5)
    captured = pre[1].readouterr()
    assert captured.out == '''ED01_0000のノードがグラフ上に存在しません。
''', '標準出力が異なる'


def test_week10_2_walk_over_step(pre):
    pre[0].walk_without_loop('ED01_1914', 100)
    captured = pre[1].readouterr()
    assert captured.out == '''ED01_1914から100ステップ分進むパスはありません。
''', '標準出力が異なる'
