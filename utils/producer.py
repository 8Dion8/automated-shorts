from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import fadein
from configparser import ConfigParser
import textwrap

class Producer:
    def __init__(self, config: ConfigParser) -> None:
        self.CONFIGSECTION = 'producer'
        self.load_config(config)
    
    def load_config(self, config: ConfigParser):
        self.videoBackgroundPath = config.get(self.CONFIGSECTION, 'VIDBG')
        
    def break_text_by_length(self, text, length=20):
        return "\n".join(textwrap.wrap(text, length))
    
    def make_short(self, id: str, segments):
        print(TextClip.list('font'))
        videoBackgroundClip = fadein(VideoFileClip(self.videoBackgroundPath), duration=1)
        placedTimes = 0
        textClips = []
        for segment in segments:
            segmentDuration = segment["end"] - segment["start"]
            textTitleClip = TextClip(
                    self.break_text_by_length(segment['text']), 
                    fontsize=120,
                    color='white',
                    font='FiraCode-Nerd-Font-Mono-Bold',
                    stroke_color="black", 
                    stroke_width=6,
                    kerning=-1
                ).set_position(('center', 'center')).set_duration(segmentDuration).set_start(placedTimes)
            textClips.append(textTitleClip)
            placedTimes += segmentDuration
        
        audioTitleClip = AudioFileClip(f'media/{id}_title.wav').set_start(1)
        
        compositeClip = CompositeVideoClip([videoBackgroundClip, *textClips]).set_duration(videoBackgroundClip.duration).set_audio(audioTitleClip)
        
        compositeClip.write_videofile(f'out/{id}.mp4', fps=videoBackgroundClip.fps)
        