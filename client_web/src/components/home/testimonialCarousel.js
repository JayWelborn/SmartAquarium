import React, {Component} from 'react';

import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

import {apiRoot, apiCall} from '../../utils/api';


export default class TestimonialCarousel extends Component {

  constructor(props){
    super(props);

    this.state = {
    };
  }

  componentDidMount() {
    let url = apiRoot + 'testimonials.json'
    let method = 'get'

    apiCall(url, method).then(testimonialData => {
      for (let i = 0; i < testimonialData.length; i++) {
        apiCall(testimonialData[i].user, method).then(userData => {
          testimonialData[i].user = userData;
          apiCall(userData.profile, method).then(profileData => {
            testimonialData[i].profile = profileData;
          });
        });
      }
      this.setState({testimonials: testimonialData})
    });
  }

  render() {
    const responsive = {
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
        responsive={responsive}
      >
        {
          testimonials ?
          testimonials.map((testimonial, i) => 
            <p>{testimonial.text}</p>
          )
          :
          <p>loading...</p>
      }
      </Carousel>
    </section>
  )
  }
}
