import React from 'react';

export default function Panel(props) {
  return(
    <div className='info-panel'>
      <img src={props.url} alt={props.header} />
      <h3>{props.header}</h3>
      <div dangerouslySetInnerHTML={{ __html: props.text }}/>
    </div>
  );
}