import json
import sys


def main():
    if len(sys.argv) < 2:
        exit(1)

    res = json.loads(sys.argv[1])
    import_id = res['data']['import_id']
    print(import_id)
    return str(res['data'])


if __name__ == '__main__':
    main()
