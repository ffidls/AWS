import argparse
parser = argparse.ArgumentParser()
parser.add_argument("help")
args = parser.parse_args()
print(args.help) 
