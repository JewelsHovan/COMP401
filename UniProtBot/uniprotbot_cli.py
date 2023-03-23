import argparse
import sys
from uniprotbot import UniProtBot

def main(args):
    bot = UniProtBot(args.config)

    if args.action == "protscraper":
        bot.run_protscraper()
    elif args.action == "fLPS2":
        bot.run_fLPS2()
    elif args.action == "unzip":
        bot.unzip_files(args.input_file, args.output_path)
    elif args.action == "transcripts":
        bot.run_transcripts()
    elif args.action == "visualize":
        bot.visualize_files(args.output_path, args.files)
    elif args.action == "modify_config":
        bot.modify_config(args.param_name, args.new_value)
    else:
        print(f"Unknown action: {args.action}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UniProtBot CLI")
    parser.add_argument("action", help="Action to perform: protscraper, fLPS2, unzip, transcripts, visualize, modify_config")
    parser.add_argument("-c", "--config", default="configs/config.yaml", help="Path to the config file")
    parser.add_argument("-i", "--input_file", help="Path to the input file (for unzip action)")
    parser.add_argument("-o", "--output_path", help="Path to the output directory (for unzip and visualize actions)")
    parser.add_argument("-f", "--files", nargs="*", help="List of file paths to be processed by visualize.py (for visualize action)")
    parser.add_argument("-p", "--param_name", help="Parameter name in the config file (for modify_config action)")
    parser.add_argument("-n", "--new_value", help="New value for the parameter in the config file (for modify_config action)")

    args = parser.parse_args()
    main(args)
