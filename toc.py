"""Generate generate table of contents within Markdown (.md) files."""

# Steps:
#
# 1. Open .md doc for reading; get the doc as a Python str
# 2. Build a generator of (level: int, header: str) for the found headers
# 3. Format & indent the found headers using []() Markdown style
# 4. Replace '<!---toc start-->', '<!---toc end-->', and text in between
#    with the str result from (3.)
# 5. Overwrite the input file with the result

from __future__ import print_function
from __future__ import unicode_literals

import pathlib
import argparse
import collections
import os
import re
import sys

import requests
from xtermcolor import colorize


TOC_PAT = re.compile(
    r"[ \t]*<\!---toc start-->(.*?)<\!---toc end-->[ \t]*",
    flags=re.DOTALL | re.M,
)

# Pattern needs to be careful for URLs containing parentheses,
# nested within the actual Markdown link's parentheses.
# I.e.
# [Text here](https://www.cool.com/this(-is-a)-link.html)
MD_LINK_PAT = re.compile(
    r"\[([^\[\]]+)\]"  # Brackets containing non-bracket characters
    r"\((([^\s)(]|\([^\s)(]*\))*)\)",  # Outer parentheses
    re.M,
)

# A Markdown "atx-style" header, GitHub-flavored.
# See https://github.github.com/gfm/#atx-heading
HEADER_PAT = re.compile(r"^\s{,3}(#{1,6})\s+(.*)")

# Used in _strip() - see docstring.
# NOTE: GitHub seems to get its own logic wrong on this one.
# It will render:
# - "### foo \###" as "foo ###"
# - "## foo #\##" as "foo ###"
# Go figure.  We take the rule for its word.
STRIP_CANDIDATE_PAT = re.compile(r"(?<!\\)[ \t#]+$|^[ \t#]+")

# Bold & italics get dropped from links
ITAL_PAT = re.compile(r"(?<!\\)_[^(?<!\\)_]+(?<!\\)_")
BOLD_PAT = re.compile(r"(?<!\\)\*[^(?<!\\)\*]+(?<!\\)\*")

class MarkdownError(Exception):
    """Markdown formatted incorrectly & unparseable."""


def _strip(x, _sub=STRIP_CANDIDATE_PAT.sub):
    """Strip surrounding spaces, tabs, and hash signs.

    Don't strip escaped hash signs.

    This is equivalent to str.strip but with the negative lookbehind
    assertion found in STRIP_CANDIDATE_PAT.
    """
    return _sub("", x)


def _replace_ital_bold(s):
    to_repl = "_*"
    for pat in (ITAL_PAT, BOLD_PAT):
        for match in pat.finditer(s):
            found = match.group(0)
            s = s.replace(found, found.strip(to_repl))
    return s


def as_link(x):
    """Convert Markdown header string into relative URL."""
    res = re.sub(
        r"[^-\w\s]",
        "",
        re.sub(r"\s+", "-", _strip(x.lower())),
        flags=re.U,  # Python 2
    )
    # Slow route: check and remove bold & italic marks.
    # TODO: find a fast route for this.
    # We also cannot simply count occurences of _ and *, since
    # they may be escaped by \
    res = _replace_ital_bold(res)

    # One more fix: if the resulting link ends with multiple hyphens,
    # make it just one.
    if res.endswith("--"):
        res = res.strip("-") + "-"
    return res


def escape(x):
    """Escape brackets, '['' and ']'."""
    return x.replace("[", "\\[").replace("]", "\\]")


def toc(md_string):
    """Takes a Markdown string, returns TOC string (in Markdown).

    Formats indented headers in []() style.
    """

    toc = []
    n_seen = collections.defaultdict(int)

    for level, header in headers(md_string):

        # If we see the same header multiple times (regardless of level),
        # it should have a 1..n suffix on the end.  The first occurence
        # gets no suffix; others get 1..n.
        link = as_link(header)
        n = n_seen[link]
        if n > 0:
            n_seen[link] += 1
            link += "-" + str(n)
        else:
            n_seen[link] += 1

        toc.append(
            "{spaces}* [{header}](#{link})".format(
                spaces="  " * (level - 1),
                header=escape(_strip(header)),
                link=link,
            )
        )
    return "\n".join(toc)


def headers(md_string):
    """Generator of (level: int, header: str) tuples from Markdown string.

    The headers are not yet formatted (cleaned); they are only generated here
    via match for what loosely describes an ATX header pattern.
    """

    is_comment_block = False
    for line in md_string.split("\n"):
        if line.startswith("```"):
            is_comment_block = not is_comment_block
        if is_comment_block:
            continue
        header = HEADER_PAT.match(line)
        if header:
            level = len(header.group(1))
            header = header.group(2)
            yield level, header


