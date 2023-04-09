from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context

from camera import Streamer

app = Flask( __name__ )
streamer = Streamer()

@app.route('/stream')
def stream():
    
    src = request.args.get( 'src', default = 0, type = int )
    
    try :
        print('before send response')
        return Response(
                    stream_with_context( stream_gen( src ) ),
                    mimetype='multipart/x-mixed-replace; boundary=frame'
                    )
        
        print('after send response')
    except Exception as e :
        
        print('[wandlab] ', 'stream error : ',str(e))

def stream_gen( src ):
  
    try :
        
        streamer.run( src )
        
        while True :
            
            frame = streamer.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #print(frame)
    except GeneratorExit :
        #print( '[wandlab]', 'disconnected stream' )
        streamer.stop()
