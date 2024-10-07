import {useEffect, useState} from "react";
import {getSessionList} from "../services/ApiService";
import SessionDiv from "./SessionDiv";

const SessionList = () => {
  const [sessions, setSessions] = useState([]);
  useEffect(() => {
    let isMounted = true;
    getSessionList().then((response) => {
      setSessions(response);
      return () => { isMounted = false };
    });
  }, []);

return (
  <div>
    <h1>Sessions</h1>
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {sessions.map((session) => (
        <SessionDiv key={session.pk} session={session} />
      ))}
    </div>
  </div>
);
}

export default SessionList;
