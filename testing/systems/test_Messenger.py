from src.systems.Messenger import Messenger

def test_process_message():
    m=Messenger(None)
    m.process_message("ABCDEFG")
    assert m.get_message_history()=="ABCDEFG"

    m.process_message("12345")
    assert m.get_message_history()=="ABCDEFG12345"

