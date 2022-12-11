import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/")
    def helloWorld():
        return "Hello World!"
    
    #  ----------------------------------------------------------------
    #  Methods
    #  ----------------------------------------------------------------
    
    # Get pagination from a list
    def pagination(page, limit, elements):
        start = (page - 1) * limit
        end = start + limit
        
        items = [element.format() for element in elements]
        current_items = items[start:end]
        
        return current_items

    #  ----------------------------------------------------------------
    #  GETs
    #  ----------------------------------------------------------------

    #  GET Questions
    @app.route('/questions')
    def retrieve_questions():
        data = {}
        
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 10, type=int)
            
            questions = Question.query.order_by(Question.id).all()
            questions_length = len(questions)
            
            paginated_questions = [] if questions_length == 0 else pagination(page, limit, questions)
            paginated_questions_length = len(paginated_questions)
            
            data = {
                "success": True,
                "real_total": questions_length,
                "paginated_total": paginated_questions_length,
                "questions": paginated_questions,
                "current_page": page
            }
        except:
            print( sys.exc_info() )
            abort(500)
            
        return jsonify(data)

    #  GET Categories
    @app.route('/categories')
    def retrieve_categories():
        data = {}
        
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 10, type=int)
            
            categories = Category.query.order_by(Category.id).all()
            categories_length = len(categories)
            
            paginated_categories = [] if categories_length == 0 else pagination(page, limit, categories)
            paginated_categories_length = len(paginated_categories)
            
            data = {
                "success": True,
                "real_total": categories_length,
                "paginated_total": paginated_categories_length,
                "categories": paginated_categories,
                "current_page": page
            }
        except:
            print( sys.exc_info() )
            abort(500)
            
        return jsonify(data)
    
    #  GET Category by ID
    @app.route('/categories/<int:category_id>')
    def retrieve_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
            
        if category is None:  
            abort(404)
        else:
            return jsonify({
                "success": True,
                "category": category.format(),
            })
            
    #  GET Questions by Category
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
            
        if category is None:  
            abort(404)
        else:
            questions = category.questions
            
            try:
                page = request.args.get("page", 1, type=int)
                limit = request.args.get("limit", 10, type=int)
                
                questions_length = len(questions)
                
                paginated_questions = [] if questions_length == 0 else pagination(page, limit, questions)
                paginated_questions_length = len(paginated_questions)
                
                return jsonify({
                    "success": True,
                    "real_total": questions_length,
                    "paginated_total": paginated_questions_length,
                    "questions": paginated_questions,
                    "current_page": page
                })
            except:
                print( sys.exc_info() )
                abort(500)
            
            
    #  GET Question by ID
    @app.route('/questions/<int:question_id>')
    def retrieve_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
            
        if question is None:  
            abort(404)
        else:
            return jsonify({
                "success": True,
                "question": question.format(),
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

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

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

    #  ----------------------------------------------------------------
    #  Erros
    #  ----------------------------------------------------------------
    
    #  Not Found
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
            }), 404,
        )
        
    #  Internal Error
    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify({
                "success": False, 
                "error": 500, 
                "message": error.description
            }), 500,
        )

    return app

