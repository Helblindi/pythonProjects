from tkinter import *
from tkinter import filedialog
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Shift:
    # Shift represents an operator with a start time and an end time

    # Non-Default Constructor
    def __init__(self, _initials, _start_time, _end_time, _shift_type):
        self.shift_type = _shift_type
        self.initials = _initials
        self.start_time = _start_time
        self.end_time = _end_time

    def __str__(self):
        return self.shift_type + " " + self.initials + ": " + self.start_time + "-" + self.end_time

    def get_shift_type(self):
        return self.shift_type

    def set_shift_type(self, _shift_type):
        self.shift_type = _shift_type

    def get_shift_initials(self):
        return self.initials

    def set_shift_initials(self, _initials):
        self.initials = _initials

    def get_shift_start_time(self):
        return self.start_time

    def set_shift_start_time(self, _start_time):
        self.start_time = _start_time

    def get_shift_end_time(self):
        return self.end_time

    def set_shift_end_time(self, _end_time):
        self.end_time = _end_time


def get_filename():
    print('getting filename')
    window = Tk()
    window.title("File Retrieval")

    # Sets default window size
    # window.geometry('350x200')

    # Open up file dialog
    filename = filedialog.askopenfilename()

    return filename


def read_file():
    print('reading file')
    # GUI implementation to retrieve filename
    filename = get_filename()

    # Open the file with read only permit
    f = open(filename, "r")

    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines in the file
    lines = list(f)

    # close the file after reading the lines.
    f.close()

    return lines


def remove_unwanted_lines(lines):
    print('Removing unwanted lines')

    # Reduce the initials from being the full name and
    # level to just the operator's initials
    words_to_remove = ["10 am", "11 am", "12 am", "10 pm", "11 pm", "12 pm",
                       "1 am", "2 am", "3 am", "4 am", "5 am", "6 am",
                       "7 am", "8 am", "9 am", "10 am", "1 pm", "2 pm",
                       "3 pm", "4 pm", "5 pm", "6 pm", "7 pm", "8 pm", "9 pm",
                       " L1-ID (Training)", " L1-ID (training)", " SC-ID", " TC-ID", " FT",
                       " L1-ID", " L2-ID", " L3-ID", " TM-L3-ID", " TM-L2-ID",
                       " L1-UT", " L2-UT", " L3-UT", " TM-L3-UT", " TM-L2-UT",
                       " TM-L2-ID", "\n", "\t", "TRANSITION WEEK ",
                       "Transition hours ", " TM-UT", " SC-UT", " Coach-UT"]

    for word in words_to_remove:
        lines = [s.replace(word, '') for s in lines]

    # edit this list of lines to remove
    words_to_remove = ["Day Shift", "Swing Shift",
                       "Grave Shift", "Negative Points",
                       "Training", "TM", "Incentive Shift"]

    # using a list comprehension to remove unwanted lines
    for word in words_to_remove:
        lines = [x for x in lines if x != word]

    # # pop off the total scheduled hours for both centers
    # lines.pop()

    # return edited lines
    return lines


def get_initials(index, lines):
    for i in range(index, 0, -1):
        if lines[i][0] == '"':
            words = lines[i].split()
            _initials = words[-1]
            if _initials == "TIME":
                _initials = "OPEN"
            return _initials
        elif index - 5 == 10:
            return 'not found'


