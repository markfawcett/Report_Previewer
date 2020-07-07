import sys

from . import feedback_v2 as feedback
import script_resources.settings as st


def run(call_back):

    if len(sys.argv) != 9:

        print('This script takes 8 Arguments:',
              '  1. The path to the HTML file you wish to process.',
              f'  2. The source. One of {st.SOURCES}.',
              '  3. The committee_name. Should be in quotes. Must be one of thoes listed in settings.py',
              '  4. The report title (in quotes)',
              f'  5. The report type. One of {st.REPORT_TYPES}',
              '  6. The report number e.g. "First"',
              '  7. The publication date (in quotes). E.g. "1 February 2019"',
              '  8. The inquire publications webpage URL', sep='\n')
        exit()

    args = sys.argv[1:]
    (html_path, source, committee_name, report_title, report_type,
     report_number, publication_date, inquiry_publications) = args
    # process_html(**nine_args)

    # do some validation
    if source not in st.SOURCES:
        feedback.writeln(f'ERROR the 1st argument must be one of {st.SOURCES}')
        exit()
    if committee_name not in st.COMMITTEES_AND_ADDRESSES.keys():
        committees = '\n'
        for committee in st.COMMITTEES_AND_ADDRESSES.keys():
            committees += f'  {committee}\n'
        feedback.writeln(
            f'ERROR the 2nd argument must be one of: {committees}')
        exit()

    committee_address = st.COMMITTEES_AND_ADDRESSES[committee_name][0]
    committee_publications = st.COMMITTEES_AND_ADDRESSES[committee_name][1]

    call_back(html_path, source,
              committee_name=committee_name,
              committee_address=committee_address,
              committee_publications=committee_publications,
              report_title=report_title,
              report_type=report_type,
              report_number=report_number,
              publication_date=publication_date,
              inquiry_publications=inquiry_publications)
