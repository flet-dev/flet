from html.parser import HTMLParser
from urllib.parse import urljoin

import pytest

from flet_web.patch_index import patch_index_html


class BaseParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "base":
            self.href = dict(attrs)["href"]


@pytest.mark.parametrize(
    "base_tag",
    ['<base href="/">', '<base href="/deployed/">', "<base href='/deployed/'>"],
)
@pytest.mark.parametrize("mount_path", ["/", "/apps/demo/"])
def test_client_scripts_resolve_under_server_mount(tmp_path, base_tag, mount_path):
    index = tmp_path / "index.html"
    index.write_text(
        f"<html><head>{base_tag}<!-- fletAppConfig --></head>"
        '<body><script src="flutter_bootstrap.js"></script></body></html>',
        encoding="utf-8",
    )

    patch_index_html(str(index), base_href=mount_path)

    parser = BaseParser()
    parser.feed(index.read_text(encoding="utf-8"))
    assert urljoin(parser.href, "flutter_bootstrap.js") == (
        mount_path + "flutter_bootstrap.js"
    )