def build_rex_ogd(lines):
    print('building rex and ogd')
    # the container for all the shifts in Rexburg
    rex_shifts = []
    ogd_shifts = []

    # build each relevant shift object
    for i in range(0, len(lines)):

        # Find all med shifts
        if lines[i] == "Meds":
            _shift_type = "MEDS"
            _initials = get_initials(i, lines)
            _start_time = lines[i + 1][0:5]
            _end_time = lines[i + 1][6:11]
            rex_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))

        # Find all message center shifts
        elif lines[i] == "Message Centers":
            _shift_type = "MSG"
            _initials = get_initials(i, lines)
            _start_time = lines[i + 1][0:5]
            _end_time = lines[i + 1][6:11]
            rex_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))

        # Find all burg shifts
        elif lines[i] == "Burgs":
            _shift_type = "BURGS"
            _initials = get_initials(i, lines)
            _start_time = lines[i + 1][0:5]
            _end_time = lines[i + 1][6:11]
            ogd_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))

        # Find all inbound shifts
        elif lines[i] == "Inbound" and lines[i - 1] != "Shift Coordinator":
            _shift_type = "INB"
            _initials = get_initials(i, lines)
            _start_time = lines[i + 1][0:5]
            _end_time = lines[i + 1][6:11]
            if lines[i - 1] == "Ogden" or lines[i - 2] == "Ogden":
                ogd_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))
            else:
                rex_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))

        # Find all transition shifts and sort them by location
        elif lines[i] == "Transition":
            # check if Ogden or Rexburg Transition Op
            if lines[i - 1] == "Ogden" or lines[i - 2] == "Ogden":
                # it is an Ogden Transition shift, we do not want to create a block for it
                _shift_type = "TRANS"
                _initials = get_initials(i, lines)
                _start_time = lines[i + 1][0:2] + ":" + lines[i + 1][2:4]  # not sure if math is correct here
                _end_time = lines[i + 1][5:7] + ":" + lines[i + 1][7:9]
                ogd_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))
            else:
                _shift_type = "TRANS"
                _initials = get_initials(i, lines)
                _start_time = lines[i + 1][0:2] + ":" + lines[i + 1][2:4]  # not sure if math is correct here
                _end_time = lines[i + 1][5:7] + ":" + lines[i + 1][7:9]
                rex_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))

        # Find all shift coordinator shifts and sort them by location
        elif lines[i] == "Shift Coordinator":
            if lines[i-1] == "Rexburg" and lines[i+1] != "14:15-15:15":
                # Rexburg SC shift (Non-meeting)
                _shift_type = "SC"
                _initials = get_initials(i, lines)
                _start_time = lines[i + 1][0:5]
                _end_time = lines[i + 1][6:11]
                rex_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))
            elif lines[i - 1] == "Ogden":
                # Ogden SC Shift
                ### May need to account for Ogden SC Meeting ###
                _shift_type = "SC"
                _initials = get_initials(i, lines)
                _start_time = lines[i + 2][0:5]
                _end_time = lines[i + 2][6:11]
                ogd_shifts.append(Shift(_initials, _start_time, _end_time, _shift_type))

    # return the shifts sorted by location
    return rex_shifts, ogd_shifts


def condense_duplicates(shifts):
    # will need to make a collection of the list items that will need to be deleted
    indices_to_be_removed = []
    # Loops through the shifts
    for i in range(0, len(shifts)):

        # For each shift, look for another shift with the same operator
        for j in range(i, len(shifts)):

            # Check to see if they are the same initials and the times match up
            # If
            # shifts[i]. == shifts[j].initials and shifts[i].end_time == shifts[j].start_time:
            if shifts[i].get_shift_initials() == shifts[j].get_shift_initials() and \
                shifts[i].get_shift_end_time() == shifts[j].get_shift_start_time() and \
                    j not in indices_to_be_removed:

                # Case 1: They are the same shift type
                if shifts[i].get_shift_type() == shifts[j].get_shift_type():
                    shifts[i].set_shift_end_time(shifts[j].get_shift_end_time())
                    indices_to_be_removed.append(j)

                # Case 2: They are different shifts
                else:
                    # delete second shift and move it right below first shift
                    temp_shift = shifts[j]
                    shifts.insert(i + 1, temp_shift)
                    indices_to_be_removed.append(j)

                    # need to increment all indices in the list
                    for num in range(len(indices_to_be_removed)):
                        if indices_to_be_removed[num] > i:
                            indices_to_be_removed[num] += 1

                    # helps keep us at the right shift we are looking for duplicates from
                    i += 1

    # Lastly we need to remove the duplicate elements
    indices_to_be_removed.sort(reverse=True)
    for it in indices_to_be_removed:
        del(shifts[it])

    return shifts


