
import { useEffect, useState } from 'react';
import './App.css';

const API_URL = '/api/ideas';

function App() {
  const [ideas, setIdeas] = useState([]);
  const [newIdea, setNewIdea] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [editingId, setEditingId] = useState(null);
  const [editContent, setEditContent] = useState('');
  const [savingId, setSavingId] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  // Fetch all ideas
  const fetchIdeas = async () => {
    try {
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error('Could not fetch ideas');
      }

      const data = await response.json();
      setIdeas(data);
    } catch {
      setError('Unable to connect to backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIdeas();
  }, []);

  // Create a new idea
  const addIdea = async (e) => {
    e.preventDefault();

    if (!newIdea.trim()) return;

    try {
      setError('');

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: newIdea.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to add idea');
      }

      const savedIdea = await response.json();

      setIdeas((previousIdeas) => [
        savedIdea,
        ...previousIdeas,
      ]);

      setNewIdea('');
    } catch {
      setError('Unable to save idea. Please try again.');
    }
  };

  // Start editing an idea
  const startEditing = (idea) => {
    setEditingId(idea.id);
    setEditContent(idea.content);
    setError('');
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingId(null);
    setEditContent('');
  };

  // Update an existing idea
  const updateIdea = async (ideaId) => {
    if (!editContent.trim()) {
      setError('Idea content cannot be empty.');
      return;
    }

    try {
      setError('');
      setSavingId(ideaId);

      const response = await fetch(`${API_URL}/${ideaId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: editContent.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update idea');
      }

      const updatedIdea = await response.json();

      setIdeas((previousIdeas) =>
        previousIdeas.map((idea) =>
          idea.id === ideaId ? updatedIdea : idea
        )
      );

      cancelEditing();
    } catch {
      setError('Unable to update idea. Please try again.');
    } finally {
      setSavingId(null);
    }
  };

  // Delete an existing idea
  const deleteIdea = async (ideaId) => {
    const confirmed = window.confirm(
      'Are you sure you want to delete this idea?'
    );

    if (!confirmed) return;

    try {
      setError('');
      setDeletingId(ideaId);

      const response = await fetch(`${API_URL}/${ideaId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete idea');
      }

      setIdeas((previousIdeas) =>
        previousIdeas.filter((idea) => idea.id !== ideaId)
      );

      if (editingId === ideaId) {
        cancelEditing();
      }
    } catch {
      setError('Unable to delete idea. Please try again.');
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="app">

      <nav className="navbar">
        <h2>💡 IdeaBoard</h2>
        <span>Turn thoughts into possibilities.</span>
      </nav>

      <main className="container">

        <section className="hero">
          <span className="tag">YOUR SPACE TO CREATE</span>

          <h1>Every great idea starts somewhere.</h1>

          <p>
            Capture your thoughts, share your ideas and make
            something amazing.
          </p>
        </section>

        {/* Create Idea Section */}
        <section className="idea-form">
          <h2>Share a new idea</h2>

          <form onSubmit={addIdea}>
            <input
              type="text"
              placeholder="What's your next big idea?"
              value={newIdea}
              onChange={(e) => setNewIdea(e.target.value)}
            />

            <button type="submit">
              + Add Idea
            </button>
          </form>
        </section>

        {/* Display Ideas Section */}
        <section className="ideas-section">

          <div className="section-heading">
            <h2>Community Ideas</h2>
            <span>{ideas.length} Ideas</span>
          </div>

          {error && (
            <p className="error">{error}</p>
          )}

          {loading ? (
            <p>Loading ideas...</p>
          ) : ideas.length === 0 ? (
            <div className="empty-state">
              <span className="empty-icon">💭</span>
              <h3>No ideas yet!</h3>
              <p>Be the first to share something creative.</p>
            </div>
          ) : (
            <div className="ideas-grid">

              {ideas.map((idea) => (
                <div className="idea-card" key={idea.id}>

                  <span className="idea-icon">💡</span>

                  {editingId === idea.id ? (
                    <div className="edit-area">

                      <textarea
                        value={editContent}
                        onChange={(e) =>
                          setEditContent(e.target.value)
                        }
                        placeholder="Edit your idea..."
                      />

                      <div className="edit-actions">

                        <button
                          type="button"
                          onClick={() => updateIdea(idea.id)}
                          disabled={savingId === idea.id}
                        >
                          {savingId === idea.id
                            ? 'Saving...'
                            : 'Save'}
                        </button>

                        <button
                          type="button"
                          onClick={cancelEditing}
                          disabled={savingId === idea.id}
                        >
                          Cancel
                        </button>

                      </div>
                    </div>
                  ) : (
                    <>
                      <p>{idea.content}</p>

                      <div className="card-actions">

                        <button
                          type="button"
                          className="edit-button"
                          onClick={() => startEditing(idea)}
                        >
                          ✏️ Edit
                        </button>

                        <button
                          type="button"
                          className="delete-button"
                          onClick={() => deleteIdea(idea.id)}
                          disabled={deletingId === idea.id}
                        >
                          {deletingId === idea.id
                            ? 'Deleting...'
                            : '🗑️ Delete'}
                        </button>

                      </div>
                    </>
                  )}

                </div>
              ))}

            </div>
          )}

        </section>
      </main>

      <footer>
        Built with React | IdeaBoard
      </footer>

    </div>
  );
}

export default App;
