from utils.utils import get_database_as_sentences
from chess import Move, Board

pgn_filepath = "chess_data/temp.pgn"
# text_filepath = "nlp_data/temp.txt"
# vocab_filepath = "nlp_data/vocab.json"

sents, vocab = get_database_as_sentences(pgn_filepath)

unigram_counts = {}
bigram_counts = {}
trigram_counts = {}

for sent in sents:
    corpus = sent.split(' ')
    size = len(corpus)

    for i in range(size):
        unigram = corpus[i]
        if(unigram in unigram_counts):
            unigram_counts[unigram] += 1
        else:
            unigram_counts[unigram] = 1
    
    for i in range(size - 1):
        bigram = (corpus[i], corpus[i+1])
        if(bigram in bigram_counts):
            bigram_counts[bigram] += 1
        else:
            bigram_counts[bigram] = 1

    for i in range(size - 2):
        trigram = (corpus[i], corpus[i+1], corpus[i+2])
        if(trigram in trigram_counts):
            trigram_counts[trigram] += 1
        else:
            trigram_counts[trigram] = 1

def get_next_best_move(board: Board, moves_played: int, unigram_counts: dict, bigram_counts: dict, trigram_counts: dict) -> Move:
    legal_moves = []
    size = moves_played

    last_move = board.pop() if (size >= 1) else None 
    second_last_move = board.pop() if (size >= 2) else None 
    for move in (second_last_move, last_move):
        if(move): board.push(move)

    for move in board.generate_legal_moves():
        word1 = move.uci()
        if(size == 0):
            # word1
            prob = (unigram_counts.get(word1,0)+1) / (len(unigram_counts)+1)
            legal_moves.append((prob, move))
        elif(size == 1):
            # word2 | word1
            word2 = last_move.uci()
            prob = (bigram_counts.get((word2, word1), 0) + 1) / (unigram_counts.get(word2,0) + 1)
            legal_moves.append((prob, move))
        else:
            # word3 | word2 | word1
            word2 = last_move.uci()
            word3 = second_last_move.uci()
            prob = (trigram_counts.get((word3, word2, word1),0) + 1) / (bigram_counts.get((word3, word2),0) + 1)
            legal_moves.append((prob, move))

    assert(len(legal_moves))

    legal_moves.sort(key=lambda x: x[0], reverse = True)
    return legal_moves[0][1]

board = Board()
moves_played = 0
print(board)
print()
while(not board.is_game_over()):
    if(board.turn):
        # move = Move.from_uci(input().strip().lower())
        move = get_next_best_move(board, moves_played, unigram_counts, bigram_counts, trigram_counts)
        assert (move in board.legal_moves), "Illegal Move"
        board.push(move)
    else:
        move = get_next_best_move(board, moves_played, unigram_counts, bigram_counts, trigram_counts)
        assert (move in board.legal_moves), "Illegal Move"
        board.push(move)
    moves_played += 1
    print(board)
    print()

print(board.xboard)