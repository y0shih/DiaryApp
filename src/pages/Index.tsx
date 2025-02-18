
import { useState, useEffect } from "react";
import { EntryCard } from "@/components/EntryCard";
import { AddEntryDialog } from "@/components/AddEntryDialog";
import { useToast } from "@/components/ui/use-toast";
import { TransitionGroup, CSSTransition } from "react-transition-group";

interface Entry {
  id: string;  // Changed from _id to id to match Flask-SQLAlchemy default
  title: string;
  content: string;
  date: string;
}

const Index = () => {
  const [entries, setEntries] = useState<Entry[]>([]);
  const { toast } = useToast();
  const API_URL = "https://flask-classroomng.onrender.com/api";  

  // Fetch entries when component mounts
  useEffect(() => {
    fetchEntries();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchEntries = async () => {
    try {
      const response = await fetch(`${API_URL}/entries`);
      if (!response.ok) throw new Error('Failed to fetch entries');
      const data = await response.json();
      setEntries(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load entries",
        variant: "destructive",
      });
    }
  };

  const handleAddEntry = async ({ title, content }: { title: string; content: string }) => {
    try {
      const response = await fetch(`${API_URL}/entries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, content }),
      });

      if (!response.ok) throw new Error('Failed to create entry');
      
      const newEntry = await response.json();
      setEntries((prev) => [newEntry, ...prev]);
      
      toast({
        title: "Entry Added",
        description: "Your new entry has been created successfully.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create entry",
        variant: "destructive",
      });
    }
  };

  const handleEditEntry = (id: string) => {
    // To be implemented in the next iteration
    toast({
      title: "Edit Feature",
      description: "Edit functionality will be added in the next update.",
    });
  };

  const handleDeleteEntry = async (id: string) => {
    try {
      const response = await fetch(`${API_URL}/entries/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete entry');

      setEntries((prev) => prev.filter((entry) => entry.id !== id));
      toast({
        title: "Entry Deleted",
        description: "The entry has been removed successfully.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete entry",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="flex flex-col items-start mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Classroom Manager</h1>
          <p className="text-gray-600">Manage your classroom entries efficiently</p>
        </div>
        
        <AddEntryDialog onSubmit={handleAddEntry} />

        <TransitionGroup>
          {entries.map((entry) => (
            <CSSTransition key={entry.id} timeout={300} classNames="card">
              <EntryCard
                id={entry.id}
                title={entry.title}
                content={entry.content}
                date={new Date(entry.date)}
                onEdit={handleEditEntry}
                onDelete={handleDeleteEntry}
              />
            </CSSTransition>
          ))}
        </TransitionGroup>

        {entries.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No entries yet. Click "Add Entry" to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;
