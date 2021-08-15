from mkad.app.utils.dict_researcher import KeyResearcher

def test_key_researcher():
    researcher = KeyResearcher()
    _dict= {
        "Test": True,
        "Foo": {
            "Test": False
        },
        "test": "Ignored"
    }

    result1= researcher.search_in(_dict, "Test")
    expected1= [True, False]

    result2= researcher.search_in(_dict, "test")
    expected2= ["Ignored"]

    result3= researcher.search_in(_dict, "Foo")
    expected3= [{"Test": False}]

    assert result1 == expected1
    assert result2 == expected2
    assert result3 == expected3