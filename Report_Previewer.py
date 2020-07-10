#!/usr/bin/env python

# std library imports
# from datetime import datetime
import os
from pathlib import Path
import sys
import time
import traceback

# needed for pyinstaller
# import distutils

# import tkinter

# Import third-party modules
from lxml import html  # type: ignore
from watchdog.observers import Observer  # type: ignore
from watchdog.events import PatternMatchingEventHandler  # type: ignore
# import webbrowser

# Import local modules
try:
    import Report_Previewer_Helpers.feedback_v2     as feedback
    import Report_Previewer_Helpers.file_IO         as file_io
    # import Report_Previewer_Helpers.id_html         as id_html
    import Report_Previewer_Helpers.shell_format_v2 as shell_format
    import Report_Previewer_Helpers.settings        as st
    import Report_Previewer_Helpers.triplets        as triplets
    import Report_Previewer_Helpers.univ_html_v2    as univ_html
    import Report_Previewer_Helpers.word_html       as word_html
    # import Report_Previewer_Helpers.cli_interface2   as cli
except ModuleNotFoundError as e:
    print('Error: The script requires the Report_Previewer_Helpers folder.\n', e)




def roubust_execution(funcs, input_html):
    for func in funcs:
        # global input_html
        if not isinstance(func, list):
            # if(type(func) != type([])):
            print('\t', func.__name__)
            try:
                input_html = func(input_html)
            except Exception as e:
                feedback.writeln('\t\t' + str(e))
        else:
            print('\t', func[0].__name__)
            try:
                input_html = func[0](input_html, func[1])
            except Exception as e:
                feedback.writeln('\t\t' + str(e))


def wait_for_file(file):

    # wait for file to finish being created or copied
    historicalSize = -1
    while (historicalSize != os.path.getsize(file)):
        historicalSize = os.path.getsize(file)
        time.sleep(1)


def on_created(event):
    print(f"{event.src_path} has been created!")
    html_file = Path(event.src_path)

    # wait for file to finish being created/copied
    wait_for_file(html_file)
    print('File creation finished.')

    parameters_file = html_file.parent.joinpath('parameters.txt')
    print(f'Looking for {str(parameters_file)}')
    if not parameters_file.exists:
        print(f'ERROR there is no parameters file associated with {str(html_file)}')
        return
    wait_for_file(parameters_file)

    parameters = {}
    with open(parameters_file, 'r') as f:
        for line in f.readlines():

            # skip blank lines
            if not line.strip():
                continue

            key_value = line.split('\t')
            if len(key_value) != 2:
                print('Error in the following line. '
                      f'Expected key followed by tab followed by vlaue\n{line}')
                return

            parameters[key_value[0].strip()] = key_value[1].strip()

    expected_args = {'committee_name', 'report_title', 'report_type',
                     'report_number', 'publication_date', 'inquiry_publications_url'}

    if not expected_args.issubset(set(parameters.keys())):
        print(f'One of the expected parameters {expected_args} not found in file {str(parameters_file)}')
    else:
        c_name = parameters['committee_name']
        parameters['committee_address'] = st.COMMITTEES_AND_ADDRESSES.get(c_name, ['', ''])[0]
        parameters['committee_publications'] = st.COMMITTEES_AND_ADDRESSES.get(c_name, ['', ''])[1]

    process_html(str(html_file), **parameters)

    # i wonder if we should now delete both parameters.txt and the html_file
    os.remove(html_file)
    os.remove(parameters_file)


def main():

    feedback.writeln('Username:\t' + feedback.USERNAME)

    # create event handler for watched folder
    patterns = ["*.htm", '*.html']
    ignore_patterns = ['*.txt', '*$*']
    ignore_directories = True
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns,
                                                ignore_directories, case_sensitive)
    event_handler.on_created = on_created

    # create cross platform path to folder to watch
    watched_folder = Path(Path.home(), 'committee_report_html/word_filtered_html')
    # create folder to watch if it does not already exsit
    if not watched_folder.exists():
        watched_folder.mkdir(parents=True, exist_ok=True)

    # current_folder_to_watch = str(Path(Path.home(), 'committee_report_html'))
    path = str(watched_folder)
    my_observer = Observer()
    my_observer.schedule(event_handler, path, recursive=False)  # not interested in sub-directories

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()



