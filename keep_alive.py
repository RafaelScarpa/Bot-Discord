from flask import Flask,render_template
from threading import Thread

app=Flask('Scarpa Bot')

@app.route('/')
def main():
  return render_template('homepage.html')

@app.route('/wordpress/wp-login.php')
def idk():
  print('El señor Comédia.')
  return render_template('lol.html')
  

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server=Thread(target=run)
  server.start()