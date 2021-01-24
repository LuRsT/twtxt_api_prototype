from twtxt_api import format_twtxt


def test_format_twtxt_username_link():
    twtxt_text = "@<gil https://tilde.pt/~gil/twtxt.txt>"
    expected_formatted_text = '<a href="https://tilde.pt/~gil/twtxt.txt" target="_blank">@gil</a>'

    formatted_text = format_twtxt(twtxt_text)

    assert formatted_text == expected_formatted_text

def test_format_twtxt_normal_link():
    twtxt_text = "are you using https://github.com/mdom/txtnish ?"
    expected_formatted_text = 'are you using <a href="https://github.com/mdom/txtnish" target="_blank">https://github.com/mdom/txtnish</a> ?'

    formatted_text = format_twtxt(twtxt_text)

    assert formatted_text == expected_formatted_text

