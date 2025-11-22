
import os

with open('image_b64.txt', 'r') as f:
    img_b64 = f.read().strip()
with open('bg_b64.txt', 'r') as f:
    bg_b64 = f.read().strip()

html_content = f"""<!DOCTYPE html>
<html>
<body>
<canvas id="c1" width="847" height="595"></canvas>
<script>
async function analyze() {{
    const loadImage = (src) => new Promise(resolve => {{
        const img = new Image();
        img.onload = () => resolve(img);
        img.src = src;
    }});

    const refSrc = "data:image/png;base64,{img_b64}";
    const bgSrc = "data:image/jpeg;base64,{bg_b64}";

    const [refImg, bgImg] = await Promise.all([
        loadImage(refSrc),
        loadImage(bgSrc)
    ]);

    const w = 847;
    const h = 595;

    const c1 = document.getElementById('c1');
    const ctx1 = c1.getContext('2d');
    
    // Draw reference image scaled to target size
    ctx1.drawImage(refImg, 0, 0, w, h);
    const refData = ctx1.getImageData(0, 0, w, h).data;

    // Create a temporary canvas for background to extract data
    const c2 = document.createElement('canvas');
    c2.width = w;
    c2.height = h;
    const ctx2 = c2.getContext('2d');
    ctx2.drawImage(bgImg, 0, 0, w, h);
    const bgData = ctx2.getImageData(0, 0, w, h).data;

    const diffs = new Uint8Array(w * h);
    const rowCounts = new Uint32Array(h);

    // Simple difference detection
    for (let i = 0; i < refData.length; i += 4) {{
        const rDiff = Math.abs(refData[i] - bgData[i]);
        const gDiff = Math.abs(refData[i+1] - bgData[i+1]);
        const bDiff = Math.abs(refData[i+2] - bgData[i+2]);
        
        // Threshold for "content" (text/logos) vs background
        if (rDiff + gDiff + bDiff > 40) {{
            const idx = i / 4;
            diffs[idx] = 1;
            const y = Math.floor(idx / w);
            rowCounts[y]++;
        }}
    }}

    // Find text bands (Y-axis)
    const bands = [];
    let inBand = false;
    let startY = 0;
    
    for (let y = 0; y < h; y++) {{
        if (rowCounts[y] > 5) {{ // Threshold for noise
            if (!inBand) {{
                inBand = true;
                startY = y;
            }}
        }} else {{
            if (inBand) {{
                inBand = false;
                if (y - startY > 8) {{ // Ignore tiny bands
                    bands.push({{y: startY, h: y - startY}});
                }}
            }}
        }}
    }}

    // For each band, find X range and dominant color
    const results = bands.map(band => {{
        let minX = w;
        let maxX = 0;
        let rSum=0, gSum=0, bSum=0, count=0;

        for (let y = band.y; y < band.y + band.h; y++) {{
            for (let x = 0; x < w; x++) {{
                const idx = y * w + x;
                if (diffs[idx]) {{
                    if (x < minX) minX = x;
                    if (x > maxX) maxX = x;
                    
                    const pIdx = idx * 4;
                    rSum += refData[pIdx];
                    gSum += refData[pIdx+1];
                    bSum += refData[pIdx+2];
                    count++;
                }}
            }}
        }}
        
        return {{
            top: band.y,
            height: band.h,
            left: minX,
            right: maxX,
            width: maxX - minX,
            color: count ? `rgb(${{Math.round(rSum/count)}}, ${{Math.round(gSum/count)}}, ${{Math.round(bSum/count)}})` : 'unknown'
        }};
    }});

    return JSON.stringify(results, null, 2);
}}
</script>
</body>
</html>"""

with open('analyze.html', 'w') as f:
    f.write(html_content)
