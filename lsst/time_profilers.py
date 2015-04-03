#!/usr/bin/env python
#
# Collection of classes that keep multiple profiling timers
# and can dump measurement results in multiple formats.


import fcntl
import time
import os


class TimeProfiler(object):
    """
    Keeps multiple ProfilingTimer objects and dumps their
    measurements when asked to.

    Actually, the only methods we will expect to be available
    from ProfilingTimer objects are:

     - get_description: expected to return timer description as string;

     - get_elapsed: expected to return elapsed seconds as float.

    This module has TimerlikeCount object that provides such interface
    and can be used for adding arbitrary integer parameters into
    the list of measurements that we keep.
    """

    EOL = "\n"
    """ End-of-line character(s) """

    CSV_SEP = ";"
    """ Separator for our CSV files """

    CSV_EOL = "\r\n"
    """ End-of-line for our CSV files """

    def __init__(self, filename, comment):
        """
        Class constructor

        Arguments:

         - filename: name of the file we will dump measurements into.
           It will be appended with the extension during the invocation
           of dump();

         - comment: comment that carries measurement information;
           can be None that means "don't write comments"; will be written
           to the file only if it is empty upon the time we open it
           for writing (after acquiring file lock).
        """

        self.timers = []
        self.timer_information = []
        self.filename = filename
        self.comment = comment
        self.set_formatter("plaintext")


    @classmethod
    def __current_timestamp(cls):
        """
        Returns string that carries current date and time
        using UTC time coordinates.

        We use YYYY-MM-DDTHH:MM:SSZ because it is easy to
        sort alphabetically (as a string) and it will yield
        proper time-wise sorting order.
        """

        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


    @classmethod
    def __comment_out(cls, string, comment_char, eol):
        """
        Comments out given (multiline) string.

        Arguments:

         - string: string to comment out;

         - comment_char: comment character (or sequence of);

         - eol: end-of-line sequence for resulting string.

        Returns commented-out version of the passed string.

        We take incoming string line separator to be "\n".
        """

        c = comment_char + ' '
        return (c + (eol + c).join(string.split("\n")) + eol)


    @classmethod
    def __plaintext_header_formatter(cls, fp, comment, timer_names):
        """
        Writes header for the plain ASCII output file.

        Arguments:

         - fp: file-like object we can write() into;

         - comment: None or string that contains description
           of the current timer set;

         - timer_names: array of timer names; guaranteed to have
           the same order as timer_tuples in record formatter.

        We will use '#' as the comment character.
        """

        comment_char = "#"
        header = ""
        # Comments can be multiline.
        if comment != None:
            header += TimeProfiler.__comment_out(comment,
              comment_char, TimeProfiler.EOL)
        fp.write(header + TimeProfiler.EOL)


    @classmethod
    def __plaintext_formatter(cls, fp, timer_tuples):
        """
        Formats record using plain ASCII output format.

        Arguments:

         - fp: file-like object we can write() into;

         - timer_tuples: array of tuples (name, seconds)
           that describe each timer.
        """

        line = str(TimeProfiler.__current_timestamp())
        for tt in timer_tuples:
            line += (TimeProfiler.EOL + "  %s: %s" % (tt[0], tt[1]))
        fp.write(line + TimeProfiler.EOL)


    @classmethod
    def __csv_header_formatter(cls, fp, comment, timer_names):
        """
        Writes header for the CSV-formatted output file.

        Arguments:

         - fp: file-like object we can write() into;

         - comment: None or string that contains description
           of the current timer set;

         - timer_names: array of timer names; guaranteed to have
           the same order as timer_tuples in record formatter.

        We will use '#' as the comment character.
        """

        comment_char = "#"
        header = ""
        if comment != None:
            header += TimeProfiler.__comment_out(comment,
              comment_char, TimeProfiler.CSV_EOL)

        header += "timestamp"
        for tn in timer_names:
            safe_name = tn.replace('"', '""')
            header += '%s"%s"' % (TimeProfiler.CSV_SEP, tn)
        fp.write(header + TimeProfiler.CSV_EOL)


    @classmethod
    def __csv_formatter(cls, fp, timer_tuples):
        """
        Formats record using CSV output format.

        Arguments:

         - fp: file-like object we can write() into;

         - timer_tuples: array of tuples (name, seconds)
           that describe each timer.
        """

        line = str(TimeProfiler.__current_timestamp())
        for tt in timer_tuples:
            line += "%s%s" % (TimeProfiler.CSV_SEP, tt[1])
        fp.write(line + TimeProfiler.CSV_EOL)



    def set_formatter(self, formatter_type):
        """
        Initializes record formatter based on the provided
        formatter type.

        Arguments:
         - formatter_type: type of formatter to use.
           Currently supported ones are:
           * plaintext: simple ASCII file
           * csv: comma-separated file

        TODO: add formatter type "own" and optional argument that
        TODO: will pass two handlers, for header and records.
        """

        if formatter_type == "plaintext":
            self.formatter = TimeProfiler.__plaintext_formatter
            self.hdr_formatter = TimeProfiler.__plaintext_header_formatter
        elif formatter_type == "csv":
            self.formatter = TimeProfiler.__csv_formatter
            self.hdr_formatter = TimeProfiler.__csv_header_formatter
        else:
            raise ArgumentError("Unknown formatter type '%s'" %\
              (formatter_type))


    def add(self, timer, info = None):
        """
        Adds timer to the list of timers we tame and milk

        Arguments:

         - timer: timer instance;

         - info: potentially long description that enables
           people to understand more about the purpose of
           this timer.
        """

        self.timers.append(timer)
        self.timer_information.append(info)


    def dump(self, extension, formatter = None):
        """
        Dumps current values for timers into the output file

        Arguments:

         - extension: file extension for output file; will be concatenated
           with base file name without dot ('.') and any other characters;

         - formatter: if specified and not None, self.set_formatter(formatter)
           will be called at the beginning of this function.
        """

        if formatter != None:
            self.set_formatter(formatter)
        t_tuples = map(lambda x: (x.get_description(), x.get_elapsed()),
          self.timers)
        t_names = map(lambda x: x[0], t_tuples)

        with open(self.filename + extension, "a") as fp:
            fcntl.lockf(fp, fcntl.LOCK_EX)
            try:
                statinfo = os.fstat(fp.fileno())
                if statinfo.st_size == 0:
                    timer_nfo = "\n".join(map(lambda x: "  %s: %s" % (x[0], x[1]),
                      zip(t_names, self.timer_information)))
                    if len(timer_nfo):
                        timer_nfo = """

Timer information:
""" + timer_nfo
                    self.hdr_formatter(fp, self.comment + timer_nfo,
                      t_names)

                self.formatter(fp, t_tuples)
            finally:
                fcntl.lockf(fp, fcntl.LOCK_UN)


class TimerlikeCount(object):
    """
    Implements ProfilingTimer-like interface suitable for putting
    static counts into TimeProfiler
    """

    def __init__(self, description):
        """ Class constructor """
        self.description = description
        self.value = 0


    def set(self, value):
        """
        Sets stored value to the provided quantity.
        """

        self.value = value


    def get(self):
        """
        Returns stored value.
        """

        return self.value


    def get_description(self):
        """
        Returns our description.
        """

        return self.description


    def get_elapsed(self):
        """
        Returns stored value.
        """

        return self.value
