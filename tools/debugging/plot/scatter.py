#!/usr/bin/env python
import argparse
import csv
import datetime
import sys

from matplotlib import dates, pyplot

parser = argparse.ArgumentParser()
parser.add_argument(
    "--header", help="If the csv does not have a header, use this to give a name to each column"
)
parser.add_argument(
    "output", help="file name for the result image, filetype is inferred from this."
)
parser.add_argument("x")
parser.add_argument("y")

args = parser.parse_args()


def parse_datetime(data):
    return datetime.datetime.fromisoformat(data)


def configure_axes(axes):
    hour_fmt = dates.DateFormatter("%H:%M")
    minutes_fmt = dates.DateFormatter("%M")

    axes.xaxis.set_major_locator(dates.HourLocator(interval=1))
    axes.xaxis.set_major_formatter(hour_fmt)
    axes.xaxis.set_minor_locator(dates.MinuteLocator(interval=5))
    axes.xaxis.set_minor_formatter(minutes_fmt)
    axes.xaxis.set_tick_params(which="major", rotation=90)
    axes.xaxis.set_tick_params(which="minor", rotation=90)

    axes.set_xlabel("time")
    axes.set_ylabel("RTT")


x_axis = list()
y_axis = list()

if args.header:
    headers = args.header.split(",")
    reader = csv.DictReader(sys.stdin, fieldnames=headers)
else:
    reader = csv.DictReader(sys.stdin)

for line in reader:
    x_axis.append(parse_datetime(line[args.x]))
    y_axis.append(float(line[args.y]))

axes = pyplot.gca()

configure_axes(axes)
axes.set_xlim(min(x_axis), max(x_axis))

pyplot.scatter(x_axis, y_axis, alpha=0.2)
pyplot.savefig(args.output)