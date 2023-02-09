#!/usr/bin/env python3

from PyPDF2 import PdfReader, PdfWriter
import re
import sys
from pathlib import Path
import os
import subprocess
import argparse

"""
This is a script to modify PDF files so that documents NOT created with the scansnap
can still be OCRed by the ABBYY converter.

It works by setting the PDF's creator metadata to "ScanSnap Manager #s1300"

The key to this hack was provided by this blog:
http://jakartaunwired.blogspot.com/2013/02/how-to-hack-scansnap-organizer-to-use.html

Example:
python fixcreator.py -o outfile in.pdf     # generates outfile/in.pdf

"""

class PdfHacker():
    
    def __init__(self, in_path, out_path):
        self.reader = PdfReader(in_path)
        self.out_path = out_path
        
        return

    def hack_file(self):
        writer = PdfWriter()

        #num_pages = self.reader.getNumPages()
        num_pages = len(self.reader.pages)
        print(f"processing ({num_pages}) pages")
        for p in self.reader.pages:
            writer.add_page(p)
        #

        writer.add_metadata(
            {
                "/Creator": "ScanSnap Manager #S1300",
            }
        )
        assert self.out_path.exists()==False, f"{self.out_path} already exists; cannot overwrite"
        with open(self.out_path, "wb") as f:
            writer.write(f)
        #
        print(f"wrote to {self.out_path}")

def parse_args():
    parser = argparse.ArgumentParser(description="convert PDF file to work w/ ABBYY; output is written to FIXED-<in_file>.pdf")
    parser.add_argument("in_file", type=str, help="input file")
    args =parser.parse_args()

    if Path(args.in_file).is_file()==False:
        print(f"{args.in_file} is not a file")
        sys.exit(0)
    #
    return args
    
if __name__=="__main__":
    args = parse_args()
    in_path = Path(args.in_file)
    assert in_path.suffix.lower()==".pdf"

    out_path = Path(f"{in_path.parent}/FIXED-{in_path.name}")

    hacker = PdfHacker(in_path, out_path)
    hacker.hack_file()




