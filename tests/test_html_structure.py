import os
from html.parser import HTMLParser

class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_nav = False
        self.in_ul = False
        self.a_count = 0
        self.in_sectiondiv1 = False
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == "nav":
            self.in_nav = True
        if tag == "ul" and self.in_nav:
            self.in_ul = True
        if tag == "a" and self.in_nav and self.in_ul:
            self.a_count += 1

        if tag == "div" and dict(attrs).get("class") == "sectiondiv1":
            self.in_sectiondiv1 = True
        if tag == "h1" and self.in_sectiondiv1:
            self.h1_count += 1

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_nav = False
            self.in_ul = False
        if tag == "ul" and self.in_nav:
            self.in_ul = False
        if tag == "div" and self.in_sectiondiv1:
            self.in_sectiondiv1 = False

def test_navigation_and_section():
    parser = StructureParser()
    root = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(root, 'index.html'), 'r', encoding='utf-8') as f:
        parser.feed(f.read())
    assert parser.a_count == 3, "Navigation should contain exactly three links"
    assert parser.h1_count == 1, "sectiondiv1 should contain exactly one h1"
