#!/usr/bin/env python
# Copyright (c) 2018, PerformLine, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the company nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PERFORMLINE, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from __future__ import absolute_import
from __future__ import unicode_literals
import sys
from performline.client import Client

COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']


def c(line, color=None, bold=False, nl=True):
    if color in COLORS:
        b = '1' if bold else '0'

        sys.stderr.write('\033[' + b + ';3' + str(COLORS.index(color)) + 'm')
        sys.stderr.write(line)
        sys.stderr.write('\033[' + b + ';m')
    else:
        sys.stderr.write(line)

    if nl:
        sys.stderr.write('\n')


def p(line, color=None, bold=False):
    c(line, color=color, bold=bold, nl=False)


try:
    try:
        client = Client(sys.argv[1])
    except IndexError:
        c('Must specify a valid PerformLine API token as the first parameter.')
        sys.exit(1)

    traffic_sources = dict()

    # iterate through all brands
    for brand in client.brands():
        c("Brand: {} (id: {})".format(brand.name, brand.id))

        # iterate through all campaigns in this brand
        for campaign in brand.campaigns():
            c("| Campaign: {} (id: {})".format(campaign.name, campaign.id))

            # iterate through all scorable items in this campaign
            for item in campaign.items():
                ts_name = ''

                try:
                    ts_name = traffic_sources[item.traffic_source_id].name
                except KeyError:
                    try:
                        traffic_sources[item.traffic_source_id] = item.traffic_source
                        ts_name = item.traffic_source.name
                    except:
                        pass
                except:
                    pass

                p("| \u2514 Item {}: {} ".format(
                    item.id,
                    item.type
                ))

                score = '(score: {:-2d})'.format(item.score or 0)

                # colorize the output based on the item's score
                if item.score <= 30:
                    p(score, 'red', bold=True)
                elif item.score <= 70:
                    p(score, 'yellow', bold=True)
                else:
                    p(score, 'green', bold=True)

                c(" (source: {})".format(ts_name))

except KeyboardInterrupt:
    c('Quitting...')
    sys.exit(0)