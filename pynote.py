import argparse
import contextlib
import json
import pathlib
import sys

NEWLINE = "\n"
DOCSTRING = '"""'
CODE_SECTION = "```"


def strip_list(data):
    def get_first_not_empty_element(data):
        for i, e in enumerate(data):
            if e:
                return i

    idx = get_first_not_empty_element(data)
    if idx:
        data = data[idx:]

    idx = get_first_not_empty_element(data[::-1])
    if idx:
        data = data[:-idx]

    return data


class IterBack:
    def __init__(self, iterable) -> None:
        self.iterable = iterable
        self.len = len(iterable)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        next, self.index = self.index, self.index + 1
        if next >= self.len:
            raise StopIteration
        val = self.iterable[next]
        return val.removesuffix("\n")

    def backward(self):
        self.index -= 1


class Block:
    def __init__(self, lines):
        self.lines = strip_list(lines)

    def render():
        ...

    def __repr__(self):
        return str(self.lines)

    def __bool__(self):
        return bool(self.lines)

    def is_empty(self):
        return not any(line for line in self.lines)


class Code(Block):
    def render(self):
        if self.is_empty():
            return []
        return [
            f"{CODE_SECTION}py",
            *self.lines,
            CODE_SECTION,
        ]


class Markdown(Block):
    def render(self):
        return [
            *self.lines,
        ]


class Document:
    def __init__(self) -> None:
        self._data = []

    def title(self):
        if not self._data:
            return ""

        block = self._data[0]
        if not isinstance(block, Markdown):
            return ""

        first_line = block.render()[0]
        if not first_line.startswith("# "):
            return ""

        return str(first_line[1:])

    def append(self, item):
        self._data.append(item)

    def to_markdown(self):
        result = []
        for block in self._data:
            if block:
                for line in block.render():
                    result.append(line)
                    result.append(NEWLINE)
                result.append(NEWLINE)
        return result

    def to_html(self):
        title = self.title()
        jsons = json.dumps(self.to_markdown(), indent=4, separators=(",", ": "))
        return (
            """
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title>"""
            + title
            + """</title>
<link rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
div#content {
    max-width: 48.5em;
    margin: 2em auto;
    padding: 3em;
    font-size: 15px;
    font-family: Helvetica, sans-serif;
    background: #fff;
    border-radius: .3em;
    border: 1px solid #ddd;
}
a{color: #0f7afc; border-bottom-color: rgba(15, 122, 252, 0.2); text-decoration:none}
a:hover{color:#cf0000; border-bottom-color: rgba(208, 64, 0, 0.2); text-decoration:none}
a:visited{ color: #800080; border-bottom-color: rgba(128, 0, 128, 0.2); text-decoration:none}
</style>
</head>
<body>
<div id="content" ></div>
<script>
    document.getElementById('content').innerHTML =
    marked.parse("""
            + jsons
            + """.join(''));
</script>
<script>hljs.highlightAll();</script>
</body>
</html>
        """
        )


def is_markdown_block(line):
    return line.startswith(DOCSTRING) and len(line) == 3


def is_markdown_oneliner(line):
    return line.startswith(DOCSTRING) and line.endswith(DOCSTRING) and len(line) > 6


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="+", type=pathlib.Path)
    parser.add_argument("--html", action=argparse.BooleanOptionalAction)
    return parser.parse_args(args)


def process_content(content):
    document = Document()
    iterator = IterBack(content)

    for line in iterator:
        if is_markdown_oneliner(line):
            line = line.removeprefix(DOCSTRING).removesuffix(DOCSTRING)
            document.append(Markdown([line]))
        elif is_markdown_block(line):
            items = []
            with contextlib.suppress(StopIteration):
                while (line := next(iterator)).startswith(DOCSTRING):
                    items.append(line)
            document.append(Markdown(items))
        else:
            items = [line]
            with contextlib.suppress(StopIteration):
                while not (line := next(iterator)).startswith(DOCSTRING):
                    items.append(line)
            document.append(Code(items))
            iterator.backward()

    return document


def process_file(file, config):
    with open(file, "r") as f:
        content = f.readlines()

    document = process_content(content)

    new_path = file.absolute().parent / "output" / file.stem
    new_path.parent.mkdir(parents=True, exist_ok=True)

    with open(new_path.with_suffix(".md"), "w") as f:
        f.writelines(document.to_markdown())

    if config.html:
        with open(new_path.with_suffix(".html"), "w") as f:
            f.write(document.to_html())


def main(config):
    for file in config.path:
        process_file(file, config)


if __name__ == "__main__":
    config = parse_args(sys.argv[1:])
    main(config)
