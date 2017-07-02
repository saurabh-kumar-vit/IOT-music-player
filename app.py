from flask import Flask, render_template, request, json, session, redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash, secure_filename
import os, pygame
from Queue import *

app = Flask(__name__)

app.secret_key = 'why would I tell you my secret key?'

mysql = MySQL()

# q = Queue()
q = []
current_song = ''
prev_song = ''
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Music'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

import thread
import threading

lock = threading.Lock()

def remove_elemnt():
    global q
    l = len(q)
    if l < 1:
        return []
    else:
        return q[1:]

def get_top_elemnt():
    global q
    l = len(q)
    if l < 1:
        return None
    else:
        return q[0]

def play_music_thread(temp):
    global q

    from pygame import mixer
    mixer.init()

    while True:

        # print 'random bullshit'
        if (not pygame.mixer.music.get_busy()):
            # print 'in'
            csong = get_top_elemnt()
            q = remove_elemnt()

            # print 'in'
            # print 'cson', csong
            if csong != None:
                # print 'csong', csong
                mixer.music.load(os.path.join('./uploads', csong))
                mixer.music.play()


@app.route("/playSong", methods=['GET'])
def playSong():
    global q, lock
    global current_song

    from pygame import mixer
    mixer.init()

    stopFlag = False
    if request.method == 'GET':
        f = request.args.get('songName')

        print f
        if f == 'stop':
            mixer.music.fadeout(1000)

        elif f == 'queue':
            mixer.music.fadeout(1000)
            q = []

        elif f != 'stop':
            if f != 'queue':
                lock.acquire()
                try:
                    q.append(f)
                finally:
                    lock.release()

        

    return render_template('music.html')

@app.route("/")
def main():
    return render_template('home.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignin')
def showSignin():
    return render_template('login.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('music.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.route('/showUpload')
def showUpload():
    return render_template('upload.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        

        print 'In the Block'
        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        


        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                print "The user session is: " + str(session['user'])
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
            

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return "User account created"

            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()


#Upload Logic test

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
	try:
		if session.get('user'):
			# Get the name of the uploaded file
			file = request.files['file']
			_user = session.get('user')
			
			conn = mysql.connect()
			cursor = conn.cursor()
			# Check if the file is one of the allowed types/extensions
			if file and allowed_file(file.filename):
				# Make the filename safe, remove unsupported chars
				filename = secure_filename(file.filename)
				# Move the file form the temporal folder to
				# the upload folder we setup
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				cursor.callproc('sp_addsong',(filename,_user))
				data = cursor.fetchall()
		        # Redirect the user to the uploaded_file route, which
		        # will basicaly show on the browser the uploaded file
				if len(data) is 0:
					conn.commit()
					return redirect('/userHome')
				else:
					return render_template('error.html',error = 'An error occurred!')

		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:
		cursor.close()
		conn.close()

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/getSong')
def getSong():
    try:
        if session.get('user'):
            _user = session.get('user')
 
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetSongByUser',(_user,))
            songs = cursor.fetchall()
 
            songs_dict = []
            for song in songs:
                song_dict = {
                        'Id': song[0],
                        'Title': song[1],
                        'Date': song[2]}
                songs_dict.append(song_dict)
 
            return json.dumps(songs_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

if __name__ == "__main__":
    # t = thread.start_new_thread(play_music_thread, ('t', ))  
    t = threading.Thread(target=play_music_thread, args=('play',), name='LockHolder')
    # t.setDaemon(True)
    t.start()
    app.run(host='0.0.0.0', debug=True)
    t.join()