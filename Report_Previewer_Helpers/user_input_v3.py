import datetime
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

# local imports
from . import settings as st


# class for the GUI app
class gui_app:
    def __init__(self, master, call_back):
        self.call_back = call_back

        self.source = tk.StringVar()
        self.committee_name = tk.StringVar()
        self.committee_address = ''
        self.committee_publications = ''
        self.report_title = tk.StringVar()
        self.report_type = tk.StringVar()
        self.report_number = tk.StringVar()
        self.publication_date = tk.StringVar()
        self.inquiry_publications = tk.StringVar()

        self.input_file_path = ''

        self.myWidgets = []

        # make background frame
        frame_padding = ttk.Frame(master)
        frame_padding.pack(fill=tk.BOTH, expand=tk.TRUE)
        windiw_frame = ttk.Frame(frame_padding)
        windiw_frame.pack(fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=10)

        # default padding around elements
        pad = {'padx': 2, 'pady': 6}

        # changing the title of our master widget
        master.title("GUI")

        committee_names = list(st.COMMITTEES_AND_ADDRESSES.keys())

        # Input file button
        ttk.Label(
            windiw_frame, text='Report raw HTML:'
        ).grid(row=0, column=0, stick='e', **pad)

        self.open_button = ttk.Button(
            windiw_frame, text="Open", width=14
        )
        self.open_button.valid = False
        self.open_button.configure(command=self.get_input_file)
        self.open_button.grid(
            row=0, column=1, stick='w', **pad)
        self.myWidgets.append(self.open_button)

        # Text entry and Drop Downs
        drop_down_choices = [
            # Lable              drop down options  validate function    variable
            ('Source:',           st.SOURCES,      self.default_validate, self.source),
            ('Committee name:',   committee_names, self.default_validate, self.committee_name),
            ('Report title:',     None,            self.default_validate, self.report_title),
            ('Report type:',      st.REPORT_TYPES, self.default_validate, self.report_type),
            ('Report number:',    st.ROPORT_NUMS,  self.default_validate, self.report_number),
            ('Publication date:', None,            self.date_validate,    self.publication_date),
            ('Inquiry publications page:', None,   self.url_validate,    self.inquiry_publications),
        ]

        for i, choice in enumerate(drop_down_choices, start=1):
            lable, drop_down, validate_func, variable = choice

            # lable
            ttk.Label(
                windiw_frame, text=lable
            ).grid(row=i, column=0, stick='e', **pad)

            if isinstance(drop_down, list):
                # dropdown
                widget = ttk.Combobox(windiw_frame, textvariable=variable, width=35,
                                      state="readonly", values=drop_down)
            else:
                # text entry
                widget = tk.Entry(windiw_frame, textvariable=variable, width=36)

            widget.valid = False
            self.myWidgets.append(widget)
            widget.bind("<FocusOut>", validate_func)
            widget.grid(row=i, column=1, stick='w', **pad)


        self.goButton = ttk.Button(windiw_frame, text="Go!", command=self.go, width=35)
        self.goButton.config(state="disabled")

        self.goButton.grid(column=0, columnspan=2, row=len(
            drop_down_choices) + 1, pady=(10, 10))


    def overall_validate(self):
        self.goButton.config(state="normal")

        for widget in self.myWidgets:
            if widget.valid is False:
                self.goButton.config(state="disabled")
                break

    def default_validate(self, event):
        entry = event.widget.get()
        if len(entry) > 0:
            event.widget.valid = True
        else:
            event.widget.valid = False
        self.overall_validate()

    def date_validate(self, event):
        dateString = event.widget.get()
        dateFormats = ["%d %b %Y", "%d %B %Y", "%d.%m.%Y", "%d/%m/%Y"]
        for dateFormat in dateFormats:
            try:
                datetime.datetime.strptime(
                    dateString, dateFormat).strftime("%d %B %Y").lstrip("0")
                event.widget.config(background="white")
                event.widget.valid = True
                break
            except:
                event.widget.config(background="#FFA07A")
                event.widget.valid = False
        self.overall_validate()

    def url_validate(self, event):
        urlString = event.widget.get()
        try:
            if urlString[0:25] == 'https://www.parliament.uk':
                event.widget.config(background="white")
                event.widget.valid = True
            else:
                event.widget.config(background="#FFA07A")
                event.widget.valid = False
        except:
            event.widget.config(background="#FFA07A")
            event.widget.valid = False
        self.overall_validate()

    def get_input_file(self):
        directory = filedialog.askopenfilename()
        self.input_file_path = directory
        print('Input file path: ', directory, '\n')

        # for validation
        if Path(self.input_file_path).exists():
            self.open_button.valid = True
        else:
            self.open_button.valid = False
        self.overall_validate()


    def go(self):
        # prevent the user form pressing go again until the call back has returned
        self.goButton.config(state="disabled")

        committee_name = self.committee_name.get()

        committee_address = st.COMMITTEES_AND_ADDRESSES[committee_name][0]
        committee_publications = st.COMMITTEES_AND_ADDRESSES[committee_name][1]

        self.call_back(
            self.input_file_path,  # already a string
            self.source.get(),
            committee_name=committee_name,
            committee_address=committee_address,
            committee_publications=committee_publications,
            report_title=self.report_title.get(),
            report_type=self.report_type.get(),
            report_number=self.report_number.get(),
            publication_date=self.publication_date.get(),
            inquiry_publications=self.inquiry_publications.get(),
        )
        # call back finished
        self.goButton.config(state="enabled")
