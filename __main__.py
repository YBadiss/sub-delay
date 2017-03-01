import click
import re
from datetime import datetime, timedelta
from os import path


class SubtitleDelayer(object):
    TIME_PATTERN = re.compile("^(?P<h>\d\d):(?P<m>\d\d):(?P<s>\d\d),(?P<ms>\d\d\d)$")

    def __init__(self, delay_in_seconds):
        self.delay = timedelta(seconds=delay_in_seconds)

    def delay_subtitle_file(self, file_path):
        input_lines = self.__read_input_file(file_path)
        out_lines = [self.__delay_subtitle(line) for line in input_lines]
        self.__write_output_file(self.__make_output_file_path(file_path), out_lines)
        
    def __delay_subtitle(self, line):
        split_line = line.split(" --> ")
        if len(split_line) == 2:
            return " --> ".join([self.__delay_time_str(time_str) for time_str in split_line])
        else:
            return line

    def __delay_time_str(self, time_str):
        match = SubtitleDelayer.TIME_PATTERN.match(time_str)
        if match:
            dt = datetime.now().replace(
                hour=int(match.group('h')),
                minute=int(match.group('m')),
                second=int(match.group('s')),
                microsecond=int(match.group('ms')) * 1000) + self.delay
            return "{:0>2d}:{:0>2d}:{:0>2d},{:0>3d}".format(dt.hour, dt.minute, dt.second, dt.microsecond / 1000)
        else:
            return line

    def __read_input_file(self, file_path):
        with open(file_path) as f:
            return f.read().splitlines()
    
    def __make_output_file_path(self, file_path):
        return path.join(path.dirname(file_path), "out.{}".format(path.basename(file_path)))

    def __write_output_file(self, file_path, lines):
        with open(file_path, "w+") as f:
            f.write("\n".join(lines))


@click.command()
@click.option('--srt', prompt='File', help='Subtitle file to delay')
@click.option('--delay', prompt='Delay (s)', help='Delay in second')
def delay_srt(srt, delay):
    delayer = SubtitleDelayer(float(delay))
    delayer.delay_subtitle_file(srt)


if __name__ == "__main__":
    delay_srt()