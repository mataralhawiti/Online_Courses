from bottle import route, run, template

@route('/')		# static route
def main():
	return ('welcome to my first web app using Bottle framework')


@route('/hello') 	# static route
def hello():
	return("Hello world :) ")


@route('/hello/<name>')		# dynamic route '<angle bracket>'
def greet(name = 'Matar'):
	return template('Hello {{name}}, how are you ?', name=name)

run(host='localhost', port=8080, debug=True)