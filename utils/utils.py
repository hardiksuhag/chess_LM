from chess import Move
from chess.pgn import Game, read_game
import io
from tqdm import tqdm
import json

def get_word(move: Move) -> str:
    return move.uci()

def get_sentence(game: Game):
    words = [get_word(move) for move in game.mainline_moves()]
    return ' '.join(words)

def read_database(filepath: str) -> list: # each game confined to a single line
    games = []
    with open(filepath, "r") as rf:
        print(f'\nReading data from {filepath} ...')
        for line in tqdm(rf):
            line = line.strip("\n").strip()
            if(line and line[0]=='1'): # that means a new pgn game has started
                games.append(line)
    return games


def get_database_as_sentences(pgn_filepath: str):
    sentences = list()
    vocab = set()

    print(f'\nParsing pgn ...')
    for move_str in tqdm(read_database(pgn_filepath)):
        pgn = io.StringIO(move_str)
        game = read_game(pgn)
        sentences.append(get_sentence(game))
        for word in sentences[-1].split(' '):
            vocab.add(word)
    
    return (sentences, vocab)
    


def save_database_as_sentences(pgn_filepath: str, text_filepath: str, vocab_filepath: str):
    sentences, vocab = get_database_as_sentences(pgn_filepath)

    print(f'\nWriting sentences to {text_filepath} ...')
    with open(text_filepath, 'w') as wf:
        for sent in tqdm(sentences):
            print(sent, file = wf)
    
    with open(vocab_filepath, "w") as wf:
        print(json.dumps(list(vocab)), file = wf)

