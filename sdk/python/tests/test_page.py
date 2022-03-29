def test_page(page):
    assert page.url != "" and page.url.startswith("http"), "Test failed"
