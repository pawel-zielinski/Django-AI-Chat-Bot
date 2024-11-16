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
                <div key={`message-${index}`} className="chat-bubble-text" dangerouslySetInnerHTML={{__html: marked(item)}}></div>
            </div>
            <div key={`date-${index}`} className={`chat-bubble-date-${index % 2 === 0 ? 'user' : 'system'}`}>{listOfDates[index]}</div>
            </>
            )) : null}
        </>
    )
}

const TextField = ({id}) => {
    const [message, setMessage] = useState('');

    const handleSendMessage = async (id) => {
    if (message.trim()) {
        const newMessage = message;
        setMessage('');

        // Create a new blinking animated chat-bubble-user field
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
            });

            // Fetch new chat history and refresh the page without user seeing the refresh
            const chatHistory = await getChatHistory(id);
            document.querySelector('.chat-bubble-user.blinking').remove();
            document.querySelector('.chat-bubbles').innerHTML = ChatBubbles({ data: chatHistory }).props.children;
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        } catch (e) {
            console.log('Error sending message:', e);
        }
    }
};

    const handleKeyPress = (event, id) => {
        if (event.key === 'Enter') {
            handleSendMessage(id);
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
    return (
        <>
            <h1>{chat_history.topic}</h1>
            <ChatBubbles data={chat_history}/>
            <TextField id={id}/>
            <div style={{height: '100px'}}></div>
        </>
    )
}

export default RenderChat;