import argparse
from pathlib import Path
# import re
import sys
import traceback
from typing import Dict

from . import feedback
from . import settings as st


def run(call_back):

    parser = argparse.ArgumentParser(description='Process committee reports HTML',
                                     argument_default='')


    parser.add_argument('--name', metavar='"Committee name"',
                        help='The committee_name (in quotes). '
                             'Must be one of those listed in settings.py')

    # set the default to `Word`
    # parser.add_argument('--source', default='Word',
    #                     help=f'The source. One of {st.SOURCES}.')

    parser.add_argument('--title', '--Inquiry', dest='title', metavar='"Report Title"',
                        help='The report title (in quotes)')

    parser.add_argument('--type', metavar='"Type"',
                        help=f'The report type. One of {st.REPORT_TYPES}')

    parser.add_argument('--number', metavar='REPORT NUMBER', type=str,
                        help='The report number e.g. "First"')

    parser.add_argument('--date', metavar='"Date"',
                        help='The publication date (in quotes). E.g. "1 February 2019"')

    parser.add_argument('--url',
                        help='The inquire publications webpage URL')

    parser.add_argument('file', metavar='File path', type=open,
                        help='File path to the HTML you wish to process. '
                             'If there are spaces in the path you must use quotes.')


    try:
        # args, unknown = parser.parse_known_args(sys.argv[1:])
        args = parser.parse_args(sys.argv[1:])
    except Exception:
        print(sys.argv)
        print("Exception in user code:")
        traceback.print_exc(file=sys.stdout)
        input()
        exit()

    # do some validation if committee name given
    if args.name and args.name not in st.COMMITTEES_AND_ADDRESSES.keys():
        committees = '\n'
        for committee in st.COMMITTEES_AND_ADDRESSES.keys():
            committees += f'  {committee}\n'
        feedback.writeln(
            f'ERROR the --name option must be one of: {committees}')
        exit()

    metadata: Dict[str, str] = {'committee_name': args.name,
                                'report_title': args.title,
                                'report_type': args.type,
                                'report_number': args.number,
                                'publication_date': args.date,
                                'inquiry_publications_url': args.url}

    html_file_Path = Path(args.file.name)

    call_back(html_file_Path, metadata)
