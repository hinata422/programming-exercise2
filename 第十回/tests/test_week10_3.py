import pytest


@pytest.fixture
def pre(capsys):
    from week10_3 import GraphWalk
    fi = open('kyotocitybus_line.dat', 'r', encoding = 'utf-8')
    bus_network = GraphWalk()
    lines = fi.readlines()
    for line in lines:
        line = line.rstrip()
        items = line.split(' ')  # 1行を半角スペースで区切ってitemsリストに代入
        bus_network.add_undirected_edge(items[0], items[1], items[3])  # 無向エッジを追加
    fi.close()
    yield bus_network, capsys


def test_week10_3_walk(pre):
    pre[0].walk_along_route('ED01_1914', 5, '快速202号系統')
    captured = pre[1].readouterr()
    assert captured.out == '''ED01_1914 --[快速202号系統]--> ED01_1936 --[快速202号系統]--> ED01_1927 --[快速202号系統]--> ED01_1883 --[快速202号系統]--> ED01_1930 --[快速202号系統]--> ED01_1742
''', '標準出力が異なる'


def test_week10_3_walk_invalid_start(pre):
    pre[0].walk_along_route('ED01_0000', 5, '快速202号系統')
    captured = pre[1].readouterr()
    assert captured.out == '''ED01_0000のノードがグラフ上に存在しません。
''', '標準出力が異なる'


def test_week10_3_walk_invalid_route(pre):
    pre[0].walk_along_route('ED01_1914', 5, '1号系統')
    captured = pre[1].readouterr()
    assert captured.out == '''1号系統ではED01_1914から5ステップ分進むパスはありません。
''', '標準出力が異なる'


def test_week10_3_walk_over_step(pre):
    pre[0].walk_along_route('ED01_1914', 100, '快速202号系統')
    captured = pre[1].readouterr()
    assert captured.out == '''快速202号系統ではED01_1914から100ステップ分進むパスはありません。
''', '標準出力が異なる'
