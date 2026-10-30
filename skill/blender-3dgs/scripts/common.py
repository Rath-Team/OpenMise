"""Shared JSON input/output for the standalone model helpers."""
import argparse
import json
from pathlib import Path
import sys

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, data):
    target = Path(path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

def cli(handler, blender=False):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True)
    parser.add_argument('--output', required=True)
    argv = sys.argv[sys.argv.index('--') + 1:] if blender and '--' in sys.argv else None
    args = parser.parse_args(argv)
    if Path(args.request).resolve() == Path(args.output).resolve():
        parser.error('request and output must be different files')
    try:
        result = handler(read(args.request))
        result = {'schema_version': 1, **result}
    except Exception as exc:
        result = {'schema_version': 1, 'status': 'failed', 'error': type(exc).__name__, 'message': str(exc)}
    write(args.output, result)
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 1 if result['status'] == 'failed' else 2 if result['status'] == 'uncertain' else 0

def validate_views(data):
    views = data['views']
    if not views or len({v['view_id'] for v in views}) != len(views):
        raise ValueError('views must be nonempty with unique view_id')
    for v in views:
        if v['camera_frame'] != 'blender_camera' or v['pixel_coordinates'] != 'xy_top_left_pixels':
            raise ValueError('unsupported camera/pixel convention')
        if not Path(v['image_path']).is_absolute() or not Path(v['image_path']).is_file():
            raise ValueError('image_path must be an existing absolute path')
    return views
