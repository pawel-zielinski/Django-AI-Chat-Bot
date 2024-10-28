import { useEffect, useState } from "react";
import axios from "axios";

// Define the Home function.
export const RenderHome = () => {
  const [topic, setTopic] = useState([]);
  const [time, setTime] = useState([]);
  const [id, setId] = useState(0);

  useEffect(() => {
    if (localStorage.getItem('access_token') === null) {
      window.location.href = '/login';
    } else {
      (async () => {
        try {
          const { data } = await axios.get('http://localhost:8000/home/', {
            headers: {
              'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          setTopic(data.map(item => item.topic));
          setTime(data.map(item => item.creation_date_time));
          setId(data.map(item => item.pk));
        } catch (e) {
          console.log('not auth');
        }
      })();
    }
  }, []);

  return (
      <>
    <div className="form-signin mt-5 text-center">
    {topic.map((t, index) => (
      <div key={index}>
        <a className="chat-session-link" href={"/home/" + id[index]}>{t}</a>
        <h3><i>{new Date(time[index]).toLocaleString()}</i></h3>
      </div>
    ))}
    </div>
    </>
  );
}

export default RenderHome;