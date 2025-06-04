import React, { useState, useEffect, useRef, useCallback } from 'react';
import './BulletTextEditor.css'; // Optional styling

function BulletTextEditor({ task, deleteTask }) {

 
 return (
 <div className="todo-item">

<p>{task.text}</p>
<button onClick={() => deleteTask(task.id)}>
 X
 </button>
 </div>
 );
}

export default BulletTextEditor;