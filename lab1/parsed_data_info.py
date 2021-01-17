import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', type=str)

    args = parser.parse_args()
    return args


def get_info(args):
    path = args.path

    with open(path) as file:
        content = json.load(file)

    ek = [a for a in content['catalog'] if a['category'] == 'ekonomika']
    kult = [a for a in content['catalog'] if a['category'] == 'kultura']
    pol = [a for a in content['catalog'] if a['category'] == 'politika']
    ob = [a for a in content['catalog'] if a['category'] == 'obschestvo']

    data = {
        'ekonomika': ek,
        'kultura': kult,
        'potika': pol,
        'obschestvo': ob
    }

    for category, d in data.items():
        print(f'{category}: {len(d)}')

    print(f'Total: {len(content["catalog"])}\n')


if __name__ == '__main__':
    args = parse_args()
    get_info(args)
