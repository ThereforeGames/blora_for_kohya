# Adapted from the original B-LoRA inference.py script
# Modified by Therefore Games

import torch, argparse
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from safetensors.torch import save_file, load_file

parser = argparse.ArgumentParser(description='Process some paths and parameters.')
parser.add_argument('--content_lora', type=str, default=None, help='Path to content lora')
parser.add_argument('--style_lora', type=str, default=None, help='Path to style lora')
parser.add_argument('--output_path', type=str, default="model.safetensors", help='Path to new file')
parser.add_argument('--content_alpha', type=float, default=1.0, help='Content alpha value')
parser.add_argument('--style_alpha', type=float, default=1.0, help='Style alpha value')
parser.add_argument('--debug', action='store_true', help='Debug mode')

args = parser.parse_args()


def is_belong_to_blocks(key, whitelist, blacklist):
	try:
		for block in whitelist:
			# print(f"Testing block: {block}")
			if block in key:
				if any(bad_block in key for bad_block in blacklist):
					continue
				if args.debug:
					print(f"VALID! Key: {key}")
				return True
			if args.debug:
				print(f"Key: {key}")
		return False
	except Exception as e:
		raise type(e)(f'failed to is_belong_to_block, due to: {e}')


def filter_lora(state_dict, whitelist, blacklist):
	try:
		return {k: v for k, v in state_dict.items() if is_belong_to_blocks(k, whitelist, blacklist)}
	except Exception as e:
		raise type(e)(f'failed to filter_lora, due to: {e}')


def scale_lora(state_dict, alpha):
	try:
		return {k: v * alpha for k, v in state_dict.items()}
	except Exception as e:
		raise type(e)(f'failed to scale_lora, due to: {e}')


CONTENT_BLOCKS = {
    "whitelist": ["lora_unet_output_blocks_0_1_"],
    "blacklist": ["ff_net", "proj_in", "proj_out", "alpha"],
}

STYLE_BLOCKS = {
    "whitelist": ["lora_unet_output_blocks_1_1_"],
    "blacklist": ["ff_net", "proj_in", "proj_out", "alpha"],
}

# Get Content B-LoRA SD
if args.content_lora is not None:
	print(f"Loading content LoRA: {args.content_lora}")
	content_B_LoRA_sd = load_file(args.content_lora)
	content_B_LoRA = filter_lora(content_B_LoRA_sd, CONTENT_BLOCKS["whitelist"], CONTENT_BLOCKS["blacklist"])  # BLOCKS['content']
	content_B_LoRA = scale_lora(content_B_LoRA, args.content_alpha)
else:
	print("No content LoRA provided.")
	content_B_LoRA = {}

# Get Style B-LoRA SD
if args.style_lora is not None:
	print(f"Loading style LoRA: {args.style_lora}")
	content_B_LoRA_sd = load_file(args.style_lora)
	style_B_LoRA = filter_lora(style_B_LoRA_sd, STYLE_BLOCKS["whitelist"], STYLE_BLOCKS["blacklist"])  # BLOCKS['style']
	style_B_LoRA = scale_lora(style_B_LoRA, args.style_alpha)
else:
	print("No style LoRA provided.")
	style_B_LoRA = {}

# Merge B-LoRAs SD
if args.content_lora and args.style_lora:
	res_lora = {**content_B_LoRA, **style_B_LoRA}
elif args.content_lora:
	res_lora = content_B_LoRA
elif args.style_lora:
	res_lora = style_B_LoRA

print("Saving new model...")
save_file(res_lora, args.output_path)
