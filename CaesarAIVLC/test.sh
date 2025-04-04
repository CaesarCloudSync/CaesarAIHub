# Run this it will run vlc in command line, It works instantly and perfectly on laptop but not at all on raspberry pi. It transcodes the video in real time and it opens it up to http://localhost:8089 or http://<ip-address>:8089.
# It literally works perfectly on a strong laptop. The transcoding works amazingly. You can add http://<ip-address> to CaesarAIMovies video and it will run perfectly because it is encoding from hevc to h.256 which is one down.
cvlc "https://81-4.download.real-debrid.com/d/VH7SENE6DGT76/Arcane%20%282021%29%20-%20S01E03%20-%20The%20Base%20Violence%20Necessary%20for%20Change%20%281080p%20NF%20WEB-DL%20x265%20t3nzin%29.mkv" \
--sout="#transcode{vcodec=h264,vb=800,scale=1,acodec=mp4a,ab=128,channels=2,samplerate=44100,scodec=none}:duplicate{dst=http{mux=mkv,dst=:8089/},dst=display}" \
--no-sout-all --sout-keep

cvlc "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_1MB.mp4" \
--sout="#transcode{vcodec=h264,vb=800,scale=1,acodec=mp4a,ab=128,channels=2,samplerate=44100,scodec=none}:duplicate{dst=http{mux=mkv,dst=:8089/},dst=display}" \
--no-sout-all --sout-keep
