# scrabble-wordscore-api
A simple api built with Flask to determine the score of a given word in Scrabble.
Using the file `acceptable_words.txt` which was obtained from [here](https://raw.githubusercontent.com/jmlewis/valett/master/scrabble/sowpods.txt), to determine the validity of words, and using the Scrabble scoring definition obtain from here [here](http://www.wordfind.com/scrabble-letter-values/) to score the valid words.

## Installation and Usage

First make sure you have [Python 2.7](https://www.python.org/download/releases/2.7/) then the latest version of [Flask](http://flask.pocoo.org/) and clone the project. Then:

```sh
$ cd scrabble-wordscore-api
```

Start the Flask server:

```sh
$ python word_score_server.py
```

To determine the score of a <word> in Scrabble, make a `GET` request to the following url:

```sh
http://localhost:8000/wordscore/<word>
```

## Example
If you want to determine the score of the word **hello** (case does not matter):

```sh
curl -i http://localhost:8000/wordscore/hello
```
##### Successful Response:
* **Code:** 200
    **Content-Type:** `application/json`
    **Content:** `{ "word" : "hello", "valid": true, "score": 8 }`
OR
* **Code:** 200
    **Content-Type**: `application/json`
    **Content:** `{ "word" : <invalid_word>, "valid": false }`
##### Failed Response:
* **Code:** 400
* **Content-Type:** `application/json`
    **Content:** `{ "error": "Not found, must be http://localhost:8000/wordscore/<word>" }`
