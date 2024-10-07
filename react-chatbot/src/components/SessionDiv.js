import React from 'react';
import axios from 'axios';

const SessionDiv = ({ session }) => {
  return (
    <div style={{ padding: '10px', border: '1px solid #ccc', margin: '5px 0' }}>
      <a href={`/home/${session.pk}`}>{session.topic}</a>
    </div>
  );
};

export default SessionDiv;