"""
Copyright (c) 2014, Eric Dill
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the {organization} nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import urllib
import re


def get_xkcd_colors():
    """

    Returns
    -------
    dict
        Dictionary of color_name : color pairs where 'color_name' is the xkcd
        color name and 'color' is the html color code of the form: #RRGGBB
    """
    # create a socket to the xkcd colors
    sock = urllib.urlopen("http://xkcd.com/color/rgb.txt")
    # read the html source
    htmlsrc = sock.read()
    # close the connection to the website
    sock.close()
    colors = {}
    # split the lines based on the new line character
    lines = re.split(r'\n+', htmlsrc)
    # loop over the lines
    for line in lines:
        # split the lines based on the tab character
        split_line = re.split(r'\t+', line)
        # if the line has two entries, treat the first as the xkcd color name
        # and the second as the html color tag
        if len(split_line) > 1:
            colors[split_line[0]] = split_line[1]
    # return the dict
    return colors

print get_xkcd_colors()