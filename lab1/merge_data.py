import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--paths', '-p', nargs='+', type=str)

    args = parser.parse_args()
    return args


def merge(args):
    paths = args.paths

    merged = []

    for path in paths:
        with open(path) as file:
            content = json.load(file)['catalog']

        merged.extend(content)

    merged = {'catalog': merged}

    with open(f'merged_parsed_news_kuklin_maxim.json', 'w') as outfile:
        json.dump(merged, outfile, ensure_ascii=False)


if __name__ == '__main__':
    args = parse_args()
    merge(args)
