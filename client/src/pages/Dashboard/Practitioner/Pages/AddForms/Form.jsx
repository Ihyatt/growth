
import React, { useState, useRef } from 'react';
import './Form.css';

function AddForm() {
    // State to hold our to-do items
    const [todos, setTodos] = useState([
        { id: '1', text: 'Learn HTML & CSS', completed: false },
        { id: '2', text: 'Master JavaScript', completed: false },
        { id: '3', text: 'Dive into React', completed: false },
        { id: '4', text: 'Build a Portfolio', completed: false },
        { id: '5', text: 'Get a great job', completed: true },
    ]);

    // State for the new todo input
    const [newTodoText, setNewTodoText] = useState('');

    // Refs to manage the dragged item and the item it's currently hovering over
    const dragItem = useRef(null); // Index of the item being dragged
    const dragOverItem = useRef(null); // Index of the item currently being hovered over

    // --- Utility Functions ---
    const addTodo = (e) => {
        e.preventDefault();
        if (newTodoText.trim() === '') return;

        const newTodo = {
            id: String(Date.now()),
            text: newTodoText.trim(),
            completed: false,
        };
        setTodos((prevTodos) => [...prevTodos, newTodo]);
        setNewTodoText('');
    };

    const toggleComplete = (id) => {
        setTodos((prevTodos) =>
            prevTodos.map((todo) =>
                todo.id === id ? { ...todo, completed: !todo.completed } : todo
            )
        );
    };

    const deleteTodo = (id) => {
        setTodos((prevTodos) => prevTodos.filter((todo) => todo.id !== id));
    };

    // --- Drag and Drop Handlers ---

    // 1. On Drag Start: Store the index of the dragged item
    const handleDragStart = (e, index) => {
        dragItem.current = index;
        // Optionally, set data for cross-application drops, though not strictly needed for internal reorder
        e.dataTransfer.setData("text/plain", JSON.stringify(todos[index]));
        e.dataTransfer.effectAllowed = "move";
        // Add a class for visual feedback
        e.currentTarget.classList.add('dragging');
    };

    // 2. On Drag Enter/Over: Prevent default to allow dropping & handle visual feedback
    const handleDragEnter = (e, index) => {
        dragOverItem.current = index;
        e.preventDefault(); // Crucial: Allows dropping
        // Optionally add styling to show hover effect
        e.currentTarget.classList.add('drag-over');
    };

    // 3. On Drag Leave: Remove visual feedback
    const handleDragLeave = (e) => {
        e.currentTarget.classList.remove('drag-over');
    };

    // 4. On Drop: Perform the reordering
    const handleDrop = (e) => {
        e.preventDefault();
        if (dragItem.current === null || dragOverItem.current === null) return;

        const draggedIndex = dragItem.current;
        const droppedIndex = dragOverItem.current;

        // If dropping onto itself or the same item, do nothing
        if (draggedIndex === droppedIndex) {
            // Remove any drag-over styling if drop was on the same item
            const currentDraggedElement = document.querySelector('.todo-item.dragging');
            if (currentDraggedElement) {
                currentDraggedElement.classList.remove('dragging');
            }
            e.currentTarget.classList.remove('drag-over');
            return;
        }

        const newTodos = [...todos];
        const [draggedTodo] = newTodos.splice(draggedIndex, 1); // Remove dragged item
        newTodos.splice(droppedIndex, 0, draggedTodo); // Insert at new position

        setTodos(newTodos);

        // Reset refs
        dragItem.current = null;
        dragOverItem.current = null;

        // Clean up styling after drop
        e.currentTarget.classList.remove('drag-over');
        const currentDraggedElement = document.querySelector('.todo-item.dragging');
        if (currentDraggedElement) {
            currentDraggedElement.classList.remove('dragging');
        }
    };

    // 5. On Drag End: Clean up any lingering styling
    const handleDragEnd = (e) => {
        const allTodoItems = document.querySelectorAll('.todo-item');
        allTodoItems.forEach(item => {
            item.classList.remove('dragging');
            item.classList.remove('drag-over');
        });
        dragItem.current = null; // Ensure refs are reset
        dragOverItem.current = null;
    };


    return (
        <div className="App">
            <h1>Custom Drag & Drop Todo List</h1>

            <form onSubmit={addTodo} className="todo-form">
                <input
                    type="text"
                    value={newTodoText}
                    onChange={(e) => setNewTodoText(e.target.value)}
                    placeholder="Add a new todo..."
                />
                <button type="submit">Add Todo</button>
            </form>

            <div className="todo-list-container">
                {todos.length === 0 ? (
                    <p className="empty-list">No todos yet! Add some above.</p>
                ) : (
                    todos.map((todo, index) => (
                        <div
                            key={todo.id}
                            className={`todo-item ${todo.completed ? 'completed' : ''}`}
                            draggable="true" // Makes the item draggable
                            onDragStart={(e) => handleDragStart(e, index)}
                            onDragEnter={(e) => handleDragEnter(e, index)}
                            onDragLeave={handleDragLeave}
                            onDrop={handleDrop}
                            onDragEnd={handleDragEnd}
                            // onDragOver must be on the draggable item or droppable container
                            // to allow drop. If on the item, ensure it also calls preventDefault.
                            onDragOver={(e) => e.preventDefault()}
                        >
                            <input
                                type="checkbox"
                                checked={todo.completed}
                                onChange={() => toggleComplete(todo.id)}
                            />
                            <span>{todo.text}</span>
                            <button className="delete-btn" onClick={() => deleteTodo(todo.id)}>
                                &times;
                            </button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default AddForm;