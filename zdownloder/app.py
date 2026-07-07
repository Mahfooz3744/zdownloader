from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        quality = request.form.get('quality', 'best')
        
        if not url:
            return "URL daal na bhai!"
        
        # Download options
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
        }
        
        if quality != 'best' and quality.isdigit():
            ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
        
        try:
            os.makedirs('downloads', exist_ok=True)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            return send_file(filename, as_attachment=True)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)