import React, {Component} from 'react';

import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

import TestimonialTile from './testimonialTile';
import {apiRoot, apiCall} from '../../utils/api';


export default class TestimonialCarousel extends Component {

  constructor(props){
    super(props);

    this.responsive = {
      desktop: {
        breakpoint: { max: 3000, min: 1024 },
        items: 3,
      },
      tablet: {
        breakpoint: { max: 1024, min: 464 },
        items: 2,
      },
      mobile: {
        breakpoint: { max: 464, min: 0 },
        items: 1,
      },
    };

    this.colors = [
      {'background': '#f6f3f2', 'text': '#08415c'},
      {'background': '#c84630', 'text': '#f6f3f2'},
      {'background': '#08415c', 'text': '#f6f3f2'},
      {'background': '#5abcb9', 'text': '#08415c'},
    ];

    this.state = {};
  }

  componentDidMount() {
    let url = apiRoot + 'testimonials.json'
    let method = 'get'

    apiCall(url, method).then(testimonialData => {
      for (let i = 0; i < testimonialData.length; i++) {
        apiCall(testimonialData[i].user, method).then(userData => {
          testimonialData[i].userData = userData;
          apiCall(userData.profile, method).then(profileData => {
            testimonialData[i].profileData = profileData;
            this.setState({testimonials: testimonialData})
          });
        });
      }
    });
  }

  render() {
    let testimonials = this.state.testimonials;

    return (
      <section className='testimonial-carousel'>
        <Carousel
          additionalTransfrom={0}
          arrows
          autoPlaySpeed={3000}
          centerMode={false}
          className=""
          containerClass="container"
          dotListClass=""
          draggable
          focusOnSelect={false}
          infinite
          itemClass=""
          keyBoardControl
          minimumTouchDrag={80}
          renderButtonGroupOutside={false}
          renderDotsOutside
          responsive={this.responsive}
        >
          {
            testimonials ?
            testimonials.map((testimonial, i) => 
              testimonial.userData && testimonial.profileData ? 
                <TestimonialTile
                  testimonial={testimonial} key={i} colors={this.colors[i % this.colors.length]}
                />
                :
                <p key={i}>loading...</p>
            )
            :
            <p>loading...</p>
        }
        </Carousel>
      </section>
    );
  }
}
