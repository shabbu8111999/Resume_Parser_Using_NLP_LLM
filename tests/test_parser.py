from resumeParser import parser

def test_email_extraction():
    text = "Contact me at shabareesh08@gmail.com.com"
    assert parser.extract_email(text) == "test.email@example.com"

def test_name_extraction():
    text = "My name is Shabareesh Nair and I am a AI Engineer."
    name = parser.extract_name(text)
    assert name is not None and isinstance(name, str)