def add_blank_shifts(shifts):
    indices_to_append = []
    # iterate through shifts looking for duplicates
    for i in range(0, len(shifts) - 1):
        if shifts[i].get_shift_initials() == shifts[i + 1].get_shift_initials() and \
           shifts[i].get_shift_type() != '*' and shifts[i+1].get_shift_type() != '*':
            # Shift(_initials, _start_time, _end_time, _shift_type)
            indices_to_append.append(i)

    # Lastly we need to remove the duplicate elements
    blank_shift = Shift("", "", "", "*")
    indices_to_append.sort(reverse=True)
    for j in indices_to_append:
        shifts.insert(j, blank_shift)

    return shifts


def split_shifts(shifts):
    # split shifts into Days, Swings, and Graves
    # set start times for various shifts
    days_times = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30',
                  '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30',
                  '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00']
    swings_times = ['14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00',
                    '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00']

    # initialize arrays for each shift
    days_shifts = []
    swings_shifts = []
    graves_shifts = []

    # place each shift into it's respective array
    for shift in shifts:
        if shift.start_time in days_times:
            days_shifts.append(shift)
        elif shift.start_time in swings_times:
            swings_shifts.append(shift)
        else:
            graves_shifts.append(shift)

    # return each array
    return days_shifts, swings_shifts, graves_shifts


def print_shifts(shifts):
    for shift in shifts:
        print(shift)


def write_to_file(shifts, filename):
    csv = open(filename, "w+")
    # "w" indicates that you're writing strings to the file
    # "+" indicates that you;re writing to a new file

    columnTitleRow = "type, initials, start_time, end time\n"
    csv.write(columnTitleRow)

    for shift in shifts:
        row = shift.shift_type + "," + shift.initials + "," + \
              shift.start_time + "," + shift.end_time + "\n"
        csv.write(row)


def write_to_google_sheets(days_shifts, swings_shifts, graves_shifts, google_doc, worksheet):
    print('writing to google sheets')
    # setting up to work with google sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # open up the sheet designated by the passed in parameters
    sheet = client.open(google_doc).worksheet(worksheet)

    # syntax to update a single cell
    # (row, col, val)
    # sheet.update_cell(4, 7, 'AB4')

    # Update Days Section
    # for i in range(0, len(days_shifts)):
    #     print(i, ' shift: ', days_shifts[i])

    # Update Swings Section

    # Update Graves Section

    # syntax to update a range
    # cell_list = sheet.range('F13:I15')
    #
    # for cell in cell_list:
    #     cell.value = ''
    #
    # sheet.update_cells(cell_list)

    return


def main():
    print("Working on it...")
    lines = read_file()
    lines = remove_unwanted_lines(lines)
    rex_shifts, ogd_shifts = build_rex_ogd(lines)
    rex_shifts = condense_duplicates(rex_shifts)
    rex_shifts = add_blank_shifts(rex_shifts)
    ogd_shifts = condense_duplicates(ogd_shifts)
    ogd_shifts = add_blank_shifts(ogd_shifts)

    """ Test Zone """
    # for line in lines:
    #    print(line)
    print_shifts(rex_shifts)
    # print_shifts(ogd_shifts)
    # for shift in rex_shifts:
    #     print(shift.get_shift_initials())

    """ Write to a file on the computer """
    # write_to_file(rex_shifts, "C:/Users/Madison/Desktop/rex_test.csv")  # on my personal laptop
    # write_to_file(ogd_shifts, "C:/Users/Madison/Desktop/ogd_test.csv")
    write_to_file(rex_shifts, "M:/Operations_Tools/Rex_Daily_Log_Tool.csv")
    write_to_file(ogd_shifts, "M:/Operations_Tools/Ogd_Daily_Log_Tool.csv")

    """ Write to google sheets (Not finished) """
    # or we can write them straight into google sheets (This option does take longer
    # rex_days, rex_swings, rex_graves = split_shifts(rex_shifts)
    # ogd_days, ogd_swings, ogd_graves = split_shifts(ogd_shifts)
    # write_to_google_sheets(days_shifts, swings_shifts, graves_shifts, 'August Daily Log 2018', 'MSS_Test_Sheet')


# While not required, it is considered good practice to have
# a main function and use this syntax to call it.
if __name__ == "__main__":
    main()

# command to create exe file
# need to navigate to the folder containing this py file
# pyinstaller --onefile Generator.py
