# Changelog
All notable changes to this project will be documented in this file.

## 0.3.0 - 6 August 2024

### Added
- New Lycoris preset `blora_content_style_clip.toml` which targets the first two layers of the text encoders (0 and 1) for training, applying the "content" and "style" separation idea of B-LoRA
- New Lycoris preset `bdora_content_style_clip.toml`: same as above, but also enables DoRA weight composition
- New B-LoRA trait `clip_2_content` for use with `blora_slicer.py`; slices layer 0 of the 2nd text encoder, which seems to effectively learn content while minimally impacting style
- New `blora_slicer.py` setting `--not_combined`: Saves out individual LoRA files instead of packing all settings into one

### Changed
- Set `use_bias_correction=True` in `sdxl_blora_fast.bat` while I run more tests to determine this option's impact on quality

## 0.2.0 - 12 July 2024

### Added
- New preset `sdxl_blora_fast.bat`: Optimized training settings to dramatically improve convergence time, while (hopefully) maintaining quality - feedback would be appreciated

### Changed
- Renamed preset `sdxl_blora_project.bat` to `sdxl_blora_classic.bat` and added 500 steps of warmup to match origin B-LoRA repo

## 0.1.0 - 1 July 2024

### Added
- New Lycoris preset `blora_content_layout_style.toml`: targets additional blocks that allegedly correlate to image layout (which may further reduce overfitting, but this is not used in original B-LoRA)
- New Lycoris preset `blora_layout_style.toml`
- The B-LoRA Slicer will now load `blora_traits.json` for arbitrary block filters, you can easily add your own to this file

### Changed
- The B-LoRA Slicer now uses `--loras`, `--traits`, and `--alphas` arguments so you can specify multiple arbitrary operations (i.e. no longer limited to just content and style)

## 0.0.1 - 30 June 2024

### Added
- Initial release