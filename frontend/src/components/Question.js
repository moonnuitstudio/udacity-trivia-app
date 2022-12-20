import React, { Component } from 'react';
import Swal from 'sweetalert2'

import '../stylesheets/Question.css';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className='Question-holder'>
        <div className='container'>
         <div className='Question'>{question}</div>
          <div className='answer-section'>
            <div
              className='show-answer'
              onClick={() => this.flipVisibility()}
            >
              {this.state.visibleAnswer ? (<i class="fa-solid fa-eye"></i>) : (<i class="fa-solid fa-eye-slash"></i>)}
            </div>
            <div className='answer-holder'>
              <span
                style={{
                  visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
                }}
              >
                Answer: {answer}
              </span>
            </div>
          </div>
        </div>
        <div className='Question-status'>
          <img
            className='category'
            alt={`${category.toLowerCase()}`}
            src={`${category.toLowerCase()}.svg`}
          />
          <div className='difficulty'>Difficulty: {difficulty}</div>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
      </div>
    );
  }
}

export default Question;
