from flask import Flask, request
import subprocess
import random

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/compile', methods=['POST']) 
def foo():

    # CREATE 30 CHAR RANDOM AS FILENAME
    filename = ''.join(random.choice('0123456789ABCDEF') for i in range(30))
    filename_full = "program/" + filename + ".py"
    program = request.json['program']

    # WRITE TEMP PROGRAM
    text_file = open(filename_full, "w+")
    text_file.write(program)
    text_file.close()
    
    # EXECUTE PROGRAM
    cmd = ["python", filename_full]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    
    # RETURN
    return out

if __name__ == '__main__':
  app.run(debug=True)