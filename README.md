# B-LoRA for Kohya-SS

This repository contains tools needed for training [B-LoRA](https://github.com/yardenfren1996/B-LoRA) files with [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts).

## What is B-LoRA and why should I care?

The B-LoRA method *"enables implicit style-content separation"* for SDXL LoRAs. In other words, if you wish to train a character, you can use this method to avoid picking up unwanted styles, colors or layouts - i.e. features that often creep into character LoRAs by mistake.

B-LoRA's approach works quite well, and it deserves more recognition in the broader Stable Diffusion community.

Combining it with sd-scripts gives you access to awesome features like aspect ratio bucketing.

## How does B-LoRA work?

B-LoRA targets specific unet blocks that correlate surprisingly well to `content` and `style`. It seems best to learn these traits in tandem, and then use the provided `blora_slicer.py` on the final LoRA to preserve only the traits you want to keep.

Additionally, the B-LoRA trainer has several non-standard options that I have specified in `sdxl_blora_project.bat`.

## Setup and Use

1. Install the [Lycoris network](https://github.com/KohakuBlueleaf/LyCORIS).
2. Download this repo and place all its files into the root of your `kohya-ss` directory.
3. Make a copy of `sdxl_blora_project.bat`, adjust it to your needs (in particular, the topmost variables and paths), then launch to begin training.
4. Run `blora_slicer.bat` on the resulting LoRA to filter out `content` or `style` blocks. This will produce a final, smaller LoRA that you can use in the WebUI or Comfy.

Note that while these batch files are for Windows, it should be trivial to adapt them to Linux.

If you're using the Kohya GUI instead of sd-scripts, the Lycoris features are pre-installed and you will need to plug in the `sdxl_blora_project.bat` settings by hand.

---

## Notes on `sdxl_blora_project.bat`

- The B-LoRA method responds well to training a substantially higher number of dimensions than usual. On my GeForce 3090, I have set the rank to `1024` and observed great results for `content` without overfitting. This does increase training time and hardware requirements, however. For anime characters and other simple subjects, you can probably get away with a much lower rank.
- Despite the use of the `prodigy` optimizer, B-LoRA training time is pretty slow, possibly due to options such as `use_bias_correction`. You can try switching to `AdamW` (all other optimizer settings can remain the same.)
- As a point of reference, one of my character datasets contains 168 images and takes ~3 hours to train to 3000 steps. This yields incredibly good likeness without significant signs of overfitting.

## Notes on `blora_slicer.bat`

This tool is adapted from B-LoRA's `inference.py`.

You only need to set up at least one of these arguments:

- `--content_lora`: Path to a `safetensors` file to include the content blocks from, presumably the combined LoRA you trained with kohya.
- `--style_lora`: Path to a `safetensors` file to include the style blocks from.

The script will output your final `model.safetensors` to the same directory.

## Notes on Lycoris presets

The Lycoris preset determines which unet blocks to train.

- `blora_content_style.toml`: This preset matches the original B-LoRA method, training content and style blocks in tandem.
- `blora_content_layout_style.toml`: In addition to content and style, this preset targets blocks that allegedly correlate to image layout. This can potentially improve learning/reduce potential for overfitting, but it has a couple drawbacks: 1) higher VRAM requirement, limiting the number of dimensions you can train. 2) In my initial testing, the layout blocks appear to contain some information that affects character likeness, or what I would classify as "content."

---

⭐ Feel free to give this repo a star if you found it helpful.

Thank you to @slashedstar for [introducing the idea of using Lycoris to recreate the B-LoRA method.](https://github.com/kohya-ss/sd-scripts/issues/1215)