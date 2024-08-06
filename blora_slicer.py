# Adapted from the original B-LoRA inference.py script

import torch, argparse, json
from safetensors.torch import save_file, load_file

print("B-LoRA Slicer v0.3.0 by Therefore Games")

print("Parsing arguments...")

parser = argparse.ArgumentParser(description='Process some paths and parameters.')
parser.add_argument("--loras", type=str, nargs="*", required=True, help="Path(s) to one or more LoRA safetensors.")
parser.add_argument("--traits", type=str, nargs="*", default=["content"], help="A list of traits to filter from the LoRAs, in the same order as the LoRAs.")
parser.add_argument("--alphas", type=float, nargs="*", default=[1.0], help="A list of alpha values to scale the LoRAs, in the same order as the LoRAs.")
parser.add_argument("--output_path", type=str, default="model.safetensors", help="Path to new file")
parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--not_combined", action="store_true", help="Save each LoRA separately")

args = parser.parse_args()

# If there are more traits than LoRAs, repeat the LoRAs for the remaining traits
if len(args.traits) > len(args.loras):
	print("More traits than LoRAs detected. Repeating the last LoRA for the remaining traits.")
	args.loras += [args.loras[-1]] * (len(args.traits) - len(args.loras))

# If there are fewer traits than LoRAs, repeat "content" for the remaining LoRAs
if len(args.traits) < len(args.loras):
	print("More LoRAs than traits detected. Targeting 'content' for the remaining LoRAs.")
	args.traits += ["content"] * (len(args.loras) - len(args.traits))

# If there are fewer alphas than LoRAs, repeat 1.0 for the remaining LoRAs
if len(args.alphas) < len(args.loras):
	print("More LoRAs than alphas detected. Using alpha value 1.0 for the remaining LoRAs.")
	args.alphas += [1.0] * (len(args.loras) - len(args.alphas))


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


print("Loading unet block traits...")
with open("blora_traits.json", "r") as f:
	traits = json.load(f)

# For each LoRA, filter and scale the traits
loras = []
for i, lora_path in enumerate(args.loras):
	print(f"Loading LoRA: {lora_path}")
	lora_sd = load_file(lora_path)
	lora = filter_lora(lora_sd, traits[args.traits[i]]["whitelist"], traits[args.traits[i]]["blacklist"])
	lora = scale_lora(lora, args.alphas[i])
	loras.append(lora)

if args.not_combined:
	print("Saving LoRAs separately...")
	for i, lora in enumerate(loras):
		save_file(lora, f"{args.traits[i]}_{i}.safetensors")
else:
	# Merge B-LoRAs
	res_lora = {}
	for lora in loras:
		res_lora = {**res_lora, **lora}

	print("Saving new model...")
	save_file(res_lora, args.output_path)
