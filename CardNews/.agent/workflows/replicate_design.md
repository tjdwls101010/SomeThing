---
description: Replicate a design from a reference image provided in chat
---

# Context

The goal is to create a pixel-perfect HTML/CSS replication of a reference image (e.g., CardNews, promotional material). The user provides the reference image via chat and text content via a file.

# Role

Expert Frontend Developer & UI Designer. You specialize in analyzing visual designs and translating them into precise code.

# Instructions

- **Visual Source**: Use the image uploaded in the chat for visual analysis (layout, color, typography). **Do NOT** use `view_file` on image files for visual information, as it only returns binary data.
- **Content Source**: Use `view_file` to read text content from provided markdown files (e.g., `text.md`).
- **Asset Generation**: If the reference image contains photos, logos, or decorative elements that are not provided as separate files, use `generate_image` to create them. Save generated assets to an appropriate directory (e.g., `assets/` or `images/`).
- **Implementation**: Use `write_to_file` to generate clean, semantic HTML and CSS in `{example_folder}/outputs/output.html`.
- **Verification**: Use the `html_to_image.py` script to generate PNG screenshots, then use `view_file` to load and visually compare them with the reference image. Iterate until the design matches.

> [!NOTE] > **Prerequisites**: Requires `html_to_image.py` script and Python virtual environment with Playwright installed (`.venv`).

# Workflow

1.  **Analysis**

    - Review the uploaded image in the chat to understand the layout structure, hierarchy, and styling.
    - Read the text content file using `view_file`.
    - Identify key design elements: font families, sizes, colors, margins, and background image usage.

2.  **Planning**

    - Create `implementation_plan.md` outlining the HTML structure and CSS strategy.
    - Define the target dimensions (match reference or user request).
    - Identify any missing visual assets (photos, logos, icons) that need to be generated.

3.  **Asset Generation** (if needed)

    - Use `generate_image` to create any missing visual elements identified in planning.
    - Save generated images to a dedicated directory with descriptive names.
    - Update the implementation plan to reference these generated assets.

4.  **Implementation**

    - Create the example folder's `outputs/` directory if it doesn't exist
    - Create `{example_folder}/outputs/output.html` with the initial implementation
    - Apply styles to match the reference
    - Ensure the background image and any generated assets are correctly referenced using relative paths

5.  **Automated Iteration & Refinement**
    - **Generate Screenshot**: Run `python3 html_to_image.py ./outputs/output.html ./outputs/output_v1.png` from the example folder
    - **Visual Comparison**: Use `view_file` to load `output_v1.png` and compare it with the reference image uploaded in chat
    - **Identify Issues**: List specific differences (spacing, font size, alignment, colors, positioning)
    - **Plan Improvements**: Document necessary changes to fix identified issues
    - **Modify Code**: Update `output.html` based on the improvement plan
    - **Repeat**: Generate `output_v2.png`, compare, refine, and continue until the output matches the reference
    - **Final Walkthrough**: Create `walkthrough.md` with before/after comparisons showing the progression from `v1` to the final version

**Example workflow for `example2/`:**

```bash
# After creating output.html
cd example2
python3 ../html_to_image.py ./outputs/output.html ./outputs/output_v1.png
# Agent uses view_file on output_v1.png, compares with reference
# Agent modifies output.html
python3 ../html_to_image.py ./outputs/output.html ./outputs/output_v2.png
# Repeat until satisfactory
```
