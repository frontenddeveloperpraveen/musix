from flask import Flask, request, send_file, render_template
import pytube
import ffmpeg
import scrapetube
import shutil
app = Flask(__name__)
@app.route('/')
def Home():
    return render_template('Home.html')
@app.route('/download', methods=['GET'])
def download():
    try:
        try:
            shutil.rmtree('Audio')
        except: pass
        video_url = request.args.get('url')
        with open('name.txt','a+') as f:
            f.write(video_url + '\n')
        file = video_url.replace(' ','+')
        videos = scrapetube.get_search((file+'+song'))
        for video in videos:
            link = (video['videoId'])
            break
        video_url = f'https://www.youtube.com/watch?v={link}'
        yt = pytube.YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download('Audio')
        video_filename = audio_stream.default_filename
        ffmpeg.input(filename=f'Audio/{video_filename}', y='').output(f'Audio/{video_filename}', acodec='libmp3lame').run()
    except: 
        pass
    mimetype = 'audio/mpeg'
    return send_file(f'Audio/{video_filename}', as_attachment=True, download_name=video_filename, mimetype=mimetype)
if __name__ == '__main__':
    app.run(debug=True)
