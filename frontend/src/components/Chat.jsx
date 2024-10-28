import { useParams } from 'react-router';
import axios from 'axios';
import { useEffect, useState } from 'react';

function getChatHistory(id) {
    const [data, setData] = useState([]);

    useEffect(() => {
    if (localStorage.getItem('access_token') === null) {
      window.location.href = '/login';
    } else {
      (async () => {
        try {
          const { data } = await axios.get(`http://localhost:8000/home/${id}`, {
            headers: {
              'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          setData(data.qa);
          return data;
        } catch (e) {
          console.log('not auth');
        }
      })();
    }
  }, []);
}

const RenderChat = () => {
    const { id } = useParams();
    const chat_history = getChatHistory(id);
    console.log(chat_history);
    return (
        <div>
            <h1>{id}</h1>
        </div>
    )
}

export default RenderChat;