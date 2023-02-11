import boto3
from boto3.dynamodb.table import TableResource


def initiate_dynamodb_table(table_name: str):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    return table


def update_table(table: TableResource, key: dict, expression: str, expression_attr: dict):
    table.update_item(Key=key,
                      UpdateExpression=expression,
                      ExpressionAttributeValues=expression_attr
                      )


def delete_from_table(table: TableResource, key: dict):
    table.delete_item(Key=key)


def insert_to_table(table: TableResource, item: dict):
    table.put_item(Item=item)


def get_from_table(table: TableResource, key: dict):
    response = table.get_item(Key=key)
    print(response)
    return response


def __main__():
    table_name = "Students"
    key = {"id": "32438"}
    expression = "SET full_name = :val1"
    expression_attr = {":val1": "Ximena González"}
    item = {'id': '32438',
            "full_name": "Ximena Lizeth González Plascencia",
            "personal_website": "ximena.cetystijuana.com"}

    students_table = initiate_dynamodb_table(table_name)
    update_table(students_table, key, expression, expression_attr)
    delete_from_table(students_table, key)
    insert_to_table(students_table, item)
    get_from_table(students_table, key)


__main__()
