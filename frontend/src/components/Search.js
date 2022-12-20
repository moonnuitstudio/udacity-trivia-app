import React, { Component } from 'react';

class Search extends Component {
  state = {
    query: '',
  };

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query);
  };

  handleInputChange = () => {
    this.setState({
      query: this.search.value,
    });
  };

  render() {
    return (
      <div className='form-search-container'>
        <form onSubmit={this.getInfo}>
          <input
            className='txt-field'
            placeholder='Search questions...'
            ref={(input) => (this.search = input)}
            onChange={this.handleInputChange}
          />
          <button type='submit' className='btn-search'><i class="fa-solid fa-magnifying-glass"></i></button>
        </form>
      </div>
    );
  }
}

export default Search;
