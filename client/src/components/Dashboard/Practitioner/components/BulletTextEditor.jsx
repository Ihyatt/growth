import React, { useState, useEffect, useRef, useCallback } from 'react';
import './BulletTextEditor.css'; // Optional styling

const BulletTextEditor = ({ initialContent = "", placeholder = "Start typing...", onContentChange }) => {
    const [content, setContent] = useState(initialContent);

    const handleChange = (event) => {
        setContent(event.target.value);
        if (onContentChange) {
            onContentChange(event.target.value);
        }
    };

    return (
        <textarea
            className="simple-text-editor"
            value={content}
            onChange={handleChange}
            placeholder={placeholder}
            rows="10" // Default height
        />
    );
};

export default BulletTextEditor;