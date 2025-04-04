import vlc
import time
import sys

def stream_url(input_url):
    # Define the streaming options
    sout_option = (
        '#transcode{vcodec=h264,vb=800,scale=Auto,acodec=mp4a,ab=128,channels=2,'
        'samplerate=44100,scodec=none}:http{mux=mkv,dst=:8089/} :no-sout-all :sout-keep'
    )

    # Create VLC instance with sout options
    instance = vlc.Instance('--sout', sout_option)

    # Create a media player object
    player = instance.media_player_new()

    # Create media with input URL and sout option
    media = instance.media_new(input_url, f':sout={sout_option}')
    player.set_media(media)

    # Play the media
    player.play()

    print(f"Streaming started from {input_url} to http://localhost:8083/")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping stream...")
        player.stop()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python stream_vlc.py <input_url>")
    else:
        stream_url(sys.argv[1])
