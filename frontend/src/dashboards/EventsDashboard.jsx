import { useEffect, useState } from "react";
import apiClient from "../api/client";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";
import EventDetail from "../components/EventDetail";

const EventsDashboard = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [limit] = useState(10);
  const [offset, setOffset] = useState(0);
  const [source, setSource] = useState("");
  const [eventType, setEventType] = useState("");
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [appliedSource, setAppliedSource] = useState("");
  const [appliedEventType, setAppliedEventType] = useState("");

  useEffect(() => {
    setLoading(true);
    apiClient
      .get("/events", {
        params: {
          limit,
          offset,
          source: appliedSource || undefined,
          event_type: appliedEventType || undefined,
        },
      })
      .then((res) => {
        setEvents(res.data.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load events");
        setLoading(false);
      });
  }, [limit, offset, appliedSource, appliedEventType]);

  const handleApplyFilters = () => {
    setAppliedSource(source);
    setAppliedEventType(eventType);
    setOffset(0); // Reset to first page when applying filters
  };

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  const getChipClass = (type, value) => {
    const normalizedValue = value.toLowerCase().replace(/_/g, "-");
    return `chip chip-${normalizedValue}`;
  };

  return (
    <div>
      <h2 style={{ marginBottom: "24px", fontSize: "24px", fontWeight: 600, color: "#111827" }}>
        Events
      </h2>

      <div className="toolbar">
        <input
          placeholder="Filter by source"
          value={source}
          onChange={(e) => setSource(e.target.value)}
        />
        <select
          value={eventType}
          onChange={(e) => setEventType(e.target.value)}
        >
          <option value="">All Event Types</option>
          <option value="login_failure">Login Failure</option>
          <option value="rate_limit">Rate Limit</option>
          <option value="temperature">Temperature</option>
          <option value="payment">Payment</option>
        </select>
        <button onClick={handleApplyFilters}>Apply</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>Source</th>
            <th>Type</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event) => (
            <tr key={event._id} onClick={() => setSelectedEvent(event)}>
              <td>
                <span className={getChipClass("source", event.source)}>
                  {event.source}
                </span>
              </td>
              <td>
                <span className={getChipClass("type", event.event_type)}>
                  {event.event_type}
                </span>
              </td>
              <td>{new Date(event.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
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

      {selectedEvent && (
        <EventDetail
          event={selectedEvent}
          onClose={() => setSelectedEvent(null)}
        />
      )}
    </div>
  );
};

export default EventsDashboard;
