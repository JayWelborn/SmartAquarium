import React from 'react';


export default function TestimonialTile(props) {
  let testimonial = props.testimonial;
  let profile = props.testimonial.profileData;
  let user = props.testimonial.userData;
  let styles = {
    backgroundColor: props.colors.background,
    color: props.colors.text
  };

  return(
    <div className='testimonial'>
      <img src={profile.picture ? profile.picture : '/assets/images/originals/silhouette.jpg'} />
      <div className='card' style={styles}>
        <h4><strong>{user.username}</strong></h4>
        <p>{testimonial.text}</p>
      </div>
    </div>
  )
}