import project
import pytest
import os


def test_get_sale_puzzle_info_empty_dict():
    with pytest.raises(SystemExit):
        project.get_sale_puzzle_info({})

def test_get_sale_puzzle_info():
    test = project.get_sale_puzzle_info({"buffalo": "https://buffalogames.com/sale/"})
    assert len(test) > 0

def test_store_puzzle_info_error():
    with pytest.raises(SystemExit):
        project.store_puzzle_info([])

def test_store_puzzle_info():
    assert os.path.exists("list_of_puzzles.csv")

def test_get_piece_count():
    assert project.get_piece_count("Eric Dowdle: Christmas Morning 300 Piece Puzzle") == "300 Pieces"

def test_get_piece_count_no_count():
    assert project.get_piece_count("Eric Dowdle: Christmas Morning") == "piece count unavailable"
