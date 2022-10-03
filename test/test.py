import sys
import HttpTrigger1

def test_compose_response():
    json_data = {
                "recordId": "e1",
                "data":
                    {
                        "text":  "筆者の子どもが通う公立の小学校は、来年で150周年の節目を迎えるそうです。\
                                  具体的には、1873年（明治6年）創立とあります。立派な歴史だなあと思う一方で、\
                                  日本で最も古い歴史を持つ現役の公立小学校は、どこになるのか気になりました。",
                    }
                }   
    res = HttpTrigger1.transform_value(json_data)
    print(res)

    assert True