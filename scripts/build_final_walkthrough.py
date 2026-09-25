import subprocess, pathlib, shlex, hashlib, json
from PIL import Image, ImageDraw, ImageFont

outdir=pathlib.Path('/Users/byron/Documents/vithia_final_edit'); outdir.mkdir(exist_ok=True)
for p in outdir.glob('*'):
    if p.is_file(): p.unlink()

font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
bold_path='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
prov='ORCHESTRATION: OpenAI Codex  |  INFERENCE: Liquid AI  |  RESEARCH: Nimble  |  TELEMETRY: RawTree  |  VISUALS: Black Forest Labs'

def run(cmd):
    p=subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:
        print(p.stderr[-5000:]); raise SystemExit(p.returncode)

def text_overlay(path,label):
    im=Image.new('RGBA',(1920,1080),(0,0,0,0));d=ImageDraw.Draw(im)
    if label:
        d.rounded_rectangle((40,38,1450,100),radius=8,fill=(0,0,0,178))
        d.text((62,47),label,font=ImageFont.truetype(bold_path,34),fill='white')
    d.rectangle((0,1022,1920,1080),fill=(0,0,0,184))
    f=ImageFont.truetype(font_path,24)
    box=d.textbbox((0,0),prov,font=f); tw=box[2]-box[0]
    d.text(((1920-tw)//2,1035),prov,font=f,fill='white')
    im.save(path)

def card(path,title,lines):
    im=Image.new('RGB',(1920,1080),(6,8,11));d=ImageDraw.Draw(im)
    d.text((110,120),title,font=ImageFont.truetype(bold_path,58),fill=(242,184,93))
    y=230
    for line,size,color in lines:
        d.text((110,y),line,font=ImageFont.truetype(font_path,size),fill=color); y+=int(size*1.65)
    d.rectangle((0,1022,1920,1080),fill=(0,0,0))
    f=ImageFont.truetype(font_path,24); box=d.textbbox((0,0),prov,font=f);tw=box[2]-box[0]
    d.text(((1920-tw)//2,1035),prov,font=f,fill='white')
    im.save(path)

def seg(src,start,dur,dst,label,crop=None,portrait=False):
    ov=outdir/(dst.stem+'_overlay.png'); text_overlay(ov,label)
    if portrait: base='scale=-2:1080,pad=1920:1080:(ow-iw)/2:0:black'
    elif crop: base=f'{crop},scale=-2:1080,pad=1920:1080:(ow-iw)/2:0:black'
    else: base='scale=1920:-2,pad=1920:1080:0:(oh-ih)/2:black'
    fc=f'[0:v]{base}[v0];[v0][1:v]overlay=0:0[v]'
    cmd=f"ffmpeg -y -ss {start} -i {shlex.quote(src)} -loop 1 -i {shlex.quote(str(ov))} -t {dur} -filter_complex {shlex.quote(fc)} -map '[v]' -map 0:a:0? -r 30 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -ac 2 -movflags +faststart {shlex.quote(str(dst))}"
    run(cmd)

def seg_pip(screen_src, screen_start, phone_src, phone_start, dur, dst, label):
    ov=outdir/(dst.stem+'_overlay.png'); text_overlay(ov,label)
    fc=(
        "[0:v]scale=1920:-2,pad=1920:1080:0:(oh-ih)/2:black[base];"
        "[1:v]scale=460:-2,format=yuv420p[phone];"
        "[phone]pad=iw+8:ih+8:4:4:white[pboxed];"
        "[base][pboxed]overlay=W-w-36:H-h-92[tmp];"
        "[tmp][2:v]overlay=0:0[v]"
    )
    cmd=(
        f"ffmpeg -y -ss {screen_start} -i {shlex.quote(screen_src)} "
        f"-ss {phone_start} -i {shlex.quote(phone_src)} "
        f"-loop 1 -i {shlex.quote(str(ov))} -t {dur} "
        f"-filter_complex {shlex.quote(fc)} -map '[v]' -map 1:a:0? "
        f"-r 30 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p "
        f"-c:a aac -b:a 160k -ar 48000 -ac 2 -movflags +faststart {shlex.quote(str(dst))}"
    )
    run(cmd)

def cardvid(dst,dur,title,lines):
    png=outdir/(dst.stem+'.png'); card(png,title,lines)
    run(f"ffmpeg -y -loop 1 -i {shlex.quote(str(png))} -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -t {dur} -r 30 -map 0:v:0 -map 1:a:0 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 128k -ar 48000 -ac 2 -movflags +faststart {shlex.quote(str(dst))}")

seg('/Users/byron/Downloads/longhorizon-cinematic-347111420.mp4',0,5,outdir/'01_open.mp4','VITHIA · VERIFIABLE LONG-HORIZON AGENTS')
phone='/Users/byron/Library/Mobile Documents/com~apple~CloudDocs/Hackathon/IMG_3607.MOV'
core='/Users/byron/Documents/Screen Recording 2026-09-25 at 3.09.31\u202fPM.mov'
seg(phone,3,16,outdir/'02_phone.mp4','BYRON LEE · LONG HORIZON AGENTS HACK',portrait=True)
seg_pip(core,0,phone,19,70,outdir/'03_core.mp4','LIVE AGENT · BOUNDED CONTEXT + AUDITABLE BP0–BP5')
seg('/Users/byron/Documents/Screen Recording 2026-09-25 at 3.09.31\u202fPM.mov',70,12.3,outdir/'04_restart.mp4','COLD RESTART · CONTEXT/MMR RECONSTRUCTION',crop='crop=1824:1442:1200:0')
cardvid(outdir/'05_lme.mp4',8,'LONGMEMEVAL-V2 · ENGINEERING EVIDENCE',[
('20 fixed cases · 15 deterministically scored · 5 abstentions',34,'white'),
('M0 no memory: 0 / 15     ·     Vithia bounded FCG: 1 / 15',34,'white'),
('Observed delta: +6.67 pp',34,(99,216,234)),
('Average memory-context tokens: 1618.8 to 945.8',34,(99,216,234)),
('41.6 percent reduction; observed correct count remained 1 / 15',31,'white'),
('Not leaderboard-comparable · generalization not established',28,(241,170,83))])
seg('/Users/byron/Documents/Screen Recording 2026-09-25 at 2.59.17\u202fPM.mov',58,32.5,outdir/'06_nimble.mp4','NIMBLE · LIVE PUBLIC-EVIDENCE RED TEAM')
seg('/Users/byron/Documents/Screen Recording 2026-09-25 at 3.04.31\u202fPM.mov',8,20,outdir/'07_rawtree.mp4','RAWTREE / TINYBIRD LANE · TELEMETRY READBACK')
cardvid(outdir/'08_seal.mp4',8,'FINAL SEAL',[
('GR0–GR15 independently replayed',36,'white'),
('SYSTEM_SEAL_STATE = PASS',44,(89,217,142)),
('Project MMR  71ff5170...08b5d67b',30,'white'),
('Publication Merkle  a6177ab2...1f6eaf45',30,'white'),
('Scientific performance: engineering smoke; generalization not established',28,(241,170,83))])
seg('/Users/byron/Downloads/project-longhorizon-107730747.mp4',0,5,outdir/'09_close.mp4','VITHIA · EVIDENCE THAT SURVIVES THE AGENT')
names=['01_open.mp4','02_phone.mp4','03_core.mp4','04_restart.mp4','05_lme.mp4','06_nimble.mp4','07_rawtree.mp4','08_seal.mp4','09_close.mp4']
(outdir/'concat.txt').write_text(''.join([f"file '{outdir/n}'\n" for n in names]))
final=pathlib.Path('/Users/byron/Documents/Vithia_Final_Walkthrough_20260925.mp4')
run(f"ffmpeg -y -f concat -safe 0 -i {shlex.quote(str(outdir/'concat.txt'))} -c copy -movflags +faststart {shlex.quote(str(final))}")
sha=hashlib.sha256(final.read_bytes()).hexdigest()
pr=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-of','json',str(final)],text=True))
print('FINAL',final);print('DURATION',pr['format']['duration']);print('SIZE',pr['format']['size']);print('SHA256',sha)
