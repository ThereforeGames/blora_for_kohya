# Changelog
All notable changes to this project will be documented in this file.

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