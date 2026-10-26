import argparse
import json
import os
import sys
from pathlib import Path
from .data import FPLClient
from .privacy import unseal
from .report import run_review,personal_markdown


def main():
    parser=argparse.ArgumentParser(description='Numerical FPL research without paid services')
    commands=parser.add_subparsers(dest='command',required=True)
    review=commands.add_parser('review');review.add_argument('--root',type=Path,default=Path.cwd())
    review.add_argument('--force',action='store_true')
    dec=commands.add_parser('decrypt');dec.add_argument('--input',type=Path,default=Path('reports/private/latest.enc'))
    dec.add_argument('--key-file',type=Path,default=Path('.private/report.key'))
    dec.add_argument('--output',type=Path,default=Path('.private/latest-report.md'))
    args=parser.parse_args()
    try:
        if args.command=='review':
            config_path=args.root/'config/entry.json'
            entry_id=json.loads(config_path.read_text())['entry_id'] if config_path.exists() else None
            raw=os.environ.get('FPL_TEAM_STATE') if entry_id is None else None
            state=json.loads(raw) if raw else None
            result=run_review(args.root,FPLClient(),state=state,key=os.environ.get('REPORT_ENCRYPTION_KEY'),force=args.force,entry_id=entry_id)
            print(json.dumps(result))
        else:
            result=unseal(args.input.read_bytes(),args.key_file.read_text().strip())
            # Avoid writing plaintext under tracked public report directories.
            if '.private' not in args.output.resolve().parts:
                raise ValueError('Decrypted output must be inside a .private directory')
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(personal_markdown(result),encoding='utf-8')
            print('Personal report decrypted into the local .private directory.')
        return 0
    except Exception:
        # Exception contents/tracebacks can include a sensitive environment value or report.
        print('Operation failed. Check inputs, connection and local tests; private payloads are not logged.',file=sys.stderr)
        return 1
