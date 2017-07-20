from tracking_code_parsing.project_setup import read_file_data

import unittest


class TestMyFunctions(unittest.TestCase):
    def test_read_file_data(self):
        import json
        sample_json = {
                      "name" : "John",
                      "shares" : 100,
                      "price" : 1230.23
                      }
        sample_json = json.dumps(sample_json, ensure_ascii=False,  encoding="utf8")
        path = "/Users/edwari/projects/question-library/qa_team/json_files"
        filename = "testcase.json"
        self.assertEqual(read_file_data(filename, path), sample_json)

if __name__ == '__main__':
    unittest.main()