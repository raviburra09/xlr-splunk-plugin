#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys

from splunklib.modularinput.event import ET

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class EventWriter(object):
    """``EventWriter`` writes events and error messages to Splunk from a modular input.

    Its two important methods are ``writeEvent``, which takes an ``Event`` object,
    and ``log``, which takes a severity and an error message.
    """

    # Severities that Splunk understands for log messages from modular inputs.
    # Do not change these
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"

    def __init__(self, output = sys.stdout, error = sys.stderr):
        """
        :param output: Where to write the output; defaults to sys.stdout.
        :param error: Where to write any errors; defaults to sys.stderr.
        """
        self._out = output
        self._err = error

        # has the opening <stream> tag been written yet?
        self.header_written = False

    def write_event(self, event):
        """Writes an ``Event`` object to Splunk.

        :param event: An ``Event`` object.
        """

        if not self.header_written:
            self._out.write("<stream>")
            self.header_written = True

        event.write_to(self._out)

    def log(self, severity, message):
        """Logs messages about the state of this modular input to Splunk.
        These messages will show up in Splunk's internal logs.

        :param severity: ``string``, severity of message, see severities defined as class constants.
        :param message: ``string``, message to log.
        """

        self._err.write("%s %s\n" % (severity, message))
        self._err.flush()

    def write_xml_document(self, document):
        """Writes a string representation of an
        ``ElementTree`` object to the output stream.

        :param document: An ``ElementTree`` object.
        """
        self._out.write(ET.tostring(document))
        self._out.flush()

    def close(self):
        """Write the closing </stream> tag to make this XML well formed."""
        self._out.write("</stream>")