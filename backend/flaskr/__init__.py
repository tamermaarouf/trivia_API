import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions



def paginate_categories():
    categories = Category.query.order_by(Category.type).all()

    if (len(categories) == 0):
        abort(404)

    current_categories = {category.id: category.type for category in categories}

    return current_categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)


    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", 
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", 
                              "GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():

        current_categories = paginate_categories()

        return jsonify({
            "success": True,
            'categories': current_categories
            })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/')
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if (len(current_questions) == 0):
            abort(404)

        current_categories = paginate_categories()


        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "categories": current_categories
            })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:questions_id>', methods=['DELETE'])
    def delete_questions(questions_id):
        try:
            question = Question.query.get(questions_id)
            print(question)

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                "success": True,
                "deleted": questions_id
                })
        except Exception as e:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def add_questions():
        if request.method == 'POST':
            try:
                body = request.get_json()
                for key, value in body.items():
                    if value != '':
                        print(value)
                        new_question = body.get("question")
                        new_answer = body.get("answer")
                        new_category = body.get("category")
                        new_difficulty = body.get("difficulty")
                    else:
                        abort(422)
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                return jsonify({
                    "success": True,
                    "questions_id": question.id
                    })
            except Exception as e:
                abort(422) 

    

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/search', methods=['POST'])
    def search_term():
        body = request.get_json()
        searchTerm = body.get("searchTerm", None)
        print(searchTerm)
        selection = Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
        if selection:
            current_questions = paginate_questions(request, selection)
            categories = paginate_categories()

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "currentCategory": None
                })
        else:
            abort(404)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def getByCategory(category_id):
        selection = Question.query.filter(Question.category==category_id).all()

        totalQuestions = len(selection)
        current_questions = paginate_questions(request, selection)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": totalQuestions,
            "current_category": None
            })


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(500)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
            405,
        )


    return app