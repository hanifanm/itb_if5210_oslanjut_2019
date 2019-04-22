from flask import Flask, request
import subprocess
import random

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

def writeProgram(program, filename_full):
    # WRITE TEMP PROGRAM
    text_file = open(filename_full, "w+")
    text_file.write(program)
    text_file.close()

@app.route('/compile', methods=['POST']) 
def foo():

    # CREATE 30 CHAR RANDOM AS FILENAME
    filename = ''.join(random.choice('0123456789ABCDEF') for i in range(30))
    program = request.json['program']
    language = request.json['lang']

    # EXECUTE PROGRAM
    if(language == 'python'):
      filename_full = "program/" + filename + ".py"
      writeProgram(program, filename_full)
      cmd = ["python", filename_full]
    elif(language == 'javascript'):
      filename_full = "program/" + filename + ".js"
      writeProgram(program, filename_full)
      cmd = ["node", filename_full]
    else:
      cmd = ["echo", "language not supproted"]

    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()


    
    # RETURN
    return out

if __name__ == '__main__':
  app.run(debug=True)