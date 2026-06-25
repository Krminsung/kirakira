-- Add credit system to kirakira database
-- Migration: Add Kira credit system

-- Step 1: Add credit fields to User table
ALTER TABLE "User" 
ADD COLUMN IF NOT EXISTS kira_balance INTEGER DEFAULT 100 NOT NULL,
ADD COLUMN IF NOT EXISTS last_daily_credit TIMESTAMP WITH TIME ZONE;

-- Step 2: Create credit_transactions table
CREATE TABLE IF NOT EXISTS credit_transactions (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    description TEXT,
    balance_after INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Step 3: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_credit_transactions_user_id ON credit_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_created_at ON credit_transactions(created_at);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_type ON credit_transactions(transaction_type);

-- Step 4: Give existing users initial credits (100 kira)
UPDATE "User" 
SET kira_balance = 100 
WHERE kira_balance IS NULL OR kira_balance = 0;

-- Step 5: Create initial transaction records for existing users
INSERT INTO credit_transactions (id, user_id, amount, transaction_type, description, balance_after, created_at)
SELECT 
    gen_random_uuid()::text,
    id,
    100,
    'signup',
    'Initial signup bonus',
    100,
    "createdAt"
FROM "User"
WHERE NOT EXISTS (
    SELECT 1 FROM credit_transactions WHERE user_id = "User".id AND transaction_type = 'signup'
);

COMMIT;
