import React from 'react';
import './AdminDashBoard.css';


export default function PaginationControls({ pagination, onNext, onPrev }) {
    return (
      <div className="pagination-controls">
        <button 
          onClick={onPrev} 
          disabled={!pagination.prevCursor}
          className="btn"
        >
          ← Previous
        </button>
        
        <button 
          onClick={onNext} 
          disabled={!pagination.hasMore}
          className="btn"
        >
          Next →
        </button>
      </div>
    );
  }