import os
import sys
import math
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
        response.headers.add("Access-Control-Allow-Origin", "*")
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
    def pagination(start, end, elements):
        items = [element.format() for element in elements]
        current_items = items[start:end]
        
        return current_items
    
    def pagination_questions(request, questions):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", QUESTIONS_PER_PAGE, type=int)
    
        questions_length = len(questions)
        
        start = (page - 1) * limit
        end = start + limit
        
        paginated_questions = [] if questions_length == 0 else pagination(start, end, questions)
        paginated_questions_length = len(paginated_questions)
        
        many_pages = math.ceil(questions_length / limit)
        
        return {
            "success": True,
            "real_total": questions_length,
            "paginated_total": paginated_questions_length,
            "questions": paginated_questions,
            "current_page": page,
            "current_limit": limit,
            "is_there_next_page": end < questions_length,
            "is_there_prev_page": start > 0,
            "many_pages": many_pages
        }
        
    def pagination_categories(request, categories):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", QUESTIONS_PER_PAGE, type=int)
        
        categories_length = len(categories)
        
        start = (page - 1) * limit
        end = start + limit
        
        paginated_categories = [] if categories_length == 0 else pagination(start, end, categories)
        paginated_categories_length = len(paginated_categories)
        
        many_pages = math.ceil(categories_length / limit)
        
        return {
            "success": True,
            "real_total": categories_length,
            "paginated_total": paginated_categories_length,
            "categories": paginated_categories,
            "current_page": page,
            "current_limit": limit,
            "is_there_next_page": end < categories_length,
            "is_there_prev_page": start > 0,
            "many_pages": many_pages
        }

    #  ----------------------------------------------------------------
    #  GETs
    #  ----------------------------------------------------------------

    #  GET Questions
    @app.route('/questions')
    def retrieve_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            
            return jsonify(pagination_questions(request, questions))
        except:
            print( sys.exc_info() )
            abort(500)

    #  GET Categories
    @app.route('/categories')
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            
            return jsonify(pagination_categories(request, categories))
        except:
            print( sys.exc_info() )
            abort(500)
    
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
            try:
                questions = category.questions
                
                return jsonify(pagination_questions(request, questions))
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

    #  ----------------------------------------------------------------
    #  POSTs
    #  ----------------------------------------------------------------

    #  POST Category
    @app.route('/categories', methods=['POST'])
    def post_categories():
        body = request.get_json()

        field_type = body.get("type", None)
        search = body.get("search", None)
        
        if search:
            try:
                search_term = "%{}%".format(search)
                categories = Category.query.order_by(Category.id).filter(Category.type.ilike(search_term)).all()
                
                return jsonify(pagination_categories(request, categories))
            except:
                print( sys.exc_info() )
                abort(500)
        elif field_type is None:
            abort(400)
        else:
            try:
                category = Category(type=field_type)
            
                category.insert()

                categories = Category.query.order_by(Category.id).all()
                
                return jsonify(pagination_categories(request, categories))
            except:
                print( sys.exc_info() )
                abort(500)
                
    #  Create Question
    @app.route('/categories/<int:category_id>/questions', methods=['POST'])
    def create_question(category_id):
        body = request.get_json()

        field_question = body.get("question", None)
        field_answer = body.get("answer", None)
        field_difficulty = body.get("difficulty", None)
        
        someone_is_none = field_question is None or field_answer is None or field_difficulty is None
        
        if someone_is_none:
            abort(400)
        
        if type(field_difficulty) != int:
            if field_difficulty.isnumeric():
                field_difficulty = int(field_difficulty)
            else:
                abort(400)
                
        if field_difficulty <= 0 or field_difficulty > 4:
            abort(400)
        
        category = Category.query.filter(Category.id == category_id).one_or_none()
            
        if category is None:  
            abort(404)
            
        try:
            question = Question(category=category_id,question=field_question,answer=field_answer,difficulty=field_difficulty)
        
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            
            return jsonify(pagination_questions(request, questions))
        except:
            print( sys.exc_info() )
            abort(500)
                
    #  Search questions
    @app.route('/questions', methods=['POST'])
    def search_questions():
        body = request.get_json()

        search = body.get("search", None)
        category_id = body.get("category_id", None)
        
        questions = []
        
        if search:
            try:
                search_term = "%{}%".format(search)
                
                if category_id is None:
                    questions = Question.query.order_by(Question.id).filter(Question.question.ilike(search_term)).all()
                else:
                    questions = Question.query.order_by(Question.id).filter(Question.question.ilike(search_term), Question.category == category_id).all()
                
                return jsonify(pagination_questions(request, questions))
            except:
                print( sys.exc_info() )
                abort(500)
        else:
            
            if category_id is not None:
                questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
            else: 
                questions = Question.query.order_by(Question.id).all()
                
            return jsonify(pagination_questions(request, questions))
            
    #  ----------------------------------------------------------------
    #  DELETEs
    #  ----------------------------------------------------------------
        
    @app.route('/categories/<int:category_id>', methods=["DELETE"])
    def delete_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
            
        if category is None:  
            abort(404)
        else:
            try:
                category.delete()

                categories = Category.query.order_by(Category.id).all()
                
                return jsonify(pagination_categories(request, categories))
            except:
                print( sys.exc_info() )
                abort(500)
                
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
            
        if question is None:  
            abort(404)
        else:
            try:
                question.delete()

                questions = Question.query.order_by(Question.id).all()
                
                return jsonify(pagination_questions(request, questions))
            except:
                print( sys.exc_info() )
                abort(500)
 
    #  ----------------------------------------------------------------
    #  PLAY
    #  ----------------------------------------------------------------

    @app.route('/questions/play', methods=["POST"])
    def play_questions():
        
        body = request.get_json()

        former_questions = body.get("former_questions", [])
        category_id = body.get("category_id", None)
        
        questions = []
            
        try:
            if category_id is None:
                questions = Question.query.filter(~Question.id.in_(former_questions)).order_by(Question.id).all()
            else:
                category = Category.query.filter(Category.id == category_id).one_or_none()
            
                if category is None:  
                    abort(404)
                else:
                    questions = Question.query.filter(
                        ~Question.id.in_(former_questions),
                        Question.category == category_id
                    ).order_by(Question.id).all()
                    
            next_lenght_questions = len(questions) - 1
            
            if next_lenght_questions >= 0:
                question = random.choice(questions)
                
                former_questions.append(question.id)
                
                return jsonify({
                    "end": False,
                    "question": question.format(),
                    "used_questions": former_questions,
                    "next_lenght_questions": next_lenght_questions
                })
            else:
                played_questions = Question.query.filter(Question.id.in_(former_questions)).order_by(Question.id).all()
                
                return jsonify({
                    "end": True,
                    "question": {},
                    "former_questions": [played_question.format() for played_question in played_questions],
                })
        except:
            print( sys.exc_info() )
            abort(500)

    #  ----------------------------------------------------------------
    #  Erros
    #  ----------------------------------------------------------------
    
    #  Not Found
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, 
                "error": 400, 
                "message": "Bad Request"
            }), 400,
        )
    
    #  Not Found
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "Resource not found"
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

