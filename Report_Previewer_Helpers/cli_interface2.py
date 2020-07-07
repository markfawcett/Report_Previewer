import argparse
import re
import sys
import traceback

from . import feedback_v2 as feedback
import script_resources.settings as st


def run(call_back):

    # log out args
    # with open('args_are.txt', 'w') as f:
    #     f.write('\n'.join(sys.argv))

    # it looks like word puts junk in document properties vaues
    beginning_junk = re.compile(r'\d+;#')
    end_junk = re.compile(r'\|[0-9a-z-_]+')

    cleaned_args = []

    for arg in sys.argv[1:]:
        arg = re.sub(beginning_junk, '', arg)
        arg = re.sub(end_junk, '', arg)
        cleaned_args.append(arg)
    print('cleaned_args', cleaned_args, sep='\n')


    parser = argparse.ArgumentParser(description='Process committee reports HTML')

    parser.add_argument('--name', metavar='COMMITTEE',
                        help='The committee_name. Should be in quotes. Must be one of thoes listed in settings.py')

    # set the default to `Word`
    parser.add_argument('--source', default='Word',
                        help=f'The source. One of {st.SOURCES}.')

    parser.add_argument('--title', '--Inquiry', dest='title', type=str, metavar='REPORT TITLE',
                        help='The report title (in quotes)')

    parser.add_argument('--type',
                        help=f'The report type. One of {st.REPORT_TYPES}')

    parser.add_argument('--number', metavar='REPORT NUMBER',
                        help='The report number e.g. "First"')

    parser.add_argument('--date',
                        help='The publication date (in quotes). E.g. "1 February 2019"')

    parser.add_argument('--url',
                        help='The inquire publications webpage URL')

    parser.add_argument('file', metavar='File path', type=open,
                        help='file path to the HTML file you wish to process')


    try:
        # args = parser.parse_args(cleaned_args)
        args, unknown = parser.parse_known_args(cleaned_args)
    except Exception:
        print(sys.argv)
        print("Exception in user code:")
        traceback.print_exc(file=sys.stdout)
        input()
        exit()

    html_path            = args.file.name
    source               = args.source
    committee_name       = args.name
    report_title         = args.title
    report_type          = args.type
    report_number        = args.number
    publication_date     = args.date
    inquiry_publications = args.url

    if committee_name:
        committee_address = st.COMMITTEES_AND_ADDRESSES[committee_name][0]
        committee_publications = st.COMMITTEES_AND_ADDRESSES[committee_name][1]
    else:
        committee_address = None
        committee_publications = None

    # do some validation
    if source and source not in st.SOURCES:
        feedback.writeln(f'ERROR the --source option must be one of {st.SOURCES}')
        exit()
    if committee_name and committee_name not in st.COMMITTEES_AND_ADDRESSES.keys():
        committees = '\n'
        for committee in st.COMMITTEES_AND_ADDRESSES.keys():
            committees += f'  {committee}\n'
        feedback.writeln(
            f'ERROR the --name option must be one of: {committees}')
        exit()

    call_back(html_path, source,
              committee_name=committee_name,
              committee_address=committee_address,
              committee_publications=committee_publications,
              report_title=report_title,
              report_type=report_type,
              report_number=report_number,
              publication_date=publication_date,
              inquiry_publications=inquiry_publications)