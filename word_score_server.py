from flask import Flask, jsonify, make_response
import mmap

word_score_server = Flask(__name__)


# determine scrabble score of word
def get_word_score(word):

	# source: http://www.wordfind.com/scrabble-letter-values/
	letter_score_map = {'A': 1, 'B': 3, 'C': 3,
						'D': 2, 'E': 1, 'F': 4,
						'G': 2, 'H': 4, 'I': 1,
						'J': 8, 'K': 5, 'L': 1,
						'M': 3, 'N': 1, 'O': 1,
						'P': 3, 'Q': 10, 'R': 1,
						'S': 1, 'T': 1, 'U': 1,
						'V': 4, 'W': 4,	'X': 8,
						'Y': 4, 'Z': 10}

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
		if s.find(word) != -1:
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
		uppercase_word = word.upper()
		if is_valid_scrabble_word(uppercase_word):
			return jsonify({'word': word, 'valid': True, 'score': get_word_score(uppercase_word)})
		else:
			return jsonify({'word': word, 'valid': False})
	except:
		return make_response(jsonify({'error': 'Invalid Request'}), 400)

if __name__ == '__main__':
	word_score_server.run(port=8000)