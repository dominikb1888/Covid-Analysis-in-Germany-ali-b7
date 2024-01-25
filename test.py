from json_to_db import JsonInDatabaseTransformer

if __name__ == "__main__":
    test_db_name = 'test_data_for_web_application.db'
    test_json_path = 'test_data.json'
    transformer = JsonInDatabaseTransformer(test_db_name)
    transformer.push_json_data_in_db(test_json_path)
