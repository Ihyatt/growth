import React, { useState } from 'react';
import BulletTextEditor from './components/BulletTextEditor';

const Practitioner = () => {
  const [myText, setMyText] = useState("This is some initial text.\n\n- You can type whatever you want here.\n- New lines are created with Enter.");

  const handleTextChange = (newText) => {
      console.log('Editor Content Updated:', newText);
      setMyText(newText);
      // You would typically save `newText` to your backend here
  };
return (
  <div>
  <h1>My Simple Text Editor</h1>
  <div style={{ maxWidth: '600px', margin: '20px auto' }}>
  <BulletTextEditor
      initialContent={myText}
      placeholder="Type your content here..."
      onContentChange={handleTextChange}
  />
</div>
<h2>Current Editor Content:</h2>
<pre>{myText}</pre>
  </div>
);
}

export default Practitioner;