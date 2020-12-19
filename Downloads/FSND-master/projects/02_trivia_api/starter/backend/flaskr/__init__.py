import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
# function for paginated questions :
def get_paginated_questions(request, questions, num_of_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * num_of_questions
    end = start + num_of_questions

    questions = [question.format() for question in questions]
    current_questions = questions[start:end]

    return current_questions
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})
   '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
   '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''  
  @app.route('/categories' , methods= ['GET'])
  def get_categories():
   #get category from database
   categories = Category.query.all()
   formatted_categories  = {}
   # if we have categories 
   try:
    for category in categories:
      formatted_categories [category.id] = category.type 
    return jsonify ({
      "success": True ,
      "categories": formatted_categories ,
     
    }) , 200
    # if categories not found 
   except:
     abort(404)
  
   '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions' , methods= ['GET'])
  def get_questions ():
   # get questions and category 
   questions = Question.query.all()
   number_of_question = len(questions)
   categories = Category.query.all()
   formatted_categories  = {}
  
   for category in categories:
      formatted_categories [category.id] = category.type 
      # if we have paginated questions 
   try:
      paginated_questions = get_paginated_questions(request, questions , QUESTIONS_PER_PAGE)
    
      return jsonify ({
      'success': True , 
      "questions": paginated_questions,
      "total questions": number_of_question , 
      "categories":formatted_categories ,
       }) , 200
   except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:id>' , methods = ['DELETE'])
  def delete_question (id):
    # get the question 
    question = Question.query.get (id)
    try:
      question.delete()
      return jsonify ({
        "success": True , 
        "deleted question id " : id , 
        "message": "The question was deleted successfully"
      }) , 200
      # if not found or can't delete the question 
    except:
      abort (404)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  def add_question ():
  info = request.get_json()
  #get info and assigned it to question , answer , categorry
  
  question = info.get('question' )
  answer = info.get ('answer' )
  category = info.get ('category' )
  difficulty_score = info.get ('diffculty')

  # check all are not empty  
  if (( questions == None ) or (answer == None) or ( category == None )
      or ( difficulty_score == None)):
      abort (422)
  # now try to insert the question
  try:
    new_question = Question (question =question , answer =answer , category = category , score =difficulty_score)
    new_question.insert()
    return jsonify ({
      'success':True , 
      'message': 'The question was inserted successfully'
    })
  except:
    abort (422)
  

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search' , methods = ['POST'])
  def search_question ():
    info = request.get_json()
    search_term = info.get('searchTerm')
    #check if searchTearm not empty 
    if (search_term == None):
      abort (442)
    # now try to found the questions list based on searchTerm 
    try:
      questions = Question.query.filter (Question.question.ilike(f'%{search_term}%')).all()
      # if the list len =0 abort 404 
      if (len(questions) == 0):
        abort (404)
      else:
        paginated_questions = get_paginated_questions(request, questions , QUESTIONS_PER_PAGE)

      return jsonify ({
        'success': True , 
        'questions': paginated_questions , 
        'total of questions': len (questions)
      })
    except:
      abort (404)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
   @app.route ('/categories/<int:id>/questions' , methods =['GET'])
  def get_questions_category (id):
    category = Category.query.get (id)

    # check category not empty 
    if ( category == None):
      abort (422)
    questions_list = Question.query.filter_by (category = category.id).all()
   # check question list length not equal 0 
    if (len (questions_list) == 0):
     abort (404)
    try:
      paginated_questions = get_paginated_questions (request , questions_list , QUESTIONS_PER_PAGE)
      return jsonify ({
        'success': True,
        'questions':paginated_questions,
        'total of questions':len (questions_list),
        'category':category.type
      })  
    except:
      abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  #@app.route ('/quizzes' , methods = ["POST"])
def start_quiz ():
  info= request.get_json()
  previousQuestion = info.get('previous_question')
  givenCategory = info.get('quiz_category')
  #check previous question and given category are not none 
  if ( (previousQuestion == None) or (givenCategory == None) ):
    abort (422)
  

  # check if the id of category ,, if it 0 then choose all category 
  if (givenCategory['id'] == 0 ):
    questions_list = Question.query.all()
  else :
    questions_list = Question.query.filter_by(category= givenCategory['id']).all()
  lengthOfQuestions = len(questions_list)
  def make_quiz ():
   return questions_list[random.randrange(0, lengthOfQuestions ,1)]
  
  def get_next_question ():
    return make_quiz()
  # check next question is not in previos questions list 
  def check_question (question):
    flag = True
    for ques in previousQuestion:
      if (ques.id == question.id):
        return flag 
    return False 
  
  nextQuestion = get_next_question()
  
# while next question is in previous list try another question 
  while (check_question (nextQuestion)):
    nextQuestion = get_next_question()

  return jsonify ({
    'success': True,
    'next question': nextQuestion.format()
  })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
   @app.errorhandler(400)
  def bad_request (error):
      return jsonify ({
        'success':False , 
        'error': 400 ,
        'message': "Bad Request" 
        
      }) , 400
  @app.errorhandler (404)
  def not_found (error):
      return jsonify ({
        "success" : False , 
        'error': 404 , 
        'message': "The Resource Not Found "
      }) , 404 
  @app.errorhandler (422)
  def unprocessable_error (error):
      return jsonify ({
        'success': False , 
        'error': 422 , 
        'message': "Unprocessable request"
      }) , 422
  @app.errorhandler(500)
  def server_error(error):
      return jsonify ({
        'success': False , 
        'error': 500 , 
        'message':'error in server'
      }) , 500
  
  return app

    