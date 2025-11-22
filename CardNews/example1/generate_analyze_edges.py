
import os

with open('image_b64.txt', 'r') as f:
    img_b64 = f.read().strip()

html_content = f"""<!DOCTYPE html>
<html>
<body>
<canvas id="c1" width="1440" height="1440"></canvas>
<script>
async function analyze() {{
    const loadImage = (src) => new Promise(resolve => {{
        const img = new Image();
        img.onload = () => resolve(img);
        img.src = src;
    }});

    const refSrc = "data:image/png;base64,{img_b64}";
    const img = await loadImage(refSrc);

    const w = 1440;
    const h = 1440;

    const c1 = document.getElementById('c1');
    const ctx = c1.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const data = ctx.getImageData(0, 0, w, h).data;

    // Grid size
    const rows = 20;
    const cols = 20;
    const cellW = w / cols;
    const cellH = h / rows;
    
    const grid = [];

    for (let r = 0; r < rows; r++) {{
        let rowStr = "";
        for (let c = 0; c < cols; c++) {{
            let edgeSum = 0;
            const startX = Math.floor(c * cellW);
            const startY = Math.floor(r * cellH);
            
            // Simple edge detection in this cell
            for (let y = startY; y < startY + cellH - 1; y+=2) {{ // skip pixels for speed
                for (let x = startX; x < startX + cellW - 1; x+=2) {{
                    const i = (y * w + x) * 4;
                    const iRight = (y * w + (x+1)) * 4;
                    const iDown = ((y+1) * w + x) * 4;
                    
                    const lum = (data[i]*0.299 + data[i+1]*0.587 + data[i+2]*0.114);
                    const lumRight = (data[iRight]*0.299 + data[iRight+1]*0.587 + data[iRight+2]*0.114);
                    const lumDown = (data[iDown]*0.299 + data[iDown+1]*0.587 + data[iDown+2]*0.114);
                    
                    if (Math.abs(lum - lumRight) > 20 || Math.abs(lum - lumDown) > 20) {{
                        edgeSum++;
                    }}
                }}
            }}
            
            // Normalize by cell area (approx)
            const density = edgeSum / ((cellW/2) * (cellH/2));
            rowStr += density > 0.05 ? "#" : ".";
        }}
        grid.push(rowStr);
    }}

    return grid.join("\\n");
}}
</script>
</body>
</html>"""

with open('analyze_edges.html', 'w') as f:
    f.write(html_content)
