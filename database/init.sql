-- Kirakira (Character Chat) Database Schema
-- Updated to match SQLAlchemy models with CamelCase table and column names

-- Enable extension for UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. User Table
CREATE TABLE IF NOT EXISTS "User" (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password TEXT, -- NULL for OAuth users
    avatar TEXT,
    "nameChanged" BOOLEAN DEFAULT false,
    "createdAt" TIMESTAMPTZ DEFAULT NOW(),
    "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Worldview Table
CREATE TABLE IF NOT EXISTS "Worldview" (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    "creatorId" TEXT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ DEFAULT NOW(),
    "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Character Table
CREATE TABLE IF NOT EXISTS "Character" (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    personality TEXT,
    greeting TEXT NOT NULL,
    greetings TEXT,
    secret TEXT,
    "exampleDialogs" TEXT,
    visibility TEXT DEFAULT 'PRIVATE',
    "profileImage" TEXT,
    "albumImages" TEXT,
    "creatorId" TEXT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    "worldviewId" TEXT REFERENCES "Worldview"(id) ON DELETE SET NULL,
    "chatCount" INTEGER DEFAULT 0,
    "likeCount" INTEGER DEFAULT 0,
    "createdAt" TIMESTAMPTZ DEFAULT NOW(),
    "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Conversation Table
CREATE TABLE IF NOT EXISTS "Conversation" (
    id TEXT PRIMARY KEY,
    title TEXT,
    "userId" TEXT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    "characterId" TEXT NOT NULL REFERENCES "Character"(id) ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ DEFAULT NOW(),
    "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Message Table
CREATE TABLE IF NOT EXISTS "Message" (
    id TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    "conversationId" TEXT NOT NULL REFERENCES "Conversation"(id) ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ DEFAULT NOW()
);

-- 6. API Usage Table
CREATE TABLE IF NOT EXISTS api_usage (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    model TEXT NOT NULL,
    used_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_user_email ON "User"(email);
CREATE INDEX IF NOT EXISTS idx_character_creator ON "Character"("creatorId");
CREATE INDEX IF NOT EXISTS idx_conversation_user ON "Conversation"("userId");
CREATE INDEX IF NOT EXISTS idx_message_conversation ON "Message"("conversationId");
CREATE INDEX IF NOT EXISTS idx_api_usage_user ON api_usage(user_id);
