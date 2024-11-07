import { useParams } from 'react-router';
import axios from 'axios';
import { marked } from 'marked';
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
  return {"qa": qa, "topic": topic};
}

const ChatBubbles = ( data ) => {
    var listOfMessages = Object.values(data.data.qa).map((item) => Object.values(item)[0]);
    var listOfDates = Object.keys(data.data.qa);
    console.log(listOfDates);
    return (
      <>
    {Array.isArray(listOfMessages) ? listOfMessages.map((item, index) => (
        <>
            <div key={index} className={`chat-bubble-${index % 2 === 0 ? 'user' : 'system'}`}>
                <div className="chat-bubble-text" dangerouslySetInnerHTML={{__html: marked(item)}}></div>
            </div>
            <div className={`chat-bubble-date-${index % 2 === 0 ? 'user' : 'system'}`}>{listOfDates[index]}</div>
            </>
            )) : null}
        </>
    )
    }

    const RenderChat = () => {
        const {id} = useParams();
    const chat_history = getChatHistory(id);
    return (
        <>
            <h1>{chat_history.topic}</h1>
            <ChatBubbles data={chat_history} />
        </>
    )
}

export default RenderChat;