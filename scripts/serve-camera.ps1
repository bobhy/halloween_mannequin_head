# comment?
# run camera server in windows, stream to UDP for consumption in WSL (which doesn't have direct access to camera device)
# on windows:
& 'C:\Program Files\VideoLAN\VLC\vlc.exe' `
    --transform-type=vflip `
    'dshow://'  `
    :sout-transcode-venc=h264 `
    :sout-transcode-fps=2 `
    :sout-transcode-scale=640x480 `
    ':sout-rtp-sdp=rtsp://:8002/001.mp4' `
    :sout-rtp-mux=ts `
    --no-sout-all --sout-keep --no-sout-audio

# works, but is hard to manage: -I dummy
