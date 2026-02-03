const EventDetail = ({ event, onClose }) => (
  <div className="overlay" onClick={onClose}>
    <div className="side-panel" onClick={(e) => e.stopPropagation()}>
      <div className="side-panel-header">
        <h3>Event Details</h3>
        <button className="side-panel-close" onClick={onClose}>
          ×
        </button>
      </div>
      <div className="side-panel-content">
        <pre>{JSON.stringify(event, null, 2)}</pre>
      </div>
    </div>
  </div>
);

export default EventDetail;
