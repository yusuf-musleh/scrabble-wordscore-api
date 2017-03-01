from flask import Flask, jsonify, make_response
import mmap

word_score_server = Flask(__name__)


# determine scrabble score of word
def get_word_score(word):

	# source: http://www.wordfind.com/scrabble-letter-values/
	letter_score_map = {'a': 1, 'b': 3, 'c': 3,
						'd': 2, 'e': 1, 'f': 4,
						'g': 2, 'h': 4, 'i': 1,
						'j': 8, 'k': 5, 'l': 1,
						'm': 3, 'n': 1, 'o': 1,
						'p': 3, 'q': 10, 'r': 1,
						's': 1, 't': 1, 'u': 1,
						'v': 4, 'w': 4,	'x': 8,
						'y': 4, 'z': 10}

	score = 0
	for letter in word:
		score += letter_score_map.get(letter)

	return score


# looking up word in list of acceptable scrabble words
# to determine if it is valid
def is_valid_scrabble_word(word):
	# using a string-like object that uses the underlying file instead of reading whole file in memory
	# source: http://stackoverflow.com/questions/4940032/search-for-string-in-txt-file-python
	with open("acceptable_words.txt", "r+b") as f:
		s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
		if s.find(word.upper()) != -1:
			return True
		return False


# return appropriate json error when given a url that doesn't match
@word_score_server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found, must be http://localhost:8000/wordscore/<word>'}), 400)


# handle api GET requests
@word_score_server.route('/wordscore/<string:word>', methods=['GET'])
def wordscore(word):
	try:
		if is_valid_scrabble_word(word):
			return jsonify({'word': word, 'valid': True, 'score': get_word_score(word)})
		else:
			return jsonify({'word': word, 'valid': False})
	except:
		return make_response(jsonify({'error': 'Invalid Request'}), 400)

if __name__ == '__main__':
	word_score_server.run(port=8000)