def modify_and_write(path, outfile=None):
    """Write a table of contents to the Markdown file at `path`.

    Overwrites the file in place.

    If no tags or improper tags (<!---toc start--> and <!---toc end-->),
    raise MarkdownError before writing back.

    If `outfile` is not None, write the results to that file.
    Otherwise, overwrite the input `path` inplace.
    """

    write_stdout = outfile is sys.stdout

    markdown = pathlib.Path(path).read_text(encoding='utf-8')
    table_of_contents = toc(markdown)

    new_markdown, replacements = TOC_PAT.subn(
        "<!---toc start-->\n\n{}\n\n<!---toc end-->".format(table_of_contents),
        markdown,
    )

    # If we couldn't find tags and 0 replacements were made, let user
    # know and raise.
    if not write_stdout:
        if not replacements:
            raise MarkdownError(
                "Document missing toc start/end tags.\n"
                "Add these delimiters to your Markdown file:\n\n"
                "\t<!---toc start-->\n"
                "\t<!---toc end-->\n\n"
                "Then, run:\n\n"
                "\t$ mdtoc %s" % path
            )

        elif replacements > 1:
            raise MarkdownError(
                "Multiple toc start/end tag pairs detected."
                " Your Markdown file should include only one pair of tags"
            )

    if outfile is None:
        # Default
        outfile = path

    if write_stdout:
        outfile.write(table_of_contents + "\n")
    else:
        pathlib.Path(path).write_text(new_markdown, encoding='utf-8')
        print(
            colorize("Success: wrote TOC to {path}".format(path=outfile), ansi=22)
        )


def get_links(md_string):
    """Find links in a Markdown string.

    Yields a 4-tuple: text, URL, linenum, colnum.
    """

    def line_col(position):
        l, c = 1, 1
        for idx, char in enumerate(md_string):
            if idx == position:
                break
            elif char in {"\r", "\n"}:
                l, c = l + 1, 1
            else:
                l, c = l, c + 1
        return (l, c)

    for m in MD_LINK_PAT.finditer(md_string):
        line, col = line_col(m.start(1))
        yield m.group(1), m.group(2), line, col


_description = """
Generates table of contents for Markdown files.

The algorithm searches for the text blocks
between the delimiters:

<!---toc start--->
... anything ...
<!---toc end--->

The contents of the block are then replaced
by a table of contents.
"""


def parse_args():
    """Parse command-line arguments."""
    from mdtoc import __version__

    parser = argparse.ArgumentParser(
        description=_description,
        epilog="Created by Scott Frazer (https://github.com/scottfrazer).\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--check-links",
        action="store_true",
        help="find all hyperlinks and ensure that\nthey point to something valid",  # noqa
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--outfile",
        help="instead of overwriting the input file,\n"
             "write to this file instead",
    )
    group.add_argument(
        "--stdout",
        action="store_true",
        help="don't write or overwrite any file;\n"
             "just print the TOC (not full .md file) to stdout",
    )
    parser.add_argument(
        "markdown_file",
        help="relative or abs. path of the Markdown\n(.md) file to overwrite",
    )
    return parser.parse_args()


def cli():
    """Command-line entry point."""
    cli = parse_args()
    cli.markdown_file = os.path.expanduser(cli.markdown_file)
    if cli.stdout:
        outfile = sys.stdout
    elif cli.outfile:
        outfile = cli.outfile
    else:
        outfile = None
    try:
        modify_and_write(cli.markdown_file, outfile=outfile)
    except OSError:
        print(
            colorize(
                "Failed: " "Not found: {path}".format(path=cli.markdown_file),
                ansi=1,
            )
        )
        return 1
    except MarkdownError as e:
        print(colorize("Failed: " + str(e), ansi=1))
        return 1

    if cli.check_links:
        with open(cli.markdown_file) as fp:
            contents = fp.read()

        valid_http_fragments = [
            "#" + as_link(h) for (l, h) in headers(contents)
        ]
        for text, link, line, col in get_links(contents):
            valid = "unrecognized link type"
            if link.startswith("#"):
                if link not in valid_http_fragments:
                    valid = colorize("INVALID", ansi=1)
                else:
                    valid = colorize("VALID", ansi=2)
            elif link.startswith("http://") or link.startswith("https://"):
                r = requests.get(link)
                valid = "Response: {}".format(r.status_code)
            print(
                "Checking {line}:{col} [{text}]({link}) --> {valid} ".format(
                    text=colorize(text, ansi=3),
                    link=colorize(link, ansi=4),
                    line=line,
                    col=col,
                    valid=valid,
                )
            )

if __name__ == "__main__":
    txt = pathlib.Path("readme.md").read_text(encoding='utf-8')
    print(toc(txt))

