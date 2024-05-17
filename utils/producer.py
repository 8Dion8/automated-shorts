from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from moviepy.video.fx.all import fadein, fadeout
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
    
    def make_short(self, id: str, titleSegments, topcommentSegments):
        placedTimes = 2
        textClips = []
        
        audioIntroClip = AudioFileClip(f'media/woosh.wav').set_start(0)
        
        audioTitleClip = AudioFileClip(f'media/{id}_title.wav').set_start(2)
        
        for segment in titleSegments:
            print(segment)
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
        
        placedTimes += 1
            
        audioCommentClip = AudioFileClip(f'media/{id}_topcomment.wav').set_start(placedTimes)
        
        for segment in topcommentSegments:
            print(segment)
            segmentDuration = segment["end"] - segment["start"]
            textTitleClip = TextClip(
                    self.break_text_by_length(segment['text']), 
                    fontsize=120,
                    color='pink',
                    font='FiraCode-Nerd-Font-Mono-Bold',
                    stroke_color="black", 
                    stroke_width=6,
                    kerning=-1
                ).set_position(('center', 'center')).set_duration(segmentDuration).set_start(placedTimes)
            textClips.append(textTitleClip)
            placedTimes += segmentDuration
            
        videoBackgroundClip = fadein(VideoFileClip(self.videoBackgroundPath).loop(duration=placedTimes+2), duration=2)
            
        compositeAudio = CompositeAudioClip([audioIntroClip, audioTitleClip, audioCommentClip])
        compositeClip = fadeout(CompositeVideoClip([videoBackgroundClip, *textClips]).set_duration(videoBackgroundClip.duration).set_audio(compositeAudio), duration=1)
        
        compositeClip.write_videofile(f'out/{id}.mp4', fps=videoBackgroundClip.fps)
        