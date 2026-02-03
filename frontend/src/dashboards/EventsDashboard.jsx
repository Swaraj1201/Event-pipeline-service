import { useEffect, useState } from "react";
import apiClient from "../api/client";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";

const EventsDashboard = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [limit] = useState(10);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    setLoading(true);
    apiClient
      .get(`/events?limit=${limit}&offset=${offset}`)
      .then((res) => {
        setEvents(res.data.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load events");
        setLoading(false);
      });
  }, [limit, offset]);

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <h2>Events</h2>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Source</th>
            <th>Type</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event) => (
            <tr key={event._id}>
              <td>{event.source}</td>
              <td>{event.event_type}</td>
              <td>{new Date(event.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: "1rem" }}>
        <button
          disabled={offset === 0}
          onClick={() => setOffset(offset - limit)}
        >
          Previous
        </button>
        <button onClick={() => setOffset(offset + limit)}>
          Next
        </button>
      </div>
    </div>
  );
};

export default EventsDashboard;