def process_html(html_path, **kwargs):

    file_io.set_up(html_path)

    meta = kwargs
    # feedback.writeln('Meta:\t' + str(meta))

    # changed to set
    accepted_classes = {'contents-heading', 'UnorderedList1', 'UnorderedList2', 'FootnoteText',
                        'figure-caption', 'caption', 'callout', 'text-center', 'text-right',
                        'table', 'table-bordered',  'header-cell'}

    input_html = html.parse(html_path).getroot()

    # remove the word vs indesign version
    # if source == "Word":
    funcs = (
        univ_html.drop_head,
        univ_html.add_footnote_heading,
        [univ_html.drop_unwanted_attributes, ['style']],
        word_html.drop_most_divs,
        univ_html.drop_cover,
        univ_html.size_images,
        word_html.format_footnotes,  # must run before footnote_refs function
        word_html.format_footnote_refs,  # must run after format_footnotes function
        [word_html.chage_class_names, [('MsoCaption', 'figure-caption')]],  # NEW
        [univ_html.drop_unwanted_attributes, [
            # --------------------------------------------- I am not sure about align
            'name', 'border', 'cellspacing', 'cellpadding', 'width', 'height', 'align']],
        [univ_html.drop_pointless_tags, ['a']],
        # name attribute must be cleared but pointless spans must still be there
        word_html.fix_ordered_lists,
        [univ_html.drop_pointless_tags, ['span', 'a']],
        [word_html.fix_bullet_points, ['UnorderedList1', 'BoxUnorderedList1']],
        univ_html.convert_box_tables,
        univ_html.add_classes_to_tables,
        univ_html.fix_blockquotes,
        univ_html.correct_internal_links,
        univ_html.conclusion_recommendation,  # must be before keep_only_accepted_classes
        # [triplets.map_classes_and_tags, [source]],
        [triplets.map_classes_and_tags, ['Word']],  # only use word version atm
        [word_html.wrap_uls, ['UnorderedList1', 'UnorderedList2', 'BoxUnorderedList1']],
    )
    roubust_execution(funcs, input_html)

    # final functions are the same regardless of source
    funcs = ([univ_html.keep_only_accepted_classes, accepted_classes],
             univ_html.tidy_cycle,
             univ_html.generic_clean,
             univ_html.tidy_cycle,  # deliberately repeated
             univ_html.free_img,   # must be before add rules
             univ_html.add_rules,  # must be after the triplets
             # univ_html.add_back_to_top,
             univ_html.no_toc_footnote_heading,
             univ_html.replace_back_pages)
    roubust_execution(funcs, input_html)

    file_io.copy_css_etc()

    # change to input name
    # base_file_name = datetime.now().strftime('%Y-%b-%d--%H-%M-%S')
    base_file_name = Path(html_path).name.replace('.html', '').replace('.htm', '')

    summary, report = univ_html.separate_summary(input_html)

    if summary is not None:
        print('\nCreating summary')
        summary = shell_format.add_meta(summary, 'summary', meta)
        file_io.write_html(summary, base_file_name + '-report-summary.html', open_in_browser=True)

        # lets also have a go at creating a print-summary
        import Report_Previewer_Helpers.print_summary as print_summary
        summary_print = print_summary.print_html(summary, **meta)
        file_io.write_html(summary_print, base_file_name + '-print-summary.html', open_in_browser=False)

    print('\nCreating full report')
    report = shell_format.add_meta(report, 'report', meta)
    file_io.write_html(report, base_file_name + '-full-report.html', open_in_browser=True)

    feedback.writeln('\n  ' + 'All Done!\n')


if __name__ == "__main__":
    try:
        os.system('color')  # coloured text in windows cmd prompt
        main()
    except Exception:
        print("Exception in user code:\n")
        traceback.print_exc(file=sys.stdout)
        input()
        exit()
