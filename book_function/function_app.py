import azure.functions as func
import datetime
import json
import logging
import pymongo

app = func.FunctionApp()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['local']
mycol = db['books']

@app.route(route="book_function", auth_level=func.AuthLevel.ANONYMOUS)
def book_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    if req.method == "GET":

        title = req.params.get('title')
        if not title:
            title = req_body.get('title')

        if title:
            book = mycol.find_one({"title": title})
            author = book.get("author")
            return func.HttpResponse(f"Author of the book {title} is {author}.")
        else:
            return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass a title in the query string or in the request body for a personalized response.",
                status_code=200
            )

    elif req.method == "PUT":
        book = mycol.find_one({"title": title})
        if not book:
            return func.HttpResponse("Book not found.", status_code=404)
        updated_book = book.copy()
        updated_book.update(req.get_json())
        mycol.replace_one({"title": title}, updated_book)
        return func.HttpResponse(f"Book {title} was replaced successfully.")

    elif req.method == "POST":
        req_body = req.get_json()
        mycol.insert_one(req_body)
        return func.HttpResponse(f"New Book was added!")

    elif req.method == "DELETE":
        title = req.params.get('title')
        book = mycol.find_one({"title": title})
        if not book:
            return func.HttpResponse(f"Book with the title {title} was not found.", status_code=404)
        mycol.delete_one({"title": title})
        return func.HttpResponse(f"Book with the title {title} was deleted successfully.", status_code=200)

    elif req.method == "PATCH":
        req_body = req.get_json()
        title = req.params.get('title')
        book = mycol.find_one({"title": title})
        mycol.update_one({"title": title}, {"$set": req_body})
        return func.HttpResponse(f"Book with the title {title} was updated successfully.")


