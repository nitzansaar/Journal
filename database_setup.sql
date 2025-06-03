-- Create the journal_entries table
CREATE TABLE IF NOT EXISTS journal_entries (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE journal_entries ENABLE ROW LEVEL SECURITY;

-- Create policy so users can only see their own entries
CREATE POLICY "Users can view their own entries" ON journal_entries
  FOR SELECT USING (auth.uid()::text = user_id);

-- Create policy so users can only insert their own entries
CREATE POLICY "Users can insert their own entries" ON journal_entries
  FOR INSERT WITH CHECK (auth.uid()::text = user_id);

-- Create policy so users can only update their own entries
CREATE POLICY "Users can update their own entries" ON journal_entries
  FOR UPDATE USING (auth.uid()::text = user_id);

-- Create policy so users can only delete their own entries
CREATE POLICY "Users can delete their own entries" ON journal_entries
  FOR DELETE USING (auth.uid()::text = user_id);

-- Create an index on user_id for better performance
CREATE INDEX IF NOT EXISTS idx_journal_entries_user_id ON journal_entries(user_id);

-- Create an index on created_at for better performance when ordering
CREATE INDEX IF NOT EXISTS idx_journal_entries_created_at ON journal_entries(created_at DESC); 