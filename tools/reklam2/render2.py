import subprocess, sys, json
from playwright.sync_api import sync_playwright
T=float(sys.argv[2]) if len(sys.argv)>2 else 15.27
out=sys.argv[1]
times=[float(x) for x in sys.argv[3:]] if len(sys.argv)>3 else None
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file:///home/claude/filmoda-repo/tools/reklam2/anim.html"); pg.evaluate("window.ready"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
    if times:
        for t in times:
            pg.evaluate(f"render({t})"); pg.screenshot(path=f"{out}_{t}.png")
    else:
        ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate","30","-i","-","-c:v","libx264","-crf","17","-preset","veryfast","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
        n=int(round(T*30))
        for i in range(n):
            pg.evaluate(f"render({i/30})"); ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
        ff.stdin.close(); ff.wait()
    b.close()
