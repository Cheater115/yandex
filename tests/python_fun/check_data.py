import json
import sys

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def main():
    if len(sys.argv) < 3:
        exit(1)

    get_data = json.loads(sys.argv[1])
    if get_data.get('data') is not None:
        get_data = get_data['data']
    post_data = ""
    with open(sys.argv[2]) as jf:
        post_data = json.load(jf)
        if post_data.get('citizens') is None:
            if post_data.get('data') is not None:
                post_data = post_data['data']
        else:
            post_data = post_data['citizens']

    if ordered(get_data) == ordered(post_data):
        return 0
    else:
        exit(1)


if __name__ == '__main__':
    main()