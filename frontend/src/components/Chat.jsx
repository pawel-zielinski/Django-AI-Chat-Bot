import { useParams } from 'react-router';
import axios from 'axios';
import { useEffect, useState } from 'react';

const getChatHistory = (id) => {
    const [qa, setQA] = useState([]);
    const [topic, setTopic] = useState([]);

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
          setQA(data.qa);
          setTopic(data.topic);
        } catch (e) {
          console.log('not auth');
        }
      })();
    }
  }, []);
  return {"data": qa, "topic": topic};
}

const RenderChat = () => {
    const { id } = useParams();
    const chat_history = getChatHistory(id);
    console.log(chat_history);
    return (
        <div>
            <h1>{chat_history.topic}</h1>
        </div>
    )
}

export default RenderChat;