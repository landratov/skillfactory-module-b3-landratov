import sys

class Tag:
    def __init__(self, tag, is_single = False, klass = None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.text = ""
        self.attributes = {}

        self.children = []

        if klass != None:
            self.attributes["class"] = " ".join(klass)

        for attribute, value in kwargs.items():
            self.attributes[attribute] = value

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        if self.attributes != {}:
            for attribute, value in self.attributes.items():
                attrs.append(f"{attribute}=\"{value}\"")
        attrs = " ".join(attrs)

        if attrs != "":
            attrs = " " + attrs

        if len(self.children) > 0:
            opening = f"<{self.tag}{attrs}>\n"
            internal = self.text
            for child in self.children:
                internal += str(child) + "\n"
            ending = f"</{self.tag}>"
            return opening + internal + ending
        else:
            if self.is_single:
                return f"<{self.tag}{attrs}>"
            else:
                return f"<{self.tag}{attrs}>{self.text}</{self.tag}>"

class TopLevelTag(Tag):
    pass

class HTML(Tag):
    def __init__(self, output = None):
        self.output = output
        self.text = ""
        self.tag = "html"
        self.children = []
        self.attributes = {}

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = None

    with HTML(output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body