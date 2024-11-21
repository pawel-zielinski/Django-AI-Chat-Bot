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
    var listOfEntities = Object.values(data.data.qa).map((item) => Object.keys(item)[0]);
    var listOfDates = Object.keys(data.data.qa);
    return (
      <>
    {Array.isArray(listOfMessages) ? listOfMessages.map((item, index) => (
        <>
            <div key={index} className={`chat-bubble-${listOfEntities[index]}`}>
                <div key={`message-${index}`} className="chat-bubble-text" dangerouslySetInnerHTML={{__html: marked(item)}}></div>
            </div>
            <div key={`date-${index}`} className={`chat-bubble-date-${listOfEntities[index]}`}>{listOfDates[index]}</div>
            </>
            )) : null}
        </>
    )
}

const TextField = ({id, is_first}) => {
    const [message, setMessage] = useState('');

    const handleSendMessage = async (id, is_first) => {
    if (message.trim()) {
        const newMessage = message;
        setMessage('');

        const chatBubble = document.createElement('div');
        chatBubble.className = 'chat-bubble-user blinking';
        chatBubble.innerHTML = newMessage;
        document.querySelector('.chat-text-field').insertAdjacentElement('beforebegin', chatBubble);
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });

        try {
            await axios.post('http://localhost:8000/create_question', {
                session: window.location.href.split('/').pop(),
                role: 'user',
                content: newMessage,
                temperature: 0.1
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            }).then(response => {
                if (response.status === 201) {
                    if (is_first) {
                        axios.post(`http://localhost:8000/create_topic`,
                            {'history_context': response.data.response_text,
                            'session_id': window.location.href.split('/').pop()}, {
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                            }
                        });
                    }
                    chatBubble.classList.remove('blinking');

                    const systemBubble = document.createElement('div');
                    systemBubble.className = 'chat-bubble-model';
                    systemBubble.innerHTML = marked(response.data.response_text);
                    document.querySelector('.chat-text-field').insertAdjacentElement('beforebegin', systemBubble);

                    const dateBubble = document.createElement('div');
                    dateBubble.className = 'chat-bubble-date-model';
                    dateBubble.innerHTML = new Date(response.data.response_date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' });
                    document.querySelector('.chat-text-field').insertAdjacentElement('beforebegin', dateBubble);

                    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
                }
            });
        } catch (e) {
            console.log('Error sending message:', e);
        }
    }
};

    const handleKeyPress = (event, id) => {
        if (event.key === 'Enter') {
            handleSendMessage(id, is_first);
        }
    };

    return (
        <div className="chat-text-field">
            <input
                type="text"
                className="form-control"
                id="chat-text"
                placeholder="Type your message here"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyPress}
            />
            <button className="btn btn-primary" onClick={handleSendMessage}><i className="fas fa-paper-plane"></i></button>
        </div>
    );
};


const RenderChat = () => {
    const { id } = useParams();
    const chat_history = getChatHistory(id);
    const is_first = Object.keys(chat_history.qa).length === 0;
    return (
        <>
            <h1 className={'topic-header'}>{chat_history.topic}</h1>
            <ChatBubbles data={chat_history}/>
            <TextField id={id} is_first={is_first}/>
            <div style={{height: '100px'}}></div>
        </>
    )
}

export default RenderChat;