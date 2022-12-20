import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';
import Swal from 'sweetalert2'


class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
      searchValue: ''
    };
  }

  componentDidMount() {
    this.getCategories();
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `http://127.0.0.1:5000/questions?page=${this.state.page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        console.log(result)
        this.setState({
          questions: result.questions,
          totalQuestions: result.real_total,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  getCategories = () => {
    $.ajax({
      url: `http://127.0.0.1:5000/categories`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        console.log(result)
        this.setState({
          categories: result.categories,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };


  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (category) => {

    const {id} = category;

    this.setState({
      currentCategory: category,
    });

    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.real_total,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  submitSearch = (searchTerm) => {
    console.log(`Searh: ${searchTerm }`)
    var data_search = {search: searchTerm}

    if (this.state.currentCategory) data_search.category_id = this.state.currentCategory.id

    $.ajax({
      url: `/questions`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(data_search),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.real_total,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  onChangeSearh = term => {
    this.setState({
      searchValue: term,
    });

  }

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      Swal.fire({
        title: 'are you sure you want to delete the question?',
        showCancelButton: true,
        confirmButtonText: 'Delete',
      }).then((result) => {
        if (result.isConfirmed) {
          $.ajax({
            url: `http://127.0.0.1:5000/questions/${id}`, //TODO: update request URL
            type: 'DELETE',
            success: (result) => {
              this.getQuestions();
              Swal.fire('Deleted!', '', 'success')
            },
            error: (error) => {
              alert('');
              Swal.fire('Unable to load questions. Please try your request again', '', 'error')
              return;
            },
          });
        } else {
          Swal.fire('The question wasn\'t deleted', '', 'info')
        }
      })
    }
  };

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <div>
            <Search submitSearch={this.submitSearch} />
          </div>
          <h2
          className='categories-list-title'
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {this.state.categories.map((category) => (
              <li
                className='item-list-category'
                key={category.id}
                onClick={() => {
                  this.setState({
                    page: 1,
                  });
                  this.getByCategory(category);
                }}
              >
                <img
                  className='category'
                  alt={`${category.type.toLowerCase()}`}
                  src={`${category.type.toLowerCase()}.svg`}
                />
                {category.type}

                <p className='arrow-category'><i className="fa-solid fa-hand-pointer"></i></p>
              </li>
            ))}
          </ul>
        </div>
        <div className='questions-list'>
          <h2 className='title-question-body'> {this.state.page}/{Math.ceil(this.state.totalQuestions / 10)} Questions {this.state.currentCategory? `By ${this.state.currentCategory.type}` : ''}</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={q.category}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
