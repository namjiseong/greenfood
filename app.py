from flask import Flask, render_template
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
  return render_template('index.html')
@app.route('/result') # 접속하는 url
def result():
  return render_template('result.html')
if __name__ == '__main__':
    app.run()